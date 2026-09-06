"""
TRUEGUARD Ablation Study
Quantifies the contribution of each intrinsic signal by evaluating:
- Full TRUEGUARD (4 Signals: ISP, AAS, EEM, DST)
- Minus ISP (-ISP)
- Minus AAS (-AAS)
- Minus EEM (-EEM)
- Minus DST (-DST)
- Individual Signal Baselines (ISP only, AAS only, EEM only, DST only)
"""

import os
os.environ["USE_TF"] = "0"
os.environ["USE_TORCH"] = "1"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import sys
import json
import numpy as np

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from src.evaluation import evaluate_cross_validation
from src.normalization import OnlineZScoreScaler
from experiments.run_benchmark import generate_benchmark_distribution

def run_ablation_study():
    print("=" * 70)
    print("[TRUEGUARD] ABLATION STUDY: SIGNAL COMPLEMENTARITY ANALYSIS")
    print("=" * 70)

    # Use combined multi-domain evaluation set
    X_full, y = generate_benchmark_distribution("TruthfulQA", n_samples=500, seed=100)
    scaler = OnlineZScoreScaler(num_features=4)
    X_norm = scaler.fit_transform(X_full)

    # Feature indices: 0: ISP, 1: AAS, 2: EEM, 3: DST
    ablation_configs = {
        "Full TRUEGUARD (4 Signals)": [0, 1, 2, 3],
        "- ISP (Without Internal State Probes)": [1, 2, 3],
        "- AAS (Without Attention Anomaly Score)": [0, 2, 3],
        "- EEM (Without Entropy-Energy Monitor)": [0, 1, 3],
        "- DST (Without Distribution Shift Tracker)": [0, 1, 2],
        "ISP Only": [0],
        "AAS Only": [1],
        "EEM Only": [2],
        "DST Only": [3]
    }

    results = {}
    full_auroc = None

    for name, indices in ablation_configs.items():
        X_sub = X_norm[:, indices]
        cv_res = evaluate_cross_validation(X_sub, y, n_splits=5, seed=42)
        mean_auc = cv_res["mean_auroc"]
        std_auc = cv_res["std_auroc"]

        if full_auroc is None:
            full_auroc = mean_auc
            delta = 0.0
        else:
            delta = mean_auc - full_auroc

        results[name] = {
            "indices": indices,
            "mean_auroc": mean_auc,
            "std_auroc": std_auc,
            "delta_from_full": delta,
            "ci_95": cv_res["ci_95"]
        }

        sign = "+" if delta > 0 else ""
        delta_str = f"{sign}{delta:.4f}" if delta != 0.0 else "---"
        print(f"  • {name:<45} AUROC: {mean_auc:.4f} +/- {std_auc:.4f} (Delta: {delta_str})")

    out_dir = os.path.join(ROOT_DIR, "results")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "ablation_results.json")

    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n[OK] Ablation study complete. Results saved to: {out_file}")
    return results

if __name__ == "__main__":
    run_ablation_study()
