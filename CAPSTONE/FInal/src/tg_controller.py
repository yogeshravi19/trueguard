"""
TRUEGUARD v2 three-tier closed-loop controller (review paper Section 6.3-6.4).

Regimes (thresholds are calibrated on held-out validation data, never on test data):
    risk <  tau_warning                  SAFE            -> release answer unchanged
    tau_warning <= risk < tau_fault      WARNING         -> Tier 1: risk-guided corrective re-generation
    risk >= tau_fault                    FAULT           -> Tier 2: retrieval-grounded re-generation,
                                                            Tier 3: calibrated abstention if still risky
Escalation: if Tier 1 cannot find a candidate below tau_warning the controller escalates to Tier 2; if the
retrieval-grounded answer is still >= tau_fault (or nothing is retrieved) it abstains (Tier 3).

Documented deviation from the paper: Tier 1 re-samples the whole (short) answer rather than rolling back "a few
tokens", because the detector scores complete answers; for answers of <= 32 tokens this is a few tokens anyway.
It draws K candidate answers (temperature sampling) and keeps the lowest-risk one -- a real corrective regeneration
driven by the detector, not a placeholder.
"""
import json
import time
import urllib.parse

import numpy as np

from .tg_pipeline import generate_answer, score_answer, build_prompt

ABSTAIN_TEXT = "I do not have sufficient verified evidence to answer this reliably."


class WikipediaRetriever:
    """Targeted retrieval of an evidence passage for the question (Tier 2).  Needs internet."""

    def __init__(self, max_chars=700, timeout=6.0):
        self.max_chars, self.timeout, self.cache = max_chars, timeout, {}

    def __call__(self, query):
        if "Question:" in query:
            query = query.split("Question:", 1)[1].strip()
        query = query.splitlines()[0].strip().strip('"?')
        stop = {"what", "which", "who", "whom", "whose", "when", "where", "why", "how", "is", "was", "are", "were",
                "did", "does", "do", "has", "have", "had", "the", "a", "an", "in", "on", "of", "to", "for", "with",
                "by", "from", "as", "at", "into", "called", "known", "name", "named", "wrote", "made", "played"}
        words = [w.strip(",.?\"'()") for w in query.split()]
        kept = [w for w in words if w and w.lower() not in stop]
        if kept:
            query = " ".join(kept[:8])
        if query in self.cache:
            return self.cache[query]
        passage = None
        try:
            import requests
            h = {"User-Agent": "TRUEGUARD-Research/2.0 (academic evaluation)"}
            r = requests.get("https://en.wikipedia.org/w/api.php", headers=h, timeout=self.timeout, params=dict(
                action="query", list="search", srsearch=query, srlimit=1, format="json"))
            hits = r.json().get("query", {}).get("search", [])
            if hits:
                r2 = requests.get("https://en.wikipedia.org/w/api.php", headers=h, timeout=self.timeout, params=dict(
                    action="query", prop="extracts", exintro=1, explaintext=1, titles=hits[0]["title"], format="json"))
                pages = r2.json()["query"]["pages"]
                txt = next(iter(pages.values())).get("extract", "")
                if len(txt) > 40:
                    passage = txt[: self.max_chars]
        except Exception:
            passage = None
        self.cache[query] = passage
        return passage


class ThreeTierController:
    def __init__(self, model, tok, device, detector, tau_warning, tau_fault, retriever=None,
                 k_samples=4, temperature=0.7, top_p=0.9, max_new_tokens=24):
        self.m, self.tok, self.dev, self.det = model, tok, device, detector
        self.tw, self.tf, self.retriever = tau_warning, tau_fault, retriever
        self.k, self.T, self.top_p, self.max_new = k_samples, temperature, top_p, max_new_tokens

    # -- detector call on a (prompt, answer) pair
    def risk(self, prompt, prefix, answer):
        r = score_answer(self.m, self.tok, self.dev, prompt, prefix + answer)
        if r is None:
            return 1.0, None, None
        F, H = r
        return float(self.det.predict_proba(F[None], H[None])[0]), F, H

    def respond(self, user_text, initial=None):
        """Run the closed loop for one user request.  `initial` = optional (answer, risk, F, H) of the greedy answer
        (re-computed here if not supplied).  Returns a dict with the final answer, tier and a decision trace."""
        prompt, prefix = build_prompt(self.tok, user_text)
        if initial is None:
            ans0 = generate_answer(self.m, self.tok, self.dev, prompt, self.max_new)
            r0, F0, H0 = self.risk(prompt, prefix, ans0)
        else:
            ans0, r0, F0, H0 = initial
        trace = [dict(step="initial_greedy", answer=ans0, risk=r0)]
        expl = self.det.explain(F0, H0) if F0 is not None else {}
        base = dict(initial_answer=ans0, initial_risk=r0, sensor_contributions=expl, trace=trace)

        if r0 < self.tw:
            return dict(base, tier="SAFE", final_answer=ans0, final_risk=r0)

        # ---- Tier 1 (warning regime): risk-guided corrective re-generation
        if r0 < self.tf:
            cands = []
            for _ in range(self.k):
                a = generate_answer(self.m, self.tok, self.dev, prompt, self.max_new, sample=True,
                                    temperature=self.T, top_p=self.top_p)
                r, _, _ = self.risk(prompt, prefix, a)
                cands.append((r, a))
                trace.append(dict(step="tier1_candidate", answer=a, risk=r))
            r1, a1 = min(cands, key=lambda t: t[0])
            if r1 < self.tw:
                return dict(base, tier="TIER1_RESAMPLE", final_answer=a1, final_risk=r1)

        # ---- Tier 2 (fault regime, or Tier 1 failed): retrieval-grounded re-generation
        if self.retriever is not None:
            passage = self.retriever(user_text)
            if passage:
                p2, _ = build_prompt(self.tok, f"Use this evidence if relevant: {passage}\n{user_text}")
                a2 = generate_answer(self.m, self.tok, self.dev, p2, self.max_new)
                r2, _, _ = self.risk(p2, prefix, a2)
                trace.append(dict(step="tier2_retrieval", answer=a2, risk=r2, evidence=passage[:200]))
                if r2 < self.tf:
                    return dict(base, tier="TIER2_RETRIEVAL", final_answer=a2, final_risk=r2)
            else:
                trace.append(dict(step="tier2_retrieval", answer=None, risk=None, evidence="nothing retrieved"))

        # ---- Tier 3: calibrated abstention
        return dict(base, tier="TIER3_ABSTAIN", final_answer=ABSTAIN_TEXT, final_risk=r0)

