# MASTER PROMPT FOR CLAUDE — 30-SLIDE FINAL CAPSTONE PRESENTATION (`python-pptx`)

Copy and paste everything inside the code block below into Claude, and attach the images from `E:\trueguard\FINAL_SUBMISSION\CLAUDE_PPT_KIT\images\`:

```text
You are an expert academic presentation designer and Python developer. Write a single, complete, token-efficient `python-pptx` script (`generate_30slide_ppt.py`) that generates a 30-slide widescreen (16:9, `16.0 x 9.0 inches`) PowerPoint presentation (`FINAL_PRESENTATION_30SLIDES.pptx`) for my M.Tech. Final Review Capstone Viva.

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
  - Use clean helper functions (`add_header(slide, title)`, `add_card_bullets(slide, items, ...)`, `add_styled_table(slide, headers, rows, ...)`, `add_image_with_caption(slide, img_path, bullets)`), and store the 40 literature papers and 40 references in compact Python lists so the entire script fits easily within one response without truncation.
- **Image Folder Path:**
  - Load images from `IMAGES_DIR = Path("images")` (fallback comfortably if an image is missing). Use the exact image filenames specified per slide below.

---

### 2. EXACT 30-SLIDE STRUCTURE & VERIFIED CONTENT

#### SLIDE 1: HERO TITLE SLIDE (Dark Obsidian-Indigo Theme `#0B1120`)
- **Exact Project / Submitted Review Paper Title:**
  `Toward Trustworthy Large Language Models: A Comprehensive Review of Hallucination Detection, Explainability, and Mitigation Strategies`
- **Candidate:** `Presented by : Yogesh Ravi M | 22MIA1052`
- **Guide:** `GUIDED BY - Dr. Pradeep Kumar T S, Professor, SCOPE, VIT Chennai`

#### SLIDE 2: PRESENTATION OUTLINE
1. **Introduction, What is TinyLlama-1.1B & Hallucination Taxonomy** (Slides 3–5)
2. **Comprehensive Literature Review — All 40 Papers Across 6 Pillars** (Slides 6–10)
3. **Problem Statement, Research Challenges, Gaps & Objectives** (Slides 11–14)
4. **Proposed TRUEGUARD Architecture & Simple-English Glossary** (Slides 15–18)
5. **Google Colab Verified Results, Plots, Tables & Prototype UI** (Slides 19–25)
6. **Comparison with Existing Works & Real-World ₹0 Cost Deployment** (Slides 26–27)
7. **Conclusion, Limitations, Future Work & 40 References** (Slides 28–30)

#### SLIDE 3: INTRODUCTION (IN SIMPLE WORDS)
- **Why This Matters:** Large Language Models (LLMs) are used in healthcare, law, and finance, but they frequently invent false facts ("hallucinations") that sound 100% fluent and authoritative.
- **Why Normal Confidence Fails:** Standard word-level probability (`softmax confidence`) fails because LLMs are often **>95% confident** when repeating popular myths or fabricated citations.
- **What We Built (TRUEGUARD):** Instead of trusting outside words or running 5–20 slow generations, our framework attaches **4 internal brain sensors** in **one single pass**, explains *which* internal mechanism failed in `0.00 ms`, and repairs the answer automatically using live Wikipedia facts.

#### SLIDE 4: WHAT IS LLM HALLUCINATION & WHAT IS TINYLLAMA-1.1B?
- **Autoregressive Generation (Word-by-Word Guessing):** LLMs write one word (`token`) at a time by guessing what sounds fluent next (`p(y_t | x, y_<t)`), rather than checking a verified database.
- **What is `TinyLlama-1.1B-Chat-v1.0`? (Our Primary Open-Brain LLM):**
  - Open-source Transformer LLM built with the exact same architecture as Meta's Llama-2, scaled to **1.1 Billion parameters** (`22 internal layers`, `2,048 hidden dimension`, `32 attention heads`), pre-trained on **3 Trillion tokens**.
  - **Why we chose it:** (1) **White-Box Access** (we can attach PyTorch hooks inside layers `10, 13, 16, 20`), and (2) **Zero-Cost Hardware Fit** (runs in FP16 on Google Colab's free 16 GB Tesla T4 GPU at ₹0 cost).
- **What is `GPT-2 (124M)`? (Our Secondary LLM):** A 12-layer (`124 Million parameter`) model probed at layers `5, 7, 9, 11` on a local CPU to prove TRUEGUARD is architecture-agnostic.

#### SLIDE 5: HALLUCINATION TAXONOMY (WITH IMAGE `01_intrinsic_vs_extrinsic.png`)
- **Left Content:**
  - **Intrinsic Hallucination (Twisting the Given Text):** Output contradicts the source document or chat history in the prompt. Caught by **AAS (Attention Anomaly Score / Focus Tracker)**.
  - **Extrinsic Hallucination (Inventing Outside Facts):** Output fabricates dates, entities, or facts absent from the prompt. Caught by **ISP (Internal State Probe / Brain Lie Detector)**.
  - **Surface Guessing & Topic Drift:** Token hesitation is caught by **EEM (Energy & Entropy Metric)**; multi-sentence derailment is tracked by **DST (Drift Score Tracker)**.
- **Right Image:** Embed `01_intrinsic_vs_extrinsic.png`.

#### SLIDES 6 TO 10: LITERATURE REVIEW — ALL 40 PAPERS (8 PAPERS PER SLIDE, 5 COLUMNS: `S.No.`, `Author(s), Year`, `Method`, `Key Contribution`, `Gap Identified`)
- **Slide 6 (Papers 1–8: Pillar 1 — Internal State Probing):**
  1. `Su et al. [1], 2024 (ACL)` | `MIND Unsupervised MLP Probe` | Unsupervised probe on hidden states + HELM dataset | Hidden states only; no attention/energy or repair.
  2. `Zhang et al. [2], 2024 (EMNLP)` | `PRISM Prompt-Guided Probing` | Prompt templates align truth subspaces across domains | Passive scoring only; no closed-loop retrieval.
  3. `Zhang et al. [5], 2025 (Neurocomp.)` | `MHAD Deep Neuron Probing` | Isolates hallucination-sensitive neurons at first/last steps | Static concatenation; no multi-sensor calibration.
  4. `Dasgupta et al. [13], 2025 (EACL)` | `HalluShift Layer Cosine Shift` | Tracks layer-to-layer hidden cosine & Wasserstein shifts | Weak on short QA without supervised probes.
  5. `Nath et al. [16], 2025 (TPAMI)` | `HalluShift++ Multimodal Shift` | Extends internal shift tracking to vision-language models | Multimodal focus; no text RAG or abstention.
  6. `Azaria & Mitchell [27], 2023 (EMNLP)` | `SAPLMA Middle-Layer Probe` | MLP classifier on middle hidden layers separates true/false | Sensitive to domain shift without OOF calibration.
  7. `Li et al. [28], 2023 (NeurIPS)` | `ITI Activation Intervention` | Shifts activations along truth directions during decoding | Fixed steering hurts fluency; cannot add missing facts.
  8. `Chen et al. [38], 2024 (AAAI)` | `Truth Forest Orthogonal Probes` | Multi-scale orthogonal probes capture truth directions | Complex probing; lacks external retrieval fallback.
- **Slide 7 (Papers 9–16: Pillars 2 & 3 — Logit Energy, Entropy & Attention):**
  9. `Ma et al. [4], 2025 (arXiv)` | `Semantic Logit Energy` | Boltzmann energy over pre-softmax logits | Output layer only; misses deep hidden conflict.
  10. `Anonymous [6], 2025 (OpenReview)` | `Z-Score Entropy Spike + RL` | Penalizes abrupt token-entropy spikes during reasoning | Requires RL fine-tuning; no runtime RAG.
  11. `Kang et al. [7], 2025 (ACM CSUR)` | `Epistemic vs Aleatoric UQ` | Formalizes single-pass vs multi-sample UQ taxonomy | Survey only; highlights 5x–20x sampling latency.
  12. `Han et al. [14], 2024 (ICML)` | `Semantic Entropy Probes (SEP)` | Single-pass linear probes approximate semantic entropy | Single signal; no attention, drift, or repair.
  13. `Moslonka et al. [17], 2025 (SPL)` | `Thermodynamic EPR` | Entropy production rate from top-k log-probabilities | Surface probabilities only; blind to hidden states.
  14. `Manakul et al. [21], 2023 (EMNLP)` | `SelfCheckGPT (5–20 Samples)` | Checks consistency across 5–20 stochastic generations | 4.65x–20x slower (169.31 ms/tok on T4 GPU).
  15. `Hajji et al. [9], 2025 (TACL)` | `Map of Misbelief Attention` | Attention drop catches intrinsic; entropy catches extrinsic | Evaluates signals separately without fusion.
  16. `Vazhentsev et al. [11], 2025 (AAAI)` | `RAUQ Attention Head UQ` | Combines uncertainty-aware attention heads + confidence | Ignores deep hidden probes and closed-loop repair.
- **Slide 8 (Papers 17–24: Pillars 3 & 4 — Trajectory & Evaluation Benchmarks):**
  17. `Sriramanan et al. [12], 2024 (NeurIPS)` | `LLM-Check Log-Det Attention` | Combines attention kernel log-det, hidden & logit scores | Static scoring without GroupKFold OOF or repair.
  18. `Mündler et al. [36], 2024 (ICLR)` | `Self-Contradiction Critique` | Detects and revises self-contradictory LLM statements | Needs multiple LLM calls; misses non-contradictory lies.
  19. `Huang et al. [3], 2024 (ICML)` | `TrustLLM Benchmark Suite` | Evaluates 16+ LLMs across 30+ datasets & 8 dimensions | Offline benchmark suite; not a runtime guardrail.
  20. `Jing et al. [10], 2025 (NAACL)` | `1–5 Faithfulness Rubric + NLI` | Calibrated 1–5 faithfulness scoring via LLM-as-judge | Heavy post-hoc judge latency.
  21. `Alansari & Luqman [18], 2024 (Access)` | `Lifecycle Hallucination Survey` | Surveys detection and mitigation across LLM lifecycle | Narrative survey; no empirical closed-loop controller.
  22. `Lin et al. [22], 2022 (ACL)` | `TruthfulQA (817 Myths)` | 817 adversarial questions targeting human misconceptions | Static dataset; requires internal probes to catch myths.
  23. `Min et al. [23], 2023 (EMNLP)` | `FActScore Atomic Verification` | Breaks biographies into atomic facts checked on Wikipedia | Offline metric requiring many LLM + retrieval calls.
  24. `Li et al. [29], 2023 (EMNLP)` | `HaluEval (35k QA/Dial/Summ)` | 35,000 paired grounded vs hallucinated benchmark responses | Single surface metrics fail across all 3 tasks.
- **Slide 9 (Papers 25–32: Pillars 4 & 5 — Audits, RL & Retrieval Grounding):**
  25. `Chern et al. [34], 2023 (arXiv)` | `FacTool Multi-Tool Verification` | Verifies claims using web search, Python, and Scholar | High multi-step post-hoc latency.
  26. `Ji et al. [35], 2023 (ACM CSUR)` | `Intrinsic/Extrinsic NLG Survey` | Foundational taxonomy of intrinsic vs extrinsic errors | Pre-LLM focus; no white-box activation probing.
  27. `Bang et al. [37], 2023 (AACL)` | `Multitask ChatGPT Audit` | Quantifies extrinsic vs intrinsic hallucination rates | Black-box audit; no internal detector or controller.
  28. `Wu et al. [15], 2025 (ICLR)` | `BehCal-RL Abstention Training` | Proper scoring rule RL reward for calibrated abstention | Needs RL training; abstains without trying RAG first.
  29. `Yao et al. [20], 2025 (WWW)` | `ExpandR DPO Query Expansion` | Aligns query expansion with DPO for dense retrieval | Runs RAG on every query instead of gating by risk.
  30. `Dhuliawala et al. [24], 2024 (ACL)` | `CoVe Chain-of-Verification` | Drafts answer, asks verification questions, and revises | 3–5 sequential LLM passes; fails when facts are missing.
  31. `Lewis et al. [25], 2020 (NeurIPS)` | `RAG Dense Passage Retrieval` | Conditions generation on retrieved Wikipedia passages | Always-on retrieval slows down easy safe queries.
  32. `Asai et al. [26], 2024 (ICLR)` | `Self-RAG Critique Tokens` | Fine-tunes LLM to emit `[Retrieve]` and `[IsSup]` tokens | Requires full fine-tuning with custom vocabulary.
- **Slide 10 (Papers 33–40: Pillars 5 & 6 — Reasoning, Post-Editing & Human-Trust XAI):**
  33. `Wei et al. [30], 2022 (NeurIPS)` | `Chain-of-Thought (CoT)` | Intermediate reasoning steps improve complex accuracy | Reasoning chains can hallucinate intermediate steps.
  34. `Du et al. [31], 2024 (ICML)` | `Multi-Agent Iterative Debate` | Multiple LLMs debate over rounds to refine factuality | Multiplies token & latency cost by 6x–15x.
  35. `Yin et al. [32], 2024 (Sci. China)` | `Woodpecker Visual Correction` | Post-hoc concept detection and rewriting for MLLMs | Heavy post-processing latency tailored to vision.
  36. `Gao et al. [33], 2023 (ACL)` | `RARR Research & Revise` | Searches web for unverified claims and edits post-hoc | Runs on every output instead of gating on internal risk.
  37. `Gou et al. [39], 2024 (ICLR)` | `CRITIC Tool Self-Correction` | Iterative verification via search and code interpreters | Multiple tool loops; no calibrated abstention bound.
  38. `Agrawal et al. [40], 2024 (NAACL)` | `Knowledge-Graph Grounding` | Surveys KG retrieval and triple verification for LLMs | Depends on curated KGs that miss open-domain facts.
  39. `Herrera [8], 2025 (Info. Fusion)` | `4-Pillar Human-Centered XAI` | Defines faithfulness, truthfulness, plausibility, contrastivity | Conceptual framework; no live attribution formula.
  40. `Sharma et al. [19], 2024 (CHI)` | `Contrastive XAI & Human Trust` | User study showing contrastive explanations calibrate trust | Mocked explanations; not linked to live internal sensors.

#### SLIDE 11: SCOPE & PROBLEM STATEMENT
- **1. Single-Signal Blindness:** Output word confidence misses fluent myths (`TruthfulQA`), while hidden probes alone miss prompt neglect in long summaries.
- **2. Signal Polarity Inversion (Overconfident Lying):** On `HaluEval-QA` and `Dialogue`, raw token entropy inverts (`34.9%` and `37.0%` AUROC — worse than random guessing!) because the LLM is overconfident when fabricating.
- **3. Prohibitive Multi-Sample Latency:** SelfCheckGPT needs 5–20 generations (`169.31 ms/token` on T4 GPU), too slow for live chat.
- **4. Open-Loop Operation & Scope:** Prior tools only raise passive alarms without explaining *why* or fixing the answer. *(Scope: White-box open-weight Transformers — TinyLlama-1.1B & GPT-2).*

#### SLIDE 12: RESEARCH CHALLENGES & GAPS
- **Challenge 1 — Single-Pass Multi-Signal Extraction:** Reading hidden states, attention maps, logit energy, and cosine drift in 1 forward pass with `<10%` latency overhead.
- **Challenge 2 — High-Dimensional Probe Overfitting:** Concatenating 4 layers (`4 x 2048 = 8,192 dims`) memorizes prompts unless strict **5-fold GroupKFold OOF** stacking is used.
- **Challenge 3 — Zero-Cost Explainability (XAI):** Replacing slow SHAP/LIME perturbations with an exact `0.00 ms` formula (`c_k = w_k * z_k`).
- **Research Gap:** No prior system unites **4-sensor fractional-depth OOF probing + 0 ms log-odds XAI + a 3-Tier Closed-Loop Wikipedia RAG Controller**.

#### SLIDE 13: RESEARCH OBJECTIVES (100% COMPLETED & VERIFIED)
- **Primary Objective:** Build and hardware-verify **TRUEGUARD** — a single-pass, 4-sensor internal telemetry fusion and 3-tier closed-loop mitigation framework.
- **Secondary Objectives:**
  1. Extract **ISP** (`{0.45, 0.60, 0.75, 0.90}L`), **AAS** (top-25% attention entropy), **EEM** (`0.6 Shannon + 0.4 Renyi-2`), and **DST** (cosine drift) in one forward pass.
  2. Fuse via leak-free **5-fold GroupKFold OOF** L2 logistic calibration + analytical log-odds attributions (`c_k = w_k * z_k`).
  3. Actuate a **Two-Threshold 3-Tier Controller** (`SAFE -> Tier 1 Re-Sample -> Tier 2 Live Wikipedia RAG -> Tier 3 Abstain`) across `3,196` static items and `300` live TriviaQA queries.

#### SLIDE 14: HIGH-LEVEL 10-STEP ARCHITECTURE (WITH IMAGE `02_architecture_10step.png`)
- Embed `02_architecture_10step.png` full-width inside the white card with a concise 2-line caption explaining the single-pass flow from User Query -> PyTorch Forward Hooks -> 4 Sensors -> OOF Fusion -> 3-Tier Controller.

#### SLIDE 15: DETAILED 12-STAGE SYSTEM BLUEPRINT (WITH IMAGE `03_blueprint_12stage.png`)
- Embed `03_blueprint_12stage.png` alongside key stage highlights: Stage 1–4 (Single-Pass Hook Extraction), Stage 5–8 (GroupKFold OOF Stacking, Z-Scoring & Log-Odds XAI), Stage 9–12 (Two-Threshold 3-Tier Closed-Loop Actuation & Re-Verification).

#### SLIDE 16: BENCHMARK CORPUS (`N = 3,496`) & TELEMETRY DETAILS
- **4 Static Benchmarks (`N = 3,196`):** `HaluEval-QA` (`800`), `HaluEval-Dialogue` (`800`), `HaluEval-Summarization` (`800`), `TruthfulQA` (`796`).
- **Live Closed-Loop Trial (`N = 300`):** Open-domain `TriviaQA` (`150 calibration / 150 test`) with live Wikipedia REST API RAG.
- **Hardware Used (`₹0 Cost`):** Google Colab Free-Tier **NVIDIA Tesla T4 GPU** (`16 GB VRAM, FP16`) + Local Intel Core CPU (`16 GB RAM, FP32`).

#### SLIDE 17: WHY 4-SENSOR OOF FUSION? (WITH IMAGE `04_four_layer_isp_probes.png`)
- **Left Content:** Explain how each sensor catches a different failure mode (`ISP` = memory lies, `AAS` = ignoring prompt, `EEM` = word guessing, `DST` = topic drift) and how **5-Fold GroupKFold OOF** fixes polarity inversion to reach **93.51% Macro AUROC** and **3.10% Macro ECE**.
- **Right Image:** Embed `04_four_layer_isp_probes.png`.

#### SLIDE 18: KEY TECHNICAL TERMS — IN SIMPLE EVERYDAY WORDS (TABLE SLIDE)
Render a clean 3-column table (`Technical Term`, `Simple Everyday Meaning`, `Role in TRUEGUARD`):
1. `TinyLlama-1.1B & GPT-2` | Open-brain LLMs (22 layers & 12 layers) run on free Colab GPU & laptop CPU | Let us read internal neuron activations for free (₹0)
2. `White-Box PyTorch Hooks` | Listening to the LLM's internal brain layers while it writes | Captures all 4 signals in 1 pass without retraining
3. `ISP (Internal State Probe)` | Brain Lie Detector at 45%, 60%, 75%, and 90% layer depth | Catches when internal memory knows an outside claim is false
4. `AAS (Attention Anomaly)` | Prompt Focus Tracker across top-25% attention heads | Catches when the LLM stops looking at the given document
5. `EEM (Energy & Entropy)` | Word Hesitation Meter (60% Shannon + 40% Renyi-2) | Catches when the LLM is torn between multiple words
6. `DST (Drift Score Tracker)` | Topic Derailment Meter (step-to-step cosine angle jump) | Catches when the LLM wanders off-topic across sentences
7. `Polarity Inversion` | Overconfident lying (LLM is 99% sure when stating a myth) | Explains why raw word confidence gets only 34.9% on QA
8. `5-Fold GroupKFold OOF` | 5-round leak-free exam on unseen questions (no memorizing) | Learns honest sensor weights -> 93.51% Macro AUROC
9. `Log-Odds XAI (c_k = w_k*z_k)` | Instant blame score showing WHICH sensor triggered the alarm | Explains every alert in 0.00 ms with zero extra compute
10. `3-Tier RAG Controller` | Traffic-light auto-fixer (Green=Pass, Amber=Retry, Red=Wikipedia) | Cuts live TriviaQA hallucinations from 62.0% to 17.33%

#### SLIDE 19: COLAB OUTPUT PLOT — 4-BENCHMARK AUROC & TRANSFER (WITH IMAGE `05_colab_4benchmark_auroc_transfer.png`)
- Embed `05_colab_4benchmark_auroc_transfer.png`.
- **Explanation:** (a) TRUEGUARD achieves **97.50%** on HaluEval-QA, **90.28%** on Dialogue, **98.63%** on Summarization, and **87.63%** on TruthfulQA (**93.51% Macro Average**), crushing Raw Entropy (`34.9%–58.0%`). (b) Cross-benchmark heatmap proves strong domain transfer.

#### SLIDE 20: COLAB OUTPUT PLOT — SENSOR ABLATION & ROC CURVES (WITH IMAGES `06_colab_sensor_ablation.png` & `07_colab_roc_curves.png`)
- Embed `06_colab_sensor_ablation.png` (top/left) and `07_colab_roc_curves.png` (bottom/right).
- **Explanation:** Removing `ISP` (`w/o ISP`, red bar) drops TruthfulQA AUROC from **87.63% to 62.58%** and HaluEval-QA from **97.49% to 91.77%**, proving deep internal brain probing is essential to catch fluent lies.

#### SLIDE 21: TOKEN SENSOR MASK & RISK CALIBRATION (WITH IMAGES `08_token_sensor_mask.png` & `09_baseline_vs_calibrated_risk.png`)
- Embed `08_token_sensor_mask.png` and `09_baseline_vs_calibrated_risk.png`.
- **Explanation:** Single-pass hooks isolate the exact fabricated tokens (`'1984'`, `'Lord Vane'`), and OOF calibration separates true vs. hallucinated distributions cleanly (`0.529` Raw Entropy -> `0.935` TRUEGUARD Macro AUROC).

#### SLIDE 22: LOG-ODDS DIAGNOSTIC TRACE & TELEMETRY TABLE (WITH IMAGE `10_terminal_log_odds_trace.png`)
- **Left Image:** Embed `10_terminal_log_odds_trace.png`.
- **Right Table (`Query Q075 Telemetry`):**
  - `ISP Layer 10 / 13 / 16 / 20`: `0.782 / 0.941 / 0.958 / 0.893`
  - `Stacked OOF ISP (s_ISP / z_ISP)`: `0.934 (z = +1.94)`
  - `AAS / EEM / DST Scores`: `0.684 (+0.82) / 0.241 (-0.35) / 0.318 (+0.61)`
  - `Dominant Log-Odds Blame (c_ISP)`: `+2.180 (Parametric Memory Fault)`
  - `Initial Risk -> Post-RAG Risk`: `0.914 (Tier 2 RAG) -> 0.182 (VERIFIED SAFE)`

#### SLIDE 23: VERIFIED PERFORMANCE METRICS TABLE (EXACT GOOGLE COLAB LOGS)
Render a high-contrast table of our exact verified metrics:
1. `HaluEval-QA Detection AUROC (N = 800)` | `97.50%  [F1 = 0.955, ECE = 0.024 | Raw Entropy = 34.9%]`
2. `HaluEval-Dialogue Detection AUROC (N = 800)` | `90.28%  [F1 = 0.820, ECE = 0.034 | Raw Entropy = 37.0%]`
3. `HaluEval-Summarization Detection AUROC (N = 800)` | `98.63%  [F1 = 0.935, ECE = 0.025 | Raw Entropy = 58.0%]`
4. `TruthfulQA Generation Detection AUROC (N = 796)` | `87.63%  [F1 = 0.817, ECE = 0.042 | Raw Entropy = 49.5%]`
5. `Macro Average AUROC — TinyLlama-1.1B (N = 3,196)` | `93.51%  [Macro F1 = 0.882 | Without ISP Grey-Box = 75.1%]`
6. `Macro Average AUROC — GPT-2 Cross-Model (N = 320)` | `85.20%  [HaluEval-QA = 96.02%, TruthfulQA = 74.40%]`
7. `Macro Expected Calibration Error (ECE ↓)` | `3.10%   (Down from 18.40% Raw Entropy & 24.10% NLL)`
8. `Live TriviaQA Answered Factual Accuracy (N = 300)` | `60.00%  (Up from 38.00% Unmitigated Baseline — +22.0% Gain)`
9. `Live TriviaQA System-Wide Emitted Hallucinations (↓)` | `17.33%  (Down from 62.00% — 72.04% Relative Reduction)`
10. `Free Colab Tesla T4 GPU Latency Overhead` | `+8.70%  (36.41 vs 33.49 ms/tok — 4.65x Faster than 5-Sample)`

#### SLIDE 24: PROTOTYPE INTERFACE & LIVE TRIVIAQA MITIGATION PLOT (WITH IMAGES `11_live_webapp_ui_screenshot.png` & `12_colab_triviaqa_3tier_mitigation.png`)
- Embed `11_live_webapp_ui_screenshot.png` (left) and `12_colab_triviaqa_3tier_mitigation.png` (right).
- **Explanation:** On `150` live TriviaQA test queries ($\tau_{\text{warn}}=0.6114, \tau_{\text{fault}}=0.8984$): `48 SAFE (32.0%)`, `11 Tier-1 Re-sampled (7.3%)`, `6 Tier-2 Wikipedia RAG (4.0%)`, `85 Tier-3 Abstain (56.7%)`, cutting emitted hallucinations by **72.04%** (`62.0% -> 17.33%`).

#### SLIDE 25: SELECTIVE PREDICTION (`AURC`) & HARDWARE LATENCY PLOTS (WITH IMAGES `13_colab_selective_prediction_aurc.png` & `14_colab_t4_gpu_cpu_latency.png`)
- Embed `13_colab_selective_prediction_aurc.png` (left) and `14_colab_t4_gpu_cpu_latency.png` (right).
- **Explanation:** (a) Selective prediction achieves **AURC = 0.412** (vs `0.526` Entropy & `0.603` NLL). (b) On Google Colab's free T4 GPU, TRUEGUARD takes **36.41 ms/tok** vs **33.49 ms/tok** vanilla (`+2.91 ms`, **4.65x faster** than `169.31 ms/tok` 5-sample SelfCheckGPT).

#### SLIDE 26: COMPARISON WITH EXISTING WORKS & REVIEW 2 EVOLUTION
- **Single-Pass 4-Sensor Fusion vs. Single-Signal / Multi-Sample:** Beats raw token entropy (`0.529` AUROC) and is **4.65x faster** than 5-sample SelfCheckGPT (`169.31 ms/tok`) while reaching **0.935 Macro AUROC**.
- **Leak-Free OOF Calibration vs. Uncalibrated Signals:** Fixes severe polarity inversion on QA (`0.349 -> 0.975`) and Dialogue (`0.370 -> 0.903`) and cuts calibration error (`ECE`) from `18.4%` to `3.1%`.
- **Review 2 -> Final Review Progression:** All open questions from Review 2 (sensor weights, `0.00 ms` log-odds XAI, and 3-tier closed-loop Wikipedia RAG) are now 100% implemented and hardware-verified.

#### SLIDE 27: REAL-WORLD DEPLOYMENT, ₹0 COST & PRACTICAL USE CASES
- **100% Free Execution (`₹0 / $0.00` Spent):** Run entirely on **Google Colab's Free-Tier NVIDIA Tesla T4 GPU** and a local laptop CPU using open-weight models (`TinyLlama-1.1B` & `GPT-2`) and the free Wikipedia REST API.
- **Ultra-Lightweight Drop-In Middleware (`< 50 KB` RAM):** Wraps any HuggingFace/PyTorch model via forward hooks with **0% LLM retraining** and outputs a JSON safety envelope (`Answer + Risk r(x,y) + Log-Odds Blame c_k + Wikipedia Evidence`).
- **Industry Use Cases:** Healthcare clinical note assistants, legal contract summarization, and enterprise customer support bots.

#### SLIDE 28: CONCLUSION, LIMITATIONS & FUTURE WORK
- **Conclusion:** TRUEGUARD unifies single-pass 4-sensor telemetry (`ISP, AAS, EEM, DST`), leak-free 5-fold GroupKFold OOF calibration (`93.51%` Macro AUROC on TinyLlama-1.1B, `85.20%` on GPT-2), `0.00 ms` log-odds XAI, and a 3-Tier Wikipedia RAG Controller that cuts live hallucinations by **72.04%**.
- **Limitations:** Requires white-box tensor access (cannot inspect closed text-only APIs); Tier 2 RAG depends on Wikipedia coverage.
- **Future Work:** Scale to `8B–70B` models with Sparse Autoencoders (SAEs), extend `AAS` to multimodal Vision-Language LLMs, and add mid-sentence KV-cache token rollback.

#### SLIDES 29 & 30: COMPLETE 40 REFERENCES (20 REFERENCES PER SLIDE) + THANK YOU FOOTER
- **Slide 29 (`References 1–20`):** List references `[1]` to `[20]` in clean 2-column or compact list layout (`13–14 pt` bold) corresponding to the 40 reviewed papers.
- **Slide 30 (`References 21–40 & Thank You Banner`):** List references `[21]` to `[40]` in the upper card (`1.35"` to `7.35"`) and place a prominent Royal-Indigo & Gold **"THANK YOU — Questions & Discussion | Yogesh Ravi M (22MIA1052) | Guided by Dr. Pradeep Kumar T S"** banner at the bottom (`7.45"` to `8.75"`).
```

