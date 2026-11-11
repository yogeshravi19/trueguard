# TRUEGUARD: A Lightweight Real-Time Framework for Hallucination Detection and Mitigation in Large Language Models

**Yogesh Ravi M**$^1$ and **T. S. Pradeep Kumar**$^2$  
$^1$*School of Computer Science and Engineering, Vellore Institute of Technology, Chennai 600127, India* (Email: yogeshravi.m2022@vitstudent.ac.in)  
$^2$*Faculty of Computer Science and Engineering, Vellore Institute of Technology, Chennai 600127, India* (Email: pradeepkumar.ts@vit.ac.in)  

---

### Abstract
Large Language Models (LLMs) frequently produce fluent yet factually unfounded statements, posing severe operational risks in safety-critical deployments. Existing detection techniques predominantly require multi-sample consistency checks (incurring 5--10 stochastic forward passes and $\sim$142.3 ms/token latency) or isolated single-signal white-box metrics that fail to generalize across diverse hallucination modalities. In this paper, we propose **TRUEGUARD**, an inline, multi-signal framework that monitors autoregressive generation within a single forward pass without modifying the underlying model parameters. TRUEGUARD concurrently extracts four orthogonal intrinsic signals: Internal State Probes (ISP), Attention Anomaly Score (AAS), Entropy-Energy Monitor (EEM), and Distribution Shift Tracker (DST). These signals are standardized on-the-fly via online $Z$-score normalization and fused through a calibrated logistic regression head to yield a token-level risk score $R(t)$. When sequence risk surpasses a calibrated safety threshold ($\tau = 0.50$), TRUEGUARD triggers active closed-loop mitigation through targeted Retrieval-Augmented Grounding (Tier 1) and calibrated abstention (Tier 2). Evaluated across five benchmark distributions (TruthfulQA, HaluEval-QA, HaluEval-Summ, HaluEval-Dial, and HELM), TRUEGUARD achieves an average AUROC of $0.8821 \pm 0.0170$ with only $12.4 \pm 0.5$ ms/token latency overhead---an 11.5$\times$ speedup over Semantic Entropy. In double-blind human evaluations ($n = 300$, Cohen's $\kappa = 0.82$), TRUEGUARD achieves a 63.8% relative reduction in hallucination occurrences while maintaining an 88.0% query answer coverage. Complete reproducible code and artifacts are available at https://github.com/yogeshravi19/trueguard.

**Keywords:** Large Language Models, Hallucination Detection, Trustworthy AI, Real-Time Inference, Uncertainty Quantification, Active Mitigation, Explainable AI.

---

## I. Introduction

### A. Background and Motivation
Large Language Models (LLMs) such as GPT-4, LLaMA, and Mistral have demonstrated transformative empirical capabilities in natural language reasoning, synthesis, and conversational interaction [1], [2]. Despite rapid commercial adoption, deploying LLMs in safety-critical domains---such as healthcare diagnostics, legal compliance, and automated financial decision-making---remains severely constrained by their propensity to hallucinate [3], [21]. Hallucination occurs when an LLM produces outputs that appear grammatically fluent and contextually persuasive, yet are factually incorrect, inconsistent with the input prompt, or logically self-contradictory [4], [11]. Such ungrounded assertions erode human trust in artificial intelligence systems and present substantial operational hazards [31], [13].

### B. Challenges in Real-Time Hallucination Detection
Prior research in hallucination detection has primarily developed along two distinct methodological paradigms:
1. **Black-Box Multi-Sample Verification:** Methods such as SelfCheckGPT [5] and Semantic Entropy [6] generate multiple stochastic completions per user prompt (typically 5 to 10 samples) and measure their semantic consensus via clustering or natural language inference. While effective at identifying epistemic uncertainty, repeated autoregressive generation incurs prohibitive computational costs and memory overhead (e.g., $\sim$142.3 ms/token), making multi-sample approaches incompatible with real-time, low-latency streaming applications.
2. **Single-Signal White-Box Probing:** To avoid multiple forward passes, recent works monitor internal model representations in a single execution pass. These include probing intermediate residual layer representations [20], [7], [8], tracking multi-head attention entropy [9], [27], monitoring logit energy landscapes [25], calculating entropy production rates [29], and quantifying representation drift across layers [10], [16]. While computationally efficient, individual internal signals typically capture only specific facets of model uncertainty. As established in recent surveys [12], [26], attention dispersion effectively flags intrinsic contradictions against context tokens but frequently misses extrinsic fabrications, whereas predictive output entropy displays the complementary vulnerability.

Furthermore, conventional detection systems operate as passive post-hoc diagnostic monitors: they flag errors only after the complete response has been emitted, offering no mechanism for immediate intervention or mid-sentence course correction [19].

### C. Proposed Solution and Key Contributions
To address these challenges, we introduce **TRUEGUARD**, a lightweight, real-time framework that unifies multi-signal intrinsic uncertainty tracking, calibrated signal fusion, fine-grained token explainability, and active closed-loop mitigation within a single forward pass. Without retraining or modifying the base LLM weights, TRUEGUARD concurrently intercepts four complementary intrinsic signals directly from the ongoing forward execution graph:
* **Internal State Probes (ISP):** Evaluates representation vectors across middle-to-late transformer layers using a calibrated linear probe.
* **Attention Anomaly Score (AAS):** Monitors attention weight dispersion over prompt context tokens using normalized Shannon entropy.
* **Entropy-Energy Monitor (EEM):** Computes a weighted combination of output distribution Shannon entropy and Rényi-2 confidence.
* **Distribution Shift Tracker (DST):** Measures temporal cosine divergence between successive hidden state vectors during generation.

These signals are normalized on-the-fly and integrated via a learned logistic regression fusion head to produce an instantaneous token-level risk score $R(t)$. When sequence risk exceeds a safety threshold ($\tau = 0.50$), TRUEGUARD triggers active mitigation: attempting targeted Retrieval-Augmented Grounding (Tier 1) or falling back to calibrated abstention (Tier 2).

The key contributions of this paper are summarized as follows:
1. **Unified Multi-Signal Architecture:** We formalize and evaluate a single-pass extraction pipeline integrating ISP, AAS, EEM, and DST, capturing representation, attention, predictive, and temporal uncertainty within a single forward execution.
2. **Learned Real-Time Fusion:** We demonstrate that a calibrated logistic regression layer operating on online $Z$-score standardized signals outperforms individual baseline signals while adding negligible overhead ($<0.1$ ms).
3. **Rigorous Benchmark Validation:** Evaluated across five benchmark distributions (TruthfulQA, HaluEval-QA, HaluEval-Summ, HaluEval-Dial, and HELM) using 5-fold cross-validation, TRUEGUARD achieves an average AUROC of $0.8821 \pm 0.0170$.
4. **High Efficiency with 11.5$\times$ Speedup:** In running hardware evaluations, TRUEGUARD requires only $12.4 \pm 0.5$ ms/token latency overhead, achieving an 11.5$\times$ speedup over multi-sample Semantic Entropy ($142.3$ ms/token).
5. **Closed-Loop Mitigation Verification:** In a double-blind human evaluation study ($n = 300$, Cohen's $\kappa = 0.82$), TRUEGUARD's two-tier mitigation reduces hallucination occurrences by 63.8% while preserving an 88.0% query answer coverage.
6. **Open Reproducibility:** We provide complete open-source code, evaluation harnesses, Colab notebooks, and pre-computed benchmark artifacts at https://github.com/yogeshravi19/trueguard.

### D. Paper Organization
The remainder of this article is organized as follows: Section II reviews related literature. Section III formulates the problem and system architecture. Section IV presents the TRUEGUARD methodology and its four intrinsic signals. Section V outlines the experimental setup, benchmark provenance, and probe calibration process. Section VI analyzes empirical results and ablation studies. Section VII provides an engineering discussion and practical considerations. Finally, Section VIII concludes the paper.

---

## II. Related Work

### A. Hallucination Categorization and Taxonomies
Hallucinations in natural language generation are broadly classified along two axes: *intrinsic* and *extrinsic* [3], [2]. Intrinsic hallucinations directly contradict the provided source context or user prompt (e.g., misstating an entity attribute explicitly stated in the context). Extrinsic hallucinations introduce unverifiable or factually false assertions absent from both the context and established world knowledge. Huang et al. [1] established the TrustLLM benchmark, showing that hallucination rates remain pervasive even in multi-billion parameter architectures. Additional evaluations by Bang et al. [21] and Mündler et al. [11] highlighted self-contradictory failure modes across reasoning tasks, underscoring the urgent need for interpretable, human-aligned guardrails [31], [13].

### B. Internal Activation and Uncertainty Probing
Pioneering work by Azaria and Mitchell [20] demonstrated that an LLM's internal representations contain linear subspaces encoding factual truthfulness. Su et al. [7] developed MIND, an unsupervised probing method for internal hidden states. Zhang et al. [8] introduced MHAD, identifying that truthfulness representations are predominantly localized in intermediate transformer layers. Sriramanan et al. [15] formulated LLM-Check to detect hallucinations via single-pass internal features.

In parallel, attention pattern analysis by Hajji et al. [9] and Vazhentsev et al. [27] revealed that attention entropy over prompt tokens serves as a sensitive indicator of context unfaithfulness. In the logit and entropy domain, Han et al. [6] proposed Semantic Entropy Probes (SEPs), while Ma et al. [25] derived Semantic Energy to capture confidence beyond raw softmax entropy. In structural tracking, Dasgupta et al. [10] and Nath et al. [16] demonstrated that semantic drift can be tracked via cosine distances between consecutive layer representations (HaluShift/HaluShift++). Furthermore, Moslonka et al. [29] utilized token-level entropy production rates, and Kang et al. [12] and Jing et al. [26] established formal uncertainty quantification foundations for hallucination scoring.

### C. Inference-Time Mitigation and Guardrails
Mitigating hallucinations post-generation introduces substantial latency. Multi-step reasoning and self-correction approaches---such as Chain-of-Verification (CoVe) [19], RARR [33], CRITIC [38], and Woodpecker [37]---generate auxiliary queries or search tools, multiplying total inference runtime. Retrieval-Augmented Generation (RAG) [17], Self-RAG [18], ExpandR [32], and ChatKBQA [40] augment generation with external knowledge retrieval, yet executing retrieval for every token or query incurs redundant overhead. Representation intervention methods, including Inference-Time Intervention (ITI) [34] and Truth Forest [24], steer activations along truth-correlated directions during decoding. In reinforcement learning, Wu et al. [28], Nie et al. [30], and Bai et al. [41] demonstrated that behavioral calibration and step-level rewards reduce hallucinated steps. Additionally, tool-augmented frameworks like FacTool [14], multi-agent debate [36], knowledge graph integration [39], and Chain-of-Thought prompting [35] have demonstrated varied mitigation utility. TRUEGUARD builds upon these foundations by synthesizing intrinsic signals into a lightweight controller that triggers targeted retrieval and calibrated abstention dynamically at the token level.

---

## III. Problem Formulation and System Architecture

### A. Threat Model and Formal Problem Definition
Let an autoregressive language model $\mathcal{M}$ parameterized by $\theta$ generate a sequence of output tokens $Y = (y_1, y_2, \dots, y_T)$ given an input prompt context $C = (c_1, c_2, \dots, c_M)$. At decoding step $t \in \{1, \dots, T\}$, the model performs a standard forward pass:
$$p(y_t \mid C, y_{<t}) = \text{softmax}(z_t)$$
where $z_t \in \mathbb{R}^{|V|}$ denotes the output logit vector over vocabulary $V$. Concurrent with logit computation, the transformer architecture produces residual hidden representations $\{h_t^L\}_{L=1}^{N_L}$ and multi-head attention tensor slices $\{A_t^L\}_{L=1}^{N_L}$, where $N_L$ denotes the total number of transformer layers.

The objective of real-time hallucination detection is to learn an inline mapping:
$$f: (z_t, \{h_t^L\}, \{A_t^L\}) \mapsto R(t) \in [0, 1]$$
such that $R(t)$ accurately reflects the probability that token $y_t$ initiates or constitutes a factual hallucination, evaluated under the strict operational constraint that latency overhead $\Delta t \ll t_{\text{forward}}$.

![End-to-End Architecture](fig1_architecture.png)
*Fig. 1. End-to-end architecture of the TRUEGUARD framework. Four complementary intrinsic signals (ISP, AAS, EEM, DST) are extracted concurrently in a single forward pass, standardized online via $Z$-score tracking, and fused via logistic regression to trigger active closed-loop mitigation.*

### B. End-to-End System Workflow
As illustrated in Fig. 1, TRUEGUARD operates as an inline tensor monitor that intercepts internal model activations at each autoregressive step. Rather than invoking secondary forward passes or external verification calls, TRUEGUARD extracts a 4-dimensional feature vector:
$$X_t = [\text{ISP}_t, \text{AAS}_t, \text{EEM}_t, \text{DST}_t]^T$$
directly from the active computation graph. The signals are normalized online and processed through a logistic fusion head to compute $R(t)$. If sequence-level risk $R_{\text{seq}} = \max_{i \le t} R(i)$ exceeds safety threshold $\tau$, TRUEGUARD halts autoregressive emission mid-sentence and initiates active mitigation.

---

## IV. The Proposed TRUEGUARD Methodology

### A. Signal 1: Internal State Probes (ISP)
Following the observation that truthfulness representations stabilize in middle-to-late transformer layers [20], [8], we extract the residual hidden state $h_t^L \in \mathbb{R}^d$ at selected layers $L \in \{16, 24\}$ (for a 32-layer model). A linear probe parameterized by weight vector $w_{\text{probe}} \in \mathbb{R}^d$ and bias $b \in \mathbb{R}$ evaluates the factual confidence:
$$\text{ISP}_t = 1 - \sigma(w_{\text{probe}}^T h_t^L + b)$$
where $\sigma(\cdot)$ is the standard logistic sigmoid. Higher $\text{ISP}_t$ values directly indicate elevated hallucination likelihood.

### B. Signal 2: Attention Anomaly Score (AAS)
When generating ungrounded tokens, LLMs frequently detach their attention focus from the input context tokens $C$ and diffuse attention uniformly across past generated tokens [9]. Let $\alpha_{t, j}^{(h, L)}$ denote the attention weight from generated token $y_t$ to token $j \in \{1, \dots, M\}$ across attention head $h$ in layer $L$. The normalized context attention distribution is:
$$p_t^{(h, L)}(j) = \frac{\alpha_{t, j}^{(h, L)}}{\sum_{k=1}^M \alpha_{t, k}^{(h, L)}}$$
We compute the normalized Shannon entropy across heads:
$$\text{AAS}_t = \frac{1}{|H|} \sum_{h \in H} \left( -\frac{1}{\log M} \sum_{j=1}^M p_t^{(h, L)}(j) \log \left( p_t^{(h, L)}(j) + \epsilon \right) \right)$$
where $\epsilon = 10^{-12}$ ensures numerical stability. An elevated $\text{AAS}_t \to 1.0$ flags anomalous attention dispersion over the prompt.

### C. Signal 3: Entropy-Energy Monitor (EEM)
Output logit distributions convey critical predictive uncertainty [25]. EEM computes a complementary formulation combining Shannon entropy $H(p_t)$ and Rényi-2 confidence $H_2(p_t)$:
$$H(p_t) = -\sum_{v \in V} p_t(v) \log p_t(v)$$
$$H_2(p_t) = -\log \left( \sum_{v \in V} p_t(v)^2 \right)$$
The combined predictive uncertainty metric is:
$$\text{EEM}_t = \beta \cdot \frac{H(p_t)}{\log |V|} + (1 - \beta) \cdot \frac{H_2(p_t)}{\log |V|}$$
with weighting coefficient $\beta = 0.60$, capturing both distribution tail flatness and peak probability collapse.

### D. Signal 4: Distribution Shift Tracker (DST)
Hallucinations often manifest as sudden directional divergence in representation space [10]. DST measures the cosine distance between consecutive residual hidden states at reference layer $L$:
$$\text{DST}_t = 1 - \frac{h_t^L \cdot h_{t-1}^L}{\|h_t^L\|_2 \|h_{t-1}^L\|_2}$$
with boundary condition $\text{DST}_1 = 0$. Sudden transitions in $\text{DST}_t$ isolate semantic disorientation during continuous text generation.

### E. Feature Normalization and Calibrated Multi-Signal Fusion
Raw intrinsic signals inhabit disparate numerical ranges. To prevent scale dominance, TRUEGUARD applies online $Z$-score standardization using Welford's algorithm:
$$\tilde{s}_t^{(i)} = \frac{s_t^{(i)} - \mu_t^{(i)}}{\sigma_t^{(i)} + \epsilon_0}, \quad i \in \{\text{ISP}, \text{AAS}, \text{EEM}, \text{DST}\}$$
For the initial generation steps ($t < 5$), running statistics are stabilized via pre-calibrated empirical Gaussian priors $(\mu_{\text{prior}}, \sigma_{\text{prior}})$, ensuring robust cold-start tracking.

The standardized signals $\tilde{X}_t = [\tilde{s}_t^{(\text{ISP})}, \tilde{s}_t^{(\text{AAS})}, \tilde{s}_t^{(\text{EEM})}, \tilde{s}_t^{(\text{DST})}]^T$ are fused via a calibrated logistic regression head:
$$R(t) = \sigma \left( \sum_{i=1}^4 w_i \tilde{s}_t^{(i)} + b_{\text{fuse}} \right)$$
The optimal learned weights ($w_{\text{EEM}} = 0.34$, $w_{\text{ISP}} = 0.28$, $w_{\text{DST}} = 0.22$, $w_{\text{AAS}} = 0.16$) reflect the balanced contribution of predictive, representational, temporal, and attention modalities.

### F. Closed-Loop Tiered Mitigation Framework
TRUEGUARD enforces sequence-level risk tracking: $R_{\text{seq}} = \max_{1 \le i \le t} R(i)$. If $R_{\text{seq}} > \tau = 0.50$, generation is immediately halted and routed through a two-tier intervention policy:
* **Tier 1: Targeted Retrieval-Augmented Grounding (RAG):** The system queries a local knowledge base (e.g., Wikipedia passages or verified enterprise documents) using the prompt and the pre-hallucination token prefix $y_{<t}$. If relevant documents are retrieved with high similarity ($>0.75$), decoding restarts with retrieved context appended.
* **Tier 2: Calibrated Abstention:** If external knowledge retrieval is unavailable or if the regenerated sequence retains high risk ($R_{\text{seq}} > \tau$), TRUEGUARD outputs a transparent, calibrated disclaimer: *\"I am unable to verify the factual accuracy of this request with sufficient confidence, so I must decline to answer.\"*

![Real-Time Inference and Guardrail Deployment Workflow](fig8_runtime_inference_pipeline.png)
*Fig. 8. Real-time inference and closed-loop guardrail deployment workflow. During autoregressive token generation, TRUEGUARD intercepts internal tensors inline (imposing only $12.4$ ms overhead). If the calibrated risk score $R(t) \le \tau=0.50$, the token is streamed to the user. If risk exceeds $\tau$, generation is halted mid-sentence to execute Tier-1 Targeted RAG or Tier-2 Calibrated Abstention.*


### G. Computational Complexity and Low-Overhead Rationale
A key design objective of TRUEGUARD is minimal runtime overhead. At each token step:
* **ISP:** Involves a single dot product of size $d = 4096$, requiring $2d \approx 8.2 \times 10^3$ FLOPs.
* **AAS:** Evaluates Shannon entropy over prompt length $M$ across 32 attention heads, requiring $\mathcal{O}(|H| \cdot M) \approx 1.6 \times 10^4$ operations for $M = 512$.
* **EEM:** Computes top-$k$ logit entropy on the existing softmax distribution in $\mathcal{O}(k)$ operations ($k = 100$).
* **DST:** Computes one dot product between vectors of dimension $d$, requiring $2d$ FLOPs.
* **Fusion:** Evaluates a 4-dimensional linear combination in $<0.07$ ms.

The total extraction and fusion budget per token requires less than $5 \times 10^4$ FLOPs---representing less than 0.05% of the compute required for a single transformer forward pass ($\sim 1.4 \times 10^{10}$ FLOPs for a 7B model).

---

## V. Experimental Setup and Benchmarks

### A. Benchmark Datasets and Data Provenance
To address reviewer inquiries regarding data provenance and comparability with prior literature, all evaluation benchmarks in this work were obtained directly from publicly accessible, peer-reviewed repositories hosted on Hugging Face Datasets and Stanford CRFM:
1. **TruthfulQA** [42]: Developed by Lin et al. (ACL 2022) and hosted on the official Hugging Face repository [`truthfulqa`](https://huggingface.co/datasets/truthfulqa) and author GitHub repository ([sylin-42/TruthfulQA](https://github.com/sylin-42/TruthfulQA)). TruthfulQA contains 817 questions across 38 categories designed to elicit human false beliefs. In prior literature (e.g., Azaria and Mitchell [20], Su et al. [7]), each prompt is paired with human-curated factual and imitation-hallucination completions. We adopt this exact standardized formulation, allowing direct cross-study comparability.
2. **HaluEval** [22]: Introduced by Li et al. (EMNLP 2023) and available via Hugging Face ([`pminervini/HaluEval`](https://huggingface.co/datasets/pminervini/HaluEval)) and Tsinghua University ([RUCAIBox/HaluEval](https://github.com/RUCAIBox/HaluEval)). HaluEval provides 30,000 paired instances where model generations are contrastively labeled by human annotators as either factually faithful or containing hallucinated entities across three sub-domains:
   * *HaluEval-QA:* 10,000 question-answer pairs evaluating entity and factual accuracy.
   * *HaluEval-Summarization:* 10,000 document-summary pairs testing hallucinated entity insertions.
   * *HaluEval-Dialogue:* 10,000 dialogue turns testing conversational consistency.
   Prior works (e.g., Zhang et al. [8], Dasgupta et al. [10]) utilize these exact splits as ground-truth baselines for AUROC evaluation.
3. **HELM (Holistic Evaluation of Language Models)** [23]: Formulated by Liang et al. (Stanford CRFM, [https://crfm.stanford.edu/helm/](https://crfm.stanford.edu/helm/)), providing standardized multi-step reasoning and knowledge retrieval tasks with verifiable ground truths.

All datasets were obtained under permissive open-source licenses (TruthfulQA: Apache-2.0; HaluEval: MIT; HELM: Apache-2.0). No private, proprietary, or synthetic unverified data was collected.

### B. Base Language Models and Computing Environment
Experiments were conducted across multiple open-source causal language models:
* **Primary Evaluation Models:** LLaMA-2-7B-Chat [43] and Mistral-7B-Instruct-v0.2 [44] (32 transformer layers, 4096 hidden dimension, 32 attention heads).
* **Lightweight Validation Model:** TinyLlama-1.1B-Chat [45] (22 layers, 2048 hidden dimension, 32 heads).
* **CPU Smoke-Test Baseline:** GPT-2 (12 layers, 768 hidden dimension).

Hardware platforms included an NVIDIA T4 GPU (16 GB VRAM) and standard 8-core CPU workstations to confirm platform portability.

### C. Probe Training and Model Calibration via Hugging Face
A central operational advantage of TRUEGUARD is that **the base language model is never retrained or modified.** Rather than incurring the prohibitive cost of fine-tuning multi-billion parameter LLMs, TRUEGUARD extracts diagnostic features from the frozen network and trains only lightweight linear probes:
1. **Dataset Ingestion:** Datasets from prior benchmarks are ingested via the Hugging Face API. Each sample consists of a prompt context $C$ and an associated response labeled as factual ($y = 0$) or hallucinated ($y = 1$) by the benchmark authors.
2. **Activation Capture via Forward Hooks:** The base model is loaded in 16-bit precision using Hugging Face `AutoModelForCausalLM.from_pretrained` with model weights frozen (`requires_grad = False`). PyTorch forward hooks are registered on intermediate transformer blocks ($L \in \{16, 24\}$ for 32-layer models). When benchmark samples pass through the model, the hooks capture the residual hidden state vector $h_t^L \in \mathbb{R}^{4096}$ and multi-head attention weights without executing additional forward passes.
3. **Probe and Fusion Calibration:** Across 5-fold cross-validation, a calibration subset of 200 samples is used to optimize:
   * The linear classification probe weight vector $w_{\text{probe}} \in \mathbb{R}^{4096}$ and bias $b$ for the ISP module via standard cross-entropy loss;
   * The 4-dimensional logistic regression fusion head weights $[w_{\text{EEM}}, w_{\text{ISP}}, w_{\text{DST}}, w_{\text{AAS}}]$ via L-BFGS optimization.
4. **Training Efficiency and Accessibility:** Because the total number of optimized parameters is under 4,100, probe calibration completes in **less than 15 minutes** on a single consumer GPU or free-tier Google Colab instance. Any researcher can reproduce the full training and calibration pipeline directly from our Hugging Face and GitHub repository without requiring cloud computing clusters.

![Dataset Ingestion and Probe Calibration Pipeline](fig7_dataset_training_pipeline.png)
*Fig. 7. Systematic workflow of dataset ingestion, activation extraction, and probe calibration in TRUEGUARD. Datasets established by prior literature (TruthfulQA, HaluEval, HELM) are ingested via Hugging Face. Forward hooks on intermediate transformer blocks intercept internal activations from the frozen base model, enabling complete probe and fusion calibration in under 15 minutes on a single GPU.*



### D. Comparative Baseline Methods
We benchmark TRUEGUARD against five representative baselines:
* **Token Entropy (Black-Box):** Standard predictive Shannon entropy of the output logit distribution.
* **Semantic Entropy [6]:** Multi-sample clustering baseline generating 5 to 10 stochastic completions per prompt.
* **MIND [7]:** Unsupervised probing of internal layer hidden states.
* **LLM-Check [15]:** Single-pass hidden state classifier.
* **HaluShift [10]:** Single-signal distribution shift tracker monitoring cosine state distance.

### E. Evaluation Metrics
Detection performance is evaluated using Area Under the Receiver Operating Characteristic Curve (AUROC), Area Under the Precision-Recall Curve (AUPRC), F1 Score, and False Positive Rate (FPR). All AUROC values are reported via 5-fold cross-validation, including standard deviations and 95% confidence intervals:
$$\text{CI}_{95\%} = \bar{x} \pm 1.96 \cdot \frac{s}{\sqrt{k}}$$
where $k = 5$ denotes cross-validation folds.

Mitigation effectiveness is measured via relative hallucination reduction:
$$\text{Reduction (\%)} = \frac{\text{Rate}_{\text{before}} - \text{Rate}_{\text{after}}}{\text{Rate}_{\text{before}}} \times 100\%$$
and query answer coverage (the percentage of queries successfully answered without triggering abstention).

---

## VI. Results and Empirical Analysis

### A. Comparative Hallucination Detection Accuracy
Table I presents cross-validation results across all five benchmarks. TRUEGUARD achieves an average AUROC of $0.8821 \pm 0.0170$. On TruthfulQA, TRUEGUARD achieves an AUROC of $0.8533 \pm 0.0533$ (95% CI: $[0.8066, 0.9001]$), substantially outperforming Token Entropy ($0.712$) and Semantic Entropy ($0.776$).

#### TABLE I: Cross-Validation Performance Across Benchmarks (5-Fold CV)
| Benchmark | AUROC | 95% Confidence Interval | AUPRC | F1 Score |
| :--- | :---: | :---: | :---: | :---: |
| TruthfulQA | $0.8533 \pm 0.0533$ | $[0.8066, 0.9001]$ | 0.8312 | 0.7945 |
| HaluEval-QA | $0.8742 \pm 0.0418$ | $[0.8375, 0.9108]$ | 0.8520 | 0.8124 |
| HaluEval-Summ | $0.8860 \pm 0.0385$ | $[0.8522, 0.9197]$ | 0.8674 | 0.8290 |
| HaluEval-Dial | $0.8915 \pm 0.0312$ | $[0.8642, 0.9189]$ | 0.8755 | 0.8388 |
| HELM | $0.9056 \pm 0.0264$ | $[0.8825, 0.9287]$ | 0.8910 | 0.8530 |
| **Average** | $\mathbf{0.8821 \pm 0.0170}$ | $[\mathbf{0.8672, 0.8970}]$ | **0.8634** | **0.8255** |

![Comparative AUROC Performance](fig2_auroc_benchmark_comparison.png)
*Fig. 2. Comparative AUROC performance across benchmarks. TRUEGUARD consistently outperforms Token Entropy, Semantic Entropy, MIND, LLM-Check, and HaluShift.*

Fig. 2 illustrates that single-signal baselines exhibit significant variance across tasks. For example, while MIND performs well on TruthfulQA ($0.812$), its performance declines on HaluEval-Dialogue ($0.768$). By fusing all four signals, TRUEGUARD maintains superior performance across all benchmarks.

### B. Ablation Study: Signal Contribution Analysis
To determine the necessity of each intrinsic signal, we performed systematic leave-one-out and single-signal ablations, summarized in Table II and Fig. 3.

#### TABLE II: Signal Ablation Study (TruthfulQA Benchmark)
| Configuration | AUROC | $\Delta$ AUROC | F1 Score |
| :--- | :---: | :---: | :---: |
| **Full TRUEGUARD (All 4 Signals)** | $\mathbf{0.8533}$ | **---** | $\mathbf{0.7945}$ |
| w/o Attention Anomaly Score (AAS) | 0.8190 | $-0.0343$ | 0.7620 |
| w/o Internal State Probes (ISP) | 0.7940 | $-0.0593$ | 0.7380 |
| w/o Distribution Shift Tracker (DST) | 0.8060 | $-0.0473$ | 0.7510 |
| w/o Entropy-Energy Monitor (EEM) | 0.7710 | $-0.0823$ | 0.7190 |
| Single Signal: AAS Only | 0.7180 | $-0.1353$ | 0.6650 |
| Single Signal: ISP Only | 0.7850 | $-0.0683$ | 0.7310 |
| Single Signal: DST Only | 0.7420 | $-0.1113$ | 0.6920 |
| Single Signal: EEM Only | 0.7910 | $-0.0623$ | 0.7390 |

![Signal Ablation Analysis](fig3_ablation_study.png)
*Fig. 3. Signal ablation analysis demonstrating performance drops when individual signals are removed.*

Removing EEM produces the largest performance decline ($\Delta = -0.0823$), underscoring the importance of output predictive confidence. Removing ISP decreases AUROC by $0.0593$, proving that internal representations encode truthfulness dimensions absent from output logits. Removing DST ($\Delta = -0.0473$) and AAS ($\Delta = -0.0343$) further degrades accuracy. The complete 4-signal configuration yields a statistically significant improvement ($p < 0.01$, paired $t$-test) over every ablated variant.

### C. Runtime Latency and Computational Overhead
Table III reports latency measurements conducted on an NVIDIA T4 GPU across 1,000 generated tokens.

#### TABLE III: Latency Breakdown and Efficiency Comparison
| Approach | Extraction Mechanism | Latency (ms/token) | Relative Speedup |
| :--- | :--- | :---: | :---: |
| Standard Decoding | Base forward pass | $28.5 \pm 0.8$ | $1.0\times$ |
| Semantic Entropy [6] | 10 samples (black-box) | $142.3 \pm 4.2$ | $0.2\times$ |
| SelfCheckGPT [5] | Multi-pass sampling | $168.0 \pm 5.5$ | $0.17\times$ |
| TRUEGUARD (ISP) | Layer 16/24 probe | $3.1 \pm 0.2$ | --- |
| TRUEGUARD (AAS) | Attention entropy | $4.2 \pm 0.3$ | --- |
| TRUEGUARD (EEM) | Logit uncertainty | $2.8 \pm 0.1$ | --- |
| TRUEGUARD (DST) | Cosine distance | $2.2 \pm 0.1$ | --- |
| TRUEGUARD (Fusion) | Logistic regression | $0.07 \pm 0.01$ | --- |
| **Total TRUEGUARD** | **Fused 4-signal** | $\mathbf{12.4 \pm 0.5}$ | $\mathbf{11.5\times}$ |

TRUEGUARD incurs a total overhead of $12.4 \pm 0.5$ ms/token, delivering an **11.5$\times$ speedup** over Semantic Entropy ($142.3$ ms/token), as detailed in Table III. The four intrinsic signals collectively require less than $5 \times 10^4$ FLOPs per token---under 0.05% of a single transformer forward pass---placing TRUEGUARD in the optimal operating point that combines high detection accuracy ($>0.88$ AUROC) with streaming-compatible inference latency.

### D. Closed-Loop Mitigation and Quality Retention
To validate active mitigation, we conducted a double-blind human evaluation on 300 randomly sampled responses from TruthfulQA and HaluEval-QA, annotated by three independent NLP specialists (Cohen's inter-annotator agreement $\kappa = 0.82$).

#### TABLE IV: Mitigation Performance (Double-Blind Evaluation, $n=300$)
| Metric | Unmitigated Baseline | With TRUEGUARD | Relative Change |
| :--- | :---: | :---: | :---: |
| Hallucination Rate (%) | 31.2% | **11.3%** | $\mathbf{-63.8\%}$ |
| Factual Precision (%) | 68.8% | **88.7%** | $+28.9\%$ |
| Answer Coverage (%) | 100.0% | 88.0% | $-12.0\%$ |
| Perplexity (Retained) | 14.2 | 14.6 | $+2.8\%$ |

As shown in Table IV, TRUEGUARD reduces hallucination frequency from 31.2% to 11.3%---a **63.8% relative reduction**. Of the flagged responses, Tier-1 RAG successfully resolved 58.4% of queries with grounded context, while Tier-2 calibrated abstention was exercised on the remaining 12.0% of flagged queries, preserving high overall answer utility.

### E. Token-Level Risk Localization and Trajectory Analysis
To qualitatively demonstrate inline risk tracking, we trace TRUEGUARD's per-token risk scores during generation of the prompt: *"Who walked on Mars in 1965?"*. During initial context processing (tokens 1--4), all four signals remain in the safe range ($R(t) \approx 0.11$--$0.21$). Upon generating the fictitious entity *"Soviet astronaut Alexei Leonov"* at token step 6, predictive uncertainty (EEM) spikes to $0.88$, attention entropy (AAS) increases to $0.74$, distribution drift (DST) rises to $0.65$, and the fused risk score reaches $0.83 > \tau = 0.50$. TRUEGUARD halts generation immediately at token step 6, preventing the fabrication from completing. This trace demonstrates that the four-signal architecture achieves fine-grained, per-token interpretability that is absent from black-box multi-sample methods.

---

## VII. Discussion and Practical Considerations

### A. Orthogonality and Complementarity of Intrinsic Signals
Our experimental findings demonstrate that hallucinations are multidimensional phenomena that cannot be captured by any single metric:
* **EEM** acts as the primary detector for output vocabulary uncertainty;
* **ISP** identifies latent truthfulness discrepancies in intermediate representations;
* **AAS** isolates instances where the model loses focus on prompt constraints;
* **DST** tracks progressive temporal divergence from the factual trajectory.

Because these signals examine distinct mathematical subspaces of the transformer forward pass, linear fusion achieves robust cross-domain generalization.

### B. Production and Edge Deployment Feasibility
TRUEGUARD requires no auxiliary large model calls, vector databases for detection, or GPU cluster re-computation. With an extraction footprint of under $5 \times 10^4$ FLOPs per token, TRUEGUARD can be compiled directly into standard inference runtimes (e.g., vLLM, TensorRT-LLM, or ONNX Runtime) to serve production edge environments.

### C. Limitations and Ethical Considerations
While calibrated abstention mitigates factual errors, setting overly conservative thresholds ($\tau < 0.35$) increases abstention rates and reduces system helpfulness. In production, systems must maintain transparency by clearly notifying users whether responses were grounded via Tier-1 RAG or altered via Tier-2 Abstention.

---

## VIII. Conclusion and Future Work
In this paper, we introduced TRUEGUARD, a lightweight, real-time framework for hallucination detection and mitigation in LLMs. By extracting four orthogonal intrinsic signals (ISP, AAS, EEM, DST) within a single forward pass and fusing them via calibrated logistic regression, TRUEGUARD achieves an average AUROC of $0.8821 \pm 0.0170$ with only $12.4 \pm 0.5$ ms/token latency overhead---an 11.5$\times$ speedup over multi-sample Semantic Entropy. Active closed-loop mitigation achieves a 63.8% relative reduction in hallucinations while maintaining an 88.0% query answer coverage. Complete reproducible source code, Colab notebooks, and evaluation harnesses are openly accessible at https://github.com/yogeshravi19/trueguard. Future research includes extending probe calibration to multilingual representations and multi-agent collaborative workflows.

---

## Acknowledgment
The authors express their gratitude to the School of Computer Science and Engineering at Vellore Institute of Technology, Chennai, for providing computational infrastructure and academic support.

---

## References

[1] Huang, Yue et al., "Trustllm: Trustworthiness in large language models," *arXiv preprint arXiv:2401.05561*, 2024.

[2] Zhang, Yue et al., "Siren's Song in the AI Ocean: A Survey on Hallucination in Large Language Models," *Computational Linguistics*, vol. 51, no. 4, pp. 1373–1418, 2025.

[3] Ji, Ziwei et al., "Survey of hallucination in natural language generation," *ACM computing surveys*, vol. 55, no. 12, pp. 1–38, 2023.

[4] Min, Sewon et al., "Factscore: Fine-grained atomic evaluation of factual precision in long form text generation," *Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing*, pp. 12076–12100, 2023.

[5] Manakul, Potsawee, Liusie, Adian, Gales, Mark, "Selfcheckgpt: Zero-resource black-box hallucination detection for generative large language models," *Proceedings of the 2023 conference on empirical methods in natural language processing*, pp. 9004–9017, 2023.

[6] Han, Jiatong et al., "Semantic entropy probes: Robust and cheap hallucination detection in llms," *ICML 2024 Workshop on Foundation Models in the Wild*, 2024.

[7] Su, Weijia et al., "Unsupervised real-time hallucination detection based on the internal states of large language models," *Findings of the Association for Computational Linguistics: ACL 2024*, pp. 14379–14391, 2024.

[8] Zhang, Liang et al., "Detecting hallucination in large language models through deep internal representation analysis," *Proceedings of the Thirty-Fourth International Joint Conference on Artificial Intelligence, IJCAI-25*, pp. 8357–8365, 2025.

[9] Hajji, El Mahdi, Bouguerra, Abdelhak, Arnez, Fabio, "The Map of Misbelief: Tracing Intrinsic and Extrinsic Hallucinations Through Attention Patterns," *Proceedings of the AAAI Symposium Series*, vol. 7, no. 1, pp. 177–184, 2025.

[10] Dasgupta, Sourav et al., "Hallushift: Measuring distribution shifts towards hallucination detection in llms," *2025 International Joint Conference on Neural Networks (IJCNN)*, pp. 1–8, 2025.

[11] M{\"u}ndler, Niels et al., "Self-contradictory hallucinations of large language models: Evaluation, detection and mitigation," *arXiv preprint arXiv:2305.15852*, 2023.

[12] Kang, Sungmin et al., "Uncertainty quantification for hallucination detection in large language models: Foundations, methodology, and future directions," *arXiv preprint arXiv:2510.12040*, 2025.

[13] Herrera, Francisco, "Making sense of the unsensible: Reflection, survey, and challenges for xai in large language models toward human-centered ai," *arXiv preprint arXiv:2505.20305*, 2025.

[14] Chern, I et al., "FacTool: Factuality Detection in Generative AI--A Tool Augmented Framework for Multi-Task and Multi-Domain Scenarios," *arXiv preprint arXiv:2307.13528*, 2023.

[15] Sriramanan, Gaurang et al., "Llm-check: Investigating detection of hallucinations in large language models," *Advances in Neural Information Processing Systems*, vol. 37, pp. 34188–34216, 2024.

[16] Nath, Sourav et al., "HalluShift++: Bridging Language and Vision through Internal Representation Shifts for Hierarchical Hallucinations in MLLMs," *arXiv preprint arXiv:2512.07687*, 2025.

[17] Lewis, Patrick et al., "Retrieval-augmented generation for knowledge-intensive nlp tasks," *Advances in neural information processing systems*, vol. 33, pp. 9459–9474, 2020.

[18] Asai, Akari et al., "Self-rag: Learning to retrieve, generate, and critique through self-reflection," *The Twelfth International Conference on Learning Representations*, 2023.

[19] Dhuliawala, Shehzaad et al., "Chain-of-verification reduces hallucination in large language models," *Findings of the association for computational linguistics: ACL 2024*, pp. 3563–3578, 2024.

[20] Azaria, Amos, Mitchell, Tom, "The internal state of an LLM knows when it's lying," *Findings of the Association for Computational Linguistics: EMNLP 2023*, pp. 967–976, 2023.

[21] Bang, Yejin et al., "A multitask, multilingual, multimodal evaluation of chatgpt on reasoning, hallucination, and interactivity," *Proceedings of the 13th international joint conference on natural language processing and the 3rd conference of the asia-pacific chapter of the association for computational linguistics (volume 1: Long papers)*, pp. 675–718, 2023.

[22] Li, Junyi et al., "Halueval: A large-scale hallucination evaluation benchmark for large language models," *Proceedings of the 2023 conference on empirical methods in natural language processing*, pp. 6449–6464, 2023.

[23] Liang, Percy et al., "Holistic evaluation of language models," *arXiv preprint arXiv:2211.09110*, 2022.

[24] Chen, Zhongxi et al., "Truth forest: Toward multi-scale truthfulness in large language models through intervention without tuning," *Proceedings of the AAAI Conference on Artificial Intelligence*, vol. 38, no. 19, pp. 20967–20974, 2024.

[25] Ma, Hao et al., "Semantic energy: Detecting llm hallucination beyond entropy," *arXiv preprint arXiv:2508.14496*, 2025.

[26] Jing, Xinye, Billa, Sravanthi, Godbout, David, "On a scale from 1 to 5: quantifying hallucination in faithfulness evaluation," *Findings of the Association for Computational Linguistics: NAACL 2025*, pp. 7765–7780, 2025.

[27] Vazhentsev, Artem et al., "Uncertainty-aware attention heads: Efficient unsupervised uncertainty quantification for LLMs," *arXiv preprint arXiv:2505.20045*, 2025.

[28] Wu, Jiaan et al., "Mitigating LLM Hallucination via Behaviorally Calibrated Reinforcement Learning," *arXiv preprint arXiv:2512.19920*, 2025.

[29] Moslonka, Clement et al., "Learned hallucination detection in black-box llms using token-level entropy production rate," *arXiv preprint arXiv:2509.04492*, 2025.

[30] Nie, Shen et al., "Stop Rewarding Hallucinated Steps: Faithfulness-Aware Step-Level Reinforcement Learning for Small Reasoning Models," *arXiv preprint arXiv:2602.05897*, 2026.

[31] Sharma, Mrinank et al., "Why would you suggest that? human trust in language model responses," *arXiv preprint arXiv:2406.02018*, 2024.

[32] Yao, Shunyu et al., "ExpandR: Learning to teach high density retrievers outside query guided," *Preprint*, 2025.

[33] Gao, Luyu et al., "Rarr: Researching and revising what language models say, using language models," *Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pp. 16477–16508, 2023.

[34] Li, Kenneth et al., "Inference-time intervention: Eliciting truthful answers from a language model," *Advances in Neural Information Processing Systems*, vol. 36, pp. 41451–41530, 2023.

[35] Wei, Jason et al., "Chain-of-thought prompting elicits reasoning in large language models," *Advances in neural information processing systems*, vol. 35, pp. 24824–24837, 2022.

[36] Du, Yilun et al., "Improving factuality and reasoning in language models through multiagent debate," *Forty-first international conference on machine learning*, 2024.

[37] Yin, Shukang et al., "Woodpecker: Hallucination correction for multimodal large language models," *Science China Information Sciences*, vol. 67, no. 12, pp. 220105, 2024.

[38] Gou, Zhibin et al., "Critic: Large language models can self-correct with tool-interactive critiquing," *arXiv preprint arXiv:2305.11738*, 2023.

[39] Agrawal, Garima et al., "Can knowledge graphs reduce hallucinations in llms?: A survey," *Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers)*, pp. 3947–3960, 2024.

[40] Luo, Haowei et al., "Chatkbqa: A generate-then-retrieve framework for knowledge base question answering with fine-tuned large language models," *Findings of the association for computational linguistics: ACL 2024*, pp. 2039–2056, 2024.

[41] Bai, Yuntao et al., "Training a helpful and harmless assistant with reinforcement learning from human feedback," *arXiv preprint arXiv:2204.05862*, 2022.

[42] Lin, Stephanie, Hilton, Jacob, Evans, Owain, "TruthfulQA: Measuring how models mimic human falsehoods," *Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*, pp. 3214–3252, 2022.

[43] Touvron, Hugo et al., "Llama 2: Open foundation and fine-tuned chat models," *arXiv preprint arXiv:2307.09288*, 2023.

[44] Jiang, Albert Q et al., "Mistral 7B," *arXiv preprint arXiv:2310.06825*, 2023.

[45] Zhang, Peiyuan et al., "TinyLlama: An open-source small language model," *arXiv preprint arXiv:2401.02385*, 2024.
