# FINAL RESEARCH READINESS REPORT (POST-REVIEW RECONCILED)

**Project:** TRUEGUARD — Empirical Study of White-Box Hallucination Risk Detection on a Frozen Small LLM  
**Workspace:** `E:\trueguard\ieee\TRUEGUARD_IEEE_FINAL`  
**Date:** 2026-11-19  
**Audit Basis:** Full reconciliation of original 10-dataset GPU experiments, independent reproducibility audit, external Colab baselines (`SelfCheckGPT-NLI`, `Semantic Entropy`), and Claude peer-review CPU-only controls (`Controls A, B, C, 4B, 4C`).  
**Pre-Review Backup Preserved At:** [publication_ready_v1_pre_review_backup](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready_v1_pre_review_backup)

---

## 1. Updated Scientific Contributions (Novelty Strictly Separated)

To ensure our claims match what the evidence actually proves, we separate established components, engineering contributions, and original empirical findings:

- **Established Components Reused:** Multi-layer L2-regularized hidden-state probing (SAPLMA-style `ISP`), token entropy/attention/drift statistics (`EEM`, `AAS`, `DST`), and risk-coverage selective abstention (`AURC`). We do **not** claim these individual signals or routing rules as architectural inventions.
- **Engineering Contributions:** A unified single-pass frozen-model white-box instrumentation harness (`tg_pipeline.py`, `0` trainable LLM parameters, `0` external NLI models, `+15.9%` post-pass / `+27.1%` online sequential latency overhead) paired with a fully reproducible 10-dataset group-disjoint benchmark (`32,590` sequences, `0` NaNs/Infs).
- **Three Strongest Original Empirical Findings:**
  1. **Quantifying Dataset Artifacts vs. Residual White-Box Signal in Teacher-Forced Detection (`Table II`, Control A):** High raw HaluEval AUROCs (`0.9880` QA, `0.9936` Summ) are heavily confounded by length (`LEN = 0.9572` on QA) and surface text style (`TF-IDF = 0.9661` QA, `0.9539` Summ); yet single-pass white-box probing beats answer-text `TF-IDF` on all five in-domain benchmarks (`+0.0219` to `+0.0709`) and retains `0.7901–0.8106` (`0.9939` Summ) AUROC under strict length matching (`|ΔL| ≤ 2` tokens).
  2. **Empirical Domain-Shift Diagnostics & Sample-Efficiency Boundaries of Target-Domain Few-Shot Refitting (`Tables III & VIII`, Controls B, 4B, 4C):** Zero-shot pooled probes collapse to chance (`0.4597–0.5205`) and source-risk recalibration fails (`0.4957–0.5242`); within-domain split-half probe weight cosines (`+0.230` to `+0.689` on homogeneous benchmarks) contrast sharply with near-zero cross-domain cosines (`-0.031` to `+0.051`), providing empirical diagnostic evidence of domain-dependent linear decision boundaries. Length-controlled EEM separates genuine length-free uncertainty signal on FaithDial (`0.7662`) and XSum (`0.6648`) from length-confounded inversion on HaluEval-QA (`0.3627 → 0.5184`). Target-only few-shot refitting (`0` source weights transferred) reveals a sharp sample-efficiency boundary: simple baselines win at `K=50`, while `K=250` refitting (`<2s` CPU) yields task-dependent gains on FaithDial (`0.8231`), FEVER (`0.7325`), and WikiBio (`0.6698`), while matching 1D length on XSum (`0.6456` vs. `0.6445`).
  3. **Single-Pass Selective Prediction vs. Multi-Sample External Baselines & Abstention-vs.-Repair Audit on Closed-Book TriviaQA (`Tables V & VII`, Control C):** On `250` held-out TinyLlama-1.1B generations, single-pass TRUEGUARD (`0.7876` AUROC, `0.4360` AURC) significantly outperforms `M=10` Semantic Entropy (`0.6859`, `p_Holm = 0.012 / 0.006`), Predictive Entropy (`0.6583`, `p_Holm = 0.006`), and NLL (`0.4678`, `p_Holm = 0.006`), and performs competitively with `M=10` SelfCheckGPT-NLI (`0.7477`, `p_Holm = 0.478 / 0.362`, n.s.) with `0` external NLI models. Forensically, **risk-calibrated selective abstention** (`55.65%`, `64/115` at `46.0%` coverage) is the primary mitigation driver; active Tier 1/2 resampling and local retrieval (`54.78%`, `63/115`; `4` repaired, `3` broken) provide no demonstrated net benefit on TinyLlama-1.1B.

---

## 2. Final Supported Claims (Zero Contradictions Allowed)

- **Claim 1 (In-Domain):** Single-pass frozen-model white-box probing outperforms answer-text `TF-IDF` on all 5 in-domain benchmarks (`+0.022` to `+0.071`) and retains `0.790–0.811` (`0.994` Summ) AUROC under strict length matching, though raw HaluEval `0.988–0.994` AUROCs are strongly inflated by dataset artifacts. `ISP` accounts for >96% of fusion weight; 4-sensor fusion does **not** consistently outperform ISP-only in AUROC.
- **Claim 2 (Cross-Domain & Target Refitting):** Zero-shot pooled transfer and source-risk recalibration fail (`0.460–0.524`). Target-only few-shot probe refitting at `K=250` yields task-dependent recovery on FaithDial (`0.8231`), FEVER (`0.7325`), and WikiBio (`0.6698`) and cuts ECE by `82–93%`, while simple baselines (`1D EEM`, `1D LEN`, `TF-IDF`) match or outperform TRUEGUARD at `K=50` and on XSum (`K=250` `0.6456` vs. `LEN 0.6445`).
- **Claim 3 (Closed-Book Selective Prediction & Abstention):** On TriviaQA (`n_test = 250`), single-pass TRUEGUARD significantly outperforms Semantic Entropy (`M=10`), Predictive Entropy, and NLL in AUROC and AURC, and matches SelfCheckGPT-NLI (`M=10`, n.s.) without extra generations or NLI models. Selective abstention cuts system-wide incorrect outputs from `66.0%` to `20.4%` (`55.65%` selective accuracy at `46.0%` coverage); active Tier 1/2 repair does not improve upon pure abstention.

---

## 3. All Corrected Tables and Figures

All 8 tables (`.md` + `.csv`) and 10 figures (`300 DPI`) in [publication_ready](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/00_PUBLICATION_PACKAGE_INDEX.md) are reconciled to immutable source files:

| Artifact | Content Summary | Underlying Source Evidence |
| :--- | :--- | :--- |
| [Table I](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/tables/Table1_Dataset_Methodology_and_Splits.md) | 10 datasets, protocol roles, splits, exclusions | `results/final_experiment_report.json` |
| [Table II](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/tables/Table2_InDomain_5Fold_GroupCV.md) | 5-fold Group CV + `LEN`, `TF-IDF`, Shuffled, Length-Matched controls | `final_experiment_report.json`, `reviewer_controls_results.json` |
| [Table III](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/tables/Table3_TargetDomain_FewShot_Refitting.md) | Target-only few-shot refitting (`K=50, 100, 250`) vs. exact Colab zero-shot, `SrcRecal`, `EEM-1D`, `LEN-1D`, `TF-IDF` | `unseen_zeroshot_*.npz`, `phase3_fewshot_adaptation_results.json`, `reviewer_controls_results.json` |
| [Table IV](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/tables/Table4_FourSensor_Ablation_and_Complementarity.md) | LOSO ablation (ISP dominance) & low-FPR complementarity | `results/final_experiment_report.json` |
| [Table V](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/tables/Table5_TriviaQA_SelectiveAbstention_and_Mitigation.md) | TriviaQA selective abstention (`64/115`) vs. 3-tier controller ablation (`63/115`, `4` fixed / `3` broken) | `mitigation_report.json`, `phase5_mitigation_deep_analysis.json`, `reviewer_controls_results.json` |
| [Table VI](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/tables/Table6_Inference_Latency_Profiling.md) | Sequential CUDA T4 latency (`eager`, `bs=1`) + non-equivalence note | `results/real_latency.json` |
| [Table VII](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/tables/Table7_External_Baselines_TriviaQA.md) | External baselines (`SelfCheckGPT-NLI`, `Semantic Entropy`) with finite-sample `p_Holm` | `external_baselines_report.json` |
| [Table VIII](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/tables/Table8_CrossDomain_Diagnostics_Cosine_and_LengthControlled_EEM.md) | Within-domain vs. cross-domain cosine & length-controlled EEM audit | `phase2_cross_domain_diagnostics.json`, `cosine_and_eem_controls.json` |
| `Fig1`–`Fig8` | Updated `Fig2` (Target Refitting vs. Simple Baselines), new `Fig8` (Cosine & Length-Controlled EEM), plus `Fig1`, `Fig3`–`Fig7` | Verified `.npz` / `.json` files |

---

## 4. Dataset-Artifact Limitations (`Table II`)

- **HaluEval-QA (`0.9880` raw):** `LEN` CV alone reaches `0.9572` and answer-text `TF-IDF` reaches `0.9661`; only `6.4%` (`128` pairs) match within `|ΔL| ≤ 2` tokens, where TRUEGUARD drops to `0.7901` (vs. `LEN 0.5516`).
- **HaluEval-Summarization (`0.9936` raw):** `LEN` is neutral (`0.4902`), but answer-text `TF-IDF` alone reaches `0.9539`, proving strong GPT-3.5 stylistic cues (`+0.0397` residual white-box gain).
- **HaluEval-Dialogue (`0.9218`), TruthfulQA (`0.8773`), HaluEval-General (`0.7204`):** `TF-IDF` scores `0.8618`, `0.8064`, and `0.6944` respectively; TRUEGUARD retains `+0.0260` to `+0.0709` gains and `0.7996–0.8106` under length matching, with shuffled-label AUROCs at chance (`0.4894–0.5123`).

---

## 5. Target-Only Few-Shot Refitting Results (`Table III`, `Fig2`)

- **Terminology Corrected:** Phase 3 fits target probes from scratch (`0` source weights transferred) and is consistently named **Target-Domain Few-Shot Refitting** (never transfer learning).
- **Source-Risk Recalibration (`SrcRecal`) Fails Completely:** `0.4957–0.5242` across all 4 targets and all `K`.
- **Low-Data (`K=50`) Caveat:** Simple baselines beat 2,048-d target-only probes on all 4 benchmarks (`1D EEM`: FaithDial `0.7473`, XSum `0.6082`; `TF-IDF`: WikiBio `0.5321`, FEVER `0.5699`).
- **Task-Dependent `K=250` Gains:** Target-only TRUEGUARD beats all simple baselines on FaithDial (`0.8231` vs. `0.7473` EEM), FEVER (`0.7325` vs. `0.6315` TF-IDF), and WikiBio (`0.6698` vs. `0.6103` TF-IDF), while **tying 1D length on XSum (`0.6456` vs. `0.6445`)**.

---

## 6. Abstain-Only vs. Full Three-Tier Controller Comparison (`Table V`)

Four distinct operational concepts are strictly separated:
1. **Risk Detection:** `0.7876` AUROC (`0.8460` AUPRC) on `250` held-out TriviaQA answers.
2. **Selective Answering:** `0.4360` AURC across all coverage thresholds (`34.0% → 55.65%` at `46.0%` coverage).
3. **Abstention-Driven Incorrect Output Reduction (Primary Outcome):** Pure abstain-only (`top-115` lowest risk) yields **`64/115` (`55.65%`)** correct among answered (`20.40%` system-wide incorrect outputs).
4. **Active Factual Correction (Intervention Ablation — No Net Gain):** Full 3-tier controller (`81` Safe, `23` T1 Resample, `11` T2 TF-IDF Retrieval, `135` T3 Abstain) yields **`63/115` (`54.78%`, `-0.87%`)**, repairing `4` hallucinations while breaking `3` originally correct answers.

---

## 7. External Baseline Comparisons (`Table VII`, `Fig7`)

- **TRUEGUARD 4-Sensor (Target-Refitted on 250 cal, `1` gen, `0` NLI):** AUROC `0.7876 [0.720, 0.852]`, AUPRC `0.8460`, F1 `0.8084`, AURC `0.4360 [0.360, 0.523]`, Acc@46% `55.6%`.
- **TRUEGUARD Pooled Zero-Shot (`0` target labels, `1` gen, `0` NLI):** AUROC `0.5504`, AUPRC `0.7124`, AURC `0.6342`, Acc@46% `37.4%` (confirming that target-domain refitting on `250` calibration labels is essential for TRUEGUARD on TriviaQA, whereas SelfCheckGPT-NLI, Semantic Entropy, Predictive Entropy, and NLL are **label-free for ranking**).
- **SelfCheckGPT-NLI (Label-Free, `11` gens, DeBERTa-v3-L):** AUROC `0.7477`, AUPRC `0.8537`, F1 `0.5920`, AURC `0.4659`, Acc@46% `50.4%` (`p_Holm = 0.478 / 0.362`, n.s.).
- **Semantic Entropy LN (Label-Free, `10` gens, DeBERTa-L):** AUROC `0.6859`, AURC `0.5411`, Acc@46% `49.6%` (target-refitted TRUEGUARD significantly better: `p_Holm = 0.012 / 0.006`).
- **Predictive Entropy / NLL (Label-Free, `1` gen):** AUROC `0.6583 / 0.4678`, AURC `0.5309 / 0.6843` (target-refitted TRUEGUARD significantly better: `p_Holm = 0.006`; NLL `0.4678` forensically verified as genuine).

---

## 8. Statistical and Reproducibility Qualifications

- **Independent Audit Passed:** `independent_reproducibility_audit.py` (zero TRUEGUARD imports) verified all metrics to `1.11e-16` and resolved the local `sklearn 1.3.2` unpickling drift by sourcing zero-shot AUROCs directly from Colab `.npz` arrays.
- **Finite-Sample Bootstrap Bounds:** `p = (1 + 2*min) / (B + 1)` with `B = 1000` (`p_raw >= 0.0010`, `p_Holm >= 0.0060`); zero `p = 0.0000` claims remain.
- **Repeated-Seed Variance Flag:** 10-seed refitting SDs hold the 40% test set fixed (Nadeau & Bengio, 2003); marginal differences (`Full` vs. `ISP-only`, `TG` vs. `LEN` on XSum) are reported as practically comparable.
- **Latency Non-Equivalence:** Sequential `4.20x–4.60x` speedup (`real_latency.json`, `eager`, `bs=1`) is explicitly decoupled from GPU-batched (`sdpa`, `bs=10`, early EOS) Colab SelfCheckGPT timings (`0.7068 s/q`).

---

## 9. Outstanding Essential Issues

- **Zero essential scientific, statistical, or consistency issues remain** under the recommended small-LLM empirical study framing.
- **Scope Limitations (Explicitly Disclosed, Not Blockers for IEEE Access):** Single `1.1B` frozen model (`TinyLlama-1.1B-Chat-v1.0`), moderate TriviaQA test power (`n_test = 250`), prior inspection of the 4 unseen datasets before target-only refitting, and un-reproduced unsupervised white-box baselines (`CCS`, `EigenScore`).

---

## 10. Recommended IEEE Access Manuscript Title & Section Structure

**Recommended Title:**  
*TRUEGUARD: An Empirical Study of White-Box Hallucination Risk Detection, Domain-Dependent Internal Signals, and Few-Shot Refitting for Selective Prediction*

**Recommended Section Structure:**
1. **Introduction** — Motivation for single-pass white-box risk detection on small frozen LLMs; explicit scope (empirical & diagnostic study, not an architectural invention); summary of the 3 empirical findings.
2. **Related Work** — Black-box multi-sampling (SelfCheckGPT, Semantic Entropy), white-box probing & internal signals (SAPLMA, CCS, ITI, EigenScore, Lookback Lens), benchmark artifacts, and selective prediction.
3. **Methodology & TRUEGUARD Instrumentation** — Frozen `TinyLlama-1.1B` single-pass extraction of `ISP`, `AAS`, `EEM`, `DST`; calibration and group-disjoint protocol; selective abstention vs. 3-tier intervention ablation.
4. **Experimental Setup & Controls** — 10-dataset benchmark (`Table I`), artifact controls (`LEN`, `TF-IDF`, shuffled, length-matched), target-only refitting protocol, faithful external baseline reproductions, and finite-sample statistical tests.
5. **In-Domain Detection & Dataset-Artifact Audit** — `Table II`, `Table IV`, `Fig5`–`Fig6`: exposing HaluEval length/style artifacts alongside residual white-box signal and ISP dominance.
6. **Domain-Shift Diagnostics & Target-Domain Few-Shot Refitting** — `Table III`, `Table VIII`, `Fig1`, `Fig2`, `Fig4`, `Fig8`: zero-shot collapse, within- vs. cross-domain probe cosine evidence, length-controlled EEM audit, and sample-efficiency boundaries (`K=50, 100, 250`).
7. **Closed-Book Selective Prediction, External Baselines, and Abstention vs. Active Repair** — `Table V`, `Table VI`, `Table VII`, `Fig3`, `Fig7`: TriviaQA head-to-head comparison, honest abstain-only (`55.65%`) vs. 3-tier controller (`54.78%`) ablation, and non-equivalent latency accounting.
8. **Limitations, Practical Recommendations, and Conclusion** — Single-model scope, deployment guidance (use `1D EEM` at `K<=50`, target-only `ISP/TG` refitting at `K>=250`, and pure selective abstention over ungrounded self-repair on 1B-class models).

---

## Final Verdict

# **READY TO DRAFT IEEE ACCESS MANUSCRIPT**

All reviewer-identified weaknesses have been either quantitatively controlled (`Controls A, B, C, 4B, 4C`), reconciled across every table/figure/manifest, or transparently scoped as explicit limitations. Every numerical claim in the `publication_ready/` package now traces cleanly to immutable, independently audited experimental evidence with zero internal contradictions.
