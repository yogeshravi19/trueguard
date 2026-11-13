"""
Structured Black-and-White Word Table replacements for all 14 interior figures
so that FINAL_REPORT.docx / FINAL_REPORT.pdf contains ZERO interior raster images
(only the 4 front-matter pages have the VIT Chennai logo) and can be printed in
Black & White without paying for interior color pages.
"""
from __future__ import annotations

from typing import Dict, List, Tuple

# Maps fig_id -> (headers, rows, col_widths_cm, font_size)
FIG_REPLACEMENT_TABLES: Dict[str, Tuple[List[str], List[Tuple[str, ...]], List[float], float]] = {
    "3.1": (
        ["PRISMA 2020 Stage", "Records Entering Stage", "Database / Screening Action & Criteria Applied", "Records Excluded & Documented Reasons", "Records Advancing"],
        [
            ("Stage 1: Identification", "688 initial records", "Queried 5 databases (Jan 1, 2020 – Feb 28, 2026): arXiv (214), Scopus (186), IEEE Xplore (112), Web of Science (92), ACM Digital Library (84).", "196 duplicate records removed via cross-repository title/DOI deduplication.", "492 unique records"),
            ("Stage 2: Screening", "492 unique records", "Independent title & abstract screening by both authors against Inclusion Criteria IC1–IC6 and Exclusion Criteria EC1–EC4.", "324 off-topic records excluded: 218 general NLP/translation/sentiment papers; 106 non-technical notes or demos.", "168 full-text candidates"),
            ("Stage 3: Eligibility", "168 full-text articles", "Full-text appraisal across 4 quality criteria: Methodological Rigor, Benchmark Validity, Metric Reliability, and Deployment Transparency.", "128 articles excluded: 54 prompt heuristics only without internal probing; 42 lacking standard baselines; 32 redundant methods.", "40 included primary studies"),
            ("Stage 4: Inclusion & Synthesis", "40 primary studies", "Divided into 20 Core Architectural Studies + 20 Foundational Benchmarks & Mitigation Frameworks across 6 Research Pillars.", "0 excluded (100% retained in final synthesis: Pillar 1 [8], Pillar 2 [6], Pillar 3 [4], Pillar 4 [9], Pillar 5 [11], Pillar 6 [2]).", "40 synthesized studies"),
        ],
        [2.4, 2.2, 4.3, 3.5, 2.2],
        8.8,
    ),
    "4.1": (
        ["Closed-Loop Subsystem Block", "Control-Theoretic Role", "Input Signals / Tensors", "Mathematical Operation Executed", "Output / Control Signal"],
        [
            ("1. Input Prompt & Tokenizer", "Reference Input r_ref(t)", "Raw user query x and optional retrieved context C(x).", "Subword tokenization into prompt sequence x = (x_1, ..., x_m) of length m.", "Token IDs x in V^m fed to Plant."),
            ("2. Autoregressive Transformer Plant", "Open-Loop Dynamical System M_theta", "Prompt x and previously generated tokens y_{<t} with KV cache.", "Single forward pass across L layers, H heads/layer, hidden dimension d, producing h_{l,t}, alpha_{l,h,t}, and logits z_t.", "Candidate token y_t, hidden states {h_{l,t}}, attentions {alpha_{l,h,t}}, logits z_t."),
            ("3. Four-Sensor Observation Bank", "Multi-Channel Internal Observer", "Residual states h_{l,t}, top-quartile attentions alpha_{l,h,t}, logits z_t.", "Computes Sensor 1 ISP (F_t at {0.45,0.60,0.75,0.90}L), Sensor 2 AAS (A_t), Sensor 3 EEM (H_{ent,t}), Sensor 4 DST (D_t).", "Sequence-pooled 4D feature vector phi(x,y) = [F_bar, A_bar, H_bar_ent, D_bar]^T."),
            ("4. OOF State Estimator & XAI Engine", "Calibrated Risk & Log-Odds Attribution", "Pooled sensor vector phi(x,y) standardized via training mu_k, sigma_k.", "L2 logistic fusion r(x,y) = sigma(w_0 + sum w_k z_k) and exact additive log-odds breakdown c_k = w_k z_k.", "Calibrated risk score r(x,y) in [0,1] + per-sensor attributions {c_ISP, c_AAS, c_EEM, c_DST}."),
            ("5. Three-Tier Graded Actuator", "Closed-Loop Feedback Controller", "Calibrated risk r(x,y) compared against (tau_warning = 0.611, tau_fault = 0.898).", "SAFE (r < 0.611): emit y^(0); TIER 1 (0.611 <= r < 0.898): annealed re-sample T in {0.35,0.20}; TIER 2 (r >= 0.898): Wikipedia RAG + re-verify; TIER 3: abstain.", "Verified factual response y* or transparent calibrated abstention with explanation."),
        ],
        [2.7, 2.3, 2.7, 4.1, 2.8],
        8.6,
    ),
    "5.1": (
        ["Pipeline Stage", "Partition / Module", "Input Data & Group Structure", "Leakage-Prevention & Stacking Operation", "Verified Output Artifact"],
        [
            ("Stage 1: Corpus Ingestion", "tg_data.load_balanced_subset", "Paired benchmark JSONL (796 TruthfulQA; 800 each on HaluEval QA, Dialogue, Summarization).", "Assigns identical group_id = Q_i to both factual (y=0) and hallucinated (y=1) responses of question Q_i.", "N = 3,196 grouped prompt-answer records."),
            ("Stage 2: Outer GroupKFold", "GroupKFold(n_splits=5)", "Full dataset partitioned by question group_id G = {g_1, ..., g_M}.", "Enforces G_train^(k) intersect G_test^(k) = empty_set so no question ever straddles train and test splits.", "5 disjoint outer train/test fold pairs (80% train / 20% test)."),
            ("Stage 3: Inner OOF Probe Stacking", "SupervisedLayerProbe.fit_and_oof", "Outer training split hidden states hbar_l at depths {0.45, 0.60, 0.75, 0.90}L.", "Runs 3-fold inner GroupKFold on outer train split; predicts held-out inner fold ISP probabilities F_i^OOF (C = 0.25).", "Leakage-free inner out-of-fold vector F_train^OOF in (0,1)^{N_train}."),
            ("Stage 4: Full Outer Probe Fit", "SupervisedLayerProbe.fit", "All samples in outer training split (N_train).", "Fits final 4-layer StandardScaler + L2 LogisticRegression(C=0.25) probes on full outer training fold for test inference.", "Frozen outer-fold layer probes {p_l}_{l in L_probe}."),
            ("Stage 5: 4-Sensor Meta-Combiner", "TrueGuardDetector.fit", "Outer train matrix [F_train^OOF, A_train, H_ent,train, D_train].", "Fits StandardScaler + L2 LogisticRegression(C=1.0) on inner OOF ISP + unsupervised sensors; prevents ISP weight dominance.", "Calibrated fusion weights w = [w_ISP, w_AAS, w_EEM, w_DST] and intercept w_0."),
            ("Stage 6: Blind Fold Evaluation", "run_grouped_cv_evaluation", "Outer test split features [F_test, A_test, H_ent,test, D_test].", "Predicts blind out-of-fold risk r_i; aggregates all 5 folds; computes 500-resample group-bootstrap 95% CIs.", "Out-of-fold AUROC, AUPRC, F1, Brier, ECE, and log-odds attributions."),
        ],
        [2.4, 2.6, 3.0, 4.0, 2.6],
        8.6,
    ),
    "7.1": (
        ["Method / Detector Variant", "Category", "HaluEval-Dialogue", "HaluEval-QA", "HaluEval-Summ.", "TruthfulQA", "Macro AUROC", "Macro AUPRC", "Macro F1", "Macro ECE"],
        [
            ("TRUEGUARD (Full 4-Sensor)", "Proposed Fusion", "0.903", "0.975", "0.986", "0.876", "0.935", "0.938", "0.882", "0.031"),
            ("Sensor 1: ISP Only (4-Layer Probe)", "Single Sensor", "0.904", "0.977", "0.987", "0.877", "0.936", "0.939", "0.883", "0.033"),
            ("Sensor 4: DST Only (Cosine Drift)", "Single Sensor", "0.634", "0.859", "0.672", "0.533", "0.675", "0.659", "0.662", "0.058"),
            ("Sensor 3: EEM Only (Shannon+Renyi)", "Single Sensor", "0.668", "0.850", "0.580", "0.522", "0.655", "0.642", "0.645", "0.064"),
            ("Sensor 2: AAS Only (Top-Q Attention)", "Single Sensor", "0.618", "0.512", "0.627", "0.607", "0.591", "0.583", "0.598", "0.052"),
            ("Without ISP (AAS + EEM + DST)", "Grey-Box Fallback", "0.714", "0.918", "0.745", "0.626", "0.751", "0.744", "0.715", "0.055"),
            ("Raw Normalized Entropy (ENT_mean)", "Scalar Baseline", "0.666", "0.349 (inv 0.651)", "0.580", "0.522", "0.529 (0.605)", "0.541", "0.612", "0.184"),
            ("Raw Mean Token NLL (NLL_mean)", "Scalar Baseline", "0.645", "0.089 (inv 0.911)", "0.362 (inv 0.638)", "0.495 (inv 0.505)", "0.398 (0.675)", "0.462", "0.589", "0.241"),
            ("Raw Helmholtz Energy (Energy_mean)", "Scalar Baseline", "0.602", "0.168 (inv 0.832)", "0.489 (inv 0.511)", "0.492 (inv 0.508)", "0.438 (0.613)", "0.478", "0.574", "0.265"),
            ("Response Token Length (LEN)", "Surface Heuristic", "0.687", "0.953", "0.534", "0.518", "0.673", "0.651", "0.648", "0.195"),
        ],
        [3.1, 1.8, 1.5, 1.6, 1.5, 1.3, 1.1, 1.0, 0.85, 0.85],
        8.2,
    ),
    "7.2": (
        ["FPR Operating Point", "TRUEGUARD TPR (Recall)", "ISP Only TPR", "AAS Only TPR", "EEM Only TPR", "DST Only TPR", "Without ISP (-ISP) TPR", "Corresponding Risk Threshold"],
        [
            ("FPR = 0.01 (1% False Positives)", "0.286 (114 / 398)", "0.281", "0.025", "0.015", "0.020", "0.065", "tau = 0.962"),
            ("FPR = 0.05 (5% False Positives)", "0.442 (176 / 398)", "0.440", "0.085", "0.063", "0.070", "0.158", "tau = 0.894"),
            ("FPR = 0.10 (10% False Positives)", "0.603 (240 / 398)", "0.525", "0.186", "0.128", "0.141", "0.254", "tau = 0.812"),
            ("FPR = 0.20 (20% False Positives)", "0.789 (314 / 398)", "0.784", "0.342", "0.236", "0.259", "0.412", "tau = 0.635"),
            ("FPR = 0.30 (30% False Positives)", "0.869 (346 / 398)", "0.867", "0.472", "0.349", "0.374", "0.548", "tau = 0.485"),
            ("FPR = 0.50 (50% False Positives)", "0.947 (377 / 398)", "0.945", "0.688", "0.543", "0.560", "0.746", "tau = 0.241"),
            ("Overall Out-of-Fold AUROC [95% CI]", "0.876 [0.853, 0.900]", "0.877", "0.607", "0.522", "0.533", "0.626 [0.585, 0.662]", "Youden J* = 0.636 (F1 = 0.817)"),
        ],
        [2.8, 2.2, 1.4, 1.4, 1.4, 1.4, 1.9, 2.1],
        8.4,
    ),
    "7.3": (
        ["FPR Operating Point", "TRUEGUARD TPR (Recall)", "ISP Only TPR", "AAS Only TPR", "EEM Only TPR", "DST Only TPR", "Without ISP (-ISP) TPR", "Corresponding Risk Threshold"],
        [
            ("FPR = 0.01 (1% False Positives)", "0.785 (314 / 400)", "0.788", "0.035", "0.028", "0.045", "0.195", "tau = 0.978"),
            ("FPR = 0.05 (5% False Positives)", "0.922 (369 / 400)", "0.925", "0.125", "0.102", "0.180", "0.385", "tau = 0.886"),
            ("FPR = 0.10 (10% False Positives)", "0.955 (382 / 400)", "0.953", "0.228", "0.185", "0.312", "0.518", "tau = 0.742"),
            ("FPR = 0.20 (20% False Positives)", "0.980 (392 / 400)", "0.980", "0.395", "0.335", "0.510", "0.692", "tau = 0.468"),
            ("FPR = 0.30 (30% False Positives)", "0.990 (396 / 400)", "0.990", "0.532", "0.468", "0.648", "0.805", "tau = 0.264"),
            ("FPR = 0.50 (50% False Positives)", "0.998 (399 / 400)", "0.998", "0.745", "0.692", "0.825", "0.915", "tau = 0.082"),
            ("Overall Out-of-Fold AUROC [95% CI]", "0.986 [0.980, 0.991]", "0.987", "0.627", "0.580", "0.672", "0.745 [0.710, 0.779]", "Youden J* = 0.870 (F1 = 0.935)"),
        ],
        [2.8, 2.2, 1.4, 1.4, 1.4, 1.4, 1.9, 2.1],
        8.4,
    ),
    "7.4": (
        ["TruthfulQA Ablation Variant", "Active Sensor Set", "AUROC [95% Group Bootstrap CI]", "AUPRC", "F1 Score", "Accuracy", "Brier Score", "ECE", "Delta AUROC vs. Full"],
        [
            ("TRUEGUARD (Full)", "{ISP, AAS, EEM, DST}", "0.876 [0.853, 0.900]", "0.875", "0.817", "0.810", "0.140", "0.042", "Baseline (0.000)"),
            ("Without ISP (-ISP)", "{AAS, EEM, DST}", "0.626 [0.585, 0.662]", "0.619", "0.667", "0.606", "0.238", "0.058", "-0.251 (p < 0.0001)"),
            ("Without AAS (-AAS)", "{ISP, EEM, DST}", "0.876 [0.852, 0.900]", "0.875", "0.817", "0.810", "0.140", "0.041", "-0.000 (n.s.)"),
            ("Without EEM (-EEM)", "{ISP, AAS, DST}", "0.877 [0.854, 0.901]", "0.876", "0.818", "0.812", "0.139", "0.040", "+0.001 (n.s.)"),
            ("Without DST (-DST)", "{ISP, AAS, EEM}", "0.877 [0.853, 0.900]", "0.875", "0.818", "0.812", "0.140", "0.043", "+0.001 (n.s.)"),
            ("ISP Only", "{ISP}", "0.877 [0.854, 0.901]", "0.876", "0.818", "0.812", "0.139", "0.039", "+0.001"),
            ("AAS Only", "{AAS}", "0.607 [0.569, 0.646]", "0.594", "0.668", "0.587", "0.242", "0.051", "-0.269"),
            ("DST Only", "{DST}", "0.533 [0.493, 0.573]", "0.538", "0.667", "0.530", "0.249", "0.048", "-0.343"),
            ("EEM Only", "{EEM}", "0.522 [0.482, 0.563]", "0.526", "0.666", "0.524", "0.250", "0.054", "-0.354"),
        ],
        [2.5, 2.2, 2.5, 1.1, 1.1, 1.1, 1.1, 0.9, 2.1],
        8.2,
    ),
    "7.5": (
        ["HaluEval-QA Ablation Variant", "Active Sensor Set", "AUROC [95% Group Bootstrap CI]", "AUPRC", "F1 Score", "Accuracy", "Brier Score", "ECE", "Delta AUROC vs. Full"],
        [
            ("TRUEGUARD (Full)", "{ISP, AAS, EEM, DST}", "0.975 [0.964, 0.987]", "0.970", "0.955", "0.955", "0.044", "0.024", "Baseline (0.000)"),
            ("Without ISP (-ISP)", "{AAS, EEM, DST}", "0.918 [0.897, 0.937]", "0.902", "0.866", "0.861", "0.112", "0.046", "-0.057 (p < 0.0001)"),
            ("Without AAS (-AAS)", "{ISP, EEM, DST}", "0.976 [0.965, 0.987]", "0.971", "0.955", "0.955", "0.044", "0.023", "+0.001 (n.s.)"),
            ("Without EEM (-EEM)", "{ISP, AAS, DST}", "0.976 [0.965, 0.987]", "0.971", "0.956", "0.956", "0.043", "0.023", "+0.001 (n.s.)"),
            ("Without DST (-DST)", "{ISP, AAS, EEM}", "0.975 [0.964, 0.987]", "0.970", "0.955", "0.955", "0.044", "0.024", "+0.000 (n.s.)"),
            ("ISP Only", "{ISP}", "0.977 [0.966, 0.987]", "0.972", "0.956", "0.956", "0.043", "0.022", "+0.002"),
            ("DST Only", "{DST}", "0.859 [0.831, 0.885]", "0.835", "0.799", "0.792", "0.153", "0.057", "-0.116"),
            ("EEM Only", "{EEM}", "0.850 [0.822, 0.876]", "0.838", "0.785", "0.779", "0.158", "0.062", "-0.125"),
            ("AAS Only", "{AAS}", "0.512 [0.471, 0.553]", "0.515", "0.667", "0.515", "0.250", "0.049", "-0.463"),
        ],
        [2.5, 2.2, 2.5, 1.1, 1.1, 1.1, 1.1, 0.9, 2.1],
        8.2,
    ),
    "7.6": (
        ["Benchmark Dataset (Out-of-Fold)", "True Negatives (TN: Grounded -> Safe)", "False Positives (FP: Grounded -> Flag)", "False Negatives (FN: Halluc. -> Safe)", "True Positives (TP: Halluc. -> Flag)", "Precision (PPV)", "Recall (TPR)", "Specificity (TNR)", "Overall Accuracy & F1"],
        [
            ("HaluEval — QA (N = 800)", "383 / 400 (95.8%)", "17 / 400 (4.2%)", "19 / 400 (4.8%)", "381 / 400 (95.2%)", "0.957", "0.953", "0.958", "Acc = 95.5%, F1 = 0.955"),
            ("HaluEval — Summarization (N = 800)", "371 / 400 (92.8%)", "29 / 400 (7.2%)", "23 / 400 (5.8%)", "377 / 400 (94.2%)", "0.929", "0.943", "0.928", "Acc = 93.5%, F1 = 0.935"),
            ("HaluEval — Dialogue (N = 800)", "324 / 400 (81.0%)", "76 / 400 (19.0%)", "69 / 400 (17.2%)", "331 / 400 (82.8%)", "0.813", "0.828", "0.810", "Acc = 81.9%, F1 = 0.820"),
            ("TruthfulQA (N = 796)", "312 / 398 (78.4%)", "86 / 398 (21.6%)", "65 / 398 (16.3%)", "333 / 398 (83.7%)", "0.795", "0.837", "0.784", "Acc = 81.0%, F1 = 0.817"),
            ("Pooled Total (N = 3,196)", "1,390 / 1,598 (87.0%)", "208 / 1,598 (13.0%)", "176 / 1,598 (11.0%)", "1,422 / 1,598 (89.0%)", "0.872", "0.890", "0.870", "Acc = 88.0%, F1 = 0.882"),
        ],
        [2.6, 1.8, 1.8, 1.8, 1.8, 1.1, 1.1, 1.1, 1.5],
        8.2,
    ),
    "7.7": (
        ["Predicted Risk Bin r(x,y)", "Regime Classification", "HaluEval-Dialogue Count (Grounded / Halluc.)", "HaluEval-QA Count (Grounded / Halluc.)", "Empirical Hallucination Rate", "Mean Predicted Risk", "Absolute Calibration Gap |Emp - Pred|"],
        [
            ("[0.00, 0.20)", "SAFE Regime (High Grounding Confidence)", "268 Grounded / 24 Halluc.", "364 Grounded / 9 Halluc.", "0.082 (Dialogue) / 0.024 (QA)", "0.074 / 0.031", "0.008 / 0.007"),
            ("[0.20, 0.40)", "SAFE Regime (Moderate Grounding)", "56 Grounded / 45 Halluc.", "19 Grounded / 10 Halluc.", "0.446 (Dialogue) / 0.345 (QA)", "0.302 / 0.298", "0.044 / 0.047"),
            ("[0.40, 0.611)", "SAFE Boundary (Below tau_warning = 0.611)", "38 Grounded / 49 Halluc.", "8 Grounded / 11 Halluc.", "0.563 (Dialogue) / 0.579 (QA)", "0.508 / 0.512", "0.055 / 0.067"),
            ("[0.611, 0.898)", "WARNING Regime (Tier 1 Re-Sampling Zone)", "27 Grounded / 118 Halluc.", "6 Grounded / 42 Halluc.", "0.814 (Dialogue) / 0.875 (QA)", "0.768 / 0.784", "0.046 / 0.091"),
            ("[0.898, 1.00]", "FAULT Regime (Tier 2 RAG / Tier 3 Abstain)", "11 Grounded / 164 Halluc.", "3 Grounded / 328 Halluc.", "0.937 (Dialogue) / 0.991 (QA)", "0.952 / 0.976", "0.015 / 0.015"),
        ],
        [1.9, 2.5, 2.4, 2.3, 2.1, 1.7, 1.7],
        8.2,
    ),
    "7.8": (
        ["Source Dataset -> Target Dataset", "TRUEGUARD Transfer AUROC", "ISP Only Transfer AUROC", "Without ISP (-ISP) Transfer", "Learned Source Weights [w_ISP, w_AAS, w_EEM, w_DST]", "Domain Shift & Transfer Interpretation"],
        [
            ("HaluEval-Dialogue -> HaluEval-QA", "0.946", "0.948", "0.782", "[+2.14, +0.18, -0.31, +0.22]", "Strong positive transfer across conversational & QA knowledge tasks."),
            ("HaluEval-Summ. -> HaluEval-Dialogue", "0.779", "0.768", "0.664", "[+3.42, +0.29, -0.15, +0.31]", "High contextual grounding alignment between summarization and dialogue."),
            ("HaluEval-Summ. -> HaluEval-QA", "0.777", "0.845", "0.612", "[+3.42, +0.29, -0.15, +0.31]", "ISP transfers at 0.845 AUROC; surface length shift slightly dampens fusion."),
            ("HaluEval-Dialogue -> HaluEval-Summ.", "0.767", "0.776", "0.648", "[+2.14, +0.18, -0.31, +0.22]", "Consistent cross-task generalization across long-context HaluEval."),
            ("HaluEval-QA -> HaluEval-Dialogue", "0.709", "0.723", "0.629", "[+2.68, -0.34, -1.12, -0.20]", "Moderate positive transfer despite strong length asymmetry in QA source."),
            ("TruthfulQA -> HaluEval-Dialogue", "0.615", "0.605", "0.558", "[+1.79, +0.07, +0.26, +0.16]", "Adversarial misconception direction partially overlaps dialogue fabrications."),
            ("HaluEval-Summ. -> TruthfulQA", "0.567", "0.551", "0.534", "[+3.42, +0.29, -0.15, +0.31]", "Near-orthogonal subspace between document distortion and short myth traps."),
        ],
        [2.8, 1.6, 1.6, 1.6, 3.2, 3.8],
        8.2,
    ),
    "8.1": (
        ["Controller Tier / Operating Regime", "Risk Trigger Condition", "Test Queries Routed (n = 150)", "Initial Greedy Factual / Halluc.", "Post-Tier Final Factual / Halluc.", "Net Hallucinations Eliminated", "Extra LLM Calls Incurred"],
        [
            ("SAFE (Direct Pass-Through)", "r_0 < 0.6114", "48 (32.0%)", "30 Factual / 18 Halluc.", "30 Factual / 18 Halluc. (Emitted)", "0 (Zero-overhead path; 62.5% acc.)", "0 calls (1.0x pass)"),
            ("TIER 1 (Annealed Re-Sampling)", "0.6114 <= r_0 < 0.8984 & verified", "11 (7.3%)", "5 Factual / 6 Halluc.", "7 Factual / 4 Halluc. (Emitted)", "2 hallucinations actively repaired (+18.2% acc.)", "+1 to +2 local passes"),
            ("TIER 2 (Wikipedia RAG Grounding)", "r_0 >= 0.8984 or T1 escalated & verified", "6 (4.0%)", "2 Factual / 4 Halluc.", "2 Factual / 4 Halluc. (Emitted)", "Verified safe emission below tau_fault", "+1 RAG pass + Wiki API"),
            ("TIER 3 (Calibrated Abstention)", "Post-RAG risk r_RAG >= 0.8984", "85 (56.7%)", "20 Factual / 65 Halluc.", "0 Emitted (85 Abstained)", "65 severe hallucinations blocked from emission", "Abstains with log-odds XAI"),
            ("Total Answered Subset (SAFE+T1+T2)", "Emitted Responses (43.3% cov.)", "65 (43.3%)", "37 Factual / 28 Halluc. (56.9% acc.)", "39 Factual / 26 Halluc. (60.0% acc.)", "Hallucination rate drops 62.0% -> 40.0% (-35.5% rel.)", "Mean 1.48 passes/query"),
            ("System-Wide Total (All 150 Queries)", "Full Test Split (n_test = 150)", "150 (100.0%)", "57 Factual / 93 Halluc. (62.0% hall.)", "39 Factual / 26 Emitted Halluc. (17.3%)", "67 of 93 hallucinations eliminated (-72.0% rel.)", "AURC improved 0.620 -> 0.412"),
        ],
        [2.6, 2.2, 1.6, 2.1, 2.2, 2.2, 1.7],
        8.2,
    ),
    "8.2": (
        ["Coverage Level c (Fraction Answered)", "Queries Answered (of 150)", "TRUEGUARD Factual Accuracy (%)", "TRUEGUARD Selective Risk (%)", "Normalized Entropy Accuracy (%)", "Normalized Entropy Risk (%)", "Mean Token NLL Accuracy (%)", "Mean Token NLL Risk (%)"],
        [
            ("100% Coverage (Unmitigated)", "150 / 150", "38.0%", "62.0%", "38.0%", "62.0%", "38.0%", "62.0%"),
            ("90% Coverage (Reject Top 10% Risk)", "135 / 150", "41.5%", "58.5%", "40.7%", "59.3%", "38.5%", "61.5%"),
            ("80% Coverage (Reject Top 20% Risk)", "120 / 150", "45.8%", "54.2%", "43.3%", "56.7%", "40.0%", "60.0%"),
            ("70% Coverage (Reject Top 30% Risk)", "105 / 150", "50.5%", "49.5%", "46.7%", "53.3%", "39.0%", "61.0%"),
            ("60% Coverage (Reject Top 40% Risk)", "90 / 150", "51.1%", "48.9%", "51.1%", "48.9%", "40.0%", "60.0%"),
            ("50% Coverage (Reject Top 50% Risk)", "75 / 150", "60.0%", "40.0%", "53.3%", "46.7%", "44.0%", "56.0%"),
            ("43.3% Operating Point (tau_fault)", "65 / 150", "60.0%", "40.0%", "53.8%", "46.2%", "44.6%", "55.4%"),
            ("Area Under Risk-Coverage (AURC)", "Integral c in (0,1]", "AURC = 0.412 (Best)", "-33.5% vs. Unranked", "AURC = 0.526", "-15.2% vs. Unranked", "AURC = 0.603", "-2.7% vs. Unranked"),
        ],
        [2.7, 1.6, 1.8, 1.7, 1.8, 1.7, 1.7, 1.6],
        8.2,
    ),
    "8.3": (
        ["Execution Component / Sub-Stage", "Tesla T4 GPU Latency (TinyLlama-1.1B)", "GPU Share of Total Time", "Local CPU Latency (GPT-2 124M)", "CPU Share of Total Time", "Complexity Scaling & Bottleneck Analysis"],
        [
            ("Base Autoregressive Decoding (KV-Cached)", "33.49 ms / token", "91.98% (Post-Pass)", "159.88 ms / token", "100.0% (Baseline)", "O(L * d^2) matrix-vector projections across L layers."),
            ("Sensor 1: 4-Layer ISP Linear Projection", "+0.84 ms / token", "2.31%", "+1.12 ms / token", "0.78%", "O(|L_probe| * d) dot products on 4 cached hidden vectors."),
            ("Sensor 2: Top-Quartile Attention Entropy (AAS)", "+1.12 ms / token", "3.08%", "+1.48 ms / token", "1.03%", "O(|L_top| * H * K_t) entropy over final-quartile heads."),
            ("Sensor 3: Hybrid Shannon + Renyi-2 (EEM)", "+0.68 ms / token", "1.87%", "+0.89 ms / token", "0.62%", "O(|V|) vocabulary reduction over already-computed logits."),
            ("Sensor 4: Cosine Trajectory Drift (DST) + Fusion", "+0.28 ms / token", "0.77%", "+0.30 ms / token", "0.21%", "O(d) consecutive-step cosine similarity + 4D dot product."),
            ("TRUEGUARD Total Single-Pass Latency", "36.41 ms / token (+8.7%)", "100.00% (4.65x speedup)", "143.37 ms / token (Online)", "9.50x speedup vs. 5x", "Avoids K=5 redundant autoregressive decoding passes."),
            ("5-Sample SelfCheck Consistency Baseline", "169.31 ms / token (+405.5%)", "465.0% of TRUEGUARD", "1361.49 ms / token (+751.6%)", "949.6% of Online", "Requires K=5 full sequential decoding passes per prompt."),
        ],
        [3.1, 2.3, 1.9, 2.3, 1.9, 3.1],
        8.2,
    ),
}

