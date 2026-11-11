# TRUEGUARD: Empirical Implementation and Evaluation of a Closed-Loop Multi-Sensor Hallucination Detection and Three-Tier Mitigation Architecture for Open-Weights LLMs

**Authors:** Yogesh Ravi M, T. S. Pradeep Kumar  
**Affiliation:** School of Computer Science and Engineering, Vellore Institute of Technology (VIT), Chennai, India

---

## Abstract

Open-weights large language models (LLMs) frequently generate fluent but factually incorrect statements ("hallucinations") with high surface confidence. While existing defences either require expensive multi-sample generation (e.g., SelfCheckGPT, Semantic Entropy) or evaluate isolated internal signals without closed-loop actuation, our companion review paper proposed **TRUEGUARD**—a control-theoretic framework that extracts four single-pass internal sensors and routes responses through a two-threshold, three-tier corrective controller. In this paper, we present the complete implementation and rigorous empirical evaluation of TRUEGUARD on real open-weights language models (`TinyLlama-1.1B-Chat-v1.0` and `GPT-2`) across four paired hallucination benchmarks (`HaluEval-QA`, `HaluEval-Dialogue`, `HaluEval-Summarization`, and `TruthfulQA`; $3{,}196$ evaluated responses) and live open-ended question answering on `TriviaQA` ($300$ queries). Under leakage-free 5-fold grouped cross-validation with inner out-of-fold stacking, TRUEGUARD achieves a **macro-average AUROC of $0.935$** ($0.986$ on `HaluEval-Summarization`, $0.975$ on `HaluEval-QA`, $0.903$ on `HaluEval-Dialogue`, and $0.876$ on `TruthfulQA`) with strong probability calibration ($\text{ECE} = 0.024\text{–}0.042$). Leave-one-sensor-out ablations reveal a key empirical insight: supervised **Internal State Probes (ISP)** over middle-to-late hidden layers outperform unsupervised logit entropy, attention anomaly, and representation drift baselines by $+0.188$ to $+0.251$ AUROC on length-matched benchmarks, while the three unsupervised sensors (`AAS`, `EEM`, `DST`) provide a training-free fallback ($0.626\text{–}0.918$ AUROC when `ISP` is removed). On live `TriviaQA` generations, TRUEGUARD attains **$0.795$ detection AUROC**, lowers the hallucination rate among answered queries from **$62.0\%$ to $40.0\%$** ($35.5\%$ relative reduction; $72.0\%$ system-wide reduction), and achieves an Area Under the Risk–Coverage curve of **$\text{AURC} = 0.412$** vs. $0.526$ (Entropy) and $0.603$ (NLL). On an NVIDIA Tesla T4 GPU, TRUEGUARD adds **$2.92\text{ ms/token}$** ($+8.7\%$) in post-pass mode and **$5.81\text{ ms/token}$** in step-by-step online mode—achieving a **$4.31\times\text{–}4.65\times$ speedup** over a 5-sample consistency baseline.

---

## 1. Introduction and Research Questions

Our first paper surveyed 40 hallucination detection and mitigation studies under PRISMA 2020 guidelines and proposed the conceptual TRUEGUARD closed-loop architecture. However, proposing a control architecture leaves open four empirical questions that can only be answered by real model execution:

- **RQ1 (Detection Effectiveness):** What AUROC, F1, and Expected Calibration Error (ECE) does TRUEGUARD achieve when all four sensors are computed from real hidden states, attention matrices, and logits across diverse hallucination benchmarks?
- **RQ2 (Sensor Complementarity vs. Dominance):** How much does each sensor (`ISP`, `AAS`, `EEM`, `DST`) contribute in leave-one-sensor-out ablations, and when do unsupervised logit/attention signals fail compared to supervised hidden-state probes?
- **RQ3 (Cross-Dataset Generalisation):** Does a detector trained on one task transfer zero-shot to other tasks, and why do answer-length/style shifts degrade zero-shot transfer between entity-style QA and sentence-style QA?
- **RQ4 (Closed-Loop Mitigation & Latency):** When coupled to two calibrated thresholds $(\tau_{\text{warning}}, \tau_{\text{fault}})$ and three corrective tiers (re-sampling, targeted Wikipedia retrieval, and calibrated abstention), how much does TRUEGUARD reduce hallucinations on live open-ended generations, and what is its exact GPU latency overhead per token?

### 1.1 Related Work and Comparison with Prior Frameworks

| Study / Framework | Signal Modality | Single-Pass? | Closed-Loop Mitigation? | Primary Limitation | TRUEGUARD v2 Empirical Advancement |
|---|---|---|---|---|---|
| SelfCheckGPT (Manakul et al., 2023) | Multi-sample black-box consistency | No (5–20x) | No | High latency (169.31 ms/tok for 5 samples on T4); passive scoring | Single-pass sensors (36.41–39.30 ms/tok; 4.31x–4.65x faster) + 3-tier mitigation |
| Semantic Entropy & SEPs (Kuhn et al., 2023; Kossen et al., 2024) | Multi-sample entropy / single hidden probe | SEPs: Yes | No | Single-probe SEPs lack multi-layer OOF stacking, fallback signals, and repair | 4-layer OOF-stacked ISP (0.876–0.986 AUROC) + AAS/EEM/DST fallback + 3-tier control |
| MIND (Su et al., 2024) & MHAD (Zhang et al., 2025) | Internal hidden states | Yes | No | Passive detection only; no calibrated warning/fault thresholds | Couples 4-layer ISP to $(\tau_{\text{warning}}, \tau_{\text{fault}})$ and 3-tier closed-loop actuation |
| Semantic Energy (Ma et al., 2024) | Penultimate logit energy & entropy | Yes | No | Surface logit uncertainty fails on fluent misconceptions (EEM = 0.522 on TruthfulQA) | Adds supervised ISP, raising TruthfulQA AUROC from 0.522 to 0.876 (+0.354) |
| LLM-Check (Sriramanan et al., 2024) | Attention + hidden/logit scores | Yes | No | Static scoring without grouped OOF probe stacking or active mitigation | Grouped OOF stacking (0.935 macro AUROC) + per-sensor log-odds attribution + 3 tiers |
| HALLUSHIFT (Dasgupta et al., 2024) | Consecutive-layer cosine drift | Yes | No | Drift alone has moderate power on short answers (DST = 0.533 on TruthfulQA) | Combines DST with ISP, AAS, and EEM inside a calibrated logistic combiner |
| Map of Misbelief (Hajji et al., 2025) & RAUQ (2026) | Attention head entropy / dispersal | Yes | No | Captures context detachment (AAS) but misses extrinsic factual errors | Fuses AAS with ISP and routes faults to Wikipedia retrieval (Tier 2) or abstention (Tier 3) |
| Behaviorally Calibrated RL (Wu et al., 2025) | RL-trained abstention | Yes | Abstention only | Requires RL fine-tuning; abstains without attempting re-sampling or retrieval | Frozen-model controller (`SAFE` -> `TIER1_RESAMPLE` -> `TIER2_RETRIEVAL` -> `TIER3_ABSTAIN`) |

---

## 2. Methodology and Architecture Implementation

### 2.1 Four Single-Pass Internal Sensors (`src/tg_pipeline.py`)

Given a prompt $P$ and generated answer $A = (y_1, \dots, y_T)$ of length $T$ tokens, a single forward pass with `output_hidden_states=True` and `output_attentions=True` (`attn_implementation="eager"`) yields per-layer hidden states $h_{l,t} \in \mathbb{R}^d$, attention weights $A^{(l,h)}_{t,1:s_t}$, and pre-softmax logits $z_t \in \mathbb{R}^{|V|}$:

1. **Internal State Probe (ISP — Supervised State Sensor):** At four fractional layer depths $L = \{\lfloor 0.45 N_L \rfloor, \lfloor 0.60 N_L \rfloor, \lfloor 0.75 N_L \rfloor, \lfloor 0.90 N_L \rfloor\}$ (layers $\{10, 13, 17, 20\}$ for 22-layer `TinyLlama-1.1B`), we compute the answer-mean hidden vector $\bar{h}_l = \frac{1}{T}\sum_{t=1}^T h_{l,t}$ and fit an $L_2$-regularised logistic regression classifier $p_l(y=1\mid\bar{h}_l) = \sigma(w_l^\top \text{Std}(\bar{h}_l) + b_l)$. The aggregate probe score is:
   $$\text{ISP}(P,A) = \frac{1}{|L|}\sum_{l \in L} p_l(y=1\mid\bar{h}_l)$$
2. **Attention Anomaly Score (AAS — Observation Sensor):** Across the final quartile of transformer layers $L_Q = [\lfloor 0.75 N_L \rfloor, N_L)$, we compute the normalised Shannon entropy of each head's causal attention row of length $s_t$:
   $$\text{AAS}_t = \frac{1}{|L_Q|\cdot H}\sum_{l \in L_Q}\sum_{h=1}^H \frac{-\sum_{i=1}^{s_t} A^{(l,h)}_{t,i}\log(A^{(l,h)}_{t,i}+\epsilon)}{\log s_t}$$
   and summarise over the answer via $(\text{AAS}_{\text{mean}}, \text{AAS}_{\text{max}})$.
3. **Entropy–Energy Monitor (EEM — Output Sensor):** Combining normalised Shannon entropy $H_{\text{norm}}(z_t)$ and normalised Rényi-2 quadratic entropy $E_{\text{norm}}(z_t) = \frac{-\log\sum_v p_{t,v}^2}{\log |V|}$ with $w_e = 0.6$:
   $$\text{EEM}_t = w_e H_{\text{norm}}(z_t) + (1 - w_e) E_{\text{norm}}(z_t)$$
   summarised via $(\text{EEM}_{\text{mean}}, \text{EEM}_{\text{max}})$.
4. **Distribution Shift Tracker (DST — Temporal Sensor):** Averaging hidden states across depths $\{0.60, 0.75, 0.90\}\cdot N_L$ into $\tilde{h}_t$, we measure step-to-step cosine distance for $t \ge 2$:
   $$\text{DST}_t = \frac{1 - \cos(\tilde{h}_t, \tilde{h}_{t-1})}{2}$$
   summarised via $(\text{DST}_{\text{mean}}, \text{DST}_{\text{max}})$.

**Equivalence of Online and Teacher-Forced Extraction:** We implement both a single teacher-forced pass (`score_answer`) and a KV-cached token-by-token monitor (`OnlineSignalMonitor`). Unit testing (`tests/test_equivalence.py`) verifies exact numerical agreement ($\max|\Delta F| = 3.49 \times 10^{-6}$, $\max|\Delta H| = 1.53 \times 10^{-5}$).

### 2.2 Leakage-Free Out-of-Fold Stacking and Logistic Fusion

A critical methodological pitfall when combining a high-dimensional linear probe ($d = 2048$) with low-dimensional summary features (`AAS`, `EEM`, `DST`) is **in-sample probe overfitting**: on training rows, an $8{,}192$-parameter probe has near-perfect fit, which would cause a naïve second-stage combiner to assign zero weight to the other sensors. Furthermore, in paired benchmarks where each question has both a grounded (`label=0`) and hallucinated (`label=1`) answer, standard random splitting leaks question context across train and test folds.

We prevent both forms of leakage in `TrueGuardDetector.fit` and `grouped_cv`:

1. **Question-grouped splitting (`GroupKFold`):** Both answers of every question share a group ID and are always placed in the same fold.
2. **Inner grouped CV for probe regularisation:** Inside each outer training fold, $C \in \{0.001, 0.01, 0.1\}$ is selected by inner 5-fold `GroupKFold`.
3. **Out-of-fold (OOF) probe stacking:** The logistic fusion combiner is trained on `[logit(ISP_oof), AAS_mean, AAS_max, EEM_mean, EEM_max, DST_mean, DST_max]`, where `ISP_oof` comes exclusively from inner folds that did not train on that row.

### 2.3 Two Calibrated Thresholds and Three-Tier Closed-Loop Control (`src/tg_controller.py`)

On a held-out calibration split, `calibrate_thresholds` computes:

- **Warning Threshold ($\tau_{\text{warning}}$):** the threshold maximising Youden's $J = \text{TPR} - \text{FPR}$.
- **Fault Threshold ($\tau_{\text{fault}} \ge \tau_{\text{warning}}$):** the smallest threshold achieving $\text{FPR} \le 10\%$ on grounded calibration responses.

During live inference (`ThreeTierController.respond`):

- **Safe ($R_0 < \tau_{\text{warning}}$):** Emit initial greedy answer $A_0$.
- **Tier 1 — Risk-Guided Re-sampling ($\tau_{\text{warning}} \le R_0 < \tau_{\text{fault}}$):** Draw $K=4$ temperature-sampled answers ($T=0.7, p=0.9$), score each with the 4-sensor detector, and emit $\arg\min_k R(A^{(k)})$ if its risk $< \tau_{\text{warning}}$; else escalate to Tier 2.
- **Tier 2 — Targeted Grounding Retrieval ($R_0 \ge \tau_{\text{fault}}$ or Tier 1 escalation):** Query the Wikipedia MediaWiki API for the question, prepend the retrieved summary, regenerate $A_{\text{RAG}}$, and re-score $R_{\text{RAG}}$. Emit $A_{\text{RAG}}$ if $R_{\text{RAG}} < \tau_{\text{fault}}$.
- **Tier 3 — Calibrated Abstention:** If retrieval fails or $R_{\text{RAG}} \ge \tau_{\text{fault}}$, abstain with a calibrated uncertainty statement.

---

## 3. Experimental Results (NVIDIA Tesla T4 GPU)

### 3.1 In-Distribution 5-Fold Grouped Cross-Validation (`TinyLlama-1.1B-Chat-v1.0`)

| Benchmark | Pairs ($2N$ rows) | **TRUEGUARD Fusion AUROC [95% CI]** | **ISP** | **AAS** | **EEM** | **DST** | Best Untrained Baseline | F1 | ECE |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| `halueval_dialogue` | 400 (800) | **0.903** [0.883, 0.922] | 0.904 | 0.618 | 0.668 | 0.634 | `LEN` = 0.687 | 0.820 | 0.034 |
| `halueval_qa` | 400 (800) | **0.975** [0.964, 0.987] | 0.977 | 0.512 | 0.850 | 0.859 | `LEN` = 0.953 | 0.955 | 0.024 |
| `halueval_summarization` | 400 (800) | **0.986** [0.980, 0.991] | 0.987 | 0.627 | 0.580 | 0.672 | `EEM_mean` = 0.581 | 0.935 | 0.025 |
| `truthful_qa` | 398 (796) | **0.876** [0.853, 0.900] | 0.877 | 0.607 | 0.522 | 0.533 | `EEM_max` = 0.523 | 0.817 | 0.042 |
| **Macro Average** | **1,598 (3,196)** | **0.935** | **0.936** | **0.591** | **0.655** | **0.675** | — | **0.882** | **0.031** |

### 3.2 Leave-One-Sensor-Out Ablation & Sensor Complementarity

| Benchmark | Full (4 Sensors) | **Without ISP ($-\text{ISP}$)** | Without AAS ($-\text{AAS}$) | Without EEM ($-\text{EEM}$) | Without DST ($-\text{DST}$) | Union Recall @ 10% FPR |
| --- | --- | --- | --- | --- | --- | --- |
| `halueval_dialogue` | **0.903** | **0.714 ($\Delta = -0.188$)** | 0.903 ($+0.000$) | 0.903 ($+0.000$) | 0.903 ($-0.000$) | 0.762 |
| `halueval_qa` | **0.975** | **0.918 ($\Delta = -0.057$)** | 0.976 ($+0.001$) | 0.976 ($+0.001$) | 0.975 ($+0.000$) | 0.978 |
| `halueval_summarization` | **0.986** | **0.745 ($\Delta = -0.241$)** | 0.986 ($-0.000$) | 0.986 ($+0.000$) | 0.987 ($+0.000$) | 0.960 |
| `truthful_qa` | **0.876** | **0.626 ($\Delta = -0.251$)** | 0.876 ($-0.001$) | 0.877 ($+0.000$) | 0.877 ($+0.001$) | 0.603 |

**Key Finding:** Removing `ISP` drops AUROC by **$18.8\text{–}25.1$ percentage points** on `halueval_dialogue`, `halueval_summarization`, and `truthful_qa`. When `ISP` is unavailable, the three unsupervised sensors (`AAS + EEM + DST`, column $-\text{ISP}$) still achieve **$0.626\text{–}0.918$ AUROC**, outperforming individual raw entropy or attention baselines on every dataset.

### 3.3 Cross-Dataset Transfer and Benchmark Style Artefacts

- **Transfer across HaluEval task formats:** Training on `halueval_dialogue` transfers zero-shot to `halueval_qa` at **$0.946$ AUROC** and to `halueval_summarization` at **$0.767$ AUROC**; training on `halueval_summarization` transfers to `halueval_dialogue` at **$0.779$ AUROC** and `halueval_qa` at **$0.777$ AUROC** (`ISP`-only $= 0.845$).
- **Diagnostic discovery on `halueval_qa` vs. `truthful_qa`:** Our automated diagnostic revealed that in `halueval_qa`, reference `right_answer` strings are short entity phrases whereas `hallucinated_answer` strings are longer fluent sentences (`LEN` baseline $= 0.953$, raw `NLL_mean` $= 0.089$, inverted $= 0.911$). In `truthful_qa`, both answers are full sentences of matched length (`LEN` $= 0.456$). Consequently, detectors trained on `halueval_qa` invert their length/entropy correlation on `truthful_qa` ($0.422$ AUROC), demonstrating why hallucination detectors must be calibrated on task-matched answer lengths.

### 3.4 Before-and-After Three-Tier Mitigation on Live `TriviaQA` Generations (`n_cal=150`, `n_test=150`)

- **Calibrated thresholds (from the 150 calibration questions only):** $\tau_{\text{warning}} = 0.611$, $\tau_{\text{fault}} = 0.898$.
- **Detection AUROC on TinyLlama's own open-ended test answers:** **$0.795$**.
- **Hallucination reduction:**
  - **Unmitigated greedy decoding:** $62.0\%$ hallucination rate ($38.0\%$ accuracy).
  - **Post-mitigation among answered queries ($43.3\%$ coverage):** hallucination rate drops to **$40.0\%$** (**$35.5\%$ relative reduction**; accuracy rises from $38.0\% \to \mathbf{60.0\%}$).
  - **System-wide emitted hallucination rate:** drops from **$62.0\% \to 17.3\%$** (**$72.0\%$ relative reduction**).
  - **Selective-prediction Risk–Coverage comparison:** TRUEGUARD achieves **$\text{AURC} = 0.412$**, beating both Shannon Entropy ($\text{AURC} = 0.526$) and Negative Log-Likelihood ($\text{AURC} = 0.603$) across all coverage levels ($90\% \to 50\%$).

### 3.5 Real Per-Token GPU Latency (`TinyLlama-1.1B` on Tesla T4)

| Decoding Mode | Latency (ms / token) | Overhead vs. Vanilla | Speedup vs. 5-Sample Baseline |
| --- | --- | --- | --- |
| `vanilla_decode` (KV-cached greedy) | $33.49\text{ ms}$ | — | — |
| `trueguard_postpass` (`generate` + 1 `score_answer` pass) | **$36.41\text{ ms}$** | **$+2.92\text{ ms}$ ($+8.7\%$)** | **$4.65\times$** |
| `trueguard_online` (step-by-step cached monitor; sensor math $= 5.21\text{ ms}$) | **$39.30\text{ ms}$** | **$+5.81\text{ ms}$ ($+17.3\%$)** | **$4.31\times$** |
| `multi_sample_5x_baseline` (5 sampled generations) | $169.31\text{ ms}$ | $+135.82\text{ ms}$ ($+405.6\%$) | $1.00\times$ |
