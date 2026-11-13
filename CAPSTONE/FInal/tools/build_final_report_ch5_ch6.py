"""
Chapters 5, 6, 7, 8, 9, and Appendices 1-3 builders for FINAL_REPORT.docx.
Every equation, table, figure, and number traces directly to the verified TRUEGUARD v2
codebase (`src/`) and hardware outputs (`outputs/`).
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

from docx.enum.text import WD_ALIGN_PARAGRAPH

from build_final_report_helpers import (
    FIG_DIR,
    add_chapter_heading,
    add_code_listing_box,
    add_equation_block,
    add_figure_with_caption,
    add_p,
    add_section_heading,
    add_styled_table,
    add_subsection_heading,
)
from report_ch4_to_ch9_data import (
    CODE_EXCERPT_1_PIPELINE,
    CODE_EXCERPT_2_SENSORS,
    CODE_EXCERPT_3_FUSION,
    CODE_EXCERPT_4_CONTROLLER,
    DATASET_SUMMARY_TABLE,
)


def build_chapter_5(doc) -> None:
    add_chapter_heading(doc, 5, "DATASET CURATION, MATHEMATICAL MODEL DESIGN AND ALGORITHMIC FORMULATION")

    add_section_heading(doc, "5.1 BENCHMARK DATASET CURATION AND PREPROCESSING")
    add_p(doc, "To evaluate hallucination detection and closed-loop mitigation across heterogeneous linguistic regimes without synthetic artifacts, five standardized, publicly verifiable benchmark corpora totaling 48,761 downloaded JSONL records are curated in `CAPSTONE/FInal/datasets/` (`tg_data.py`). Table 5.1 summarizes the corpus scale, evaluation subset structure, and primary failure modes probed by each dataset.")
    add_styled_table(
        doc,
        "5.1",
        "Curated Benchmark Datasets and Evaluation Split Architecture",
        ["Benchmark Dataset", "JSONL File", "Total Records", "Evaluated Subset", "Hallucination Regime & Task Description"],
        DATASET_SUMMARY_TABLE,
        [3.0, 2.7, 2.0, 2.4, 4.5],
        font_size=9.5,
    )
    add_p(doc, "For the four paired detection benchmarks (TruthfulQA, HaluEval-QA, HaluEval-Dialogue, and HaluEval-Summarization), each source question Q_i (identified by `group_id`) yields exactly one factually grounded reference response (label y_i = 0) and one hallucinated response (label y_i = 1). Across all four datasets on TinyLlama-1.1B-Chat-v1.0, this produces N = 3,196 evaluated prompt-response pairs (796 on TruthfulQA and 800 each on HaluEval-QA, HaluEval-Dialogue, and HaluEval-Summarization). For live closed-loop mitigation on open-domain TriviaQA [44], 300 distinct entity-centric questions are partitioned into a held-out calibration split (n_cal = 150) used exclusively to calibrate (tau_warning, tau_fault) and a disjoint blind test split (n_test = 150).")

    add_section_heading(doc, "5.2 QUESTION-GROUPED SPLITTING AND DATA-LEAKAGE PREVENTION")
    add_p(doc, "A subtle yet pervasive methodological flaw in prior probing studies is random row-level cross-validation across paired responses. If the factual response (x_i, y_i^+) falls into the training fold while the paired hallucinated response (x_i, y_i^-) for the exact same prompt x_i falls into the test fold, high-dimensional hidden-state probes can memorize prompt-specific lexical embeddings rather than learning a generalizable truthfulness direction. To eliminate prompt leakage completely, every cross-validation split in TRUEGUARD enforces strict partition disjointness over question group identifiers G = {g_1, ..., g_M}:")
    add_equation_block(doc, "G_train(k) intersect G_test(k) = Ø,    for all outer folds k in {1, ..., K} and inner folds j in {1, ..., K_inner}", "5.1")
    add_p(doc, "Figure 5.1 illustrates the complete two-level grouped cross-validation and inner out-of-fold (OOF) probe stacking data-flow pipeline implemented in `src/tg_eval.py` and `src/tg_pipeline.py`.")
    add_figure_with_caption(doc, FIG_DIR / "fig_oof_dataflow_pipeline.png", "5.1", "Leakage-Free Grouped K-Fold Cross-Validation and Inner Out-of-Fold (OOF) Stacking Pipeline", width_cm=14.4)

    add_section_heading(doc, "5.3 SENSOR 1: MULTI-LAYER SUPERVISED INTERNAL STATE PROBE (ISP)")
    add_p(doc, "Let M_theta be a frozen causal Transformer with L layers. Given prompt tokens x = (x_1, ..., x_m) and generated answer tokens y = (y_1, ..., y_n), let layer activation h_{l,t} in R^d denote the residual-stream hidden state at layer l and generated token step t in {1, ..., n}. Rather than probing only the final layer, TRUEGUARD attaches four supervised L2-regularized logistic probes at fractional network depths Lambda = {0.45, 0.60, 0.75, 0.90}:")
    add_equation_block(doc, "l_q = round(q * (L - 1)),    q in {0.45, 0.60, 0.75, 0.90}", "5.2")
    add_p(doc, "On 22-layer TinyLlama-1.1B (d = 2048), Equation (5.2) selects layers L_probe = {10, 13, 16, 20}; on 12-layer GPT-2 (d = 768), it selects layers L_probe = {5, 7, 9, 11}. For sequence-level probe training, the generated answer's hidden trajectory at layer l is mean-pooled across the n generated tokens:")
    add_equation_block(doc, "hbar_l(x, y) = (1 / n) * sum_{t=1}^{n} layer activation h_{l,t} in R^d,    for each l in L_probe", "5.3")
    add_p(doc, "Each probe layer l standardizes hbar_l via zero-mean unit-variance scaling ztilde_l = (hbar_l - mu_l) / sigma_l and applies an L2-regularized logistic classifier with penalty parameter C = 0.25:")
    add_equation_block(doc, "p_l(x, y) = sigma(w_l^T ztilde_l + b_l) = 1 / (1 + exp(-(w_l^T ztilde_l + b_l))) in (0, 1)", "5.4")
    add_p(doc, "The multi-layer Internal State Probe score Fbar(x,y) is the unweighted ensemble mean across the four probed depths, and its token-level online counterpart F_t is evaluated at each step t:")
    add_equation_block(doc, "Fbar(x, y) = (1 / |L_probe|) * sum_{l in L_probe} p_l(x, y),    F_t = (1 / |L_probe|) * sum_{l in L_probe} sigma(w_l^T ztilde_{l,t} + b_l)", "5.5")
    add_p(doc, "To prevent Fbar(x,y) from overfitting the d = 2048 hidden dimension on the outer training fold and dominating the downstream fusion weights, `SupervisedLayerProbe.fit_and_oof` computes out-of-fold probe score F_OOF(x_i, y_i) via 3-fold inner GroupKFold before fitting the 4-sensor logistic combiner.")

    add_section_heading(doc, "5.4 SENSOR 2: FINAL-QUARTILE ATTENTION ANOMALY SCORE (AAS)")
    add_p(doc, "Let L_top = {floor(3L/4), ..., L - 1} denote the final quartile of transformer layers (layers 16..21 on TinyLlama-1.1B; layers 9..11 on GPT-2), and let attention weights α_{l,h,t} in probability simplex Δ^{K-1} denote the causal attention distribution of head h in {1, ..., H} at generated step t over the K_t = m + t available context tokens. The step-wise Attention Anomaly Score A_t measures the normalized Shannon entropy averaged across all heads in L_top:")
    add_equation_block(doc, "A_t = (1 / (|L_top| * H * ln(K_t))) * sum_{l in L_top} sum_{h=1}^{H} ( -sum_{k=1}^{K_t} alpha_{l,h,t,k} ln(alpha_{l,h,t,k}) ) in [0, 1]", "5.6")
    add_p(doc, "Dividing by ln(K_t) makes A_t invariant to context-window length K_t, ensuring that long summarization prompts and short trivia prompts map onto the same [0, 1] dispersion scale.")

    add_section_heading(doc, "5.5 SENSOR 3: HYBRID SHANNON AND RENYI-2 ENERGY-ENTROPY MONITOR (EEM)")
    add_p(doc, "Given the pre-softmax logit vector z_t in |V|-dimensional vocabulary space at decoding step t and predictive probability distribution p_t = softmax(z_t), TRUEGUARD computes both normalized Shannon entropy and normalized quadratic Renyi entropy (alpha = 2):")
    add_equation_block(doc, "H_Shan,norm(p_t) = (-sum over vocabulary tokens p_t(v) ln(p_t(v))) / ln|V|,    H_Renyi2,norm(p_t) = (-ln(sum over vocabulary tokens p_t(v)^2)) / ln|V|", "5.7")
    add_p(doc, "The step-wise Energy and Entropy Monitor score energy-entropy score H_{ent}(t) is the convex combination:")
    add_equation_block(doc, "energy-entropy score H_{ent}(t) = 0.6 * H_Shan,norm(p_t) + 0.4 * H_Renyi2,norm(p_t) in [0, 1]", "5.8")
    add_p(doc, "In addition, the Helmholtz free-energy baseline score E_t = -T ln(sum over vocabulary tokens exp(z_t(v) / T)) is recorded at each step for comparative baseline benchmarking.")

    add_section_heading(doc, "5.6 SENSOR 4: DIRECTIONAL SEMANTIC TRAJECTORY (DST)")
    add_p(doc, "To capture abrupt kinematic jumps in the final-layer residual stream final-layer activation h_t across consecutive generated tokens, Sensor 4 computes the step-wise cosine distance:")
    add_equation_block(doc, "D_t = 1 - (final-layer activation h_t^T final-layer activation h_t-1) / (||final-layer activation h_t||_2 * ||final-layer activation h_t-1||_2 + epsilon),    for t >= 2 (with D_1 = 0)", "5.9")
    add_p(doc, "Across an answer of length n, the four token-level sensor trajectories are mean-pooled into the 4-dimensional sequence feature vector:")
    add_equation_block(doc, "phi(x, y) = [ Fbar(x,y),  Abar(x,y),  Hbar_ent(x,y),  Dbar(x,y) ]^T in R^4", "5.10")

    add_section_heading(doc, "5.7 CALIBRATED LOGISTIC FUSION AND LOG-ODDS ATTRIBUTION")
    add_p(doc, "`TrueGuardDetector` standardizes each component k in {1, 2, 3, 4} of phi(x,y) using training-fold statistics z_k = (phi_k - mu_k) / sigma_k and computes the calibrated posterior hallucination risk r(x,y) via L2-regularized logistic regression:")
    add_equation_block(doc, "r(x, y) = P(y is hallucinated | phi(x,y)) = sigma( w_0 + sum_(k=1..4) w_k z_k ) in (0, 1)", "5.11")
    add_p(doc, "Because log(r / (1 - r)) = w_0 + sum_(k=1..4) w_k z_k is strictly additive in log-odds space, each sensor's exact signed contribution to a specific prediction is given by:")
    add_equation_block(doc, "c_k(x, y) = w_k * z_k = w_k * ((phi_k(x, y) - mu_k) / sigma_k),    k in {ISP, AAS, EEM, DST}", "5.12")
    add_p(doc, "Positive c_k values indicate that sensor k pushes the decision toward hallucination risk, whereas negative c_k values indicate grounding confidence.")

    add_section_heading(doc, "5.8 TWO-THRESHOLD CALIBRATION AND THREE-TIER ACTUATION")
    add_p(doc, "On a held-out calibration set D_cal = {(x_i, y_i^(0), l_i)}_{i=1}^{n_cal} where l_i in {0, 1} denotes whether the greedy answer y_i^(0) is hallucinated, `calibrate_thresholds` computes two operating thresholds:")
    add_equation_block(doc, "tau_warning = argmax_{tau in (0,1)} [ TPR_cal(tau) - FPR_cal(tau) ],    tau_fault = min { tau > tau_warning : Precision_cal(tau) >= 0.80 }", "5.13")
    add_p(doc, "Given a live user query x, the closed-loop actuator (`TrueGuardController`) executes the following four-regime state machine:")
    add_equation_block(doc, "Action(x) = { SAFE (r_0 < tau_warn);  TIER 1 Re-Sample (tau_warn <= r_0 < tau_fault);  TIER 2 RAG (r_0 >= tau_fault or Tier 1 fail);  TIER 3 Abstain (r_RAG >= tau_fault) }", "5.14")
    add_p(doc, "Finally, selective prediction performance across all coverage levels c in (0, 1] is quantified by the Area Under the Risk–Coverage Curve (AURC):")
    add_equation_block(doc, "AURC = integral_{0}^{1} Risk(c) dc,    where Risk(c) = E[ l_i | r(x_i, y_i) <= quantile_c(r) ]", "5.15")


def build_chapter_6(doc) -> None:
    add_chapter_heading(doc, 6, "SYSTEM IMPLEMENTATION AND CODE ARCHITECTURE")

    add_section_heading(doc, "6.1 MODULAR PACKAGE STRUCTURE AND EXECUTION WORKFLOW")
    add_p(doc, "The TRUEGUARD v2 framework is implemented as a clean, modular Python package under `CAPSTONE/FInal/src/` with zero synthetic placeholders, paired with automated CLI experiment drivers in `CAPSTONE/FInal/experiments/` and a numerical equivalence test suite in `CAPSTONE/FInal/tests/test_equivalence.py`. Table 6.1 details the core source files, classes, and lines of production code.")
    add_styled_table(
        doc,
        "6.1",
        "TRUEGUARD v2 Production Source Modules and Functional Responsibilities",
        ["Module Path", "Core Classes & Functions", "Verified Responsibility in Pipeline"],
        [
            ("src/tg_pipeline.py", "StepSignals, AnswerSignals, OnlineSignalMonitor, HuggingFaceBackend, SupervisedLayerProbe, TrueGuardDetector", "Single-pass teacher-forced & KV-cached online extraction of ISP, AAS, EEM, DST; 4-layer inner OOF probing; L2 logistic fusion & log-odds attribution."),
            ("src/tg_controller.py", "WikipediaRetriever, ControllerDecision, TrueGuardController", "Keyword-cleaned MediaWiki API retrieval; two-threshold 3-tier closed-loop actuation (SAFE, TIER1_RESAMPLE, TIER2_RETRIEVAL, TIER3_ABSTAIN)."),
            ("src/tg_eval.py", "run_grouped_cv_evaluation, calibrate_thresholds, run_cross_dataset_matrix, compute_risk_coverage", "Leakage-free GroupKFold CV, 500-draw group bootstrap 95% CIs, polarity diagnostics, complementarity at 10% FPR, AURC, and figure generation."),
            ("src/tg_data.py", "BenchmarkItem, download_and_prepare_datasets, load_balanced_subset, grade_generated_answer", "HuggingFace JSONL curation, group-balanced sampling, QA prompt formatting, and normalized token-F1 / Exact-Match grading."),
            ("tests/test_equivalence.py", "test_teacher_forced_equals_online_monitor, test_no_leakage_on_random_labels, test_controller_tiers", "Automated verification of teacher-forced vs. online KV-cached signal identity, OOF noise leakage protection, and 3-tier state transitions."),
        ],
        [3.4, 4.4, 6.8],
        font_size=9.5,
    )

    add_section_heading(doc, "6.2 MULTI-LAYER INNER OOF PROBE IMPLEMENTATION")
    add_p(doc, "Listing 6.1 presents the production implementation of `SupervisedLayerProbe` in `src/tg_pipeline.py`. Notice how `select_layers` deterministically maps fractional depths {0.45, 0.60, 0.75, 0.90} to integer layer indices for any transformer backbone, and `fit_and_oof` uses `GroupKFold` over question identifiers so that out-of-fold ISP probabilities have zero in-sample inflation when passed to the fusion classifier.")
    add_code_listing_box(doc, "LISTING 6.1: LEAKAGE-FREE 4-LAYER SUPERVISED PROBE (`src/tg_pipeline.py`)", CODE_EXCERPT_1_PIPELINE)

    add_section_heading(doc, "6.3 SINGLE-PASS SENSOR EXTRACTION AND DUAL-MODE MONITOR")
    add_p(doc, "Listing 6.2 shows the core mathematical functions `_attention_entropy_from_step` (Sensor 2: AAS) and `_logit_entropy_and_energy` (Sensor 3: EEM) from `src/tg_pipeline.py`. Both functions are invoked identically inside `HuggingFaceBackend.score_answer` (post-pass teacher forcing) and `OnlineSignalMonitor.step` (step-by-step KV-cached generation), guaranteeing mathematical equivalence between offline benchmark evaluation and live streaming deployment.")
    add_code_listing_box(doc, "LISTING 6.2: TOP-QUARTILE ATTENTION ENTROPY & HYBRID SHANNON/RENYI-2 EEM (`src/tg_pipeline.py`)", CODE_EXCERPT_2_SENSORS)

    add_section_heading(doc, "6.4 LOGISTIC FUSION AND LOG-ODDS EXPLAINABILITY ENGINE")
    add_p(doc, "Listing 6.3 displays `TrueGuardDetector` from `src/tg_pipeline.py`. The `active_sensors` parameter supports arbitrary sensor subsets for leave-one-out ablation studies (`without_ISP`, `without_AAS`, `without_EEM`, `without_DST`), while `explain()` returns the exact signed log-odds contribution c_k = w_k * z_k for each active sensor.")
    add_code_listing_box(doc, "LISTING 6.3: CALIBRATED 4-SENSOR FUSION AND LOG-ODDS ATTRIBUTION (`src/tg_pipeline.py`)", CODE_EXCERPT_3_FUSION)

    add_section_heading(doc, "6.5 CLOSED-LOOP THREE-TIER CONTROLLER AND WIKIPEDIA RAG")
    add_p(doc, "Listing 6.4 presents the `TrueGuardController.generate` method from `src/tg_controller.py`. When an initial greedy generation y_0 exceeds tau_warning, Tier 1 re-samples at annealed temperatures T in {0.35, 0.20} and accepts a candidate only if its re-evaluated risk drops below both r_0 and tau_fault. Otherwise, Tier 2 strips interrogative stopwords from the prompt, queries the Wikipedia REST API for top-3 factual summaries, prepends the retrieved evidence, and re-evaluates the grounded answer before deciding whether to emit or abstain (Tier 3).")
    add_code_listing_box(doc, "LISTING 6.4: CLOSED-LOOP THREE-TIER GRADED ACTUATOR (`src/tg_controller.py`)", CODE_EXCERPT_4_CONTROLLER)

    add_section_heading(doc, "6.6 AUTOMATED NUMERICAL EQUIVALENCE AND INTEGRITY VERIFICATION")
    add_p(doc, "Before running any benchmark experiment, `tests/test_equivalence.py` executes three automated verification checks on real `gpt2` activations (`outputs/logs/test_equivalence_run.log`): (1) Teacher-forced vs. online KV-cached equivalence confirms max |Delta F| = 3.49 x 10^-6 (< 10^-4 threshold) and max |Delta H_ent| = 1.53 x 10^-5 (< 10^-4 threshold); (2) Pure-noise group leakage test confirms that inner OOF stacking does not fabricate high AUROC on random labels; and (3) Controller state-transition verification confirms deterministic routing across SAFE, TIER2_RETRIEVAL, and TIER3_ABSTAIN.")

