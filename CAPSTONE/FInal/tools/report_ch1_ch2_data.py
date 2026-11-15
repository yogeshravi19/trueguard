"""
Chapters 1, 2, 4, and 5 content definitions for TRUEGUARD Final Project Report.
Streamlined for 1.5 standard line spacing to maintain exactly <= 70 pages.
"""

CH1_SECTIONS = [
    ("1.1 INTRODUCTION", None, [
        "Large Language Models (LLMs) built upon the autoregressive Transformer architecture have fundamentally transformed automated question answering, abstractive document summarization, legal and clinical analysis, code generation, and multi-turn dialogue [3, 18]. Scaling next-token prediction across trillions of tokens alongside instruction tuning and reinforcement learning from human feedback produces remarkable linguistic fluency and broad generalization. However, generative language model deployment in high-stakes operational environments remains severely constrained by their propensity to hallucinate—generating assertions that are grammatically coherent, rhetorically confident, and contextually plausible, yet factually false with respect to world knowledge or directly contradictory to the provided source context [22, 35].",
        "From an architectural standpoint, hallucinations emerge as a structural consequence of open-loop maximum-likelihood autoregressive decoding. At each step t, standard decoders sample or select the next token y_t from P_theta(y_t | x, y_{<t}) without any closed-loop internal state observer verifying whether intermediate residual-stream representations remain anchored to factual memory or whether causal attention heads remain grounded on prompt context [9, 27]. Once an early token deviates into an ungrounded trajectory, causal self-attention conditions all subsequent tokens on that fabricated premise, creating a compounding error cascade that surface token probabilities fail to signal [13, 36]. To resolve this, this project introduces TRUEGUARD (Trustworthy Real-Time Uncertainty and Internal-Signal Guard), a unified closed-loop feedback control framework for single-pass multi-signal hallucination detection, log-odds explainability, and graded three-tier runtime mitigation."
    ]),
    ("1.2 BACKGROUND OF THE PROJECT", None, [
        "Research into language model generation reliability between 2020 and 2025 has evolved through three distinct paradigms [18, 35]. First-generation approaches treated the model as an opaque black box and relied on post-hoc external verification pipelines—such as Retrieval-Augmented Generation (RAG) [25], RARR [33], FacTool [34], and Chain-of-Verification (CoVe) [24]—which decompose generated text into claims and query external search engines or auxiliary verifier models. While effective offline, always-on external verification introduces substantial network and multi-call latency on every user query, even when the model's initial response is already factual.",
        "Second-generation approaches sought to estimate uncertainty from output token distributions or stochastic ensembles. Kadavath et al. and Kuhn et al. [41] demonstrated that clustering multiple sampled generations into semantic equivalence classes yields semantic entropy, while Manakul et al. [21] showed that agreement across stochastic samples flags fabrications. However, generating 5 to 20 full completions per prompt multiplies inference latency by 5x to 20x [7, 14]. Third-generation interpretability studies discovered that intermediate hidden representations and attention maps encode rich, linearly decodable truthfulness signals during the single forward pass [27, 28, 42]. TRUEGUARD synthesizes these internal observations into an end-to-end closed-loop control system."
    ]),
    ("1.3 MOTIVATION", None, [
        "Five concrete engineering and scientific observations motivate the TRUEGUARD framework:",
        "1. Orthogonal Signal Blind Spots: Surface logit entropy (EEM) detects vocabulary-level guessing but misses confident misconceptions [22]. Conversely, attention dispersion (AAS) captures context detachment [9], directional cosine drift (DST) captures semantic leaps [13], and supervised hidden probes (ISP) capture factual encoding [27]. Fusing all four signals provides multi-layered defense-in-depth.",
        "2. Elimination of Multi-Sample Latency Bottlenecks: In interactive serving, systems cannot tolerate the 5x–20x latency penalty of SelfCheckGPT [21] or multi-agent debate [31]. TRUEGUARD operates on the exact hidden states, attention matrices, and logits computed during a single forward pass (+2.91 ms/tok, +8.7% overhead).",
        "3. Prevention of Stacking Overfitting and Polarity Inversion: Naive in-sample fitting causes logistic classifiers to overfit high-capacity probes. Furthermore, raw entropy and NLL reverse polarity on benchmarks with length asymmetry. An inner out-of-fold (OOF) grouped stacking protocol with automatic sign adaptation is therefore essential.",
        "4. Bridging Detection and Graded Runtime Repair: Abstaining on every uncertain query harms utility, while unconditionally invoking external RAG wastes compute. A two-threshold controller (tau_warning, tau_fault) enables proportional intervention: temperature-annealed re-sampling for warnings, targeted Wikipedia retrieval for faults, and calibrated abstention when repair fails.",
        "5. Economic Viability on Standard Hardware: Commercial multi-call APIs incur heavy recurring costs. TRUEGUARD executes directly on self-hosted, open-weights infrastructure (single T4 GPU or local CPU) with zero external licensing fees, reducing operational compute overhead by over 76% compared to multi-sample voting."
    ]),
    ("1.4 PROBLEM STATEMENT", None, [
        "Given an input prompt token sequence x = (x_1, ..., x_m) and an autoregressive Transformer M_theta, standard decoding generates an output sequence y = (y_1, ..., y_n) open-loop without verifying factual grounding. Single-pass surface heuristics (entropy, NLL) achieve near-chance AUROC (0.50–0.65) on misconceptions and invert polarity under length asymmetry, while multi-sample detectors multiply latency by 5x–20x. The core objective of this project is to design, mathematically formulate, implement, and empirically validate TRUEGUARD: a single-pass white-box multi-sensor architecture that extracts hidden probes, attention entropy, hybrid logit entropy, and semantic drift; fuses them via leakage-free out-of-fold logistic calibration with exact log-odds attributions; and dynamically routes generations across SAFE pass-through, Tier 1 re-sampling, Tier 2 Wikipedia retrieval repair, and Tier 3 calibrated abstention at minimal latency."
    ]),
    ("1.5 RESEARCH GAP", None, [
        "Our PRISMA 2020 systematic review of 40 primary studies across Six Research Pillars identifies five major gaps:",
        "Gap 1 — Signal Isolation (Pillars 1–3): Prior detectors evaluate hidden-state probes [27], attention dispersion [9], or logit entropy [4] in isolation without out-of-fold multi-sensor calibration or polarity-inversion handling.",
        "Gap 2 — Computational Overhead and Equivalence (Pillars 1–3): Multi-sample uncertainty requires 5 to 20 generation passes per query [21], while white-box studies rarely establish numerical equivalence between offline scoring and step-by-step KV-cached generation.",
        "Gap 3 — Disconnection of Mitigation from Detection (Pillar 5): Detection systems emit risk scores without triggering repair, while mitigation pipelines (RAG [25], CoVe [24], BehCal-RL [15]) operate without closed-loop multi-sensor diagnostic feedback or graded escalation thresholds.",
        "Gap 4 — Explainability Deficit (Pillar 6): Existing detectors output opaque scalar probabilities rather than decomposing risk into signed per-sensor log-odds attributions satisfying Herrera's [8] four XAI criteria.",
        "Gap 5 — Human Trust Calibration Gap (Pillar 6): Explanations only improve human trust when presented comparatively alongside calibrated abstention rather than isolated overconfident predictions [19]."
    ]),
    ("1.6 OBJECTIVES", None, [
        "The technical objectives of this project are:",
        "1. To conduct a PRISMA 2020 systematic literature review of 40 peer-reviewed studies (2020–2025) across Six Research Pillars and establish a taxonomy of hallucination signals and mitigation mechanisms.",
        "2. To formulate and implement four single-pass white-box sensors (ISP, AAS, EEM, DST) supporting both post-pass evaluation and step-by-step KV-cached online monitoring with verified numerical equivalence (max |Delta| < 10^-4).",
        "3. To design a leakage-free question-grouped K-fold evaluation and inner out-of-fold (OOF) probe stacking architecture that prevents probe overfitting, adapts to polarity inversions, and outputs signed log-odds attributions.",
        "4. To implement a closed-loop Three-Tier Graded Actuator governed by two calibrated thresholds (tau_warning, tau_fault) escalating across local re-sampling, targeted Wikipedia retrieval repair, and calibrated abstention.",
        "5. To benchmark TRUEGUARD on real hardware across five datasets (TruthfulQA, HaluEval-QA, HaluEval-Dialogue, HaluEval-Summarization, TriviaQA) using TinyLlama-1.1B on Tesla T4 GPU and GPT-2 (124M) on CPU."
    ]),
    ("1.7 SCOPE OF THE PROJECT", None, [
        "The scope covers theoretical formulation, modular PyTorch implementation, automated numerical equivalence testing, multi-benchmark grouped cross-validation, live TriviaQA mitigation, and hardware latency profiling. Evaluations are conducted on open-weights Transformer models (TinyLlama-1.1B-Chat-v1.0 on Tesla T4 GPU across N = 3,196 benchmark responses and N = 300 live TriviaQA queries, plus GPT-2 124M on CPU). For black-box APIs restricting hidden states, our leave-one-out ablation (-ISP) explicitly quantifies the performance of the surface/attention fallback (AAS + EEM + DST)."
    ]),
    ("1.8 CONTRIBUTIONS OF THE PROJECT", None, [
        "This project makes eight verifiable contributions to trustworthy large language model engineering:"
    ]),
    (None, "1.8.1 PRISMA 2020 SIX-PILLAR TAXONOMY OF 40 PRIMARY STUDIES", [
        "We synthesize 40 peer-reviewed papers (2020–2025) into a structured Six-Pillar taxonomy covering Internal States, Uncertainty & Entropy, Attention, Benchmarks, Mitigation & RAG, and Human Trust."
    ]),
    (None, "1.8.2 FOUR-SENSOR SINGLE-PASS WHITE-BOX OBSERVATION BANK", [
        "We implement four complementary single-pass sensors (ISP, AAS, EEM, DST) in src/tg_pipeline.py and verify that post-pass extraction and KV-cached online monitoring agree to within 3.49 x 10^-6 on ISP and 1.53 x 10^-5 on EEM."
    ]),
    (None, "1.8.3 LEAKAGE-FREE INNER OUT-OF-FOLD (OOF) PROBE STACKING", [
        "We introduce an inner GroupKFold out-of-fold stacking protocol for multi-layer hidden probes across fractional depths {0.45, 0.60, 0.75, 0.90}L, preventing in-sample overfitting and preserving balanced multi-sensor weights."
    ]),
    (None, "1.8.4 AUTOMATED POLARITY DIAGNOSTICS AND SIGN-ADAPTIVE FUSION", [
        "We audit polarity inversion on length-asymmetric benchmarks (where raw NLL achieves AUROC = 0.089) and implement signed L2 logistic fusion that automatically aligns inverted surface signals."
    ]),
    (None, "1.8.5 THREE-TIER CLOSED-LOOP MITIGATION CONTROLLER", [
        "We formulate a graded actuator governed by two calibrated thresholds (tau_warn = 0.611, tau_fault = 0.898) escalating from local temperature-annealed re-sampling (Tier 1) to Wikipedia retrieval grounding (Tier 2) and calibrated abstention (Tier 3)."
    ]),
    (None, "1.8.6 EMPIRICAL VALIDATION ON NVIDIA TESLA T4 GPU (N = 3,196)", [
        "Across 3,196 answers, TRUEGUARD achieves 0.935 macro AUROC (0.986 Summarization, 0.975 QA, 0.903 Dialogue, 0.876 TruthfulQA) and 0.031 ECE, outperforming single-pass entropy by +30.6 AUROC points."
    ]),
    (None, "1.8.7 LIVE CLOSED-LOOP TRIVIAQA MITIGATION AND SELECTIVE PREDICTION", [
        "On 150 live TriviaQA generations, the controller cuts the answered hallucination rate from 62.0% to 40.0% (-35.5% relative, -72.0% system-wide) with an AURC of 0.412, outperforming entropy (0.526) and NLL (0.603)."
    ]),
    (None, "1.8.8 REAL HARDWARE LATENCY PROFILING AND COMPUTE REDUCTION", [
        "On Tesla T4 GPU, TRUEGUARD adds +2.91 ms/tok (+8.7% overhead) in post-pass mode and +5.81 ms/tok (+17.3%) in online KV-cached mode, operating 4.31x to 4.65x faster than 5-sample SelfCheck consistency."
    ]),
]

CH2_SECTIONS = [
    ("2.1 TRANSFORMER DECODERS AND INTERNAL REPRESENTATIONS", None, [
        "Autoregressive language models generate text by conditioning each token on prefix history through stacked Transformer decoder layers [3, 27]. Let x = (x_1, ..., x_m) be the input prompt. At step t, the model processes the concatenated sequence (x, y_{<t}) through L transformer blocks. Each block l consists of multi-head causal self-attention (MHA) followed by a position-wise feed-forward network (FFN) with residual connections and layer normalization. The intermediate hidden state h_t^{(l)} in R^d evolves through residual addition:",
        "EQUATION_2_1: h_t^{(l)} = h_t^{(l-1)} + MHA^{(l)}(LN(h_t^{(l-1)})) + FFN^{(l)}(LN(h_t^{(l,-)}))",
        "At layer L, final hidden states are projected via lm_head onto vocabulary logits z_t = W_u h_t^{(L)} in R^{|V|}, yielding next-token probabilities P(y_t | x, y_{<t}) = softmax(z_t). Crucially, middle-to-late residual representations h_t^{(l)} (fractional depths 0.45L to 0.90L) linearize semantic factual associations before final vocabulary selection, providing a direct observation window into model truthfulness [27, 28]."
    ]),
    ("2.2 MECHANISM OF HALLUCINATIONS IN GENERATIVE LLMS", None, [
        "Hallucinations arise from two distinct mechanisms: intrinsic contradictions (where the generated output conflicts with user context) and extrinsic fabrications (where the model invents unsupported details absent from context and training memory) [18, 35]. In autoregressive decoding, ungrounded tokens emerge when: (i) the model lacks parametric knowledge for an entity, flattening logit distributions; (ii) attention heads fail to anchor to source tokens, dispersing mass onto stylistic sink positions [9]; or (iii) adversarial prompts activate superficial word associations over factual reasoning [22]. Once a hallucinated token is sampled, causal masking forces all subsequent positions to treat it as true premise, driving the latent trajectory into an unrecoverable error state [13]."
    ]),
    ("2.3 LIMITATIONS OF BLACK-BOX DETECTION METHODS", None, [
        "Black-box detection methods inspect only final surface text and output probabilities [21, 41]. While non-invasive, they suffer from severe operational limitations: (1) Latency Scaling: Multi-sample consistency (SelfCheckGPT [21]) requires K = 5 to 20 full completions, multiplying compute and memory bandwidth; (2) Inversion Vulnerability: On length-asymmetric QA tasks, concise factual answers exhibit higher token entropy than verbose hallucinated sentences, inverting raw entropy and NLL discrimination; and (3) Misconception Blindness: When models generate common misconceptions, they do so with high confidence and low entropy [22], completely fooling surface uncertainty metrics."
    ]),
    ("2.4 CONTROL-THEORETIC FRAMING OF HALLUCINATION MITIGATION", None, [
        "TRUEGUARD models LLM generation through the lens of closed-loop control engineering: the frozen transformer is the plant, four single-pass hooks form the sensor bank, logistic stacking acts as the state observer, and the three-tier controller provides graded corrective actuation. Instead of treating generation as open-loop sampling, TRUEGUARD continuously monitors internal state deviations, computes calibrated risk r(x,y), and applies proportional closed-loop feedback (temperature annealing, retrieval re-prompting, or refusal) to guarantee bounded error rates."
    ]),
]
