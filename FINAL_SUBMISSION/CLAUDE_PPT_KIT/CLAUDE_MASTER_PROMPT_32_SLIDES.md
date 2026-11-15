# MASTER PROMPT FOR CLAUDE — 32-SLIDE FINAL CAPSTONE PRESENTATION (`python-pptx`)
*(7 Literature Review Slides for All 40 Papers + 25 Core/Results Slides = 32 Slides Total)*

Copy and paste everything inside the box below into Claude, and attach the 14 images from `E:\trueguard\FINAL_SUBMISSION\CLAUDE_PPT_KIT\images\`:

```text
You are an expert academic presentation designer and Python developer. Write a single, complete, token-efficient `python-pptx` script (`generate_32slide_ppt.py`) that generates a 32-slide widescreen (16:9, `16.0 x 9.0 inches`) PowerPoint presentation (`FINAL_PRESENTATION_32SLIDES.pptx`) for my M.Tech. Final Review Capstone Viva.

### 1. DESIGN THEME & STRICT VISUAL RULES (CRITICAL)
- **Theme ("Royal-Indigo Header + Crisp White Card + Emerald Accent"):**
  - Slide Background: Soft Pearl-Slate (`#F1F5F9`).
  - Top Header Banner (`0.0"` to `1.15"` height): Deep Royal-Indigo (`#0F172A` to `#1E3A8A`) with a thin `0.06"` Emerald-Cyan accent strip (`#10B981`) along the bottom of the banner.
  - Main Content Card (`1.35"` to `8.65"` height, `0.45"` left/right margins): Elevated Pure White rounded card (`#FFFFFF`) with a subtle Cobalt border (`#93C5FD`).
- **Typography (LARGE, BOLD, PROJECTOR-READABLE):**
  - Header Font: `Trebuchet MS` Bold, `30–34 pt`, Crisp White (`#FFFFFF`).
  - Body Font: `Segoe UI`, `18–21 pt` (never smaller than `16 pt` on content slides), Deep Ink-Slate (`#0F172A`), bold Royal-Cobalt subheadings/prefixes (`#1D4ED8`), and Deep Emerald highlights (`#047857`).
  - Table Styling: Header row in Royal-Indigo (`#1E3A8A`) with White bold text (`15–17 pt`); alternating rows in Soft Ice-Blue (`#EFF6FF`) and White (`#FFFFFF`) with Dark Ink text (`#0F172A`).
- **Token-Efficiency Rule for Code:**
  - Use clean helper functions (`add_header`, `add_card_bullets`, `add_styled_table`, `add_image_slide`), and store the 40 literature papers and 40 references in compact Python lists so the entire script fits easily in one response without truncation.
- **Image Folder Path:**
  - Load images from `IMAGES_DIR = Path("images")` (fallback gracefully if an image is missing).

---

### 2. EXACT 32-SLIDE STRUCTURE (7 LITERATURE REVIEW SLIDES + 25 CORE/RESULTS SLIDES)

#### SLIDE 1: HERO TITLE SLIDE (Dark Obsidian-Indigo Theme `#0B1120`)
- **Exact Project / Submitted Review Paper Title:**
  `Toward Trustworthy Large Language Models: A Comprehensive Review of Hallucination Detection, Explainability, and Mitigation Strategies`
- **Candidate:** `Presented by : Yogesh Ravi M | 22MIA1052`
- **Guide:** `GUIDED BY - Dr. Pradeep Kumar T S, Professor, SCOPE, VIT Chennai`

#### SLIDE 2: PRESENTATION OUTLINE (32 SLIDES)
1. **Introduction, Hallucination Types & Why TinyLlama-1.1B** (Slides 3–4)
2. **Literature Review — All 40 Papers in 7 Slides (~6 Papers/Slide)** (Slides 5–11)
3. **Problem Statement, Research Gap, Challenges & Objectives** (Slides 12–13)
4. **Proposed TRUEGUARD Architecture, 4 Sensors & Simple Terms Guide** (Slides 14–18)
5. **Original Google Colab Output Plots, Tables & Prototype UI** (Slides 19–28)
6. **Comparison, Real-World ₹0 Deployment, Conclusion & Future Work** (Slides 29–30)
7. **Complete 40-Paper References & Thank You** (Slides 31–32)

#### SLIDE 3: INTRODUCTION & HALLUCINATION TAXONOMY (WITH IMAGE `01_intrinsic_vs_extrinsic.png`)
- **Why LLMs Hallucinate (Word-by-Word Guessing):** LLMs write one word (`token`) at a time by guessing what sounds fluent next (`p(y_t | x, y_<t)`), rather than checking a verified database.
- **Why Normal Confidence Fails:** Surface word probability fails on popular myths (`TruthfulQA`), where the LLM is `>95%` confident while stating a false belief.
- **Intrinsic Hallucination (Twisting Prompt Text):** Contradicts the source document or chat history in the prompt. Caught by **AAS (Prompt Focus Tracker)**.
- **Extrinsic Hallucination (Inventing Outside Facts):** Fabricates fake dates, citations, or people. Caught by **ISP (Internal Brain Lie Detector)**.
- **Guessing & Topic Drift:** Word hesitation is caught by **EEM (Logit Energy)**, and multi-sentence topic derailment is tracked by **DST (Cosine Drift)**.
- **Right Image:** Embed `01_intrinsic_vs_extrinsic.png`.

#### SLIDE 4: WHAT IS TINYLLAMA-1.1B & WHY WE USED IT (3 SIMPLE REASONS + GPT-2)
- **Subtitle:** `What is TinyLlama-1.1B-Chat-v1.0? (Meta Llama-2 Architecture, 1.1 Billion Parameters, 22 Layers, 3T Tokens)`
- **1. 100% Open-Source & "White-Box" (Open Brain):** Closed models like ChatGPT hide their internal layers. Because TinyLlama is open-weight on HuggingFace, we attach PyTorch hooks (`register_forward_hook`) directly inside its 22 layers (at **Layers 10, 13, 16, and 20 = 45%, 60%, 75%, and 90% depth**) to read its internal thoughts in one pass.
- **2. Runs for Free (₹0 Cost) on Google Colab:** Because it has `1.1B` parameters, it takes only `~2.2 GB` of GPU memory (`FP16`) — fitting effortlessly on **Google Colab's free-tier 16 GB NVIDIA Tesla T4 GPU** without paying a single rupee.
- **3. Fast Real-Time Speed (`33.49 ms/token`):** Generates `~30 words/second`, allowing us to evaluate `3,196` benchmark responses + `300` live TriviaQA queries and prove our 4 sensors add only `+2.91 ms/token (+8.7%)` overhead.
- **❖ Why We Also Tested GPT-2 (`124M Parameters, 12 Layers`):** To prove TRUEGUARD does not only work on TinyLlama, we also tested OpenAI's GPT-2 (layers `5, 7, 9, 11`) on a normal laptop CPU — achieving **85.20% Macro AUROC** (`96.02%` on HaluEval-QA).

#### SLIDES 5 TO 11 (7 SLIDES): LITERATURE REVIEW — ALL 40 PAPERS (6 PAPERS ON SLIDES 5–9, 5 PAPERS ON SLIDES 10–11)
Render a 5-column table on each slide (`S. No.`, `Author(s), Year`, `Method / Approach`, `Key Contribution`, `Gap Identified`):
- **Slide 5 (Papers 1–6):**
  1. `Su et al. [1], 2024 (ACL)` | `MIND Unsupervised MLP Probe` | Unsupervised probe on hidden states + HELM dataset | Hidden states only; no attention/energy or repair.
  2. `Zhang et al. [2], 2024 (EMNLP)` | `PRISM Prompt-Guided Probing` | Prompt templates align truth subspaces across domains | Passive scoring only; no closed-loop retrieval.
  3. `Zhang et al. [5], 2025 (Neurocomp.)` | `MHAD Deep Neuron Probing` | Isolates hallucination-sensitive neurons at first/last steps | Static concatenation; no multi-sensor calibration.
  4. `Dasgupta et al. [13], 2025 (EACL)` | `HalluShift Layer Cosine Shift` | Tracks layer-to-layer hidden cosine & Wasserstein shifts | Weak on short QA without supervised probes.
  5. `Nath et al. [16], 2025 (TPAMI)` | `HalluShift++ Multimodal Shift` | Extends internal shift tracking to vision-language models | Multimodal focus; no text RAG or abstention.
  6. `Azaria & Mitchell [27], 2023 (EMNLP)` | `SAPLMA Middle-Layer Probe` | MLP classifier on middle hidden layers separates true/false | Sensitive to domain shift without OOF calibration.
- **Slide 6 (Papers 7–12):**
  7. `Li et al. [28], 2023 (NeurIPS)` | `ITI Activation Intervention` | Shifts activations along truth directions during decoding | Fixed steering hurts fluency; cannot add missing facts.
  8. `Chen et al. [38], 2024 (AAAI)` | `Truth Forest Orthogonal Probes` | Multi-scale orthogonal probes capture truth directions | Complex probing; lacks external retrieval fallback.
  9. `Ma et al. [4], 2025 (arXiv)` | `Semantic Logit Energy` | Boltzmann energy over pre-softmax logits | Output layer only; misses deep hidden conflict.
  10. `Anonymous [6], 2025 (OpenReview)` | `Z-Score Entropy Spike + RL` | Penalizes abrupt token-entropy spikes during reasoning | Requires RL fine-tuning; no runtime RAG.
  11. `Kang et al. [7], 2025 (ACM CSUR)` | `Epistemic vs Aleatoric UQ` | Formalizes single-pass vs multi-sample UQ taxonomy | Survey only; highlights 5x–20x sampling latency.
  12. `Han et al. [14], 2024 (ICML)` | `Semantic Entropy Probes (SEP)` | Single-pass linear probes approximate semantic entropy | Single signal; no attention, drift, or repair.
- **Slide 7 (Papers 13–18):**
  13. `Moslonka et al. [17], 2025 (SPL)` | `Thermodynamic EPR` | Entropy production rate from top-k log-probabilities | Surface probabilities only; blind to hidden states.
  14. `Manakul et al. [21], 2023 (EMNLP)` | `SelfCheckGPT (5–20 Samples)` | Checks consistency across 5–20 stochastic generations | 4.65x–20x slower (169.31 ms/tok on T4 GPU).
  15. `Hajji et al. [9], 2025 (TACL)` | `Map of Misbelief Attention` | Attention drop catches intrinsic; entropy catches extrinsic | Evaluates signals separately without fusion.
  16. `Vazhentsev et al. [11], 2025 (AAAI)` | `RAUQ Attention Head UQ` | Combines uncertainty-aware attention heads + confidence | Ignores deep hidden probes and closed-loop repair.
  17. `Sriramanan et al. [12], 2024 (NeurIPS)` | `LLM-Check Log-Det Attention` | Combines attention kernel log-det, hidden & logit scores | Static scoring without GroupKFold OOF or repair.
  18. `Mündler et al. [36], 2024 (ICLR)` | `Self-Contradiction Critique` | Detects and revises self-contradictory LLM statements | Needs multiple LLM calls; misses non-contradictory lies.
- **Slide 8 (Papers 19–24):**
  19. `Huang et al. [3], 2024 (ICML)` | `TrustLLM Benchmark Suite` | Evaluates 16+ LLMs across 30+ datasets & 8 dimensions | Offline benchmark suite; not a runtime guardrail.
  20. `Jing et al. [10], 2025 (NAACL)` | `1–5 Faithfulness Rubric + NLI` | Calibrated 1–5 faithfulness scoring via LLM-as-judge | Heavy post-hoc judge latency.
  21. `Alansari & Luqman [18], 2024 (Access)` | `Lifecycle Hallucination Survey` | Surveys detection and mitigation across LLM lifecycle | Narrative survey; no empirical closed-loop controller.
  22. `Lin et al. [22], 2022 (ACL)` | `TruthfulQA (817 Myths)` | 817 adversarial questions targeting human misconceptions | Static dataset; requires internal probes to catch myths.
  23. `Min et al. [23], 2023 (EMNLP)` | `FActScore Atomic Verification` | Breaks biographies into atomic facts checked on Wikipedia | Offline metric requiring many LLM + retrieval calls.
  24. `Li et al. [29], 2023 (EMNLP)` | `HaluEval (35k QA/Dial/Summ)` | 35,000 paired grounded vs hallucinated benchmark responses | Single surface metrics fail across all 3 tasks.
- **Slide 9 (Papers 25–30):**
  25. `Chern et al. [34], 2023 (arXiv)` | `FacTool Multi-Tool Verification` | Verifies claims using web search, Python, and Scholar | High multi-step post-hoc latency.
  26. `Ji et al. [35], 2023 (ACM CSUR)` | `Intrinsic/Extrinsic NLG Survey` | Foundational taxonomy of intrinsic vs extrinsic errors | Pre-LLM focus; no white-box activation probing.
  27. `Bang et al. [37], 2023 (AACL)` | `Multitask ChatGPT Audit` | Quantifies extrinsic vs intrinsic hallucination rates | Black-box audit; no internal detector or controller.
  28. `Wu et al. [15], 2025 (ICLR)` | `BehCal-RL Abstention Training` | Proper scoring rule RL reward for calibrated abstention | Needs RL training; abstains without trying RAG first.
  29. `Yao et al. [20], 2025 (WWW)` | `ExpandR DPO Query Expansion` | Aligns query expansion with DPO for dense retrieval | Runs RAG on every query instead of gating by risk.
  30. `Dhuliawala et al. [24], 2024 (ACL)` | `CoVe Chain-of-Verification` | Drafts answer, asks verification questions, and revises | 3–5 sequential LLM passes; fails when facts are missing.
- **Slide 10 (Papers 31–35):**
  31. `Lewis et al. [25], 2020 (NeurIPS)` | `RAG Dense Passage Retrieval` | Conditions generation on retrieved Wikipedia passages | Always-on retrieval slows down easy safe queries.
  32. `Asai et al. [26], 2024 (ICLR)` | `Self-RAG Critique Tokens` | Fine-tunes LLM to emit `[Retrieve]` and `[IsSup]` tokens | Requires full fine-tuning with custom vocabulary.
  33. `Wei et al. [30], 2022 (NeurIPS)` | `Chain-of-Thought (CoT)` | Intermediate reasoning steps improve complex accuracy | Reasoning chains can hallucinate intermediate steps.
  34. `Du et al. [31], 2024 (ICML)` | `Multi-Agent Iterative Debate` | Multiple LLMs debate over rounds to refine factuality | Multiplies token & latency cost by 6x–15x.
  35. `Yin et al. [32], 2024 (Sci. China)` | `Woodpecker Visual Correction` | Post-hoc concept detection and rewriting for MLLMs | Heavy post-processing latency tailored to vision.
- **Slide 11 (Papers 36–40):**
  36. `Gao et al. [33], 2023 (ACL)` | `RARR Research & Revise` | Searches web for unverified claims and edits post-hoc | Runs on every output instead of gating on internal risk.
  37. `Gou et al. [39], 2024 (ICLR)` | `CRITIC Tool Self-Correction` | Iterative verification via search and code interpreters | Multiple tool loops; no calibrated abstention bound.
  38. `Agrawal et al. [40], 2024 (NAACL)` | `Knowledge-Graph Grounding` | Surveys KG retrieval and triple verification for LLMs | Depends on curated KGs that miss open-domain facts.
  39. `Herrera [8], 2025 (Info. Fusion)` | `4-Pillar Human-Centered XAI` | Defines faithfulness, truthfulness, plausibility, contrastivity | Conceptual framework; no live attribution formula.
  40. `Sharma et al. [19], 2024 (CHI)` | `Contrastive XAI & Human Trust` | User study showing contrastive explanations calibrate trust | Mocked explanations; not linked to live internal sensors.

#### SLIDE 12: PROBLEM STATEMENT & RESEARCH GAP
- **Single-Signal Blindness:** Output word confidence misses fluent myths (`TruthfulQA`), while hidden probes alone miss prompt neglect in long summaries.
- **Signal Polarity Inversion (Overconfident Lying):** On `HaluEval-QA` and `Dialogue`, raw token entropy inverts (`34.9%` and `37.0%` AUROC — worse than random guessing!).
- **Multi-Sample Latency Bottleneck:** SelfCheckGPT needs 5–20 generations (`169.31 ms/token` on T4 GPU), making real-time chat impossible.
- **Research Gap:** No prior system unites **4-sensor fractional-depth OOF probing + 0.00 ms log-odds XAI + a 3-Tier Closed-Loop Wikipedia RAG Controller**.

#### SLIDE 13: RESEARCH CHALLENGES & OBJECTIVES (100% COMPLETED)
- **Challenges Overcome:** (1) Extracting 4 internal signals in `<3 ms/token`, (2) Preventing `8,192-dim` hidden probe overfitting via **5-fold GroupKFold OOF stacking**, and (3) Zero-cost `0.00 ms` log-odds XAI (`c_k = w_k * z_k`).
- **Completed Objectives:**
  1. Extract **ISP** (`{0.45, 0.60, 0.75, 0.90}L`), **AAS** (top-25% attention entropy), **EEM** (`0.6 Shannon + 0.4 Renyi-2`), and **DST** (cosine drift) in one pass.
  2. Fuse via leak-free **5-fold GroupKFold OOF** L2 logistic calibration (`93.51%` Macro AUROC on TinyLlama-1.1B, `85.20%` on GPT-2).
  3. Validate the **Two-Threshold 3-Tier Controller** (`SAFE -> Tier 1 Re-Sample -> Tier 2 Live Wikipedia RAG -> Tier 3 Abstain`) across `3,196` static items and `300` live TriviaQA queries.

#### SLIDE 14: HIGH-LEVEL 10-STEP ARCHITECTURE (WITH IMAGE `02_architecture_10step.png`)
- Embed `02_architecture_10step.png` full-width inside the white card.

#### SLIDE 15: DETAILED 12-STAGE SYSTEM BLUEPRINT (WITH IMAGE `03_blueprint_12stage.png`)
- Embed `03_blueprint_12stage.png`.

#### SLIDE 16: DATASET FORMAT & PYTORCH EXTRACTION PIPELINE
- **Left Card: Benchmark Corpus & JSON Format (`N = 3,496` Total):**
  - **4 Static Benchmarks (`N = 3,196`):** `HaluEval-QA (800)`, `HaluEval-Dialogue (800)`, `HaluEval-Summarization (800)`, `TruthfulQA (796)`.
  - **Live Closed-Loop Trial (`N = 300`):** `Open-Domain TriviaQA (150 Cal / 150 Test)` decoded live with real-time Wikipedia REST API.
  - **Paired Ground-Truth JSON Schema:**
    ```json
    {
      "question_id": "qa_0412",
      "prompt": "What causes the green aurora borealis?",
      "response": "Excited oxygen atoms emitting at 557.7nm...",
      "ground_truth": "Atmospheric particle collision...",
      "label": 0   // 0 = Factual, 1 = Hallucinated
    }
    ```
  - **Balanced Pair Testing:** Every question is paired with both truthful and hallucinated responses to prevent detector length or keyword bias.
- **Right Dark Card: Single-Pass PyTorch Forward-Hook Extraction:**
  - **Non-Invasive Hooks:** Using `register_forward_hook()` directly inside the LLM during token generation — 0% model retraining or weights altered.
  - **Sensor 1 (ISP - Internal State):** Hidden states $h_l$ at 4 depths $\{10, 13, 16, 20\}$ (`45%, 60%, 75%, 90%` depth) on TinyLlama (`{5, 7, 9, 11}` on GPT-2).
  - **Sensor 2 (AAS - Focus Tracker):** Attention weights from top-quartile heads to measure prompt dispersion $1 - \sum_{i \in \text{prompt}} A_{t,i}$.
  - **Sensor 3 (EEM - Word Hesitation):** Pre-softmax vocabulary logits $\rightarrow 0.6 \cdot \text{Shannon} + 0.4 \cdot \text{Renyi-2}$ entropy.
  - **Sensor 4 (DST - Topic Drift):** Final residual stream cosine drift $1 - \cos(h_t, h_{t-1})$.
  - **Free Tesla T4 Execution:** `+2.91 ms/token` (`+8.7%`) latency overhead, `4.65x` faster than 5-sample blackbox approaches.

#### SLIDE 17: TRAINING METHODOLOGY, CALIBRATION & LOG-ODDS XAI (WITH IMAGE `04_four_layer_isp_probes.png`)
- **Left Card: How We Used Data to Train & Calibrate:**
  - **Step 1 — Sequence-Level Pooling:** Token-level sensor trajectories are mean-pooled across generated answer tokens to create a compact 4D feature vector $\phi(x,y) = [\phi_{ISP}, \phi_{AAS}, \phi_{EEM}, \phi_{DST}]$.
  - **Step 2 — Leak-Free 5-Fold `GroupKFold`:** Grouped strictly by `question_id` so questions in training folds NEVER appear in validation or testing folds — zero memorization or data leakage.
  - **Step 3 — Z-Score & $L_2$ Logistic Fusion:** Features standardized $z_k = (\phi_k - \mu_k)/\sigma_k$. Solves $\min_\mathbf{w} \mathcal{L}_{CE} + \lambda \|\mathbf{w}\|_2^2$ to optimize weights $\mathbf{w} = [w_{ISP}, w_{AAS}, w_{EEM}, w_{DST}]$.
  - **Result:** Fixes polarity inversion, achieving **93.51% Macro AUROC** & **3.10% ECE** on TinyLlama (**85.20%** on GPT-2 CPU).
- **Right Card: Log-Odds XAI & 3-Tier Actuator Logic:**
  - **Transparent Log-Odds Attribution (`0.00 ms`):** $\log(r / (1 - r)) = w_0 + \sum_{k=1}^4 c_k(x, y)$, where $c_k = w_k \cdot z_k$. Provides exact mathematical blame showing WHICH sensor caught the error with zero added latency.
  - **Calibrated Risk Thresholds (Held-Out Set):**
    - **Green (`r < 0.611`):** SAFE $\rightarrow$ Direct emission (`32.0%`)
    - **Amber (`0.611 <= r < 0.898`):** MILD $\rightarrow$ Local Re-sample at $T=0.35$ (`7.33%`)
    - **Red (`r >= 0.898`):** CRITICAL $\rightarrow$ Wikipedia RAG (`4.0%`) $\rightarrow$ Safe Abstain (`56.67%`)
  - **Proven Outcome:** Cuts emitted hallucinations on live TriviaQA from **62.00% down to 17.33%** (`72.0%` relative drop). Embed `04_four_layer_isp_probes.png`.

#### SLIDE 18: KEY TECHNICAL TERMS — IN SIMPLE EVERYDAY WORDS (10-ROW GLOSSARY TABLE)
Render a clean 3-column table (`Technical Term in PPT`, `Simple Meaning (Plain Everyday Words)`, `Why We Used It in TRUEGUARD`):
1. `White-Box PyTorch Hooks` | Listening to the LLM's internal brain layers while it writes | Captures lies inside the model in 1 pass without changing weights
2. `ISP (Internal State Probe)` | Brain Lie Detector at 45%, 60%, 75%, and 90% layer depth | Catches when internal memory knows an outside claim is false
3. `AAS (Attention Anomaly)` | Prompt Focus Tracker across top-25% attention heads | Catches when the LLM stops reading the given document or chat
4. `EEM (Energy & Entropy)` | Word Hesitation Meter (60% Shannon + 40% Renyi-2) | Catches when the LLM is confused and guessing between words
5. `DST (Drift Score Tracker)` | Topic Derailment Meter (step-to-step cosine angle jump) | Catches when the LLM slowly wanders off-topic in long answers
6. `Polarity Inversion` | Overconfident lying (model is 99% sure when stating a myth) | Explains why raw word confidence fails (34.9% on HaluEval-QA)
7. `5-Fold GroupKFold OOF` | 5-round leak-free exam on unseen questions (no memorizing) | Learns honest sensor weights and boosts accuracy to 93.51%
8. `Log-Odds XAI (c_k = w_k*z_k)` | Instant blame score showing WHICH sensor caught the lie | Explains the exact reason for every alert in 0.00 ms (zero extra cost)
9. `AUROC / ECE / AURC` | AUROC = Separation accuracy | ECE = Honesty of % | AURC = Risk | Proves 93.51% accuracy, 3.10% error, and safe selective answering
10. `3-Tier RAG Controller` | Traffic-light auto-fixer (Green=Pass, Amber=Retry, Red=Wikipedia) | Cuts final hallucinations on live TriviaQA from 62.0% down to 17.33%

#### SLIDE 19: RESULTS DISCUSSION — TOKEN SENSOR MASK (WITH IMAGE `08_token_sensor_mask.png`)
- Embed `08_token_sensor_mask.png` + 3 bullets explaining how single-pass hooks isolate fabricated tokens (`'1984'`, `'Lord Vane'`).

#### SLIDE 20: RESULTS DISCUSSION — RISK CALIBRATION (WITH IMAGE `09_baseline_vs_calibrated_risk.png`)
- Embed `09_baseline_vs_calibrated_risk.png` comparing Raw Token Entropy (`0.529` Macro AUROC) vs. TRUEGUARD OOF-Calibrated Risk (`0.935` Macro AUROC).

#### SLIDE 21: RESULTS DISCUSSION — LOG-ODDS DIAGNOSTIC TRACE (WITH IMAGE `10_terminal_log_odds_trace.png`)
- Embed `10_terminal_log_odds_trace.png`.

#### SLIDE 22: RESULTS DISCUSSION — 4-BENCHMARK AUROC & TRANSFER (WITH IMAGE `05_colab_4benchmark_auroc_transfer.png`)
- Embed `05_colab_4benchmark_auroc_transfer.png` + 2-bullet explanation (`97.50%` QA, `90.28%` Dialogue, `98.63%` Summarization, `87.63%` TruthfulQA = `93.51%` Macro AUROC).

#### SLIDE 23: RESULTS DISCUSSION — SENSOR ABLATION STUDY (WITH IMAGE `06_colab_sensor_ablation.png`)
- Embed `06_colab_sensor_ablation.png` + explanation showing that removing `ISP` (`w/o ISP`) drops TruthfulQA accuracy from `87.63%` to `62.58%`.

#### SLIDE 24: RESULTS DISCUSSION — LIVE TRIVIAQA MITIGATION (WITH IMAGE `12_colab_triviaqa_3tier_mitigation.png`)
- Embed `12_colab_triviaqa_3tier_mitigation.png` + 2 bullets (`48 SAFE 32.0%, 11 Tier-1 7.3%, 6 Tier-2 RAG 4.0%, 85 Tier-3 Abstain 56.7%`, cutting emitted hallucinations from `62.0%` to `17.33%`).

#### SLIDE 25: RESULTS DISCUSSION — T4 GPU & CPU LATENCY (WITH IMAGE `14_colab_t4_gpu_cpu_latency.png`)
- Embed `14_colab_t4_gpu_cpu_latency.png` + 2 bullets (`36.41 ms/tok` vs `33.49 ms/tok` vanilla on Free Google Colab Tesla T4 GPU = `+8.7%` overhead, `4.65x` faster than `169.31 ms/tok` 5-sample SelfCheckGPT).

#### SLIDE 26: RESULTS DISCUSSION — EXTRACTED TELEMETRY TABLE (`Query Q075`)
- Render the 12-row telemetry table for `Query Q075` (`ISP Layer 10/13/16/20 = 0.782/0.941/0.958/0.893`, `Stacked ISP = 0.934 (z=+1.94)`, `c_ISP = +2.180`, `Initial Risk = 0.914 -> Post-RAG Risk = 0.182 VERIFIED SAFE`).

#### SLIDE 27: RESULTS DISCUSSION — VERIFIED PERFORMANCE METRICS TABLE (EXACT GOOGLE COLAB LOGS)
Render the 10-row table of exact Google Colab metrics:
1. `HaluEval-QA Detection AUROC (N = 800)` | `97.50%  [F1 = 0.955, ECE = 0.024 | Raw ENT = 34.9%]`
2. `HaluEval-Dialogue Detection AUROC (N = 800)` | `90.28%  [F1 = 0.820, ECE = 0.034 | Raw ENT = 37.0%]`
3. `HaluEval-Summarization Detection AUROC (N = 800)` | `98.63%  [F1 = 0.935, ECE = 0.025 | Raw ENT = 58.0%]`
4. `TruthfulQA Generation Detection AUROC (N = 796)` | `87.63%  [F1 = 0.817, ECE = 0.042 | Raw ENT = 49.5%]`
5. `Macro Average AUROC — TinyLlama-1.1B (N = 3,196)` | `93.51%  [Macro F1 = 0.882 | Without ISP Grey-Box = 75.1%]`
6. `Macro Average AUROC — GPT-2 Cross-Model (N = 320)` | `85.20%  [HaluEval-QA = 96.02%, TruthfulQA = 74.40%]`
7. `Macro Expected Calibration Error (ECE ↓)` | `3.10%   (Down from 18.40% Raw Entropy & 24.10% NLL)`
8. `Live TriviaQA Answered Accuracy (N = 300: 150 Cal / 150 Test)` | `60.00%  (Up from 38.00% Unmitigated Greedy Baseline)`
9. `Live TriviaQA System-Wide Emitted Hallucinations (↓)` | `17.33%  (Down from 62.00% — 72.04% Relative Reduction)`
10. `Google Colab Free T4 GPU Telemetry Latency Overhead` | `+8.70%  (36.41 vs. 33.49 ms/tok — 4.65x Faster than 5-Sample)`

#### SLIDE 28: RESULTS DISCUSSION — PROTOTYPE WEB INTERFACE (WITH IMAGE `11_live_webapp_ui_screenshot.png`)
- Embed `11_live_webapp_ui_screenshot.png`.

#### SLIDE 29: COMPARISON WITH EXISTING WORKS & REAL-WORLD ₹0 DEPLOYMENT
- Compare single-pass 4-sensor fusion vs single-signal/SelfCheckGPT, highlight Review 2 -> Final Review completion, and explain **100% Free Execution (`₹0` on Google Colab T4 GPU, `< 50 KB` RAM, `0%` retraining)** and industry use cases (healthcare, legal, finance).

#### SLIDE 30: CONCLUSION, LIMITATIONS & FUTURE WORK
- Summarize hardware-verified results across `N = 3,496` responses, note white-box hook and Wikipedia coverage limitations, and outline future scaling to `8B–70B` models with Sparse Autoencoders (SAEs), multimodal VLLMs, and mid-sentence KV-cache rollback.

#### SLIDE 31: COMPLETE 40 REFERENCES (2-COLUMN LAYOUT: `[1]–[20]` LEFT, `[21]–[40]` RIGHT)
- Render all 40 references in two clean side-by-side columns (`13 pt` bold).

#### SLIDE 32: THANK YOU SLIDE (Dark Obsidian-Indigo Theme `#0B1120`)
- Large Amber-Gold **"THANK YOU"** (`88 pt`) + **"Yogesh Ravi M (22MIA1052) | Guided by Dr. Pradeep Kumar T S"**.
```

