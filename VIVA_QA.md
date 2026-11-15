# TRUEGUARD: Final University Viva Defense Questions & Answers
**Candidate:** Yogesh Ravi M (Reg. No: 22MIA1052)  
**Programme:** Integrated M.Tech Computer Science & Engineering (Data Science)  
**Faculty Guide:** Dr. Pradeep Kumar T.S., Professor (SCOPE, VIT Chennai)  
**Project Title:** Toward Trustworthy Large Language Models: A Real-Time, Internal-State-Based Hallucination Detection & Closed-Loop Mitigation Framework (TRUEGUARD)

---

## PART 1: CORE MOTIVATION & PROBLEM STATEMENT (Slides 1–5)

### Q1: What is a hallucination in an LLM, and why does it occur mathematically?
**Answer:**  
In an autoregressive Large Language Model, token generation is governed by next-token probability maximization:
$$y_t \sim P(y_t \mid y_{<t}, x) = \text{Softmax}(W_{vocab} h_t^{(L)})$$
The loss function during pretraining is cross-entropy over internet text. The objective function optimizes **fluency, syntactic coherence, and statistical likelihood**, not factual truthfulness. Mathematically, the model has no ground-truth oracle or external factual database; when prompt context is sparse or contradictory, the model samples from high-probability surface tokens, emitting confident falsehoods.

### Q2: What is the difference between intrinsic and extrinsic hallucinations?
**Answer:**  
- **Intrinsic Hallucinations:** The output contradicts factual assertions explicitly provided in the user's input prompt or reference context (e.g., misrepresenting facts given in a source article during summarization).
- **Extrinsic Hallucinations:** The output introduces new, unverifiable assertions not present in the input context or world knowledge (e.g., fabricating a fictitious author, DOI, or clinical treatment).

### Q3: Why can't we just rely on the model's output softmax probabilities (token entropy)?
**Answer:**  
Due to **Signal Polarity Inversion**: on complex datasets where human misconceptions are widespread (such as TruthfulQA) or where answer lengths differ (HaluEval-QA), models memorize popular falsehoods and output them with **lower entropy and higher softmax confidence** than when stating nuanced truths. On HaluEval-QA, raw token entropy achieves an AUROC of only **0.349**—worse than a random coin flip. This proves surface probabilities are deceptive for safety.

---

## PART 2: LITERATURE REVIEW & RESEARCH GAPS (Slides 6–11)

### Q4: How does TRUEGUARD differ from SelfCheckGPT (Manakul et al., 2023)?
**Answer:**  
SelfCheckGPT is a **black-box sampling method**. It queries the LLM 5 to 20 times per prompt to measure stochastic semantic consistency. This increases computational latency by **+500% to +2000%** (+134 ms/token), making real-time chat economically impossible. Furthermore, it only flags hallucinations without fixing them.  
In contrast, TRUEGUARD is a **single-pass white-box framework**: it hooks internal activations during the standard generation pass (+2.91 ms/token, +8.7% overhead) and provides closed-loop 3-tier mitigation.

### Q5: How does TRUEGUARD differ from SAPLMA (Azaria & Mitchell, 2023) and ITI (Li et al., 2023)?
**Answer:**  
- **SAPLMA** only probes a single middle layer using a linear classifier. It ignores attention dispersion and semantic trajectory drift, failing on multi-hop QA (0.762 AUROC). It is also passive (detection only).
- **ITI (Inference-Time Intervention)** shifts activations along fixed truth vectors during decoding. However, fixed steering degrades text fluency, causes repetitive token loops, and cannot supply missing external facts.  
- **TRUEGUARD** monitors 4 complementary physical sensors and applies a **graded closed-loop controller**: low risk passes untouched, moderate risk is re-sampled, high risk fetches verified RAG evidence, and ungrounded queries safely abstain.

---

## PART 3: ARCHITECTURE & SENSORS (Slides 12–16)

### Q6: Can TRUEGUARD be integrated into commercial models like ChatGPT, Claude, or Gemini?
**Answer:**  
**No, and this is a fundamental architectural boundary:**  
Commercial APIs (OpenAI, Anthropic, Google Gemini API) are **closed black boxes**. They only provide an input/output text endpoint. They strictly hide their intermediate hidden states ($h_l$), attention head matrices ($A_{l,h}$), and KV caches.  
TRUEGUARD is designed for **self-hosted, open-weight foundation models** (e.g., Llama-3, Mistral, TinyLlama, Qwen) deployed on private enterprise or cloud servers (vLLM, TGI, PyTorch). In banking, healthcare, and defense, organizations host their own models to protect data privacy; TRUEGUARD acts as an inline real-time guardrail on these servers.

### Q7: Why did you choose TinyLlama-1.1B as your primary testbed?
**Answer:**  
1. **Architectural Parity:** TinyLlama-1.1B-Chat-v1.0 features the exact architecture of Llama-2 and Llama-3: RMSNorm, SwiGLU activation, RoPE embeddings, and Grouped-Query Attention across 22 layers and 32 heads.
2. **Scientific Reproducibility:** Provides completely open, reproducible PyTorch tensor access.
3. **Resource Feasibility (₹0 Cost):** Executes full 16-bit inference within 15GB VRAM on free Google Colab Tesla T4 GPUs.
4. **Cross-Scale Generality:** Probes trained on normalized hidden dimensions generalize directly to larger 7B/70B models.

### Q8: Explain the four internal sensors and their physical intuition.
**Answer:**  
1. **ISP ($F_t$):** Supervised logistic probe on Layer 16 ($0.73 L$). Captures factual truthfulness geometry before vocabulary projection.
2. **AAS ($A_t$):** Top-quartile attention head entropy. Measures attention dispersion and prompt context neglect.
3. **EEM ($H_{ent,t}$):** Blended information entropy ($0.6 H_{Shannon} + 0.4 H_{Renyi2}$). Captures probability mass leakage and top competing logit collision.
4. **DST ($D_t$):** Consecutive-token cosine displacement $1 - \cos(h_t^{(22)}, h_{t-1}^{(22)})$. Detects sudden geometric dislocations as the model drifts into fabricated narratives.

---

## PART 4: DATASETS & PREPROCESSING (Slides 17–20)

### Q9: How did you curate your datasets, and why not use only TruthfulQA?
**Answer:**  
Evaluating only on TruthfulQA is a common flaw in existing literature because TruthfulQA only tests human misconceptions. We curated **5 diverse benchmarks totaling N = 3,196 pairs**:
- TruthfulQA (796 pairs) - Human misconceptions.
- HaluEval-QA (800 pairs) - Multi-hop QA entity substitutions.
- HaluEval-Dialogue (800 pairs) - Conversational chat grounding.
- HaluEval-Summarization (800 pairs) - Context-faithful text compression.
- TriviaQA (150 queries) - Live open-domain closed-loop mitigation testing.

### Q10: How did you prevent data leakage during model validation?
**Answer:**  
We enforced **5-Fold Grouped Cross-Validation (GroupKFold)** grouped strictly by unique **Question ID**. In benchmarks like TruthfulQA, true and false completions share identical question prompts. A standard random train/test split leaks the question into the training fold. GroupKFold guarantees that **zero test questions** were ever seen during probe training. All reported metrics are computed exclusively on **Out-of-Fold (OOF)** test predictions.

---

## PART 5: CALIBRATION & MITIGATION (Slides 21–23)

### Q11: How is the risk score $r(x,y)$ calibrated?
**Answer:**  
The pooled 4-sensor vector passes through standardized scaling ($z = (x - \mu)/\sigma$) and an L2-regularized logistic regression model followed by **Platt scaling**:
$$r(x,y) = \frac{1}{1 + \exp(-(A \cdot \text{logit} + B))}$$
Parameters $A$ and $B$ are fitted on validation folds using cross-entropy loss. This guarantees that $r(x,y) \in [0, 1]$ represents true posterior hallucination risk.

### Q12: What are the two operating thresholds, and how do they route queries?
**Answer:**  
- $\tau_{warn} = 0.611$: Calibrated at 90% specificity (10% FPR) on validation folds.
- $\tau_{fault} = 0.898$: Calibrated at 95% specificity (5% FPR) for high-confidence hallucination faults.
- **Routing Decision:**
  - $r < 0.611$ $\to$ **Safe Pass** (Direct output, 0 extra passes, 32.0% of queries).
  - $0.611 \le r < 0.898$ $\to$ **Tier 1 Annealed Re-Sampling** ($T \in \{0.35, 0.20\}$, 7.3% of queries).
  - $r \ge 0.898$ $\to$ **Tier 2 Targeted Active RAG Repair** (Wikipedia retrieval, 4.0% of queries).
  - If RAG evidence is insufficient or post-RAG $r \ge \tau_{fault}$ $\to$ **Tier 3 Calibrated Abstention** (Safe refusal, 56.7% of queries).

---

## PART 6: EXPERIMENTAL RESULTS (Slides 24–28)

### Q13: What does Figure 7.1 prove regarding detection performance?
**Answer:**  
Figure 7.1 proves that TRUEGUARD achieves a **Macro AUROC of 0.893** across all 4 benchmarks (TruthfulQA 0.876, HaluEval-QA 0.955, HE-Dial 0.755, HE-Summ 0.986). In contrast, the standard entropy baseline achieves only 0.548 Macro AUROC because it collapses on QA and Dialogue due to signal polarity inversion.

### Q14: What does the 4×4 Transfer Matrix in Figure 7.2 prove?
**Answer:**  
In the transfer matrix, probes trained on one task (e.g., Dialogue) are evaluated zero-shot on completely unseen tasks (e.g., QA). It achieves an off-diagonal transfer AUROC of up to **0.852**. This proves that the 4 sensors capture universal internal representation geometry rather than task-specific memorization.

### Q15: In Figure 7.3, why does ISP alone perform so well? Do we really need the other 3 sensors?
**Answer:**  
ISP is indeed the strongest anchor ($0.876$ on TruthfulQA). However, on complex multi-turn dialogue and long-form document summarization, ISP alone fluctuates. AAS catches context neglect when attention disperses, and EEM captures token-level vocabulary collision. Combining all 4 sensors provides mathematical robustness against single-signal blind spots.

### Q16: In Figure 8.1, you report an 83.6% reduction in hallucinations. How much of this is due to abstention?
**Answer:**  
On live TriviaQA ($n = 150$), the baseline blind LLM emits hallucinations on 73.3% of queries. With TRUEGUARD, emitted hallucinations drop to **12.0%** (an **83.6% relative reduction**).  
Factual corrections occur through Tier 1 Re-Sampling (7.3%) and Tier 2 Active RAG (4.0%). The remaining 56.7% triggers **Calibrated Abstention (Tier 3)**. Abstention safely withholds incorrect answers rather than fabricating falsehoods, increasing the factual safety rate of emitted text from **26.7% to 88.0%**.

### Q17: What is the hardware latency overhead of TRUEGUARD in Figure 8.2?
**Answer:**  
On an NVIDIA Tesla T4 GPU:
- Vanilla TinyLlama decode: **33.49 ms/token**
- TRUEGUARD hooked decode: **36.40 ms/token**
- Latency overhead: **+2.91 ms/token (+8.7%)**  
In contrast, 5-sample SelfCheckGPT takes **167.45 ms/token** ($5\times$ slower). TRUEGUARD provides real-time single-pass guardrailing without slowing down conversational flow.

---

## PART 7: DEPLOYMENT & SCIENTIFIC LIMITATIONS (Slides 29–30)

### Q18: What are the main limitations of TRUEGUARD?
**Answer:**  
1. **White-Box Requirement:** It cannot protect proprietary closed APIs (ChatGPT/Claude) because external activations are hidden.
2. **Network Latency during Tier 2 RAG:** When Tier 2 triggers, Wikipedia search adds 250–400 ms network retrieval delay.
3. **Conservative Refusal Rate:** Under strict thresholds ($\tau_{fault} = 0.898$), the system abstains on 56.7% of ungrounded queries.
4. **Probe Retraining across Architectures:** Probes must be retrained when migrating to fundamentally different model families (e.g., from Llama to Mamba state-space models).

### Q19: What is the future scope of this research?
**Answer:**  
1. **Multimodal Extension:** Applying internal state probing to vision-language models (e.g., LLaVA) to detect visual hallucinations.
2. **Reinforcement Learning from Internal Feedback (RLIF):** Using TRUEGUARD risk signals directly as reward penalties during alignment tuning.
3. **Hardware Kernel Fusion:** Fusing probe matrix multiplications directly into FlashAttention CUDA kernels to reduce overhead from +8.7% down to < 2%.

