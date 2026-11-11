"""
Step 3 of the evaluation pipeline: end-to-end before-and-after mitigation evaluation on TriviaQA.

Split (strict, no leakage):
  * Calibration split (`n_cal` questions): greedy-generate an answer, extract features, label against TriviaQA gold
    aliases, fit TrueGuardDetector and calibrate (tau_warning, tau_fault) on this split only.
  * Test split (`n_test` disjoint questions): run ThreeTierController (SAFE / TIER1_RESAMPLE / TIER2_RETRIEVAL /
    TIER3_ABSTAIN) and compare:
      - Unmitigated hallucination rate  = P(wrong) across all test questions
      - Post-mitigation hallucination rate among answered questions = P(wrong | not abstained)
      - System-level hallucination rate = P(answered AND wrong) across all test questions
      - Answer coverage                 = P(not abstained)
      - Selective-prediction curve (accuracy at 100%, 90%, ..., 50% coverage) for TRUEGUARD vs NLL / Entropy baselines
      - Tier-by-tier transition counts (how many greedy hallucinations Tier 1 and Tier 2 actually fixed).
"""
import argparse, json, os, sys, time
os.environ.setdefault("USE_TF", "0")
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
from src.tg_pipeline import load_model, build_prompt, generate_answer, score_answer, TrueGuardDetector, FEATURE_NAMES
from src.tg_data import load_triviaqa, is_correct
from src.tg_eval import auc_safe, calibrate_thresholds, risk_coverage, plot_bars
from src.tg_controller import ThreeTierController, WikipediaRetriever, ABSTAIN_TEXT


def _gen_and_score(model, tok, device, items, max_new=24):
    Fs, Hs, ys, qs, ans = [], [], [], [], []
    for i, it in enumerate(items):
        p, pre = build_prompt(tok, it["user_text"])
        a = generate_answer(model, tok, device, p, max_new_tokens=max_new)
        r = score_answer(model, tok, device, p, pre + a)
        if r is None:
            continue
        F, H = r
        Fs.append(F); Hs.append(H)
        ys.append(1 - is_correct(a, it["gold"]))   # 1 = hallucinated / wrong
        qs.append(it); ans.append(a)
    return np.array(Fs, np.float64), np.array(Hs, np.float32), np.array(ys, int), qs, ans


def run_mitigation(model_name, n_cal=150, n_test=150, use_wikipedia=True, out_dir=None, fourbit=False):
    model, tok, device = load_model(model_name, load_in_4bit=fourbit)
    cal_items = load_triviaqa(n_cal, seed=42, offset=0)
    test_items = load_triviaqa(n_test, seed=42, offset=n_cal)

    print(f"[mitigation] scoring calibration split (n={n_cal})...", flush=True)
    F_cal, H_cal, y_cal, _, _ = _gen_and_score(model, tok, device, cal_items)
    if len(np.unique(y_cal)) < 2 or min(y_cal.sum(), len(y_cal) - y_cal.sum()) < 5:
        raise RuntimeError(f"Calibration split has {int(y_cal.sum())}/{len(y_cal)} hallucinations; "
                           "use a stronger model or larger --n_cal so both classes are represented.")
    det = TrueGuardDetector().fit(F_cal, H_cal, y_cal)
    tw, tf = calibrate_thresholds(y_cal, det.train_risk_)
    print(f"[mitigation] calibrated thresholds: tau_warning={tw:.3f}  tau_fault={tf:.3f}", flush=True)

    print(f"[mitigation] scoring test split (n={n_test})...", flush=True)
    F_te, H_te, y_te, qs_te, ans_te = _gen_and_score(model, tok, device, test_items)
    risk_te = det.predict_proba(F_te, H_te)

    retr = WikipediaRetriever() if use_wikipedia else None
    ctrl = ThreeTierController(model, tok, device, det, tw, tf, retriever=retr)

    tiers, final_correct, answered, records = [], [], [], []
    t1_fixed = t2_fixed = 0
    for i, it in enumerate(qs_te):
        res = ctrl.respond(it["user_text"], initial=(ans_te[i], float(risk_te[i]), F_te[i], H_te[i]))
        tier = res["tier"]; tiers.append(tier)
        if tier == "TIER3_ABSTAIN":
            answered.append(0); final_correct.append(0)
        else:
            answered.append(1)
            c = is_correct(res["final_answer"], it["gold"])
            final_correct.append(c)
            if y_te[i] == 1 and c == 1:
                if tier == "TIER1_RESAMPLE":
                    t1_fixed += 1
                elif tier == "TIER2_RETRIEVAL":
                    t2_fixed += 1
        if len(records) < 30:
            records.append(dict(question=it["question"], gold=it["gold"][:3], greedy_answer=ans_te[i],
                                greedy_correct=int(1 - y_te[i]), initial_risk=float(risk_te[i]),
                                tier=tier, final_answer=res["final_answer"],
                                final_correct=None if tier == "TIER3_ABSTAIN" else int(final_correct[-1]),
                                sensor_contributions=res["sensor_contributions"]))

    answered = np.array(answered, bool); final_correct = np.array(final_correct, int)
    greedy_correct = 1 - y_te
    before_halluc = float(y_te.mean())
    after_halluc_among_answered = float(1 - final_correct[answered].mean()) if answered.any() else 0.0
    after_halluc_system = float(((1 - final_correct) * answered).mean())
    cov = float(answered.mean())
    rel_drop_answered = (before_halluc - after_halluc_among_answered) / max(before_halluc, 1e-9)
    rel_drop_system = (before_halluc - after_halluc_system) / max(before_halluc, 1e-9)

    idx = {n: i for i, n in enumerate(FEATURE_NAMES)}
    sel = dict(
        TRUEGUARD=risk_coverage(greedy_correct, risk_te),
        NLL_baseline=risk_coverage(greedy_correct, F_te[:, idx["NLL_mean"]]),
        Entropy_baseline=risk_coverage(greedy_correct, F_te[:, idx["ENT_mean"]]),
    )
    out = dict(
        model=model_name, n_cal=int(len(y_cal)), n_test=int(len(y_te)),
        tau_warning=tw, tau_fault=tf,
        test_detection_auroc_on_own_generations=auc_safe(y_te, risk_te),
        before=dict(accuracy=float(greedy_correct.mean()), hallucination_rate=before_halluc),
        after=dict(coverage=cov, accuracy_among_answered=1 - after_halluc_among_answered,
                   hallucination_rate_among_answered=after_halluc_among_answered,
                   hallucination_rate_system_wide=after_halluc_system,
                   relative_hallucination_reduction_among_answered=rel_drop_answered,
                   relative_hallucination_reduction_system_wide=rel_drop_system),
        tier_counts={t: int((np.array(tiers) == t).sum()) for t in
                     ("SAFE", "TIER1_RESAMPLE", "TIER2_RETRIEVAL", "TIER3_ABSTAIN")},
        greedy_hallucinations_corrected=dict(by_tier1_resample=t1_fixed, by_tier2_retrieval=t2_fixed),
        selective_prediction_accuracy_at_coverage=sel,
        examples=records,
    )
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        json.dump(out, open(os.path.join(out_dir, "mitigation_report.json"), "w"), indent=2)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    ap.add_argument("--n_cal", type=int, default=150)
    ap.add_argument("--n_test", type=int, default=150)
    ap.add_argument("--no_wikipedia", action="store_true")
    ap.add_argument("--4bit", dest="fourbit", action="store_true")
    ap.add_argument("--out", default=os.path.join(ROOT, "results", "v2", "mitigation"))
    a = ap.parse_args()
    r = run_mitigation(a.model, a.n_cal, a.n_test, not a.no_wikipedia, a.out, a.fourbit)
    print(json.dumps({k: v for k, v in r.items() if k != "examples"}, indent=2))

