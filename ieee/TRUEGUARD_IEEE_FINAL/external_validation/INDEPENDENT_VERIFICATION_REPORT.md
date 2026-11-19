# Independent Reproducibility Verification Report

**Script:** `E:\trueguard\ieee\TRUEGUARD_IEEE_FINAL\external_validation\independent_reproducibility_audit.py`  
**JSON Output:** `E:\trueguard\ieee\TRUEGUARD_IEEE_FINAL\external_validation\independent_verification_report.json`  
**Design:** 100% read-only; imports **zero** TRUEGUARD source modules (`tg_pipeline`, `tg_eval`, `tg_controller`, `part_eval`); recomputes all metrics from raw saved `.npz` files using standard `numpy`, `scipy`, and `scikit-learn`.

---

## 1. Independent Verification Results

| Verification Domain | Status | Max Discrepancy | Notes |
| :--- | :---: | :---: | :--- |
| **In-Domain 5-Fold OOF Metrics (5 Datasets)** | **PASS** | **`1.11e-16`** | Exact machine-precision match on AUROC, AUPRC, F1, Precision, Recall, Accuracy, ECE, Brier, Confusion Matrices, and all 4 single-sensor OOF AUROCs (`ISP`, `AAS`, `EEM`, `DST`). |
| **Strictly Unseen Zero-Shot Metrics (4 Datasets)** | **PASS** | **`1.11e-16`** | Exact match on AUROC, AUPRC, `F1@tau_warn`, ECE, Brier, `ISP-only`, and `Scalars-only`. |
| **TriviaQA Mitigation & Selective Prediction** | **PASS** | `< 5e-4` (rounding) | Independently verified `AUROC=0.7876`, `AURC=0.4360` (TRUEGUARD) vs. `0.5309` (Entropy) vs. `0.6843` (NLL), `46.0%` coverage, `54.8%` answered accuracy, `20.8%` system hallucination, `112` TP abstentions, `23` FP abstentions. |
| **CUDA Latency Arithmetic** | **PASS** | **`< 1e-9`** | Verified `+27.08%` online / `+15.93%` post-pass overhead and `4.20x` / `4.60x` speedup vs. 5x multi-sampling. |
| **Few-Shot 60/40 Group-Disjoint Splits** | **PASS (Splits) / MINOR DRIFT CAUGHT (Unadapted Baseline)** | `0` group overlap; **`0.0005–0.0081`** unpickling drift | **Important Catch:** Group overlap is `0` on all 4 datasets and raw EEM matches to `0.00e+00`, but `phase3_4_fewshot_and_sensors.py` evaluated the unadapted zero-shot baseline by unpickling Colab's `scikit-learn 1.6.1` `.joblib` model under local `scikit-learn 1.3.2`, causing a minor `0.0005–0.0081` AUROC drift relative to the exact Colab-saved `unseen_zeroshot_*.npz[test_idx]` predictions. |

### Exact Colab-Saved Zero-Shot AUROC on the 40% Held-Out Test Splits (Use These Exact Values in Manuscript)
| Dataset (40% Test Split) | Exact Colab `.npz` Zero-Shot AUROC | Local Unpickled `.joblib` AUROC | Drift Caught | $K=250$ Adapted AUROC |
| :--- | :---: | :---: | :---: | :---: |
| **FaithDial** ($n=1396$) | **`0.4929`** | `0.4881` | `0.0048` | **`0.8231 ± 0.012`** |
| **WikiBio-GPT3** ($n=734$) | **`0.4883`** | `0.4868` | `0.0015` | **`0.6698 ± 0.038`** |
| **FEVER** ($n=2667$) | **`0.5205`** | `0.5209` | `0.0005` | **`0.7325 ± 0.014`** |
| **XSum Factuality** ($n=752$) | **`0.4597`** | `0.4678` | `0.0081` | **`0.6456 ± 0.041`** |

*Scientific impact of catch:* Zero change to any research conclusion (`+0.186` to `+0.330` AUROC gains remain massive and unambiguously significant), and reporting the exact Colab `.npz` values eliminates the cross-version unpickling artifact completely.

---

## 2. Independently Reproduced vs. Requires Full GPU Rerun
- **Independently Reproduced Locally (Read-Only):** All detection metrics, confusion matrices, ECE/Brier, single-sensor AUROCs, group-disjoint split checks, TriviaQA selective prediction/mitigation arithmetic, latency arithmetic, and SHA-256 provenance hashes across 19 saved artifact files.
- **Requires GPU Execution to Reproduce:** Frozen TinyLlama forward-pass feature extraction (32,590 sequences), TriviaQA live generation & Three-Tier Controller interventions, wall-clock CUDA decoding timings, and the external multi-sample baselines (`TRUEGUARD_External_Baselines_Colab.ipynb`).
