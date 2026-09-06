# TRUEGUARD: A Lightweight Real-Time Framework for Hallucination Detection and Mitigation in Large Language Models

**Yogesh Ravi M$^1$ and T. S. Pradeep Kumar$^2$**  
*School of Computer Science and Engineering, Vellore Institute of Technology, Chennai 600127, India*  
Emails: `yogeshravi.m2022@vitstudent.ac.in`, `pradeepkumar.ts@vit.ac.in`  

---

### Abstract
Large Language Models (LLMs) frequently generate fluent yet factually unfounded statements---a phenomenon known as hallucination. Existing detection approaches generally mandate either multi-sample semantic consistency checks (which require 5–10 stochastic forward passes and introduce $\sim$142.3 ms/token overhead) or isolated single-signal white-box metrics that fail to capture heterogeneous hallucination modes. In this paper, we propose **TRUEGUARD**, an inline, multi-signal framework that monitors autoregressive generation in a single forward pass without disrupting standard decoding. TRUEGUARD extracts four complementary intrinsic signals at each decoding step: Internal State Probes (ISP), Attention Anomaly Score (AAS), Entropy-Energy Monitor (EEM), and Distribution Shift Tracker (DST). These signals are dynamically standardized via online $Z$-score normalization and fused through a learned logistic regression layer to produce a calibrated token-level risk score $R(t)$. When the sequence risk exceeds a calibrated safety threshold ($\tau = 0.50$), TRUEGUARD triggers an active closed-loop mitigation pipeline incorporating targeted Retrieval-Augmented Grounding (RAG) and calibrated abstention. Evaluated across five benchmark distributions (TruthfulQA, HaluEval-QA, HaluEval-Summ, HaluEval-Dial, and HELM), TRUEGUARD achieves an average AUROC of $0.8821 \pm 0.0170$ (with $0.8533 \pm 0.0533$ on TruthfulQA) while imposing merely $12.4 \pm 0.5$ ms/token latency overhead---an 11.5$\times$ speedup over Semantic Entropy. In human-annotated mitigation evaluations ($n = 300$, Cohen’s $\kappa = 0.82$), TRUEGUARD achieves a 63.8% relative reduction in hallucination occurrence while maintaining an 88.0% query answer coverage. Complete reproducible code, Colab notebooks, and evaluation harnesses are available at [https://github.com/yogeshravi19/trueguard](https://github.com/yogeshravi19/trueguard).

**Index Terms:** Large Language Models, Hallucination Detection, Trustworthy AI, Real-Time Inference, Uncertainty Quantification, Active Mitigation, Explainable AI.

---

## I. Introduction

Large Language Models (LLMs) such as GPT-4, LLaMA, and Mistral have demonstrated remarkable empirical capabilities in language generation, reasoning, and synthesis. Despite their widespread adoption across diverse software environments, their deployment in safety-critical domains---including healthcare, legal informatics, and automated financial analysis---remains severely constrained by their propensity to hallucinate. Hallucinations occur when an LLM produces outputs that appear syntactically coherent and contextually plausible but are factually false, unfaithful to the prompt context, or logically contradictory.

Prior research in hallucination detection has largely pursued two contrasting design philosophies:
1. **Black-Box Multi-Sample Consistency Checks:** Methods such as SelfCheckGPT and Semantic Entropy sample multiple stochastic completions per prompt and evaluate their semantic variance. While these methods achieve reliable detection accuracy, generating multiple responses consumes significant memory bandwidth and compute time (incurring $\sim$142.3 ms/token overhead), making them impractical for low-latency streaming applications.
2. **Single-Signal White-Box Probes:** To bypass multi-pass latency, recent works monitor internal model activations in a single forward pass. Representative examples include internal representation probes (MIND, MHAD), attention pattern tracking, semantic energy logits analysis, and distribution shift trackers like HaluShift. However, individual internal signals typically capture only specific facets of uncertainty. As empirical studies demonstrate, attention dispersion effectively flags intrinsic contradictions against context tokens but often misses extrinsic fabrications, whereas predictive output entropy exhibits the inverse behavior.

Furthermore, a persistent disconnect exists between detection engines and downstream intervention: most systems operate as post-hoc diagnostic monitors rather than active mitigation controllers.

To resolve these limitations, we introduce **TRUEGUARD**, a lightweight, real-time framework that unifies multi-signal intrinsic uncertainty tracking, learned signal fusion, token-level explainability, and active closed-loop mitigation within a single forward pass.

---

## II. Related Work

### A. Hallucination Categorization and Taxonomies
Hallucinations in natural language generation are systematically classified along two major axes: *intrinsic* and *extrinsic*. Intrinsic hallucinations directly contradict the provided source context or user prompt. Extrinsic hallucinations introduce unverifiable or fabricated assertions absent from both the context and global world knowledge. TrustLLM demonstrated that hallucination frequency correlates inversely with model parameter scale, yet remains pervasive even in state-of-the-art architectures.

### B. White-Box Activation and Uncertainty Probing
Recent research demonstrates that an LLM's internal activations contain latent representations indicative of truthfulness and confidence. MIND introduced unsupervised probing of internal layer hidden states. MHAD showed that truthfulness awareness is concentrated in specific intermediate transformer layers. Concurrently, Semantic Entropy Probes (SEPs) approximate semantic entropy directly from hidden states in a single forward pass. In the predictive domain, Semantic Energy measures raw logit confidence through a Boltzmann-inspired formulation, while HaluShift measures distribution shift via cosine distance. In attention analysis, Hajji et al. mapped hallucination traces through attention entropy.

### C. Inference-Time Mitigation
Addressing hallucinations after full sequence generation introduces substantial latency. Chain-of-Verification and RARR generate auxiliary verification queries, multiplying overall inference time. Universal Retrieval-Augmented Generation (RAG) grounds generation in external knowledge bases, but universal retrieval on every query introduces redundant overhead. In contrast, calibrated abstention trains models to recognize empirical uncertainty bounds and decline answering when confidence is low. TRUEGUARD synthesizes these insights by deploying targeted RAG and calibrated abstention conditionally based on real-time token risk.

---

## III. Problem Formulation

Let an autoregressive language model $\mathcal{M}$ generate a sequence of output tokens $Y = (y_1, y_2, \dots, y_T)$ given an input prompt context $C = (c_1, c_2, \dots, c_M)$. At generation step $t \in \{1, \dots, T\}$, the model performs a forward pass:
$$p(y_t \mid C, y_{<t}) = \text{softmax}(z_t)$$
where $z_t \in \mathbb{R}^{|V|}$ denotes the output logit vector over vocabulary $V$. Concurrent with logit computation, the model produces residual hidden representations $\{h_t^L\}_{L=1}^{N_L}$ and multi-head attention matrices $\{A_t^L\}_{L=1}^{N_L}$, where $N_L$ is the total number of transformer layers.

The objective of real-time hallucination detection is to learn an inline mapping:
$$f: (z_t, \{h_t^L\}, \{A_t^L\}) \mapsto R(t) \in [0, 1]$$
such that $R(t)$ accurately reflects the probability that token $y_t$ initiates or constitutes a factual hallucination, evaluated with minimal latency overhead $\Delta t \ll t_{\text{forward}}$.

---

## IV. The TRUEGUARD Framework

```
Prompt C ──► [ LLM Forward Pass ] ──► (h_t^L, A_t, z_t)
                    │
   ┌────────────────┼────────────────┬────────────────┐
   ▼                ▼                ▼                ▼
 [ISP]            [AAS]            [EEM]            [DST]
Hidden State    Attention        Entropy-Energy   Distribution
 Probes          Anomaly          Monitor          Shift Tracker
   │                │                │                │
   └────────────────┴────────┬───────┴────────────────┘
                             ▼
              Online Z-Score Normalization
                             ▼
              Learned Logistic Regression: R(t) = σ(W^T X̂_t + b)
                             ▼
                    [ Risk Decision ]
                   /                 \
        R(t) ≤ 0.50                   R(t) > 0.50
     [ Safe Emission ]             [ Active Mitigation ]
                                   /                   \
                        Tier 1: Targeted RAG     Tier 2: Abstention
```

### A. Signal 1: Internal State Probes (ISP)
Truthfulness-related information is concentrated in middle-to-late transformer layers ($L_{\text{isp}} = \{15, 20, 25, 30\}$ for 32-layer models). For each layer $L \in L_{\text{isp}}$, a linear classification probe projects the hidden state $h_t^L \in \mathbb{R}^{d_h}$ to a scalar probability:
$$\text{ISP}_t^L = \sigma(w_L^T h_t^L + b_L)$$
$$\text{ISP}_t = \frac{1}{|L_{\text{isp}}|} \sum_{L \in L_{\text{isp}}} \text{ISP}_t^L$$

### B. Signal 2: Attention Anomaly Score (AAS)
We quantify attention dispersal by computing normalized Shannon entropy over attention weights in the final quartile of layers $L_{\text{aas}} = \{25, 26, \dots, 31\}$:
$$H^{h, L}(t) = -\sum_{i=1}^t A_{t, i}^{h, L} \log(A_{t, i}^{h, L} + \epsilon)$$
$$H_{\text{norm}}^{h, L}(t) = \frac{H^{h, L}(t)}{\log(t)}$$
$$\text{AAS}_t = \frac{1}{|L_{\text{aas}}| \cdot |H|} \sum_{L \in L_{\text{aas}}} \sum_{h=1}^{|H|} H_{\text{norm}}^{h, L}(t)$$

### C. Signal 3: Entropy-Energy Monitor (EEM)
Output token uncertainty combines normalized Shannon entropy with Rényi-2 sharpness:
$$H_{\text{norm}}(t) = \frac{-\sum_{k=1}^{|V|} p_{t, k} \log(p_{t, k} + \epsilon)}{\log(|V|)}$$
$$E_{\text{norm}}(t) = \frac{-\log\left(\sum_{k=1}^{|V|} p_{t, k}^2 + \epsilon\right)}{\log(|V|)}$$
$$\text{EEM}_t = w_e \cdot H_{\text{norm}}(t) + (1 - w_e) \cdot E_{\text{norm}}(t), \quad w_e = 0.6$$

### D. Signal 4: Distribution Shift Tracker (DST)
Semantic drift is tracked via normalized cosine distance of averaged hidden representations:
$$\bar{h}_t = \frac{1}{|L_{\text{dst}}|} \sum_{L \in L_{\text{dst}}} h_t^L, \quad L_{\text{dst}} = \{20, 25, 30\}$$
$$d_t = \frac{1 - \cos(\bar{h}_t, \bar{h}_{t-1})}{2}$$
$$\text{DST}_t = \frac{1}{t-1} \sum_{t'=2}^t d_{t'}$$

### E. Online Normalization and Learned Fusion
Signals are normalized online via running Welford statistics:
$$\hat{X}_t = \frac{X_t - \mu_t}{\sigma_t + \epsilon_s}$$
and fused into token risk:
$$R(t) = \sigma(W^T \hat{X}_t + b)$$
Sequence-level risk incorporates a persistence penalty:
$$R_{\text{seq}} = \min\left(1.0, \, \max_t R(t) \cdot \left[1 + \gamma \cdot \frac{\sum_{t=1}^T \mathbb{I}(R(t) > \tau)}{T}\right]\right)$$

### F. Active Closed-Loop Mitigation
When $R(t) > \tau$ ($\tau = 0.50$), TRUEGUARD triggers:
- **Tier 1 (Targeted RAG):** Key entities are retrieved from verified knowledge bases to regenerate the segment with grounding.
- **Tier 2 (Calibrated Abstention):** If ungrounded or persistent uncertainty remains, emits an honest disclaimer: *"I do not have sufficient verified evidence to answer this query reliably without risk of factual inaccuracy."*

---

## V. Experimental Methodology

- **Models:** LLaMA-2-7B-Chat, Mistral-7B-Instruct-v0.2, TinyLlama-1.1B-Chat, and GPT-2 (CPU verification).
- **Benchmarks:** TruthfulQA (817 questions, 38 categories), HaluEval (QA, Summarization, Dialogue subsets), and HELM.
- **Validation Protocol:** 5-fold cross-validation reporting mean, standard deviation, and 95% confidence intervals.
- **Hardware:** NVIDIA T4 GPU (16 GB VRAM) for GPU reproduction; local CPU workstations for smoke-test validation.

---

## VI. Results and Empirical Analysis

### A. Overall Benchmark Performance
| Benchmark | AUROC | 95% Confidence Interval | AUPRC | F1 Score |
| :--- | :---: | :---: | :---: | :---: |
| **TruthfulQA** | **0.8533 $\pm$ 0.0533** | [0.8066, 0.9001] | 0.8140 | 0.7186 |
| **HaluEval-QA** | **0.8840 $\pm$ 0.0185** | [0.8678, 0.9003] | 0.8739 | 0.7874 |
| **HaluEval-Summ** | **0.8797 $\pm$ 0.0440** | [0.8411, 0.9184] | 0.8459 | 0.7252 |
| **HaluEval-Dial** | **0.8872 $\pm$ 0.0387** | [0.8533, 0.9212] | 0.8484 | 0.7373 |
| **HELM** | **0.9063 $\pm$ 0.0454** | [0.8665, 0.9461] | 0.8552 | 0.7545 |
| **Overall Average** | **0.8821 $\pm$ 0.0170** | --- | **0.8475** | **0.7446** |

### B. Ablation Study
| Configuration | AUROC | Std | $\Delta$ from Full | Key Finding |
| :--- | :---: | :---: | :---: | :--- |
| **Full TRUEGUARD (4 Signals)** | **0.8475** | $\pm$ 0.0324 | **Reference** | **Optimal multi-signal synergy** |
| $- \text{EEM}$ (No Entropy/Energy) | 0.7957 | $\pm$ 0.0316 | $-0.0518$ | Largest single-signal performance drop |
| $- \text{ISP}$ (No Hidden Probes) | 0.8093 | $\pm$ 0.0465 | $-0.0382$ | Hidden states contain critical factual cues |
| $- \text{DST}$ (No Dist. Shift) | 0.8320 | $\pm$ 0.0237 | $-0.0155$ | Prevents temporal cognitive drift |
| $- \text{AAS}$ (No Attention Anomaly) | 0.8370 | $\pm$ 0.0395 | $-0.0105$ | Attention catches context detachment |
| EEM Only | 0.7516 | $\pm$ 0.0395 | $-0.0959$ | Single signal lacks representation cues |
| ISP Only | 0.7445 | $\pm$ 0.0537 | $-0.1030$ | Single probe misses output uncertainty |
| DST Only | 0.6812 | $\pm$ 0.0626 | $-0.1663$ | Temporal shift alone is insufficient |
| AAS Only | 0.6317 | $\pm$ 0.0345 | $-0.2158$ | Attention entropy alone has high variance |

### C. Inference Latency & Speedup
| Method | Passes per Token | Overhead Latency | Speedup vs Semantic Entropy |
| :--- | :---: | :---: | :---: |
| **Semantic Entropy** | 5 to 10 | $142.3 \pm 3.8$ ms | $1.0\times$ (Baseline) |
| **LLM-Check** | 1 | $31.5 \pm 1.2$ ms | $4.5\times$ |
| **HaluShift** | 1 | $18.2 \pm 0.6$ ms | $7.8\times$ |
| **TRUEGUARD (Ours)** | **1** | **$12.4 \pm 0.5$ ms** | **$11.5\times$ faster** |

Component breakdown: ISP ($0.49$ ms), AAS ($1.26$ ms), EEM ($0.47$ ms), DST ($0.26$ ms), Fusion ($0.07$ ms).

### D. Mitigation Effectiveness ($n=300, \kappa=0.82$)
| Stage | Hallucination Rate | Factual Accuracy | Query Coverage |
| :--- | :---: | :---: | :---: |
| Base LLM (No Guard) | 31.2% | 68.8% | 100.0% |
| Detection Flag Only | 31.2% | 68.8% | 100.0% |
| + Targeted RAG (Tier 1) | 18.4% | 79.3% | 100.0% |
| + Calibrated Abstention (Tier 2) | 12.7% | 84.1% | 95.0% |
| **Full TRUEGUARD Closed-Loop** | **11.3%** | **85.6%** | **88.0%** |

Relative Hallucination Reduction:
$$\text{Relative Reduction} = \frac{31.2\% - 11.3\%}{31.2\%} = \mathbf{63.8\%}$$

---

## VII. Discussion & Limitations

TRUEGUARD demonstrates that multi-signal white-box monitoring achieves high hallucination detection accuracy without multi-sample overhead. Open challenges include dependence on white-box model weights, external knowledge base coverage for Tier-1 RAG, and extending calibration to multilingual settings.

---

## VIII. Conclusion

TRUEGUARD unifies four intrinsic model signals (ISP, AAS, EEM, DST) and learned logistic regression fusion into a real-time guard layer. Evaluated across five benchmark distributions, it achieves $0.8821 \pm 0.0170$ AUROC with only $12.4 \pm 0.5$ ms/token latency ($11.5\times$ speedup over Semantic Entropy). Closed-loop mitigation achieves a verified 63.8% relative hallucination reduction while maintaining 88.0% answer coverage, establishing a practical, reproducible foundation for trustworthy LLM inference.
