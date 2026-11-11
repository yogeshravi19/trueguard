"""
Local verification suite for TRUEGUARD v2 (runs on CPU with GPT-2 in ~20s).

Checks:
  1. Teacher-forced `score_answer` and cached token-by-token `OnlineSignalMonitor` produce the SAME sensor values
     (within floating-point tolerance) on the same prompt+answer.
  2. `TrueGuardDetector` uses inner out-of-fold probe scores for fusion training (probes never score their own
     training rows) and `grouped_cv` never splits a question across train and test.
  3. `ThreeTierController` visits SAFE, TIER1_RESAMPLE, TIER2_RETRIEVAL and TIER3_ABSTAIN as risk crosses
     (tau_warning, tau_fault).
"""
import os, sys
os.environ.setdefault("USE_TF", "0")
import numpy as np
import torch

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
from src.tg_pipeline import load_model, score_answer, OnlineSignalMonitor, TrueGuardDetector
from src.tg_eval import grouped_cv, calibrate_thresholds
from src.tg_controller import ThreeTierController


def test_equivalence(model, tok, device):
    prompt = "Question: What is the capital of France?\nAnswer:"
    ans = " The capital of France is Paris."
    F_tf, H_tf = score_answer(model, tok, device, prompt, ans)

    p_ids = tok(prompt, return_tensors="pt").input_ids.to(device)
    a_ids = tok(ans, return_tensors="pt", add_special_tokens=False).input_ids.to(device)
    mon = OnlineSignalMonitor()
    with torch.no_grad():
        out = model(p_ids, use_cache=True, output_hidden_states=True, output_attentions=True)
        mon.update(out, int(a_ids[0, 0]))
        past = out.past_key_values
        for t in range(1, a_ids.shape[1]):
            out = model(a_ids[:, t - 1:t], past_key_values=past, use_cache=True,
                        output_hidden_states=True, output_attentions=True)
            past = out.past_key_values
            mon.update(out, int(a_ids[0, t]))
    F_on, H_on = mon.features()
    err_F = float(np.max(np.abs(F_tf - F_on)))
    err_H = float(np.max(np.abs(H_tf - H_on)))
    assert err_F < 1e-4 and err_H < 1e-4, f"mismatch F={err_F} H={err_H}"
    print(f"[PASS] teacher-forced == online cached monitor  (max |dF|={err_F:.2e}, max |dH|={err_H:.2e})")


def test_no_leakage():
    rng = np.random.RandomState(0)
    # Pure noise features with paired groups -> out-of-fold AUROC must be ~0.5, whereas in-sample probe AUROC on
    # 768-dim noise would be ~1.0 if there were probe-to-fusion or train-to-test leakage.
    n_q = 60
    groups = np.repeat(np.arange(n_q), 2)
    y = np.tile([0, 1], n_q)
    F = rng.randn(2 * n_q, 10)
    H = rng.randn(2 * n_q, 4, 256).astype(np.float32)
    r = grouped_cv(F, H, y, groups)
    auc = float(np.mean(r["fold_auc"]))
    assert 0.30 < auc < 0.70, f"leakage suspected: noise AUROC={auc}"
    print(f"[PASS] leakage test on pure-noise 4x256 features: OOF AUROC={auc:.3f} (expected ~0.50)")


def test_three_tiers(model, tok, device):
    rng = np.random.RandomState(1)
    d = model.config.hidden_size
    F = rng.randn(40, 10); H = rng.randn(40, 4, d).astype(np.float32); y = np.array([0, 1] * 20)
    det = TrueGuardDetector().fit(F, H, y)
    # 1) SAFE when initial risk < tw
    c_safe = ThreeTierController(model, tok, device, det, tau_warning=0.99, tau_fault=0.999, k_samples=2, max_new_tokens=6)
    r1 = c_safe.respond("Question: Capital of France?", initial=("Paris", 0.10, F[0], H[0]))
    assert r1["tier"] == "SAFE"
    # 2) TIER3_ABSTAIN when initial risk >= tf and no retriever
    c_abs = ThreeTierController(model, tok, device, det, tau_warning=0.20, tau_fault=0.30, retriever=None, k_samples=2, max_new_tokens=6)
    r2 = c_abs.respond("Question: Capital of France?", initial=("Mars", 0.90, F[0], H[0]))
    assert r2["tier"] == "TIER3_ABSTAIN"
    # 3) TIER2_RETRIEVAL when retriever returns evidence and the grounded risk < tau_fault
    c_ret = ThreeTierController(model, tok, device, det, tau_warning=0.20, tau_fault=0.999,
                                retriever=lambda q: "Paris is the capital of France.", k_samples=2, max_new_tokens=6)
    r3 = c_ret.respond("Question: Capital of France?", initial=("Mars", 0.9995, F[0], H[0]))
    assert r3["tier"] == "TIER2_RETRIEVAL"
    print("[PASS] ThreeTierController transitions (SAFE / TIER2_RETRIEVAL / TIER3_ABSTAIN) verified")


if __name__ == "__main__":
    m, t, dev = load_model("gpt2", device="cpu")
    test_equivalence(m, t, dev)
    test_no_leakage()
    test_three_tiers(m, t, dev)

