# TRUEGUARD: A LIGHTWEIGHT REAL-TIME FRAMEWORK FOR HALLUCINATION DETECTION AND MITIGATION IN LARGE LANGUAGE MODELS

---

## CHAPTER 1 INTRODUCTION

### 1.1 INTRODUCTION
Large Language Models (LLMs) such as GPT-4, LLaMA, and Mistral have demonstrated transformative empirical capabilities in natural language reasoning, synthesis, and conversational interaction. Despite rapid commercial adoption, deploying LLMs in safety-critical domains—such as healthcare diagnostics, legal compliance, and automated financial decision-making—remains severely constrained by their propensity to hallucinate. Hallucination occurs when an LLM produces outputs that appear grammatically fluent and contextually persuasive, yet are factually incorrect, inconsistent with the input prompt, or logically self-contradictory. Such ungrounded assertions erode human trust in artificial intelligence systems and present substantial operational hazards.

### 1.2 OVERVIEW OF LARGE LANGUAGE MODEL HALLUCINATIONS
Hallucinations in natural language generation are broadly classified along two axes: intrinsic and extrinsic. Intrinsic hallucinations directly contradict the provided source context or user prompt (e.g., misstating an entity attribute explicitly stated in the context). Extrinsic hallucinations introduce unverifiable or factually false assertions absent from both the context and established world knowledge. Empirical studies demonstrate that even in multi-billion parameter architectures, hallucination rates remain pervasive, underscoring the urgent need for interpretable, human-aligned guardrails.

### 1.3 CHALLENGES PRESENT IN EXISTING DIAGNOSTIC MODALITIES
Prior research in hallucination detection has primarily developed along two distinct methodological paradigms, both presenting critical operational bottlenecks:
1. **Black-Box Multi-Sample Verification:** Methods such as Semantic Entropy generate multiple stochastic completions per user prompt (typically 5 to 10 samples) and measure their semantic consensus. While effective at identifying epistemic uncertainty, repeated autoregressive generation incurs prohibitive computational costs and memory overhead (e.g., ~142.3 ms/token latency), making multi-sample approaches incompatible with real-time streaming applications.
2. **Single-Signal White-Box Probing:** To avoid multiple forward passes, recent works monitor internal model representations in a single execution pass (e.g., tracking multi-head attention entropy, monitoring logit energy landscapes, or measuring representation drift). While computationally efficient, individual internal signals typically capture only specific facets of model uncertainty, leaving systems vulnerable to heterogeneous hallucination modes.

Furthermore, conventional detection systems operate as passive post-hoc diagnostic monitors: they flag errors only after the complete response has been emitted, offering no mechanism for immediate intervention.

### 1.4 PROJECT STATEMENT
To resolve these clinical and infrastructural challenges, this project presents the design, implementation, and empirical validation of TRUEGUARD, an end-to-end, lightweight, real-time framework that unifies multi-signal intrinsic uncertainty tracking, calibrated signal fusion, and active closed-loop mitigation within a single forward pass.

### 1.5 OBJECTIVES
1. To develop a multi-signal white-box extraction pipeline directly from the LLM execution graph, capturing representation, attention, predictive, and temporal uncertainty without modifying base model weights.
2. To standardize and fuse signals online via Z-score normalization and a calibrated logistic regression head.
3. To maintain ultra-low latency overhead to support real-time token streaming operations.
4. To implement and validate a two-tier closed-loop active mitigation strategy (Targeted Retrieval-Augmented Grounding and Calibrated Abstention) when risk exceeds a safety threshold.

### 1.6 SCOPE OF THE PROJECT
The scope of TRUEGUARD encompasses the software-based interception of autoregressive generation using PyTorch forward hooks. It is evaluated across five benchmark distributions (TruthfulQA, HaluEval-QA, HaluEval-Summ, HaluEval-Dial, and HELM) using open-source models (LLaMA-2-7B-Chat, Mistral-7B-Instruct). 
*[FLAG: Needs more detail regarding deployment environments. Unlike the reference project which outlines hardware IoT deployments, TRUEGUARD is purely a software inference engine. If cloud/edge deployment specifics are required for your scope, they must be added here.]*

---

## CHAPTER 2 BACKGROUND & LITERATURE REVIEW

### 2.1 INTRODUCTION TO LITERATURE REVIEW
Understanding the mechanics of LLM hallucinations requires a cross-disciplinary examination of internal activation probing, output distribution uncertainty, and dynamic inference-time mitigation techniques. 

### 2.2 SURVEY ON BLACK-BOX AND MULTI-SAMPLE PREDICTION MODELS
Pioneering work in hallucination detection focused on semantic consistency. SelfCheckGPT and Semantic Entropy Probes (SEPs) generate 5-10 stochastic responses to measure variance. While accurate, these methods fundamentally require repeated full-sequence generation, establishing a severe computational bottleneck.

### 2.3 SURVEY ON WHITE-BOX ACTIVATION AND UNCERTAINTY PROBING
Recent studies demonstrated that an LLM's internal representations contain linear subspaces encoding factual truthfulness (MIND, MHAD). Attention pattern analysis revealed that attention entropy over prompt tokens serves as a sensitive indicator of context unfaithfulness. HaluShift demonstrated that semantic drift can be tracked via cosine distances between consecutive layer representations. However, these works typically evaluate signals in isolation.

### 2.4 SURVEY ON INFERENCE-TIME MITIGATION
Mitigating hallucinations post-generation introduces substantial latency. Approaches such as Chain-of-Verification or universal Retrieval-Augmented Generation (RAG) execute retrieval for every query, incurring redundant overhead. Behavioral calibration techniques demonstrate that models can be taught to recognize empirical uncertainty bounds, yet lack a dynamic token-level trigger mechanism.

### 2.5 THEMATIC COMPARISON & LITERATURE SYNTHESIS
Existing literature presents a strict trade-off between detection accuracy and inference latency. TRUEGUARD synthesizes the insights from white-box probing by extracting four complementary signals—Internal State Probes (ISP), Attention Anomaly Score (AAS), Entropy-Energy Monitor (EEM), and Distribution Shift Tracker (DST)—and uniquely deploying them as an active trigger for targeted RAG and calibrated abstention.

### 2.6 CRITICAL SUMMARY AND RESEARCH EVOLUTION
The evolution from post-hoc evaluation to real-time intervention highlights a critical gap: the absence of a unified, single-pass multi-signal controller capable of halting ungrounded text mid-sentence.

---

## CHAPTER 3 RESEARCH GAP & SYSTEM ARCHITECTURE

### 3.1 RESEARCH GAPS IN EXISTING STATE-OF-THE-ART
1. **Latency Bottlenecks:** Multi-sample methods are incompatible with real-time streaming architectures.
2. **Signal Isolation:** Single-signal white-box metrics fail to capture the full spectrum of intrinsic and extrinsic hallucinations.
3. **Passive Monitoring:** Current systems lack an integrated mechanism to stop generation and correct hallucinations on the fly.

### 3.2 PROPOSED INTEGRATED SYSTEM SOLUTION
TRUEGUARD acts as an inline tensor monitor that intercepts internal model activations at each autoregressive step. Rather than invoking secondary forward passes, TRUEGUARD extracts a 4-dimensional feature vector directly from the active computation graph, normalizing it online and processing it through a logistic fusion head to compute an instantaneous token-level risk score R(t).

### 3.3 OVERALL SYSTEM ARCHITECTURE
The system operates natively within the transformer architecture. Forward hooks intercept:
- Residual hidden states from middle-to-late layers.
- Multi-head attention tensor slices.
- Output logit distributions.
If the sequence-level risk exceeds a safety threshold (τ = 0.50), generation is halted and routed to the mitigation engine.

### 3.4 MULTI-TIER MITIGATION DATA FLOW
- **Tier 1 (Targeted RAG):** The system queries a local knowledge base using the prompt and the pre-hallucination token prefix. If relevant documents are retrieved with high similarity (>0.75), decoding restarts with the retrieved context appended.
- **Tier 2 (Calibrated Abstention):** If retrieval fails or risk remains high, the system emits a calibrated disclaimer declining to answer due to low factual confidence.

---

## CHAPTER 4 METHODOLOGY & SYSTEM DESIGN

### 4.1 DATASET PROVENANCE & CLINICAL DESCRIPTION
TRUEGUARD was evaluated across rigorous NLP benchmarks sourced from Hugging Face:
- TruthfulQA: 817 questions across 38 categories designed to elicit human false beliefs.
- HaluEval: 30,000 paired instances contrastively labeled by human annotators (QA, Summarization, Dialogue).
- HELM: Multi-step reasoning and knowledge retrieval tasks with verifiable ground truths.

### 4.2 SIGNAL 1: INTERNAL STATE PROBES (ISP)
Evaluating representation vectors across middle-to-late transformer layers (L=16, 24) using a calibrated linear probe. Higher ISP values directly indicate elevated hallucination likelihood.

### 4.3 SIGNAL 2: ATTENTION ANOMALY SCORE (AAS)
Monitoring attention weight dispersion over prompt context tokens using normalized Shannon entropy across attention heads. An elevated AAS flags anomalous attention detachment from the source context.

### 4.4 SIGNAL 3: ENTROPY-ENERGY MONITOR (EEM)
Computing a weighted combination of output distribution Shannon entropy and Rényi-2 confidence (β = 0.60). This captures both distribution tail flatness and peak probability collapse.

### 4.5 SIGNAL 4: DISTRIBUTION SHIFT TRACKER (DST)
Measuring temporal cosine divergence between successive hidden state vectors during generation. Sudden transitions isolate semantic disorientation.

### 4.6 ONLINE NORMALIZATION AND FUSION FORMULATION
Raw signals inhabit disparate numerical ranges. TRUEGUARD applies online Z-score standardization using Welford's algorithm. The standardized signals are fused via a calibrated logistic regression head optimized via L-BFGS over a 5-fold cross-validation calibration subset.

### 4.7 HARDWARE DATA ACQUISITION SUBSYSTEM DESIGN
*[FLAG: The reference project includes a detailed embedded IoT hardware section (ESP32, sensors) here. TRUEGUARD is entirely software-based (PyTorch tensors). If your course requires a hardware/systems engineering component, you must document the specific computing infrastructure (NVIDIA T4 GPUs, CPU workstations, memory management) here to match the required depth.]*

---

## CHAPTER 5 IMPLEMENTATION & SOFTWARE PLATFORM

### 5.1 PYTORCH INFERENCE ARCHITECTURE
TRUEGUARD is implemented using the PyTorch framework and the Hugging Face Transformers library. The base language model (e.g., LLaMA-2-7B) is loaded in 16-bit precision with weights frozen (requires_grad=False). 

### 5.2 FORWARD HOOK INTERCEPTION
Instead of modifying the model's source code, PyTorch forward hooks are dynamically registered on intermediate transformer blocks. As token generation proceeds, these hooks seamlessly capture the residual hidden state vector (R^4096) and attention matrices with negligible overhead.

### 5.3 IN-MEMORY SINGLETON INFERENCE ENGINE
*[FLAG: The reference report details a Django 5.2 full-stack platform, REST API, and SQLite database. TRUEGUARD's implementation details are currently limited to the inference scripts. To match the depth of the reference, you should deeply expand on your Python software architecture, class structures (e.g., `TrueGuardController`), and how the mitigation loop interacts with the text generation loop.]*

### 5.4 DUAL-TIER MITIGATION PIPELINE
Implemented as a state-machine that intercepts the generation stream. When `R(t) > 0.50`, the generation loop breaks, triggering an asynchronous call to a localized vector database for Tier 1 RAG retrieval, followed by conditional prompt rewriting.

---

## CHAPTER 6 RESULTS AND DISCUSSION

### 6.1 EXPERIMENTAL SETUP & VALIDATION METHODOLOGY
Evaluations were conducted on an NVIDIA T4 GPU (16 GB VRAM) using 5-fold cross-validation. Detection performance is evaluated using Area Under the Receiver Operating Characteristic Curve (AUROC), AUPRC, and F1 Score.

### 6.2 MODEL PERFORMANCE BENCHMARKS & METRICS
TRUEGUARD achieves an average AUROC of 0.8821 ± 0.0170 across all five benchmarks. 
- TruthfulQA: 0.8533 ± 0.0533
- HaluEval-QA: 0.8840 ± 0.0185
- HELM: 0.9063 ± 0.0454

### 6.3 ABLATION STUDY & SIGNAL IMPORTANCE
A leave-one-out ablation study confirmed the necessity of all four signals. Removing the Entropy-Energy Monitor (EEM) produced the largest performance decline (-0.0518 AUROC), underscoring the importance of output predictive confidence. Removing Internal State Probes (ISP) proved that internal representations encode truthfulness dimensions absent from output logits.

### 6.4 LATENCY AND COMPUTATIONAL OVERHEAD
TRUEGUARD incurs a total overhead of 12.4 ± 0.5 ms/token. 
- Semantic Entropy Baseline: 142.3 ms/token.
- TRUEGUARD Speedup: 11.5x.
The extraction and fusion budget requires less than 0.05% of the compute required for a single transformer forward pass, proving exceptional feasibility for streaming.

### 6.5 MITIGATION EFFECTIVENESS (DOUBLE-BLIND HUMAN EVAL)
In a double-blind human evaluation (n=300, Cohen's κ = 0.82), TRUEGUARD reduced hallucination frequency from 31.2% to 11.3%—a 63.8% relative reduction. Tier-1 RAG successfully resolved 58.4% of queries, while Tier-2 abstention preserved an 88.0% query answer coverage.

### 6.6 TECHNICAL & CLINICAL LIMITATIONS
While calibrated abstention mitigates factual errors, overly conservative thresholds (τ < 0.35) reduce system helpfulness by abstaining too frequently. Production deployments require clear transparency mechanisms to notify users when responses are altered via Tier-1 or Tier-2 guardrails.

---

## CHAPTER 7 CONCLUSION AND FUTURE WORK

### 7.1 KEY CONCLUSIONS & SUMMARY OF ACHIEVEMENTS
TRUEGUARD successfully unifies four intrinsic model signals (ISP, AAS, EEM, DST) and learned logistic regression fusion into a real-time guard layer. Evaluated across five benchmark distributions, it achieves 0.8821 AUROC with only 12.4 ms/token latency. 

### 7.2 PERFORMANCE AGAINST PLANNED TARGETS
The system achieved an 11.5x speedup over state-of-the-art multi-sample methods (Semantic Entropy) and verified a 63.8% relative reduction in hallucinations without severely crippling the model's empirical utility (retaining 88% coverage).

### 7.3 FUTURE SCOPE OF WORK & ENGINEERING ROADMAP
Future research includes extending probe calibration to multilingual representations, expanding the Tier-1 RAG knowledge bases dynamically, and exploring multi-agent collaborative workflows to further validate intermediate reasoning steps before final emission.
