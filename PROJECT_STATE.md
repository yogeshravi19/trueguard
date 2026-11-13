# PROJECT_STATE.md — Full Repository & Git Audit (`E:\trueguard`)

**Project Title:** Toward Trustworthy Large Language Models: A Comprehensive Review of Hallucination Detection, Explainability, and Mitigation Strategies  
**Audit Date:** November 2026  
**Author / Candidate:** Yogesh Ravi M (`22MIA1052`)  
**Supervisor / Guide:** Dr. Pradeep Kumar T.S.  
**Programme:** M.Tech. (Integrated) Computer Science and Engineering with Specialization in Business Analytics  
**Institution:** School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology (VIT), Chennai  

---

## 1. Git History & Working Tree Audit

### 1.1 Active Branch & Remote Status
- **Active Branch:** `main` (tracking `origin/main` at `https://github.com/Yogesh1290/trueguard.git`).
- **Working Tree Status:** Clean on tracked source files; untracked reference/template files reside under `CAPSTONE/sample/`, `CAPSTONE/friend report.pdf`, and `CAPSTONE/FInal/results/_ref/`.

### 1.2 Chronological Commit History (`git log --all`)

| Commit Hash | Date (ISO 8601) | Author | Commit Message & Summary of Changes |
| :--- | :--- | :--- | :--- |
| `5ac8dde` (`HEAD -> main`, `origin/main`) | `2026-11-11 16:40:28 +0530` | Yogesh1290 | **Add downloaded benchmark JSONL datasets** (`truthful_qa.jsonl` [817 rows], `halueval_qa.jsonl` [10,000 rows], `halueval_dialogue.jsonl` [10,000 rows], `halueval_summarization.jsonl` [10,000 rows], `trivia_qa.jsonl` [17,944 rows]). |
| `6f847ec` | `2026-11-11 16:37:52 +0530` | Yogesh1290 | **Add TRUEGUARD v2 pipeline, verified Tesla T4 GPU results, Paper 2 manuscripts, and 40-paper Pillar Literature Review** (78 files changed, 7,355 insertions). Added `src/tg_pipeline.py`, `src/tg_controller.py`, `src/tg_eval.py`, `src/tg_data.py`, `experiments/`, `tests/test_equivalence.py`, `results/v2/TinyLlama__TinyLlama-1.1B-Chat-v1.0/`, `results/v2/gpt2/`, `paper/paper2_trueguard_empirical.tex`, and `TRUEGUARD_40_Papers_Literature_Review_By_Pillars.docx`. |
| `52b8ac4` | `2026-04-06 10:42:37 +0530` | Yogesh1290 | **Capstone project update** (Added initial `CAPSTONE/` folder containing Paper 1 `Toward Trustworthy Large Language Models_standard.docx` and legacy v1 prototype files under `CAPSTONE/FInal/`). |
| `de4cf96` | `2026-03-11 08:40:25 +0530` | Yogesh1290 | Initial repository commit (`README.md`). |

---

## 2. File Inventory & Implementation Status

### 2.1 Production-Verified Code (`CAPSTONE/FInal/src/` & `experiments/` — Commit `6f847ec`)
These modules constitute the **authoritative, verified TRUEGUARD v2 implementation** and are treated as the single source of truth for the Final Project Report:

| File Path | Status | Purpose & Verified Functionality |
| :--- | :--- | :--- |
| `CAPSTONE/FInal/src/tg_pipeline.py` | **VERIFIED (v2)** | Core single-pass sensor extraction (`score_answer` teacher-forced and `OnlineSignalMonitor` KV-cached step-by-step), 4-layer supervised logistic `ISP` probe with grouped inner CV (`GroupKFold`) and inner out-of-fold (OOF) stacking, `AAS` final-quartile attention Shannon entropy, `EEM` hybrid Shannon/Rényi-2 normalized entropy, `DST` consecutive-token hidden-state cosine distance, and `TrueGuardDetector` logistic fusion + log-odds attribution (`explain`). |
| `CAPSTONE/FInal/src/tg_controller.py` | **VERIFIED (v2)** | Closed-loop 3-tier actuator (`TrueGuardController`) with two calibrated thresholds ($\tau_{\text{warning}}, \tau_{\text{fault}}$), Tier 1 local temperature-annealed re-sampling (`TIER1_RESAMPLE`), Tier 2 targeted retrieval-augmented re-grounding (`TIER2_RETRIEVAL`) via cleaned-query `WikipediaRetriever`, and Tier 3 calibrated abstention (`TIER3_ABSTAIN`). |
| `CAPSTONE/FInal/src/tg_eval.py` | **VERIFIED (v2)** | Leakage-free grouped evaluation (`run_grouped_cv_evaluation`), 500-draw group bootstrap 95% confidence intervals, threshold calibration (`calibrate_thresholds`), cross-dataset transfer matrix (`run_cross_dataset_matrix`), pairwise sensor complementarity (`compute_complementarity`), Risk–Coverage (`AURC`) curves (`compute_risk_coverage`), and publication-grade matplotlib plotters. |
| `CAPSTONE/FInal/src/tg_data.py` | **VERIFIED (v2)** | Real HuggingFace dataset downloader (`download_and_prepare_datasets`), group-stratified balanced sampler (`load_balanced_subset`), prompt formatters (`format_qa_prompt`), and normalized token-F1/EM grader (`grade_generated_answer`). |
| `CAPSTONE/FInal/tests/test_equivalence.py` | **VERIFIED (v2)** | End-to-end verification suite checking teacher-forced vs. KV-cached online signal numerical equivalence ($\max |\Delta F| = 3.49 \times 10^{-6} < 10^{-4}$, $\max |\Delta H_{\text{ent}}| = 1.53 \times 10^{-5} < 10^{-4}$), zero out-of-fold leakage on random noise features, and 3-tier controller transitions. |
| `CAPSTONE/FInal/experiments/extract_activations.py` | **VERIFIED (v2)** | Runs real LLM forward passes over benchmark JSONL records and saves compressed `.npz` per-layer hidden states and raw sensor features. |
| `CAPSTONE/FInal/experiments/evaluate_detection.py` | **VERIFIED (v2)** | Runs grouped K-fold CV across all 12 methods (4 baselines, 4 single sensors, 4 leave-one-out ablations, and `TRUEGUARD_full`), cross-dataset transfer, complementarity, and figure generation. |
| `CAPSTONE/FInal/experiments/evaluate_mitigation.py` | **VERIFIED (v2)** | Runs live open-domain QA generation on `TriviaQA`, calibrates $(\tau_{\text{warning}}, \tau_{\text{fault}})$ on a held-out calibration split, executes the 3-tier controller on the test split, and computes Risk–Coverage (`AURC`). |
| `CAPSTONE/FInal/experiments/benchmark_latency.py` | **VERIFIED (v2)** | Measures real wall-clock per-token latency (`ms/tok`) and peak memory across Vanilla decoding, TRUEGUARD Post-pass, TRUEGUARD Online, and 5-sample SelfCheck consistency. |

### 2.2 Legacy Prototype Files (`CAPSTONE/FInal/` — Commit `52b8ac4`, Superseded)
The following files from the earlier v1 commit are **deprecated/superseded** and are **NOT** used as experimental evidence in the report (they are documented honestly in the mismatch audit below):
- `CAPSTONE/FInal/experiments/run_benchmark.py`: Contained synthetic Gaussian score generation (`rng.normal(...)`) rather than real LLM inference.
- `CAPSTONE/FInal/cpu_smoke_test.py` & `latency_profiler.py`: Timed synthetic random tensors rather than real HuggingFace model forward passes.
- `CAPSTONE/FInal/src/signal_extractors.py` & `src/mitigation.py`: Early v1 prototype that used an untrained dispersion heuristic `sigmoid(std(h)-1)` for ISP and implemented only a single threshold (`0.50`) and 2 corrective tiers.
- `CAPSTONE/FInal/results/benchmark_results.json` & `cpu_validation_results.json`: Legacy simulated output artifacts.

### 2.3 Latest Authoritative Results & Datasets
1. **Primary GPU Results (`TinyLlama/TinyLlama-1.1B-Chat-v1.0` on Google Colab Tesla T4 GPU):**
   - `CAPSTONE/FInal/results/v2/TinyLlama__TinyLlama-1.1B-Chat-v1.0/detection_report.json` ($N = 3{,}196$ real answers across `truthful_qa`, `halueval_qa`, `halueval_dialogue`, `halueval_summarization`).
   - `CAPSTONE/FInal/results/v2/TinyLlama__TinyLlama-1.1B-Chat-v1.0/mitigation/mitigation_report.json` ($n_{\text{cal}} = 150, n_{\text{test}} = 150$ live open-domain `TriviaQA` generations).
   - `CAPSTONE/FInal/results/v2/TinyLlama__TinyLlama-1.1B-Chat-v1.0/real_latency.json` (real CUDA-synchronized Tesla T4 latency measurements).
   - `CAPSTONE/FInal/results/v2/TinyLlama__TinyLlama-1.1B-Chat-v1.0/figures/` (17 high-resolution PNG figures).
2. **Secondary CPU Architecture-Generality Verification (`gpt2` 124M on Local CPU):**
   - `CAPSTONE/FInal/results/v2/gpt2/detection_report.json` ($N = 480$ real answers across all 4 datasets, 3-fold grouped CV).
   - `CAPSTONE/FInal/results/v2/gpt2/real_latency.json` (real CPU latency measurements).
3. **Real Benchmark Datasets (`CAPSTONE/FInal/datasets/`):**
   - `truthful_qa.jsonl` ($817$ items), `halueval_qa.jsonl` ($10{,}000$ items), `halueval_dialogue.jsonl` ($10{,}000$ items), `halueval_summarization.jsonl` ($10{,}000$ items), `trivia_qa.jsonl` ($17{,}944$ items), documented in `datasets/manifest.json` and `datasets/DATASET_SOURCES.md`.
4. **Core Research Manuscripts:**
   - **Paper 1 (Review & Architecture):** `CAPSTONE/sample/Toward Trustworthy Large Language Models_standard.docx` and `TRUEGUARD_40_Papers_Literature_Review_By_Pillars.docx` (PRISMA 2020 review of 40 peer-reviewed studies across 6 Pillars + TRUEGUARD closed-loop architecture specification).
   - **Paper 2 (Empirical Implementation & Evaluation):** `CAPSTONE/FInal/paper/paper2_trueguard_empirical.tex` and `CAPSTONE/FInal/results/v2/TinyLlama__TinyLlama-1.1B-Chat-v1.0/PAPER2_RESULTS_SUMMARY.md`.

---

## 3. Comprehensive Mismatch Cross-Check Table

In strict compliance with Step 1 instructions, every discrepancy discovered across Paper 1, Paper 2, legacy v1 files, and the latest v2 code/results is catalogued below. **No mismatch is hidden; the latest verified v2 code and real hardware outputs (`6f847ec` / `5ac8dde`) are used as truth throughout `FINAL_REPORT.docx`.**

| ID | Claim / Component | Where It Appears | What Latest Code & Verified Results Show | Resolution Applied in Final Report |
| :--- | :--- | :--- | :--- | :--- |
| **M-01** | **Evaluation Execution vs. Synthetic Simulation** | Legacy v1 `CAPSTONE/FInal/experiments/run_benchmark.py` and `results/benchmark_results.json` claimed `0.8821 ± 0.0170` AUROC across 5 benchmarks including `HELM`, `12.4 ms/tok` latency (`11.5x` speedup), and `63.8%` hallucination drop (`31.2% -> 11.3%`) at `88%` coverage. | Legacy v1 scripts generated synthetic Gaussian draws (`rng.normal(...)`) without loading an LLM or dataset. Latest v2 (`src/tg_pipeline.py`, `experiments/evaluate_detection.py`) runs real HuggingFace forward passes on **3,196 answers (`TinyLlama-1.1B` on Tesla T4 GPU)** and **480 answers (`GPT-2 124M` on CPU)** across 4 real datasets (`TruthfulQA`, `HaluEval-QA`, `HaluEval-Dialogue`, `HaluEval-Summarization`) plus live generation on `TriviaQA` ($N=300$). | Report uses **exclusively the real v2 hardware results** (`0.935` macro AUROC on `TinyLlama-1.1B`, `0.802` macro AUROC on `GPT-2`, real `TriviaQA` mitigation, and real Tesla T4 / CPU latency) and explicitly documents why legacy v1 synthetic scripts were replaced. |
| **M-02** | **Internal State Probe (`ISP`) Formulation** | Paper 1 Section 6.2 specifies supervised linear probes on intermediate hidden states ($50\%\text{–}75\%$ depth). Legacy v1 `src/signal_extractors.py` used an untrained dispersion heuristic $\sigma(\text{std}(h)-1)$. | Latest v2 `src/tg_pipeline.py` (`SupervisedLayerProbe`) trains leakage-free L2-regularized `LogisticRegression` probes at 4 fractional depths $\{0.45, 0.60, 0.75, 0.90\}$ (layers `[10, 13, 16, 20]` on 22-layer `TinyLlama-1.1B`; layers `[5, 7, 9, 11]` on 12-layer `GPT-2`) using inner `GroupKFold(3)` out-of-fold predictions (`inner_oof_isp`) before fitting `TrueGuardDetector`. | Report presents the exact 4-layer supervised probe formulation and inner OOF stacking algorithm from `src/tg_pipeline.py`, explaining how inner OOF prevents ISP from dominating fusion weights (`w_ISP = +5.79` vs. `+0.87` for `AAS`, `+1.83` for `EEM`, and `+0.74` for `DST`). |
| **M-03** | **Attention Anomaly Score (`AAS`) Formulation** | Paper 1 Section 6.2 describes monitoring attention entropy over retrieved context tokens or prompt grounding dispersion. Legacy v1 `src/signal_extractors.py` returned $1 - \bar{H}_{\text{norm}}$ across all layers. | Latest v2 `src/tg_pipeline.py` computes normalized Shannon entropy of the causal attention distribution averaged across heads in the **final quartile of transformer layers** ($\mathcal{L}_{\text{top}} = [\lfloor 3L/4 \rfloor, L)$) at each generated token: $A_t = \frac{1}{|\mathcal{L}_{\text{top}}| H \ln K_t} \sum_{\ell \in \mathcal{L}_{\text{top}}} \sum_{h=1}^H \left(-\sum_{k=1}^{K_t} \alpha_{\ell,h,t,k} \ln \alpha_{\ell,h,t,k}\right)$. | Report documents the exact final-quartile normalized attention Shannon entropy equation implemented in `src/tg_pipeline.py` and verified by `tests/test_equivalence.py`. |
| **M-04** | **Energy & Entropy Monitor (`EEM`) Formulation** | Paper 1 Section 6.2 describes combining predictive Shannon entropy and Rényi entropy ($\alpha=2$) with free energy. Legacy v1 mixed unbounded energy $\sigma(-E/10)$ with entropy. | Latest v2 `src/tg_pipeline.py` computes bounded, scale-invariant hybrid uncertainty in $[0,1]$: $H_{\text{ent},t} = 0.6 \frac{H_{\text{Shannon}}(p_t)}{\ln |V|} + 0.4 \frac{H_{\text{Rényi-2}}(p_t)}{\ln |V|}$, while also computing `energy_score` $= T \ln \sum_v \exp(z_{t,v}/T)$ as a standalone baseline. | Report presents the exact scale-invariant `0.6 Shannon + 0.4 Rényi-2` formulation used in `src/tg_pipeline.py` alongside the standalone Energy baseline comparison. |
| **M-05** | **Threshold Count & 3-Tier Controller Actuation** | Paper 1 Section 6.3 specifies **2 thresholds** (`Warning` $\tau_1$ and `Fault` $\tau_2$) and **3 tiers** (Tier 1 Re-sampling, Tier 2 Retrieval, Tier 3 Abstention). Legacy v1 `src/mitigation.py` had only 1 threshold (`0.50`) and 2 tiers (skipping Tier 1). | Latest v2 `src/tg_controller.py` implements both calibrated thresholds ($\tau_{\text{warning}} = 0.611$, $\tau_{\text{fault}} = 0.898$ on `TinyLlama-1.1B` `TriviaQA` calibration split) and all 3 corrective tiers (`SAFE`, `TIER1_RESAMPLE`, `TIER2_RETRIEVAL`, `TIER3_ABSTAIN`) with risk-verification fallback (`r_new < r_initial` and `r_new < tau_fault`). | Report documents the complete 2-threshold, 3-tier closed-loop state machine in `src/tg_controller.py` and its real `TriviaQA` tier distribution (`15.3%` `SAFE`, `18.0%` `TIER1_RESAMPLE`, `10.0%` `TIER2_RETRIEVAL`, `56.7%` `TIER3_ABSTAIN`). |
| **M-06** | **Headline Quantitative Claims (Paper 1 vs. Paper 2 / v2 Results)** | Paper 1 (`Toward Trustworthy Large Language Models_standard.docx`) is a PRISMA systematic review and architectural proposal that intentionally omitted empirical numbers after removing an unverified `~65%` placeholder. Paper 2 (`paper2_trueguard_empirical.tex`) reports the real v2 empirical study. | On `TinyLlama-1.1B` (Tesla T4 GPU): Detection macro AUROC = **`0.935`** (`0.876` TruthfulQA, `0.975` HaluEval-QA, `0.903` HaluEval-Dialogue, `0.986` HaluEval-Summarization); live `TriviaQA` mitigation reduces hallucination rate among answered queries by **`35.5%` relative** (`62.0% -> 40.0%`, accuracy `38.0% -> 60.0%` at `43.3%` coverage) and reduces system-wide emitted hallucinations by **`72.0%` relative** (`62.0% -> 17.3%`); post-pass overhead is **`+2.92 ms/tok` (`+8.7%`, `4.65x` faster than 5-sample consistency)**. | Report integrates Paper 1 (Chapters 1–4: Introduction, Theoretical Foundations, 40-Paper 6-Pillar PRISMA Literature Review, Problem Statement & Architecture) seamlessly with Paper 2 (Chapters 5–8: Mathematical Formulation, Datasets, Implementation, and Real Tesla T4 / CPU Experimental Results). |
| **M-07** | **Cross-Dataset Transfer Generalization** | Legacy v1 claimed uniform `~0.88` AUROC without testing cross-dataset transfer. | Latest v2 `cross_dataset_matrix` on `TinyLlama-1.1B` reveals strong positive transfer across `HaluEval` tasks (`0.930` Dialogue $\to$ QA; `0.931` Summarization $\to$ QA; `0.816` QA $\to$ Summarization) but near-chance or inverted transfer between `TruthfulQA` (short adversarial misconception traps) and `HaluEval` (`0.223–0.517`). | Report presents the full $4 \times 4$ cross-dataset transfer matrix (Figure & Table) and analyzes domain-shift mechanics between adversarial short-answer misconceptions (`TruthfulQA`) and long-form contextual hallucinations (`HaluEval`), motivating task-family probe calibration. |
| **M-08** | **Candidate & Guide Metadata Across Templates** | `MIA-Project Template.docx` has generic placeholders (`NAME OF THE CANDIDATE (Reg. No.)`, `GUIDENAME`, `December, 2025`). `friend report.pdf` has `ABISHEK. B (22MIA1075)` and `Dr. SIVAGAMI M`. Paper 1 & v2 codebase have `Yogesh Ravi M (22MIA1052)` and `Dr. Pradeep Kumar T.S.`. | Candidate's real identity in project files (`CAPSTONE/FInal/paper/paper2_trueguard_empirical.tex` and `CAPSTONE/sample/Toward Trustworthy Large Language Models_standard.docx`) is **Yogesh Ravi M (`22MIA1052`)**, supervised by **Dr. Pradeep Kumar T.S.**, School of Computer Science and Engineering (SCOPE), VIT Chennai. | Report populates **YOGESH RAVI M (22MIA1052)** and **Dr. PRADEEP KUMAR T.S.** on the Cover, Title, Declaration, Certificate, and Acknowledgement pages, and uses explicit bracketed placeholders (`[Examiner 1 Name]`, `[Examiner 2 Name]`, `[Date of Viva]`, `[Signature]`) where manual completion is required. |

