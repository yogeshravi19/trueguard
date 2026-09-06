"""
TRUEGUARD Closed-Loop Mitigation Pipeline
Implements two-tier active mitigation:
- Tier 1: Targeted Retrieval-Augmented Grounding (RAG)
- Tier 2: Calibrated Abstention
"""

import time
import urllib.parse
import requests

class TrueGuardMitigationPipeline:
    """
    Closed-loop mitigation controller for TRUEGUARD.
    When generation risk breaches the threshold, intercepts output and coordinates
    targeted retrieval and calibrated abstention.
    """
    def __init__(self, detector, config=None):
        self.detector = detector
        self.config = config or {}
        mit_cfg = self.config.get("mitigation", {})
        self.threshold = mit_cfg.get("risk_threshold", 0.50)
        self.abstention_template = mit_cfg.get(
            "abstention_template",
            "I do not have sufficient verified evidence to answer this query reliably without risk of factual inaccuracy."
        )
        self.user_agent = "TRUEGUARD-Research/1.0 (academic-eval@vit.ac.in)"

    def retrieve_grounding_fact(self, query):
        """Attempts to retrieve grounding facts via Wikipedia REST API."""
        stop_words = {"what", "who", "when", "where", "which", "why", "how", "is", "was", "are", "were", "the", "in", "on", "at", "a", "an"}
        words = [w.strip("?,.") for w in query.split() if w.lower().strip("?,.") not in stop_words and len(w) > 2]
        search_term = " ".join(words[:4]) if words else query

        try:
            encoded = urllib.parse.quote(search_term)
            url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"
            headers = {"User-Agent": self.user_agent}
            resp = requests.get(url, headers=headers, timeout=3.0)
            if resp.status_code == 200:
                data = resp.json()
                extract = data.get("extract", "")
                if extract and len(extract) > 40:
                    sentences = extract.split(". ")
                    return ". ".join(sentences[:2]) + "."
        except Exception:
            pass
        return None

    def execute_closed_loop(self, prompt, max_new_tokens=40):
        """
        Runs generation with closed-loop mitigation active.
        
        Returns:
            dict containing:
                - final_output: str
                - initial_output: str
                - initial_risk: float
                - mitigation_tier: "NONE", "TIER_1_RAG", or "TIER_2_ABSTENTION"
                - hallucination_averted: bool
                - explanation: str
        """
        # Step 1: Run baseline guided generation
        det_result = self.detector.generate_and_guard(
            prompt=prompt,
            max_new_tokens=max_new_tokens,
            halt_on_risk=True
        )

        r_seq = det_result["sequence_risk"]
        initial_text = det_result["generated_text"]

        if r_seq <= self.threshold and not det_result["halted_early"]:
            # Output is safe, release as is
            return {
                "final_output": initial_text,
                "initial_output": initial_text,
                "sequence_risk": r_seq,
                "mitigation_tier": "NONE",
                "hallucination_averted": False,
                "tokens": det_result["tokens"],
                "token_risks": det_result["token_risks"],
                "explanation": "Generation verified within safe algorithmic uncertainty bounds."
            }

        # Step 2: Risk exceeded -> Tier 1 Targeted Retrieval
        grounding_fact = self.retrieve_grounding_fact(prompt)

        if grounding_fact:
            augmented_prompt = f"Verified Context: {grounding_fact}\nQuestion: {prompt}\nAnswer:"
            # Regenerate with grounding
            rag_result = self.detector.generate_and_guard(
                prompt=augmented_prompt,
                max_new_tokens=max_new_tokens,
                halt_on_risk=False
            )
            rag_risk = rag_result["sequence_risk"]

            if rag_risk <= self.threshold:
                return {
                    "final_output": rag_result["generated_text"].strip(),
                    "initial_output": initial_text,
                    "sequence_risk": rag_risk,
                    "mitigation_tier": "TIER_1_RAG",
                    "grounding_evidence": grounding_fact,
                    "hallucination_averted": True,
                    "tokens": rag_result["tokens"],
                    "token_risks": rag_result["token_risks"],
                    "explanation": f"High risk intercepted ({r_seq:.3f}). Successfully grounded using factual evidence."
                }

        # Step 3: Retrieval unavailable or uncertainty persisted -> Tier 2 Calibrated Abstention
        return {
            "final_output": self.abstention_template,
            "initial_output": initial_text,
            "sequence_risk": r_seq,
            "mitigation_tier": "TIER_2_ABSTENTION",
            "hallucination_averted": True,
            "tokens": det_result["tokens"],
            "token_risks": det_result["token_risks"],
            "explanation": f"High hallucination risk detected ({r_seq:.3f} > {self.threshold:.2f}). Triggered calibrated abstention."
        }
