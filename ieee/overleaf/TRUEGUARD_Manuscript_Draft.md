# TRUEGUARD: An Empirical Study of White-Box Hallucination Detection, Domain Shift, and Selective Prediction in Large Language Models

**[Author 1 Name]¹**, **[Author 2 Name]¹**, **[Author 3 Name]¹**  
¹[Department Name, University / Institution Name, City, Postal Code, Country]  
*Corresponding author: [Author Name] (e-mail: [author@institution.edu]).*  
*(Placeholder note: Confirmed author names, affiliations, ORCID IDs, and funding acknowledgments are not stored in the research repository and will be inserted prior to IEEE Access submission.)*

---

## ABSTRACT

Large language models (LLMs) frequently generate fluent text that is factually incorrect or unsupported by context. Many established hallucination detectors rely on generating multiple stochastic responses and comparing them with external natural language inference (NLI) models, which increases inference cost and requires hosting auxiliary neural models. White-box detectors estimate hallucination risk in a single forward pass using internal activations, attention patterns, and token probabilities, yet their reliability under dataset artifacts, cross-domain shift, and real-time selective prediction remains insufficiently understood, particularly on small frozen models. This paper presents an empirical study of **TRUEGUARD**, a unified single-pass white-box framework instrumented on frozen `TinyLlama/TinyLlama-1.1B-Chat-v1.0` without updating base model weights. TRUEGUARD extracts four intrinsic signal families—Internal State Probe (ISP), Attention Anomaly Score (AAS), Energy/Entropy Monitor (EEM), and Directional Semantic Trajectory (DST)—and fuses them into a calibrated hallucination risk score coupled with a three-tier selective response controller. Across ten benchmarks (`32,590` evaluated sequences), three main empirical findings emerge. First, although in-domain 5-fold group cross-validation reaches `0.8773–0.9936` AUROC on paired benchmarks and `0.7204` on HaluEval-General, artifact controls show that surface text and length cues strongly inflate raw HaluEval scores (answer-text TF-IDF alone reaches `0.9661` on HaluEval-QA and `0.9539` on HaluEval-Summarization; answer length reaches `0.9572` on HaluEval-QA). Even so, TRUEGUARD significantly outperforms answer-text TF-IDF on all four paired benchmarks under strict length matching (`|ΔL| ≤ 2` tokens; `0.7901–0.9939` AUROC, `p ≤ 0.035`), with ISP accounting for over `96%` of fusion weight. Second, zero-shot pooled probes collapse to chance across four unseen domains (`0.4597–0.5205` AUROC), and source-risk recalibration fails (`0.4957–0.5242`). Diagnostic analysis shows higher within-domain split-half probe weight alignment (`+0.1125` to `+0.6707` at equal sample size `N = 900`) than cross-domain alignment (`-0.0151` to `+0.0204`), and separates length-free EEM signal on FaithDial (`0.7662` within length quartiles) and XSum (`0.6648`) from length-confounded inversion on HaluEval-QA. Target-domain few-shot refitting (training target probes from scratch with zero source weight transfer) yields task-dependent gains at `K = 250` on FaithDial (`0.8231`), FEVER (`0.7325`), and WikiBio (`0.6698`) while matching 1D length on XSum (`0.6456` vs. `0.6445`), whereas simple baselines win at `K = 50`. Third, on `250` held-out closed-book TriviaQA generations, target-refitted single-pass TRUEGUARD (`K = 250` calibration examples) achieves `0.7876` AUROC and `0.4360` AURC, significantly outperforming label-free `M = 10` Semantic Entropy (`0.6859`, `p_Holm = 0.012`), Predictive Entropy (`0.6583`, `p_Holm = 0.006`), and length-normalized NLL (`0.4678`, `p_Holm = 0.006`), and performing competitively with label-free `M = 10` SelfCheckGPT-NLI (`0.7477`, `p_Holm = 0.478`, n.s.), whereas zero-shot pooled TRUEGUARD reaches only `0.5504`. Finally, selective abstention at `46.0%` coverage raises answered accuracy from `34.00%` to `55.65%` (`64/115`), whereas the full three-tier controller yields `54.78%` (`63/115`; `4` repaired, `3` broken), establishing no measurable net benefit from active resampling or retrieval interventions on this `1.1B` model.

## INDEX TERMS

Large language models, hallucination detection, white-box probing, internal representations, domain shift, dataset artifacts, few-shot refitting, selective prediction, abstention.

---

## I. INTRODUCTION

### A. Background and Motivation

Large language models (LLMs) are increasingly deployed in question answering, summarization, dialogue, and decision-support systems. Despite strong fluency, these models regularly produce hallucinations—statements that contradict external facts, fabricate unsupported details, or deviate from provided source context [@review35], [@review18]. Because hallucinated outputs are often phrased with confident language, end users struggle to distinguish accurate responses from fabricated ones, undermining human trust in automated systems [@review19], [@review03].

Detecting hallucinations reliably at inference time is especially challenging in resource-constrained deployments where small, frozen open-weight models are preferred for privacy, memory, or latency reasons. Prominent black-box detection methods such as SelfCheckGPT [@review21] and Semantic Entropy [PENDING_APPROVAL: kuhn2023semantic], [PENDING_APPROVAL: farquhar2024detecting] estimate uncertainty by sampling multiple independent generations for every prompt and scoring semantic consistency with an auxiliary NLI model. While effective without access to model weights, multi-sample methods multiply decoding work and require hosting an additional neural classifier. White-box methods offer an alternative: by reading hidden representations, attention distributions, and output logit uncertainty during a single forward pass, a lightweight detector can estimate risk without modifying the base LLM or generating extra candidate responses [@review27], [@review01], [@review12].

### B. Problem Statement

Although white-box hallucination probes often report high AUROC scores on standard benchmarks, several practical questions remain unresolved when moving from controlled benchmark splits to realistic deployment. First, widely used hallucination benchmarks such as HaluEval [@review29] pair ground-truth answers with synthetically generated hallucinations; it is unclear how much of a white-box detector's in-domain accuracy reflects factual error detection versus length or stylistic artifacts. Second, supervised linear probes trained on one set of benchmarks frequently fail under domain shift, yet the empirical conditions under which target-domain few-shot refitting outperforms simple one-dimensional or text-only baselines have not been systematically mapped. Third, when a risk estimator is coupled with a mitigation controller on a small model's own closed-book generations, it is necessary to separate the gains of selective abstention from the actual net effect of active regeneration or retrieval interventions.

### C. Research Gap

Existing studies typically examine individual components in isolation: linear hidden-state probing [@review27], [@review28], attention diagnostics [@review09], [@review11], token entropy or energy [@review04], [@review17], multi-sample black-box consistency [@review21], or retrieval-based revision [@review25], [@review33]. Few works evaluate all four internal signal families inside one frozen small model across ten datasets while simultaneously running strict dataset-artifact controls, diagnosing zero-shot cross-domain failure with equal-sample-size representation checks, comparing target-only few-shot refitting against simple baselines (`1D EEM`, `1D length`, and answer-text `TF-IDF`), and auditing selective abstention against active multi-tier intervention on the same held-out closed-book generations alongside reproduced external baselines.

### D. Research Objectives and Questions

This study investigates four concrete research questions using frozen `TinyLlama/TinyLlama-1.1B-Chat-v1.0` as a controlled small-LLM testbed:

1. **RQ1 (In-Domain Detection and Artifacts):** How accurately do single-pass white-box signals detect hallucinations in-domain, and how much of that accuracy persists after controlling for answer length and surface-text `TF-IDF` artifacts?
2. **RQ2 (Cross-Domain Shift and Diagnostics):** Why do pooled white-box detectors fail under zero-shot domain shift, and what do within-domain versus cross-domain probe directions and length-controlled entropy checks reveal about this failure?
3. **RQ3 (Target-Domain Few-Shot Refitting):** When target-domain probes are refitted from scratch on `K ∈ {50, 100, 250}` labeled examples, when do white-box probes outperform source-risk recalibration and simple `1D` or text-only baselines?
4. **RQ4 (Selective Prediction, External Baselines, and Active Intervention):** On closed-book TriviaQA generations, how does target-refitted single-pass white-box risk detection compare with label-free multi-sample external baselines (`SelfCheckGPT-NLI`, `Semantic Entropy`), and does a three-tier active controller outperform pure selective abstention at matched coverage?

### E. Main Research Contributions

Rather than claiming individual white-box signals or selective routing as new algorithmic inventions, this work frames **TRUEGUARD** as a unified experimental framework and makes three evidence-backed empirical contributions alongside an auditable single-pass instrumentation pipeline:

1. **Controlled In-Domain Detection and Artifact Quantification:** Across five in-domain benchmarks (`18,141` rows), we show that headline HaluEval scores (`0.9880` QA, `0.9936` Summarization) are strongly confounded by length (`LEN = 0.9572` on HaluEval-QA) and surface text cues (`TF-IDF = 0.9661` QA, `0.9539` Summ). Nonetheless, TRUEGUARD significantly beats answer-text `TF-IDF` on all four paired benchmarks even under strict length matching (`|ΔL| ≤ 2` tokens; `+0.0331` to `+0.0829` AUROC, `p ≤ 0.035`), while leave-one-sensor-out ablations establish that ISP dominates fusion (`>96%` standardized weight).
2. **Cross-Domain Failure Diagnostics and Target-Domain Few-Shot Refitting Boundaries:** Across four initially unseen benchmarks (`13,949` rows), pooled zero-shot probes collapse to chance (`0.4597–0.5205`) and source-risk recalibration fails (`0.4957–0.5242`). Equal-sample-size (`N = 900`) diagnostics show substantially higher within-domain split-half probe weight alignment (`+0.1125` to `+0.6707`) than cross-domain alignment (`-0.0151` to `+0.0204`), while length-controlled entropy checks separate genuine length-free EEM signal on FaithDial (`0.7662`) and XSum (`0.6648`) from length-confounded inversion on HaluEval-QA. Target-only few-shot refitting (`0` source weights transferred) reveals a clear sample-efficiency boundary: simple baselines win at `K = 50`, whereas `K = 250` refitting (`<2 s` CPU) yields task-dependent gains on FaithDial (`0.8231`), FEVER (`0.7325`), and WikiBio (`0.6698`), while matching `1D` length on XSum (`0.6456` vs. `0.6445`).
3. **Selective Prediction vs. External Baselines and Abstention-vs.-Repair Audit:** On `250` held-out TriviaQA generations, target-refitted single-pass TRUEGUARD (`K = 250`, `0.7876` AUROC, `0.4360` AURC) significantly outperforms label-free `M = 10` Semantic Entropy (`0.6859`, `p_Holm = 0.012`), Predictive Entropy (`0.6583`, `p_Holm = 0.006`), and verified length-normalized NLL (`0.4678`, `p_Holm = 0.006`), and performs competitively with label-free `M = 10` SelfCheckGPT-NLI (`0.7477`, `p_Holm = 0.478`, n.s.) without extra generations or external NLI models—whereas zero-shot pooled TRUEGUARD drops to `0.5504`. Forensically, pure selective abstention (`64/115 = 55.65%` at `46.0%` coverage) accounts for the observed accuracy gain, while the full three-tier controller (`63/115 = 54.78%`; `4` repaired, `3` broken) shows no measurable net benefit from active regeneration or Wikipedia retrieval on this `1.1B` model.

### F. Organization of the Paper

Section II reviews related work on hallucination detection, domain shift, benchmark artifacts, and mitigation. Section III describes the TRUEGUARD framework and exact sensor formulations. Section IV details the experimental methodology, datasets, controls, and statistical protocol. Section V presents the empirical results across all ten benchmarks. Section VI interprets the findings, practical implications, and limitations. Section VII concludes the paper and outlines future work.

---

## II. RELATED WORK

### A. Hallucinations in Large Language Models

Surveys of natural language generation categorize hallucinations into intrinsic errors, which contradict provided source text, and extrinsic errors, which introduce unverified claims beyond the source [@review35], [@review18]. Evaluation studies on instruction-tuned models show that hallucination rates remain substantial in closed-book factual recall, long-form biography generation, and open-domain dialogue [@review37], [@review23]. Benchmarks such as TruthfulQA [@review22], HaluEval [@review29], and self-contradiction suites [@review36] have standardized detection testing, while broader evaluations connect hallucination mitigation to human trust and calibration [@review03], [@review19].

### B. Internal-State Hallucination Detection

White-box probing methods test whether a frozen LLM's hidden activations encode signals of truthfulness or fabrication. Azaria and Mitchell [@review27] introduced SAPLMA, training lightweight classifiers over intermediate hidden layers to distinguish true from false statements. Subsequent work expanded internal-state analysis through unsupervised real-time hidden-state monitoring (MIND) [@review01], prompt-guided representation probing (PRISM) [@review02], deep layer-wise representation analysis [@review05], and representation-shift metrics such as HalluShift [@review13]. Related approaches train linear probes to predict semantic entropy directly from hidden states in a single pass [@review14] or intervene along truthful activation directions during decoding, as in Inference-Time Intervention (ITI) [@review28] and Truth Forest [@review38].

### C. Attention-Based and Uncertainty-Based Detection

Beyond hidden-state vectors, researchers have investigated attention distributions and token-level predictive uncertainty. LLM-Check [@review12] evaluates hidden-state eigenvalues, attention maps, and token perplexity across hallucination settings. Recent studies trace intrinsic and extrinsic hallucinations through attention patterns [@review09] and identify uncertainty-aware attention heads for unsupervised scoring [@review11]. On the output-distribution side, uncertainty quantification surveys [@review07] highlight predictive entropy, token-level entropy production rates [@review17], and energy-based scores beyond standard Shannon entropy [@review04]. In black-box settings, SelfCheckGPT [@review21] samples multiple stochastic responses and measures contradiction via NLI or text similarity, while Semantic Entropy [PENDING_APPROVAL: kuhn2023semantic], [PENDING_APPROVAL: farquhar2024detecting] clusters sampled answers by bidirectional entailment before computing entropy over semantic equivalence classes.

### D. Cross-Domain Generalization and Benchmark Artifacts

A recurring concern in supervised hallucination detection is whether high benchmark accuracy transfers across tasks, domains, and generation regimes. Benchmark construction differences—such as pairing human-written reference answers with LLM-generated hallucinations in HaluEval [@review29]—can introduce systematic disparities in answer length, phrasing, or fluency. Similarly, token-level likelihood and entropy signals can invert direction between teacher-forced synthetic pairs and naturally generated model errors. Evaluating detectors without surface-text controls (`TF-IDF`, answer length) or strict group-disjoint cross-domain splits risks overstating generalization.

### E. Hallucination Mitigation and Selective Prediction

Mitigation strategies include retrieval-augmented generation (RAG) [@review25], self-reflective retrieval (Self-RAG) [@review26], multi-step verification such as Chain-of-Verification (CoVe) [@review24], tool-augmented fact-checking such as RARR [@review33], FacTool [@review34], and CRITIC [@review39], multi-agent debate [@review31], and behaviorally calibrated reinforcement learning [@review15]. When external verification is unavailable or a small model lacks parametric knowledge, selective prediction—abstaining on high-risk queries and reporting accuracy across coverage thresholds via area under the risk–coverage curve (AURC) [PENDING_APPROVAL: geifman2017selective]—provides a principled safety mechanism.

### F. Positioning of TRUEGUARD

TRUEGUARD combines four established white-box signal families (`ISP`, `AAS`, `EEM`, `DST`) into one frozen-model instrumentation pipeline and uses this unified testbed to conduct a rigorous empirical study. Unlike papers that propose a single sensor and report unqualified benchmark AUROCs, our study systematically tests (i) how much in-domain performance survives length and `TF-IDF` controls, (ii) why pooled white-box probes collapse zero-shot and when target-only few-shot refitting beats simple baselines, (iii) how target-refitted single-pass detection compares with label-free multi-sample `SelfCheckGPT-NLI` and `Semantic Entropy` under explicit supervision disclosure, and (iv) whether active regeneration and retrieval actually improve upon pure selective abstention on a `1.1B` model.

---

## III. PROPOSED TRUEGUARD FRAMEWORK

### A. System Architecture

TRUEGUARD is a modular white-box monitoring and selective-response framework attached to a frozen autoregressive LLM without modifying any base model weights. As implemented in `tg_pipeline.py` and `tg_controller.py`, the framework operates in three stages: (1) single-pass extraction of four intrinsic signal families from hidden states, attention weights, and output logits; (2) calibrated hallucination-risk estimation via a regularized logistic fusion classifier; and (3) threshold-governed response routing through a three-tier controller. Two mathematically equivalent extraction paths are implemented and unit-tested for parity: a teacher-forced pass (`score_answer`) for offline training and benchmark evaluation, and a step-by-step cached monitor (`OnlineSignalMonitor`) for real-time decoding. Fig. 1 summarizes the end-to-end architecture.

> **[FIGURE 1 PLACEHOLDER — Vector TikZ/SVG Schematic for LaTeX Preparation]**  
> **FIGURE 1.** Overview of the TRUEGUARD single-pass white-box framework attached to frozen `TinyLlama-1.1B-Chat-v1.0`. Four intrinsic signal families (ISP, AAS, EEM, DST) are extracted from intermediate hidden states, final-quartile causal attention weights, and output logits in one forward pass, fused by an L2-regularized logistic classifier into a calibrated hallucination risk score $r \in [0, 1]$, and routed through a three-tier selective response controller (`SAFE`, `TIER1_RESAMPLE`, `TIER2_RETRIEVAL`, `TIER3_ABSTAIN`).

### B. Foundation Language Model

All experiments use the frozen open-weight instruction model `TinyLlama/TinyLlama-1.1B-Chat-v1.0` [PENDING_APPROVAL: zhang2024tinyllama], which has $L = 22$ transformer decoder layers ($N_h = 23$ hidden-state tensors including the input embedding layer), hidden dimension $d = 2048$, and vocabulary size $V = 32{,}000$. The model is loaded in `float16` on CUDA in evaluation mode (`0` trainable parameters) with `attn_implementation="eager"` so that exact multi-head attention weight matrices are accessible for AAS computation. Prompts are formatted using the model's native chat template (`apply_chat_template` with `add_generation_prompt=True`), truncated to at most `384` prompt tokens and `48` answer tokens for teacher-forced scoring (`24` generated tokens for closed-book TriviaQA).

### C. Internal State Probe (ISP)

The Internal State Probe follows multi-layer linear probing [@review27]. Hidden states are extracted at four depth fractions $\mathcal{F}_{\text{ISP}} = \{0.45, 0.60, 0.75, 0.90\}$ of the $N_h = 23$ hidden-state tensors, corresponding to layer indices $\mathcal{L}_{\text{ISP}} = \{10, 13, 17, 20\}$. For an answer spanning token positions $[a_{\text{start}}, a_{\text{end}})$ of length $T_a = a_{\text{end}} - a_{\text{start}}$, the state predicting token $t$ is read at position $p = t - 1$. Each probed layer's representations are mean-pooled across all answer tokens:

$$\bar{h}_l = \frac{1}{T_a} \sum_{p = a_{\text{start}} - 1}^{a_{\text{end}} - 2} h_{l,p} \in \mathbb{R}^{d}, \qquad l \in \mathcal{L}_{\text{ISP}}, \tag{1}$$

where $h_{l,p} \in \mathbb{R}^{d}$ is the hidden-state vector at layer $l$ and sequence position $p$, $d = 2048$ is the model hidden dimension, and $\bar{h}_l$ is the answer-mean representation for layer $l$.

For each layer $l \in \mathcal{L}_{\text{ISP}}$, an independent pipeline of z-score standardization ($\tilde{h}_l$) and L2-regularized logistic regression with weight vector $w_l \in \mathbb{R}^{d}$, bias $b_l \in \mathbb{R}$, and inverse regularization strength $C \in \{0.001, 0.01, 0.1\}$ is fitted on training examples only, with $C$ selected via inner 5-fold group-preserving (or stratified) cross-validation maximizing AUROC. Layer probabilities are averaged and mapped to clipped log-odds:

$$p_{\text{ISP}} = \frac{1}{|\mathcal{L}_{\text{ISP}}|} \sum_{l \in \mathcal{L}_{\text{ISP}}} \sigma\!\left(w_l^\top \tilde{h}_l + b_l\right), \qquad z_{\text{ISP}} = \log\!\left(\frac{\tilde{p}}{1 - \tilde{p}}\right), \tag{2}$$

where $\sigma(x) = (1 + e^{-x})^{-1}$ is the logistic sigmoid function, $|\mathcal{L}_{\text{ISP}}| = 4$, and $\tilde{p} = \text{clip}(p_{\text{ISP}}, 10^{-4}, 1 - 10^{-4})$ prevents unbounded log-odds prior to fusion.

### D. Attention Anomaly Score (AAS)

The Attention Anomaly Score measures dispersion in causal self-attention weights across the final quartile of transformer layers, $\mathcal{L}_{\text{AAS}} = \{\lfloor 0.75 L \rfloor, \dots, L - 1\}$ (layers `16` through `21` in TinyLlama-1.1B). For each answer-token query position $p$, there are $p + 1$ valid causal key positions. Let $a_{l,h,p,j} \in [0, 1]$ denote the attention weight of head $h \in \{1, \dots, H\}$ in layer $l \in \mathcal{L}_{\text{AAS}}$ from query $p$ to key $j$. The normalized Shannon entropy of each causal attention row is averaged over all heads and final-quartile layers:

$$\text{AAS}_p = \frac{1}{|\mathcal{L}_{\text{AAS}}|\, H} \sum_{l \in \mathcal{L}_{\text{AAS}}} \sum_{h=1}^{H} \frac{-\sum_{j=1}^{p+1} a_{l,h,p,j} \log\!\left(a_{l,h,p,j} + \epsilon\right)}{\max(\log(p+1),\, 1)}, \tag{3}$$

where $H$ is the number of attention heads per layer, $\epsilon = 10^{-10}$ ensures numerical stability, and $\max(\log(p+1), 1)$ normalizes entropy by the maximum possible entropy over $p + 1$ keys (avoiding division by zero when $p = 0$). Answer-level features are aggregated as $\text{AAS}_{\text{mean}}$ and $\text{AAS}_{\text{max}}$ over all answer token positions.

### E. Energy/Entropy Monitor (EEM)

The Energy/Entropy Monitor combines two normalized uncertainty statistics computed from the raw vocabulary logit vector $v_p \in \mathbb{R}^{V}$ at each answer-token position $p$. Letting $q_p = \text{softmax}(v_p)$ denote the predictive token distribution over vocabulary size $V = 32{,}000$, the normalized Shannon entropy $H_{\text{norm}}(q_p)$ and normalized Rényi-2 (collision) entropy $E_{\text{norm}}(q_p)$ are defined as:

$$H_{\text{norm}}(q_p) = \text{clip}\!\left(\frac{-\sum_{i=1}^{V} q_{p,i} \log(q_{p,i} + \epsilon)}{\log V},\, 0,\, 1\right), \qquad E_{\text{norm}}(q_p) = \text{clip}\!\left(\frac{-\log\!\left(\sum_{i=1}^{V} q_{p,i}^2 + \epsilon\right)}{\log V},\, 0,\, 1\right), \tag{4}$$

where $q_{p,i}$ is the probability of vocabulary token $i$ at position $p$, $\log V$ is the maximum possible entropy over $V$ tokens, and $\epsilon = 10^{-10}$. These two quantities are combined using fixed weight $w_e = 0.6$:

$$\text{EEM}_p = w_e\, H_{\text{norm}}(q_p) + (1 - w_e)\, E_{\text{norm}}(q_p), \tag{5}$$

and aggregated across answer tokens as $\text{EEM}_{\text{mean}}$ and $\text{EEM}_{\text{max}}$. Standalone predictive Shannon entropy ($\text{ENT}_{\text{mean}}$, $\text{ENT}_{\text{max}}$), token-length-normalized negative log-likelihood ($\text{NLL}_{\text{mean}}$), and answer token length ($\text{LEN}$) are also recorded strictly as comparison baselines and are never passed to the TRUEGUARD fusion classifier.

### F. Directional Semantic Trajectory (DST)

The Directional Semantic Trajectory tracks token-to-token representational drift during answer generation. At each answer position $p$, hidden states are averaged across three upper-middle layers $\mathcal{L}_{\text{DST}} = \{13, 17, 20\}$ (corresponding to depth fractions $\{0.60, 0.75, 0.90\}$) to form $u_p = \frac{1}{|\mathcal{L}_{\text{DST}}|} \sum_{l \in \mathcal{L}_{\text{DST}}} h_{l,p} \in \mathbb{R}^{d}$. For consecutive answer tokens ($p \ge a_{\text{start}}$), the normalized cosine drift is:

$$\text{DST}_p = \text{clip}\!\left(\frac{1 - \cos(u_p, u_{p-1})}{2},\, 0,\, 1\right), \tag{6}$$

where $\cos(u_p, u_{p-1}) = (u_p^\top u_{p-1}) / (\|u_p\|_2 \|u_{p-1}\|_2)$ is the cosine similarity between consecutive layer-averaged hidden states. For the initial answer token (or single-token answers), $\text{DST}_p$ is undefined (`NaN`) and omitted during aggregation, defaulting to $0.0$ for one-token answers. Answer-level features are $\text{DST}_{\text{mean}}$ and $\text{DST}_{\text{max}}$.

### G. Risk Fusion Classifier

The four sensor families are assembled into a 7-dimensional feature vector $z \in \mathbb{R}^7$ and mapped to a calibrated hallucination probability $r \in [0, 1]$ by an L2-regularized logistic regression fusion classifier ($C_{\text{fusion}} = 1.0$) preceded by feature standardization ($\tilde{z}$):

$$z = \big[z_{\text{ISP}},\; \text{AAS}_{\text{mean}},\; \text{AAS}_{\text{max}},\; \text{EEM}_{\text{mean}},\; \text{EEM}_{\text{max}},\; \text{DST}_{\text{mean}},\; \text{DST}_{\text{max}}\big]^\top \in \mathbb{R}^7, \qquad r = \sigma\!\left(w_{\text{f}}^\top \tilde{z} + b_{\text{f}}\right), \tag{7}$$

where $w_{\text{f}} \in \mathbb{R}^7$ and $b_{\text{f}} \in \mathbb{R}$ are the learned fusion weights and intercept. To eliminate probe-to-fusion leakage, `TrueGuardDetector.fit` constructs $z_{\text{ISP}}$ on the training set exclusively from inner out-of-fold ISP probabilities produced at the selected $C$, fits $(w_{\text{f}}, b_{\text{f}})$ on those unbiased scores, and then refits the four layer probes on the full training fold for test-time inference. Signed per-sensor log-odds attributions are obtained directly from element-wise products $\tilde{z}_j w_{\text{f},j}$.

### H. Risk-Based Response Controller

For closed-book generation, `ThreeTierController` routes an initial greedy answer $a_0$ with risk $r_0$ using two calibration-selected thresholds $\tau_{\text{warning}} < \tau_{\text{fault}}$:

$$g(r_0;\, \tau_{\text{warning}}, \tau_{\text{fault}}) = \begin{cases} \text{SAFE } (\text{release } a_0), & r_0 < \tau_{\text{warning}}, \\ \text{TIER 1 } (\text{sample } k=4 \text{ candidates}; \text{ release } a_1 \text{ if } r_1 < \tau_{\text{warning}}), & \tau_{\text{warning}} \le r_0 < \tau_{\text{fault}}, \\ \text{TIER 2 } (\text{Wikipedia extract } \le 700 \text{ chars}; \text{ release } a_2 \text{ if } r_2 < \tau_{\text{fault}}), & r_0 \ge \tau_{\text{fault}} \text{ or T1 escalation}, \\ \text{TIER 3 } (\text{abstain with fixed refusal}), & \text{if T2 fails or } r_2 \ge \tau_{\text{fault}}, \end{cases} \tag{8}$$

where $a_1$ and $r_1$ denote the lowest-risk candidate among $k = 4$ stochastic samples ($T = 0.7$, $\text{top\_p} = 0.9$, `max_new_tokens = 24`), and $a_2$ and $r_2$ denote the greedy answer and risk score obtained after prepending an introductory Wikipedia passage retrieved via `WikipediaRetriever`.

### I. Computational Characteristics

During monitoring, TRUEGUARD requires one forward pass of the frozen base LLM (`0` auxiliary NLI models, `0` extra stochastic generations). The linear probes ($4 \times 2048$ parameters) and 7-feature fusion classifier add negligible arithmetic overhead, while reading eager attention matrices introduces a bounded monitoring overhead quantified in Section V-J. Additional decoding or retrieval latency in mitigation mode is incurred only on queries exceeding $\tau_{\text{warning}}$.

---

## IV. EXPERIMENTAL METHODOLOGY

### A. Experimental Design

The experimental protocol comprises five controlled stages designed to prevent data leakage and separate genuine error detection from benchmark artifacts: (1) in-domain 5-fold group-preserving cross-validation and leave-one-sensor-out ablations across five datasets; (2) dataset-artifact control experiments (`LEN`, answer-text `TF-IDF`, shuffled labels, and length-matched pairs); (3) strict zero-shot cross-domain transfer to four initially unseen benchmarks plus equal-sample-size representation diagnostics; (4) target-domain few-shot refitting (`K ∈ {50, 100, 250}`) compared against source-risk recalibration and simple baselines; and (5) closed-book TriviaQA selective prediction comparing target-refitted TRUEGUARD, zero-shot pooled TRUEGUARD, label-free `SelfCheckGPT-NLI`, label-free `Semantic Entropy`, and pure selective abstention versus the full three-tier controller.

### B. Datasets and Task Definitions

Ten public benchmarks spanning `32,590` evaluated sequences are used (Table I). Datasets 1–5 form the in-domain cross-validation and pooled source-training suite: HaluEval-Dialogue, HaluEval-QA, HaluEval-Summarization, HaluEval-General [@review29], and TruthfulQA [@review22]. Datasets 6–9 serve as initially unseen cross-domain transfer and target-domain few-shot refitting benchmarks: FaithDial [PENDING_APPROVAL: dziri2022faithdial], WikiBio-GPT3 [@review21], XSum-Factuality [PENDING_APPROVAL: maynez2020faithfulness], and FEVER [PENDING_APPROVAL: thorne2018fever]. FEVER is explicitly separated as a **claim-verification transfer** task (`SUPPORTS` vs. `REFUTES`, excluding `12,333` `NOT ENOUGH INFO` items) rather than open-ended generative hallucination detection. Dataset 10, TriviaQA [PENDING_APPROVAL: joshi2017triviaqa], evaluates closed-book generation, external baselines, and selective mitigation on `250` calibration and `250` disjoint held-out test questions.

**TABLE I**  
**10-DATASET BENCHMARK SUITE, PROTOCOL ROLES, SPLITS, AND EXCLUSIONS**  
*(Source: `publication_ready/tables/Table1_Dataset_Methodology_and_Splits.md`)*

| # | Dataset | Protocol Role | Raw Rows | Usable Rows | Groups | Label 0 | Label 1 | Prevalence | Excluded |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | `halueval_dialogue` | `IN_DOMAIN_CV_AND_POOL` | 10,000 | 4,000 | 2,000 | 2,000 | 2,000 | 0.500 | 0 |
| 2 | `halueval_qa` | `IN_DOMAIN_CV_AND_POOL` | 10,000 | 4,000 | 2,000 | 2,000 | 2,000 | 0.500 | 0 |
| 3 | `halueval_summarization` | `IN_DOMAIN_CV_AND_POOL` | 10,000 | 4,000 | 2,000 | 2,000 | 2,000 | 0.500 | 0 |
| 4 | `truthful_qa` | `IN_DOMAIN_CV_AND_POOL` | 817 | 1,634 | 817 | 817 | 817 | 0.500 | 0 |
| 5 | `halueval_general` | `IN_DOMAIN_CV_AND_POOL` | 4,507 | 4,507 | 4,507 | 3,692 | 815 | 0.181 | 0 |
| 6 | `faithdial` | `UNSEEN_ZEROSHOT_AND_TARGET_REFIT` | 3,539 | 3,507 | 791 | 946 | 2,561 | 0.730 | 32 |
| 7 | `wikibio_gpt3` | `UNSEEN_ZEROSHOT_AND_TARGET_REFIT` | 1,908 | 1,908 | 238 | 516 | 1,392 | 0.730 | 0 |
| 8 | `xsum_factuality` | `UNSEEN_ZEROSHOT_AND_TARGET_REFIT` | 5,597 | 1,868 | 498 | 185 | 1,683 | 0.901 | 1 |
| 9 | `fever` | `UNSEEN_CLAIM_VERIFICATION_REFIT` | 18,999 | 6,666 | 6,666 | 3,333 | 3,333 | 0.500 | 12,333 |
| 10 | `trivia_qa` | `CLOSED_BOOK_SELECTIVE_PREDICTION` | 17,944 | 250 cal + 250 test | 500 | Dynamic | Dynamic | 0.660 (test) | 0 |

### C. Data Preparation and Feature Extraction

For Datasets 1–9, benchmark-provided responses are evaluated via teacher forcing (`score_answer`) through frozen `TinyLlama-1.1B-Chat-v1.0` (`seed = 42`), storing feature matrices $F \in \mathbb{R}^{N \times 10}$, four-layer mean hidden states $H \in \mathbb{R}^{N \times 4 \times 2048}$, binary labels $y \in \{0, 1\}$ (`1 = hallucinated`), and prompt/document group identifiers. Paired benchmarks retain exact two-row groups (`1` factual, `1` hallucinated per prompt). Extraction produced zero `NaN` or `Inf` values across all `32,590` sequences. For TriviaQA (Dataset 10), TinyLlama generates its own closed-book greedy answers (`max_new_tokens = 24`), labeled against TriviaQA gold answer aliases (`y = 1` if incorrect) and scored through the exact same `score_answer` extractor. Token-length-normalized negative log-likelihood (`NLL`) is computed identically across all datasets as:

$$\text{NLL} = \frac{1}{T_a} \sum_{t = a_{\text{start}}}^{a_{\text{end}} - 1} \left(-\log \text{softmax}(v_{t-1})_{x_t}\right), \tag{9}$$

where $x_t$ is the target answer token at position $t$, $v_{t-1} \in \mathbb{R}^{V}$ is the model's raw logit vector predicting token $t$, and $T_a$ is the answer token length.

### D. Model Training and Cross-Validation

All in-domain evaluations use 5-fold `GroupKFold` so that paired answers or multi-sentence passages sharing a prompt or document never split across train and test folds (`0` group overlap). Inner probe regularization and inner out-of-fold ISP probabilities are computed strictly within each outer training fold. For pooled zero-shot transfer, `POOLED_DETS` is trained on the union of Datasets 1–5 (`18,141` rows) without seeing any row from Datasets 6–10.

### E. In-Domain Detection Evaluation

Each in-domain dataset is evaluated on full 4-sensor fusion, individual sensors (`ISP`, `AAS`, `EEM`, `DST`), leave-one-sensor-out ablations (`-ISP`, `-AAS`, `-EEM`, `-DST`), and low-FPR complementarity (`Recall@10% FPR` for ISP alone vs. union across all four sensors).

### F. Dataset-Artifact Control Experiments

Four CPU-only artifact controls are executed on identical 5-fold `GroupKFold` splits using saved checkpoints and aligned answer texts: (1) **1D Answer Length (`LEN`)** logistic regression; (2) **Answer-Text TF-IDF** (word 1–2 grams + character `char_wb` 3–5 grams, `15,000` features each, L2 logistic regression on answer text alone with zero LLM and zero prompt); (3) **Shuffled-Label Control** (randomly flipping pair labels to verify zero leakage); and (4) **Length-Matched Subsets** restricting paired benchmarks to pairs whose answer token lengths differ by at most `2` tokens (`|ΔL| ≤ 2`), comparing TRUEGUARD against `LEN` and `TF-IDF` (evaluated both from full OOF predictions and refitted strictly inside the length-matched subset) with paired group-level bootstrap 95% confidence intervals (`B = 1,000`).

### G. Zero-Shot Cross-Domain Evaluation

The pooled source detector (`Datasets 1–5`) is applied unchanged to Datasets 6–9 and to TriviaQA test generations (`TRUEGUARD_Pooled_ZeroShot`). To diagnose zero-shot failure, we measure (i) target 5-fold ISP AUROC, (ii) pooled fusion standardized weights, (iii) within-domain split-half probe weight cosine similarity versus cross-domain cosine similarity both on full datasets and under strictly **equal sample size (`N_fit = 900` per half, 3 seeds × 4 layers)** compared against the theoretical random 2,048-d Gaussian null (`0.0000 ± 0.0221`), and (iv) **length-controlled EEM AUROC** within four answer-length quartiles and on length-matched pairs (`|ΔL| ≤ 2`) alongside Spearman $\rho(\text{EEM}_{\text{mean}}, \text{LEN})$.

### H. Target-Domain Few-Shot Refitting

Because Phase 3 trains fresh target-domain probes from scratch without transferring any source-trained probe weights, we refer to this procedure strictly as **Target-Domain Few-Shot Refitting (Target-Only Probe Training)**. Each of the four unseen benchmarks is split 60/40 into a group-disjoint adaptation pool and held-out test set (`random_state = 2026`, `0` group overlap). Across `10` fixed seeds (`0..9`), `K ∈ {50, 100, 250}` grouped labeled examples are sampled from the 60% pool to fit fresh TRUEGUARD probes and fusion classifiers, evaluated on the fixed 40% test set. Exact zero-shot baselines are read directly from the Colab `.npz` prediction arrays (avoiding a `0.0005–0.0081` local `scikit-learn 1.3.2` vs. Colab `1.6.1` unpickling drift identified by our independent audit). Target-only TRUEGUARD is compared directly against four baselines trained on the exact same `K` examples: **Source Risk Recalibration (`SrcRecal`)**, **1D EEM Calibrated**, **1D Length (`LEN`)**, and **Answer-Text TF-IDF** (zero LLM). Because these four benchmarks were previously inspected during zero-shot failure diagnosis, the 40% splits validate target-only sample efficiency on unseen groups rather than serving as unexamined external confirmation.

### I. Baseline Methods

Internal baselines include `ISP-only` (internal SAPLMA-style multi-layer probe proxy [@review27]), `Scalars-only` (`AAS+EEM+DST`), `Predictive Entropy` (`ENT_mean`), and token-length-normalized `NLL`. On TriviaQA (`n_cal = 250`, `n_test = 250`), we additionally reproduce two published external multi-sample baselines on the exact same frozen TinyLlama model and `250` held-out questions (`M = 10` stochastic samples at `T = 0.7`, `top_p = 0.9`):

- **SelfCheckGPT-NLI** [@review21]: Uses official `potsawee/deberta-v3-large-mnli` (`{0: entailment, 1: contradiction}`) with exact `(greedy_answer, sample_m)` ordering averaged over `M = 10` samples. *Documented deviations:* TriviaQA answers are short single-sentence phrases (mean `13.98` words, `0` empty), so each answer is scored as one sentence; NLI inference ran in `float16`.
- **Semantic Entropy** [PENDING_APPROVAL: kuhn2023semantic], [PENDING_APPROVAL: farquhar2024detecting]: Uses official `microsoft/deberta-large-mnli` (`{0: contradiction, 1: neutral, 2: entailment}`, `float32`) over `M = 10` samples with case-insensitive exact-duplicate fast-path clustering and both length-normalized log-likelihood (`SE_LN`) and discrete (`SE_Disc`) formulations. *Documented deviation:* Uses Farquhar et al.'s relaxed bidirectional entailment clustering rule (neither direction contradicts and at least one entails) rather than Kuhn et al.'s stricter both-directions-entail rule.

### J. TriviaQA Selective Prediction

For the closed-book TriviaQA selective-prediction experiment (`n_cal = 250`, `n_test = 250`, disjoint question sets), TRUEGUARD's four-layer ISP probes, logistic fusion layer, and risk thresholds ($\tau_{\text{warning}} = 0.5973$, $\tau_{\text{fault}} = 0.8415$) were **fitted from scratch using the `250` labeled calibration generations** (`det_tqa.fit(F_cal, H_cal, y_cal)`), with zero access to test labels. For direct zero-shot comparison without target supervision, `TRUEGUARD_Pooled_ZeroShot` is evaluated unchanged on the same `250` test questions. All external and uncertainty baselines (`SelfCheckGPT-NLI`, `Semantic Entropy`, `Predictive Entropy`, `NLL`) are **completely label-free for ranking** (`AUROC`, `AUPRC`, `AURC`, `Acc@46%`) and use the `250` calibration labels solely to choose a scalar Youden's J cutoff for binary `F1`. Mitigation results separate (1) risk detection, (2) selective answering (`AURC`), (3) pure selective abstention at matched `46.0%` coverage (`115/250`), and (4) the full three-tier controller intervention ablation (`Tier 1 + Tier 2 + Tier 3`).

### K. Evaluation Metrics

Discrimination is measured by `AUROC` and `AUPRC`; binary operating performance by `Precision`, `Recall`, and `F1`; probability calibration by Expected Calibration Error (`ECE`, 15 bins) and Brier score; and selective prediction by Area Under the Risk–Coverage Curve (`AURC`, lower is better) and selective accuracy at matched coverage (`Acc@46%`, `Acc@50%`).

### L. Statistical Evaluation

In-domain 95% confidence intervals use `500` group-level bootstrap resamples. TriviaQA 95% confidence intervals and paired two-sided `p`-values use $B = 1{,}000$ paired bootstrap resamples with the finite-sample bound:

$$p_{\text{boot}} = \frac{1 + 2 \min(n_{\le 0},\, n_{\ge 0})}{B + 1}, \tag{10}$$

where $n_{\le 0}$ and $n_{\ge 0}$ count bootstrap resamples with non-positive and non-negative metric differences, respectively ($p_{\text{boot}} \ge 0.0010$), Holm-Bonferroni adjusted across the `6` head-to-head TriviaQA comparisons ($p_{\text{Holm}} \ge 0.0060$). For 10-seed refitting (`Table IV`), means and standard deviations quantify adaptation-sample draw variance over a fixed 40% test set [PENDING_APPROVAL: nadeau2003inference]; small differences within test-set bootstrap uncertainty are reported as practically comparable. An independent zero-import audit script (`independent_reproducibility_audit.py`) verified all saved metrics to $1.11 \times 10^{-16}$.

### M. Implementation and Hardware

Main extraction, cross-validation, TriviaQA mitigation, latency profiling, and external baselines were executed on Google Colab NVIDIA T4 GPUs (`16 GB` VRAM, PyTorch + HuggingFace Transformers, `seed = 42`). Controlled sequential latency (`real_latency.json`) was measured on `25` prompts × `24` forced tokens (`attn_implementation="eager"`, `batch_size = 1`). All reviewer artifact controls, target-refitting comparisons, and cosine diagnostics ran strictly on CPU from saved `.npz` checkpoints.

---

## V. RESULTS AND ANALYSIS

### A. In-Domain Hallucination Detection

Across the five in-domain benchmarks (Table II), TRUEGUARD achieves `0.9218` AUROC on HaluEval-Dialogue, `0.9880` on HaluEval-QA, `0.9936` on HaluEval-Summarization, `0.8773` on TruthfulQA, and `0.7204` (`0.3868` AUPRC, `2.1×` random baseline at `18.1%` prevalence) on HaluEval-General, with well-calibrated probabilities (`ECE = 0.0055–0.0251`). Representative ROC curves are shown in Fig. 2. Across every dataset, `ISP-only` (`0.7225–0.9936`) matches 4-sensor fusion within `±0.0021` AUROC.

**TABLE II**  
**IN-DOMAIN 5-FOLD GROUP-PRESERVING CV WITH DATASET-ARTIFACT CONTROLS**  
*(Sources: `Table2_InDomain_5Fold_GroupCV.md`, `final_pre_manuscript_checks.json`)*

| Dataset | Rows | TRUEGUARD AUROC [95% CI] | ISP-Only | ECE | LEN CV | Answer TF-IDF | Shuffled Label | LM (`\|ΔL\|≤2`) `n` (`%`) | LM: TG [95% CI] | LM: TF-IDF [95% CI] | LM: $\Delta$ (`p_boot`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `halueval_dialogue` | 4,000 | **0.9218** [0.915, 0.929] | 0.9221 | 0.0220 | 0.7087 | 0.8618 | 0.5072 | 1,352 (33.8%) | **0.7996** [0.782, 0.818] | 0.7167 [0.697, 0.737] | **`+0.0829`** (`0.0010`) |
| `halueval_qa` | 4,000 | **0.9880** [0.984, 0.991] | 0.9880 | 0.0095 | **0.9572** | **0.9661** | 0.4894 | 256 (6.4%) | **0.7901** [0.744, 0.837] | 0.7440 [0.693, 0.794] | **`+0.0461`** (`0.0350`) |
| `halueval_summarization` | 4,000 | **0.9936** [0.992, 0.995] | 0.9936 | 0.0099 | 0.4902 | **0.9539** | 0.4971 | 3,546 (88.6%) | **0.9939** [0.992, 0.995] | 0.9608 [0.955, 0.966] | **`+0.0331`** (`0.0010`) |
| `truthful_qa` | 1,634 | **0.8773** [0.861, 0.894] | 0.8772 | 0.0251 | 0.5510 | 0.8064 | 0.4928 | 714 (43.7%) | **0.8106** [0.782, 0.840] | 0.7394 [0.707, 0.772] | **`+0.0712`** (`0.0010`) |
| `halueval_general` | 4,507 | **0.7204** [0.702, 0.740] | 0.7225 | 0.0055 | 0.5089 | 0.6944 | 0.5123 | N/A | N/A | N/A | N/A |

> **FIGURE 2.** Representative in-domain 5-fold group-preserving ROC curves for TRUEGUARD and individual sensors on (a) HaluEval-QA (`Fig5a_ROC_HaluEval_QA.png`), (b) TruthfulQA (`Fig5b_ROC_TruthfulQA.png`), and (c) HaluEval-General (`Fig5c_ROC_HaluEval_General.png`). *(Verified 300-DPI PNGs in `publication_ready/figures/`.)*

### B. Dataset-Artifact Controls

Table II exposes substantial dataset artifacts in HaluEval. On **HaluEval-QA**, 1D answer length alone reaches `0.9572` AUROC and answer-text `TF-IDF` (zero LLM, zero context) reaches `0.9661`; only `6.4%` (`128` pairs) have answer lengths within `±2` tokens. When length is matched (`LEN ≈ 0.5516`), TRUEGUARD drops by `19.8` percentage points (`0.9880 → 0.7901`). On **HaluEval-Summarization**, length is uninformative (`0.4902`), yet answer-text `TF-IDF` alone reaches `0.9539` (`0.9608` on length-matched pairs), demonstrating strong surface-style differences between reference and synthetically hallucinated summaries. High raw AUROCs (`0.9880–0.9936`) on HaluEval therefore do **not** alone establish generalizable factual hallucination understanding.

Crucially, however, genuine above-surface signal remains after these controls. Shuffled-label AUROCs stay at chance (`0.4894–0.5123`), confirming zero leakage. Across all five full datasets, TRUEGUARD beats answer-text `TF-IDF` by `+0.0219` to `+0.0709` AUROC. Under strict length matching (`|ΔL| ≤ 2` tokens), TRUEGUARD significantly outperforms `TF-IDF` on all four paired benchmarks—by `+0.0829` on HaluEval-Dialogue (`p = 0.0010`), `+0.0461` on HaluEval-QA (`p = 0.0350`), `+0.0331` on HaluEval-Summarization (`p = 0.0010`), and `+0.0712` on TruthfulQA (`p = 0.0010`)—with virtually identical margins when `TF-IDF` is refitted strictly inside each length-matched subset (`0.7072`, `0.7322`, `0.9586`, `0.7501`).

### C. Four-Sensor Ablation Study

Leave-one-sensor-out ablations (Table III; Fig. 3) confirm that **ISP is the dominant in-domain signal**. Removing ISP reduces AUROC by `-0.0584` to `-0.2709` across the five datasets, whereas removing AAS, EEM, or DST changes in-domain AUROC by at most `0.0018`. In the pooled source fusion model (`phase2_cross_domain_diagnostics.json`), standardized `ISP_logit` receives weight `+2.9353` (`>96%` of total magnitude), compared with `|w| ≤ 0.0680` for all six scalar features. Four-sensor fusion therefore does **not** consistently outperform ISP-only in AUROC. Auxiliary sensors contribute primarily through low-FPR unique detections (`Union Recall@10% FPR` rises from `0.348` to `0.529` on HaluEval-General, `+18.1%`) and as unsupervised/low-`K` fallbacks when ISP fails under domain shift.

**TABLE III**  
**LEAVE-ONE-SENSOR-OUT ABLATION AND LOW-FPR COMPLEMENTARITY**  
*(Source: `publication_ready/tables/Table4_FourSensor_Ablation_and_Complementarity.md`)*

| Dataset | Full (4) | `-ISP` ($\Delta$) | `-AAS` ($\Delta$) | `-EEM` ($\Delta$) | `-DST` ($\Delta$) | ISP Rec@10%FPR | Union Rec@10%FPR | Unique AAS / EEM / DST |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `halueval_dialogue` | 0.9218 | 0.7249 (`-0.1968`) | 0.9218 (`0.0000`) | 0.9220 (`+0.0002`) | 0.9219 (`0.0000`) | 0.778 | 0.817 | 0.005 / 0.015 / 0.015 |
| `halueval_qa` | 0.9880 | 0.9296 (`-0.0584`) | 0.9880 (`0.0000`) | 0.9880 (`-0.0001`) | 0.9880 (`0.0000`) | 0.976 | 0.984 | 0.001 / 0.003 / 0.004 |
| `halueval_summarization` | 0.9936 | 0.7233 (`-0.2709`) | 0.9935 (`-0.0001`) | 0.9936 (`+0.0001`) | 0.9936 (`0.0000`) | 0.987 | 0.990 | 0.002 / 0.001 / 0.001 |
| `truthful_qa` | 0.8773 | 0.6073 (`-0.2694`) | 0.8772 (`0.0000`) | 0.8778 (`+0.0005`) | 0.8767 (`-0.0006`) | 0.575 | 0.640 | 0.015 / 0.006 / 0.032 |
| `halueval_general` | 0.7204 | 0.6226 (`-0.0981`) | 0.7207 (`+0.0003`) | 0.7222 (`+0.0018`) | 0.7205 (`+0.0001`) | 0.348 | 0.529 | 0.066 / 0.049 / 0.054 |

> **FIGURE 3.** Leave-one-sensor-out ablation on imbalanced HaluEval-General (`Fig6_Ablation_HaluEval_General.png`), showing ISP dominance in AUROC alongside low-FPR complementarity from auxiliary sensors. *(Verified 300-DPI PNG in `publication_ready/figures/`.)*

### D. Zero-Shot Cross-Domain Performance

When the pooled source detector trained on Datasets 1–5 is transferred zero-shot to Datasets 6–9, performance collapses to near-chance across every benchmark (exact Colab `.npz` test AUROCs on the 40% splits): **FaithDial `0.4929`**, **WikiBio-GPT3 `0.4883`**, **XSum-Factuality `0.4597`**, and **FEVER `0.5205`** (with poor calibration, `ECE = 0.3419–0.6574`). Even within the five in-domain datasets (Fig. 4), cross-dataset transfer degrades substantially relative to in-domain CV. Crucially, frozen TinyLlama hidden states do retain target-domain linear separability—target 5-fold ISP AUROC reaches `0.8927` on FaithDial, `0.8754` on FEVER, `0.7427` on WikiBio-GPT3, and `0.6794` on XSum-Factuality—demonstrating that zero-shot collapse stems from domain-dependent probe orientation rather than absent internal signal.

> **FIGURE 4.** In-domain 5×5 cross-dataset transfer AUROC matrix (`Fig4_InDomain_5x5_Transfer_Matrix.png`), showing strong diagonal in-domain performance and sharp off-diagonal degradation across tasks. *(Verified 300-DPI PNG in `publication_ready/figures/`.)*

### E. Target-Domain Few-Shot Refitting

Table IV and Fig. 5 present **Target-Domain Few-Shot Refitting (Target-Only Probe Training)** across `K ∈ {50, 100, 250}` (`10` seeds, `<2 s` CPU per refit). Three findings stand out. First, **Source Risk Recalibration (`SrcRecal`)** remains at chance (`0.4957–0.5242`) on every dataset and `K`, confirming zero recoverable transfer from pooled source probabilities. Second, **at `K = 50`, simple baselines outperform 2,048-dimensional target-only probes on all four targets**: `1D EEM` leads on FaithDial (`0.7473` vs. `0.6987`) and XSum (`0.6082` vs. `0.5401`), while answer-text `TF-IDF` leads on WikiBio (`0.5321` vs. `0.5088`) and FEVER (`0.5699` vs. `0.5394`). Third, **at `K = 250`, gains are task-dependent**: target-only TRUEGUARD clearly outperforms all simple baselines on FaithDial (`0.8231`, `+0.0758` over `1D EEM`, `+0.1616` over `TF-IDF`), FEVER (`0.7325`, `+0.1010` over `TF-IDF`), and WikiBio (`0.6698`, `+0.0595` over `TF-IDF`) while cutting ECE by `82–93%`, **whereas on XSum-Factuality TRUEGUARD (`0.6456`) approximately matches the 1D answer-length baseline (`0.6445`)**.

**TABLE IV**  
**TARGET-DOMAIN FEW-SHOT REFITTING (TARGET-ONLY PROBE TRAINING) VS. SOURCE RECALIBRATION AND SIMPLE BASELINES**  
*(Source: `publication_ready/tables/Table3_TargetDomain_FewShot_Refitting.md`)*

| Target Dataset (40% Test) | Zero-Shot Exact | `K` | Target-Only TG (10 seeds) | Source Risk Recal. | 1D EEM Cal. | 1D Length (`LEN`) | Answer TF-IDF | `K=250` ECE (ZS ECE) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `faithdial` | 0.4929 | 50 | 0.6987 ± 0.0881 | 0.4957 ± 0.0060 | **0.7473** ± 0.0000 | 0.6721 ± 0.0000 | 0.5818 ± 0.0406 | — |
| `faithdial` | 0.4929 | 100 | **0.7899** ± 0.0313 | 0.5029 ± 0.0069 | 0.7473 ± 0.0000 | 0.6721 ± 0.0000 | 0.6145 ± 0.0249 | — |
| `faithdial` | 0.4929 | 250 | **0.8231** ± 0.0121 | 0.5043 ± 0.0060 | 0.7473 ± 0.0000 | 0.6721 ± 0.0000 | 0.6615 ± 0.0187 | **0.0443** (0.6574) |
| `wikibio_gpt3` | 0.4883 | 50 | 0.5088 ± 0.0562 | 0.4977 ± 0.0121 | 0.5000 ± 0.0235 | 0.4909 ± 0.0470 | **0.5321** ± 0.0274 | — |
| `wikibio_gpt3` | 0.4883 | 100 | 0.4939 ± 0.0840 | 0.4977 ± 0.0121 | 0.5045 ± 0.0231 | 0.4727 ± 0.0384 | **0.5785** ± 0.0395 | — |
| `wikibio_gpt3` | 0.4883 | 250 | **0.6698** ± 0.0381 | 0.5023 ± 0.0121 | 0.4955 ± 0.0231 | 0.4909 ± 0.0470 | 0.6103 ± 0.0290 | **0.0737** (0.4336) |
| `xsum_factuality` | 0.4597 | 50 | 0.5401 ± 0.0686 | 0.5000 ± 0.0425 | **0.6082** ± 0.0855 | 0.5867 ± 0.1218 | 0.5329 ± 0.0457 | — |
| `xsum_factuality` | 0.4597 | 100 | 0.6058 ± 0.0430 | 0.5242 ± 0.0340 | 0.6352 ± 0.0000 | **0.6445** ± 0.0000 | 0.5331 ± 0.0370 | — |
| `xsum_factuality` | 0.4597 | 250 | **0.6456** ± 0.0410 | 0.5161 ± 0.0389 | 0.6352 ± 0.0000 | **0.6445** ± 0.0000 | 0.5456 ± 0.0323 | **0.0383** (0.5629) |
| `fever` *(claim verif.)* | 0.5205 | 50 | 0.5394 ± 0.0482 | 0.5123 ± 0.0173 | 0.5176 ± 0.0425 | 0.4977 ± 0.0117 | **0.5699** ± 0.0183 | — |
| `fever` *(claim verif.)* | 0.5205 | 100 | **0.6195** ± 0.0395 | 0.5000 ± 0.0216 | 0.5264 ± 0.0371 | 0.4955 ± 0.0110 | 0.5966 ± 0.0224 | — |
| `fever` *(claim verif.)* | 0.5205 | 250 | **0.7325** ± 0.0136 | 0.5000 ± 0.0216 | 0.5264 ± 0.0371 | 0.5045 ± 0.0110 | 0.6315 ± 0.0104 | **0.0430** (0.3419) |

> **FIGURE 5.** Target-domain few-shot refitting (`K = 50, 100, 250`, 10 seeds) compared with zero-shot unrefitted TRUEGUARD, source risk recalibration, `1D EEM`, `1D LEN`, and answer-text `TF-IDF` across four group-disjoint 40% test sets (`Fig2_TargetDomain_FewShot_Refitting_vs_Baselines.png`). *(Verified 300-DPI PNG in `publication_ready/figures/`.)*

### F. Cross-Domain Probe Diagnostics

Because random unit vectors in `2,048` dimensions naturally have near-zero cosine similarity (`0.0000 ± 0.0221`), cross-domain cosines alone are uninformative without a within-domain stability baseline. Table V and Fig. 6(a) compare within-domain split-half probe weight cosines against cross-domain cosines. On full datasets, within-domain split-half cosines reach `+0.2300` to `+0.6888` on homogeneous benchmarks (`10–31×` the random-noise standard deviation), whereas cross-domain cosines against the pooled source probe fall between `-0.0306` and `+0.0510`. To eliminate sample-size confounding, our equal-sample-size control (`N_fit = 900` per half, 3 seeds × 4 layers) confirms the exact same pattern: within-domain cosines remain `+0.1125` (XSum) to `+0.6707` (HaluEval-Summ), whereas cross-domain cosines (`HaluEval → Target`) remain centered on zero (`-0.0151 ± 0.0263` FaithDial, `+0.0032 ± 0.0176` WikiBio, `+0.0204 ± 0.0381` FEVER, `+0.0092 ± 0.0249` XSum). Although L2-regularized coefficients in correlated high-dimensional spaces cannot be interpreted as unique causal axes, this contrast provides clear empirical diagnostic evidence of domain-dependent linear decision boundaries.

**TABLE V**  
**EMPIRICAL DOMAIN-SHIFT DIAGNOSTICS: PROBE ALIGNMENT AND LENGTH-CONTROLLED EEM**  
*(Sources: `Table8_CrossDomain_Diagnostics_Cosine_and_LengthControlled_EEM.md`, `final_pre_manuscript_checks.json`)*

| Dataset | Within-Domain Split-Half Cos (Full) | Within-Domain Cos (`N=900`) | Cross-Domain Cos (Pool / `N=900`) | Raw `EEM_mean` AUROC | Spearman `ρ(EEM, LEN)` | Within-Quartile Mean EEM | LM (`\|ΔL\|≤2`) EEM |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `halueval_summarization` | +0.6888 ± 0.0132 | +0.6707 ± 0.0129 | — (source) | 0.5787 | -0.0658 | 0.5331 | 0.5770 |
| `halueval_qa` | +0.4358 ± 0.0246 | +0.4999 ± 0.0363 | — (source) | **0.3627** | **-0.2909** | 0.4465 | **0.5184** |
| `halueval_dialogue` | +0.3929 ± 0.0379 | +0.3930 ± 0.0280 | — (source) | **0.3740** | -0.1038 | **0.3795** | **0.4525** |
| `truthful_qa` | +0.3440 ± 0.0269 | — | — (source) | 0.4912 | -0.3678 | 0.4720 | 0.5030 |
| `halueval_general` | +0.0506 ± 0.0252 | — | — (source) | 0.4829 | -0.1637 | 0.4545 | N/A |
| `fever` | +0.3680 ± 0.0212 | +0.2668 ± 0.0189 | +0.0510 / +0.0204 | 0.5417 | -0.4285 | 0.5547 | N/A |
| `faithdial` | +0.2300 ± 0.0206 | +0.2205 ± 0.0168 | -0.0306 / -0.0151 | **0.7456** | **+0.0058** | **0.7662** | N/A |
| `wikibio_gpt3` | +0.1290 ± 0.0224 | +0.1282 ± 0.0318 | -0.0045 / +0.0032 | 0.5207 | -0.2348 | 0.5278 | N/A |
| `xsum_factuality` | +0.1073 ± 0.0272 | +0.1125 ± 0.0295 | +0.0280 / +0.0092 | **0.6648** | **-0.0321** | **0.6648** | N/A |
| *Random 2048-d Null* | *0.0000 ± 0.0221* | *0.0000 ± 0.0221* | *0.0000 ± 0.0221* | *0.5000* | *0.0000* | *0.5000* | *0.5000* |

> **FIGURE 6.** Empirical domain-shift diagnostics (`Fig8_CrossDomain_Diagnostics_Cosine_and_LengthControlled_EEM.png`): (a) within-domain split-half vs. cross-domain ISP probe weight cosine similarity relative to the 2,048-d random noise band; (b) raw vs. length-controlled `EEM_mean` AUROC across nine benchmarks. *(Verified 300-DPI PNG in `publication_ready/figures/`.)*

### G. Length-Controlled Entropy Analysis

Raw sensor AUROCs (Fig. 7) show an apparent sign reversal in `EEM_mean` between synthetic HaluEval (`0.3627` QA, `0.3740` Dialogue) and natural FaithDial (`0.7456`) and XSum (`0.6648`). Length-controlled analysis (Table V, Fig. 6(b)) refines this observation into three distinct regimes: (1) on **FaithDial** ($\rho = +0.0058$, quartile-mean `0.7662`) and **XSum** ($\rho = -0.0321$, quartile-mean `0.6648`), positive EEM signal is completely independent of answer length; (2) on **HaluEval-QA**, `EEM_mean` correlates negatively with length ($\rho = -0.2909$), and matching length (`|ΔL| ≤ 2`) eliminates the inversion (`0.3627 → 0.5184`); and (3) on **HaluEval-Dialogue**, the inverse association persists within length quartiles (`0.3795`) and partially under length matching (`0.4525`).

> **FIGURE 7.** Raw unsupervised sensor AUROCs across nine teacher-forced benchmarks (`Fig1_Sensor_Sign_Inversion_9Datasets.png`), illustrating domain-dependent signal polarity between synthetic HaluEval and natural dialogue/summarization datasets. *(Verified 300-DPI PNG in `publication_ready/figures/`.)*

### H. Comparison With Existing Detection Methods

Table VI and Fig. 8 compare TRUEGUARD against reproduced external and uncertainty baselines on the exact same `250` held-out TriviaQA generations, explicitly distinguishing supervision settings. Target-refitted single-pass `TRUEGUARD_4sensor` (`K = 250` calibration labels) achieves `0.7876` AUROC (`95% CI [0.720, 0.852]`) and `0.4360` AURC (`[0.360, 0.523]`), significantly outperforming label-free `M = 10` Semantic Entropy (`0.6859` LN / `0.6856` Disc AUROC, `p_Holm = 0.012`; `0.5411` AURC, `p_Holm = 0.006`), label-free Predictive Entropy (`0.6583`, `p_Holm = 0.006`), and label-free NLL (`0.4678`, `p_Holm = 0.006`). Compared with label-free `M = 10` SelfCheckGPT-NLI (`0.7477` AUROC, `0.4659` AURC, `0.8537` AUPRC), TRUEGUARD's observed AUROC (`+0.0399`) and AURC (`-0.0299`) gains are not statistically significant (`p_Holm = 0.478 / 0.362`), while SelfCheckGPT-NLI achieves slightly higher AUPRC (`0.8537` vs. `0.8460`). Crucially, without TriviaQA labels, `TRUEGUARD_Pooled_ZeroShot` drops to `0.5504` AUROC (`0.6342` AURC), trailing every label-free baseline except NLL. Forensic inspection confirmed that NLL's `0.4678 [0.396, 0.542]` AUROC is genuine (`100%` non-negative, `r(NLL, ENT) = +0.6698`), occurring because TinyLlama-1.1B assigns slightly lower mean NLL to fluent hallucinated answers (`0.7711 ± 0.2003`) than to terse correct factual entities (`0.7991 ± 0.2370`).

**TABLE VI**  
**HEAD-TO-HEAD COMPARISON AGAINST EXTERNAL BASELINES ON IDENTICAL 250 TRIVIAQA TEST QUESTIONS (SUPERVISION-DISTINGUISHED)**  
*(Source: `publication_ready/tables/Table7_External_Baselines_TriviaQA.md`)*

| Method (`n_cal=250, n_test=250`) | Supervision / Target Labels | LLM Gens/Q | Extra Model | AUROC [95% CI] | AUPRC | F1 (Cal Thr) | AURC [95% CI] | Acc@46% | $\Delta$AUROC (`p_Holm`) | $\Delta$AURC (`p_Holm`) |
| :--- | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TRUEGUARD_4sensor** | Supervised (250 cal) | 1 | None | **0.7876** [0.720, 0.852] | 0.8460 | **0.8084** | **0.4360** [0.360, 0.523] | **55.6%** | — | — |
| **TRUEGUARD_ISP_only** | Supervised (250 cal) | 1 | None | 0.7706 [0.701, 0.834] | 0.8476 | 0.8062 | 0.4473 [0.369, 0.532] | 53.9% | +0.0170 (`0.478`) | -0.0113 (`0.451`) |
| **TRUEGUARD_Pooled_ZS** | Zero-Shot (0 target) | 1 | None | 0.5504 | 0.7124 | — | 0.6342 | 37.4% | +0.2372 | -0.1982 |
| **SelfCheckGPT_NLI** | Label-Free (0 rank; 250 thr) | 11 | DeBERTa-v3-L | 0.7477 [0.681, 0.812] | **0.8537** | 0.5920 | 0.4659 [0.385, 0.559] | 50.4% | +0.0399 (`0.478`) | -0.0299 (`0.362`) |
| **Semantic_Entropy_LN** | Label-Free (0 rank; 250 thr) | 10 | DeBERTa-L | 0.6859 [0.621, 0.756] | 0.8059 | 0.6377 | 0.5411 [0.450, 0.627] | 49.6% | **+0.1017 (`0.012`)** | **-0.1051 (`0.006`)** |
| **Semantic_Entropy_Disc** | Label-Free (0 rank; 250 thr) | 10 | DeBERTa-L | 0.6856 [0.620, 0.753] | 0.8025 | 0.6403 | 0.5414 [0.452, 0.629] | 48.7% | **+0.1020 (`0.012`)** | **-0.1054 (`0.006`)** |
| **Predictive_Entropy** | Label-Free (0 rank; 250 thr) | 1 | None | 0.6583 [0.587, 0.730] | 0.7471 | 0.5985 | 0.5309 [0.448, 0.617] | 45.2% | **+0.1293 (`0.006`)** | **-0.0949 (`0.006`)** |
| **NLL (Length-Norm.)** | Label-Free (0 rank; 250 thr) | 1 | None | 0.4678 [0.396, 0.542] | 0.6453 | 0.5423 | 0.6843 [0.603, 0.760] | 31.3% | **+0.3198 (`0.006`)** | **-0.2483 (`0.006`)** |

> **FIGURE 8.** Risk–coverage selective prediction curves on the `250` held-out TriviaQA test questions comparing target-refitted TRUEGUARD with label-free `SelfCheckGPT-NLI`, `Semantic Entropy`, `Predictive Entropy`, and `NLL` (`Fig7_External_Baselines_RiskCurve.png`). *(Verified 300-DPI PNG in `publication_ready/figures/`.)*

### I. Selective Prediction and Abstention

Table VII and Fig. 9 separate risk detection, selective answering, abstention-driven error reduction, and active correction on the `250` TriviaQA test questions (`34.00%` baseline greedy accuracy, `66.00%` hallucination rate). At `46.0%` coverage (`115/250` answered), **pure selective abstention** (answering the `115` lowest-risk questions) achieves **`64/115` (`55.65%`) selective accuracy**, reducing system-wide incorrect outputs from `66.00%` to `20.40%`. By contrast, the **full three-tier controller** (`81` Safe, `23` Tier-1 Resample, `11` Tier-2 Wikipedia Retrieval, `135` Tier-3 Abstain) achieves **`63/115` (`54.78%`, `-0.87%`)** selective accuracy (`20.80%` system-wide incorrect outputs). Forensically, active Tier 1/2 interventions repaired `4` originally incorrect answers (`2` via resampling, `2` via Wikipedia retrieval) while changing `3` originally correct greedy answers into incorrect ones, a net difference of one question. **No measurable benefit from the active intervention tiers was established on this test set**; risk-based selective abstention is the primary demonstrated mitigation mechanism.

**TABLE VII**  
**TRIVIAQA CLOSED-BOOK SELECTIVE ABSTENTION VS. FULL THREE-TIER CONTROLLER INTERVENTION ABLATION (`n_test = 250`)**  
*(Source: `publication_ready/tables/Table5_TriviaQA_SelectiveAbstention_and_Mitigation.md`)*

| System / Method | Role | AUROC | AURC [95% CI] | Coverage | Correct / Answered | Selective Acc. | System Halluc. | Active Fixed / Broken |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Greedy Baseline | Unfiltered baseline | — | — | 100.0% (250/250) | 85 / 250 | 34.00% | 66.00% | 0 / 0 |
| **TRUEGUARD Pure Abstain-Only** | **Primary selective abstention** | **0.7876** | **0.4360** [0.360, 0.524] | 46.0% (115/250) | **64 / 115** | **55.65%** | **20.40%** | 0 / 0 |
| TRUEGUARD Full 3-Tier Controller | Intervention ablation (T1+T2+T3) | 0.7876 | — (fixed pt) | 46.0% (115/250) | 63 / 115 | 54.78% (`-0.87%`) | 20.80% | 4 fixed / 3 broken |
| TRUEGUARD ISP-Only (Abstain) | Single-sensor ablation | 0.7706 | 0.4473 [0.369, 0.532] | 46.0% (115/250) | 62 / 115 | 53.91% | 21.20% | 0 / 0 |
| Scalars-Only (Abstain) | No-ISP ablation | 0.7130 | 0.4891 [0.404, 0.577] | 46.0% (115/250) | 57 / 115 | 49.57% | 23.20% | 0 / 0 |
| Predictive Entropy (Abstain) | Uncertainty baseline | 0.6583 | 0.5309 [0.448, 0.617] | 46.0% (115/250) | 52 / 115 | 45.22% | 25.20% | 0 / 0 |
| Length-Norm. NLL (Abstain) | Likelihood baseline | 0.4678 | 0.6843 [0.603, 0.760] | 46.0% (115/250) | 36 / 115 | 31.30% | 31.60% | 0 / 0 |

> **FIGURE 9.** Matched-coverage selective prediction accuracy across coverage thresholds on TriviaQA (`Fig3_TriviaQA_Matched_Coverage_RiskCurve.png`), comparing TRUEGUARD 4-sensor fusion with ISP-only, scalars-only, predictive entropy, and length-normalized NLL. *(Verified 300-DPI PNG in `publication_ready/figures/`.)*

### J. Computational Efficiency

Under controlled sequential single-query decoding on a CUDA T4 GPU (`real_latency.json`: `attn_implementation="eager"`, `batch_size = 1`, `25` prompts × `24` forced tokens; Table VIII), vanilla TinyLlama averages `29.78 ms/token`. TRUEGUARD post-pass scoring averages `34.52 ms/token` (`+4.74 ms/token`, `+15.9%` overhead, `4.60×` faster than sequential 5-sample decoding at `158.77 ms/token`), and online per-token monitoring averages `37.84 ms/token` (`+8.06 ms/token`, `+27.1%` overhead, `4.20×` faster than sequential 5-sample decoding).

We explicitly disclose **protocol non-equivalence** with the external baseline Colab run, where `M = 10` samples were generated in parallel (`batch_size = 10`) using PyTorch's `sdpa` attention kernel with early EOS stopping (`0.6545 s/q` sampling + `0.0523 s/q` SelfCheckGPT NLI, omitting the initial greedy pass, totaling `0.7068 s/q`; `1.6622 s/q` for Semantic Entropy including `1.0078 s/q` bidirectional DeBERTa-large NLI and `2.47 GB` peak NLI VRAM). Therefore, **no direct wall-clock speedup over GPU-batched SelfCheckGPT-NLI is claimed**. TRUEGUARD's verified resource advantage is architectural (`1` LLM generation and `0` auxiliary 435M-parameter NLI models) and sequential (`4.20–4.60×` under matched `bs = 1` eager serving).

**TABLE VIII**  
**CONTROLLED SEQUENTIAL INFERENCE LATENCY PROFILING ON CUDA T4 (`eager`, `bs = 1`, `25 × 24` TOKENS)**  
*(Source: `publication_ready/tables/Table6_Inference_Latency_Profiling.md`)*

| Decoding Configuration | Mean Latency (ms/tok) | Overhead vs. Vanilla | Speedup vs. 5× Sequential |
| :--- | :---: | :---: | :---: |
| Vanilla TinyLlama-1.1B (Greedy) | 29.78 | — | 5.33× |
| TRUEGUARD Post-Pass Monitoring | 34.52 | +4.74 ms (+15.9%) | **4.60×** |
| TRUEGUARD Online Per-Token Monitoring | 37.84 | +8.06 ms (+27.1%) | **4.20×** |
| Sequential 5× Multi-Sample Baseline | 158.77 | +129.00 ms (+433.2%) | 1.00× |

---

## VI. DISCUSSION

### A. Interpretation of the Main Findings

Taken together, our experiments show that single-pass white-box hallucination detection on a small frozen LLM is neither a universal drop-in solution nor a mere benchmark mirage. Rather, its utility depends sharply on three factors: benchmark construction, target-domain supervision, and deployment objective. Within a fixed domain, linear probes over frozen hidden states capture meaningful error signals beyond surface length and `TF-IDF` features. Across domains, however, those linear boundaries do not transfer zero-shot, making lightweight target-domain refitting (`K ≈ 250`) essential whenever single-pass white-box detection is deployed on a new task.

### B. Effect of Benchmark Artifacts

Our Control A results provide a cautionary lesson for hallucination-detection evaluation. Because HaluEval-QA exhibits a massive length disparity (`LEN = 0.9572`) and HaluEval-Summarization exhibits strong stylistic cues (`TF-IDF = 0.9539`), reporting raw `0.988–0.994` AUROCs without surface baselines severely overstates factual error understanding. Requiring length-matched pair controls and answer-text `TF-IDF` baselines should become standard practice for teacher-forced hallucination benchmarks.

### C. Domain Shift and Detector Reliability

The contrast between within-domain split-half probe alignment (`+0.11` to `+0.67` at equal `N = 900`) and near-zero cross-domain alignment (`-0.015` to `+0.020`) explains why pooled white-box probes collapse on unseen benchmarks and why simple probability recalibration (`SrcRecal ≈ 0.50`) cannot rescue them. Moreover, because pooled fusion places `>96%` weight on ISP, auxiliary uncertainty sensors are suppressed even on natural datasets like FaithDial (`0.7456` raw EEM) and XSum (`0.6648` raw EEM) where EEM carries genuine length-free signal.

### D. Value and Limitations of Few-Shot Refitting

Target-domain few-shot refitting (`<2 s` CPU, zero source weights transferred) demonstrates a practical trade-off rather than uniform superiority. At `K = 50`, fitting `2,048`-dimensional linear probes overfits relative to `1D EEM` or `TF-IDF`. At `K = 250`, white-box refitting delivers clear gains on FaithDial, FEVER, and WikiBio, but merely matches `1D` length on XSum-Factuality. Practitioners deploying small LLMs should therefore benchmark target-refitted probes directly against `1D EEM`, `1D length`, and `TF-IDF` at their actual label budget.

### E. Selective Abstention Versus Active Correction

On closed-book TriviaQA, TinyLlama-1.1B achieves only `34.00%` baseline accuracy. Under this low parametric-knowledge regime, risk-calibrated selective abstention reliably cuts system-wide errors (`66.0% → 20.4%`, lifting answered accuracy to `55.65%`), whereas Tier 1 stochastic resampling and Tier 2 single-passage Wikipedia retrieval introduced almost as many regressions (`3` broken) as repairs (`4` fixed). Active self-repair without a strong verifier or high-recall RAG pipeline should not be assumed to beat pure abstention on 1B-class models.

### F. Practical Implications

For edge or latency-sensitive deployments using frozen small LLMs, our results suggest a concrete three-step recipe: (1) if zero target labels are available, avoid zero-shot supervised white-box probes and use `1D EEM` (single-pass) or `SelfCheckGPT-NLI` (if multi-sample compute is affordable); (2) if `~250` labeled target examples can be collected, refit a lightweight ISP/TRUEGUARD detector (`<2 s` CPU) for single-pass risk estimation without hosting an external NLI model; and (3) pair the calibrated risk score with **pure selective abstention** unless a stronger external grounding pipeline is validated to outperform abstention at matched coverage.

### G. Limitations and Threats to Validity

Several limitations bound our conclusions. First, all experiments evaluate a single small frozen model (`TinyLlama-1.1B-Chat-v1.0`); larger `7B–70B` models with higher parametric accuracy may exhibit stronger active Tier 1/2 repair rates and different cross-domain probe transfer. Second, the TriviaQA test set (`n_test = 250`) has limited statistical power to separate TRUEGUARD (`0.7876`) from SelfCheckGPT-NLI (`0.7477`, `p_Holm = 0.478`) or ISP-only (`0.7706`, `p_Holm = 0.478`). Third, on TriviaQA, TRUEGUARD used `250` labeled target calibration examples for supervised fitting, whereas `SelfCheckGPT-NLI` and `Semantic Entropy` were label-free for ranking. Fourth, the four unseen datasets were inspected during zero-shot diagnosis before designing target-only refitting. Fifth, unsupervised white-box methods such as CCS [PENDING_APPROVAL: burns2023discovering] and EigenScore/INSIDE [PENDING_APPROVAL: chen2024inside] were not reproduced on TinyLlama-1.1B. Finally, Datasets 1–9 use teacher-forced scoring of benchmark responses rather than free-form TinyLlama generations.

---

## VII. CONCLUSION AND FUTURE WORK

### A. Conclusion

This paper presented an empirical study of single-pass white-box hallucination detection, cross-domain failure, target-domain few-shot refitting, and selective prediction using the TRUEGUARD framework on frozen `TinyLlama-1.1B-Chat-v1.0` across ten benchmarks (`32,590` sequences). Rigorous artifact controls demonstrated that while raw HaluEval scores (`0.9880–0.9936`) are heavily inflated by length and surface style, white-box probing retains statistically significant gains over answer-text `TF-IDF` even under strict length matching (`0.7901–0.9939`, `p ≤ 0.035`), driven primarily by ISP. Zero-shot pooled transfer collapses to chance (`0.4597–0.5205`) due to domain-dependent linear decision boundaries verified under equal-sample-size cosine controls, whereas target-only few-shot refitting at `K = 250` yields task-dependent gains on FaithDial, FEVER, and WikiBio (while tying `1D` length on XSum and trailing simple baselines at `K = 50`). On closed-book TriviaQA, target-refitted single-pass TRUEGUARD (`0.7876` AUROC, `0.4360` AURC) significantly outperforms label-free `M = 10` Semantic Entropy and uncertainty baselines and matches label-free `M = 10` SelfCheckGPT-NLI without external NLI models, while forensic mitigation auditing establishes selective abstention (`55.65%`)—not active Tier 1/2 regeneration or retrieval (`54.78%`)—as the demonstrated mechanism of error reduction.

### B. Future Work

Future work should extend this controlled evaluation protocol to larger open-weight LLMs (`7B–70B`), expand closed-book test sets (`n ≥ 1,000`) for higher statistical power, investigate genuine source-to-target transfer methods (such as low-rank probe adaptation or unsupervised domain alignment) that outperform target-only refitting at `K ≤ 50`, benchmark unsupervised white-box detectors (CCS, EigenScore) under identical splits, and evaluate selective abstention alongside high-recall dense retrieval pipelines on models capable of reliable evidence synthesis.

---

## REFERENCES

*(Citations using `[@reviewXX]` map verbatim to the original 40-entry `E:\trueguard\ieee\overleaf\references.bib`, which remains untouched. Entries marked `[PENDING_APPROVAL: key]` are documented with verified metadata in `ADDITIONAL_REFERENCES_FOR_APPROVAL.md` for explicit author approval prior to LaTeX/BibTeX conversion. Sequential IEEE numerical citations `[1]`, `[2]`, ... will be generated automatically by `\bibliographystyle{IEEEtran}` upon LaTeX compilation.)*

---

## AUTHOR BIOGRAPHIES

**[Author 1 Name]** *(Placeholder — insert confirmed degree, institution, research interests, and IEEE membership grade prior to IEEE Access submission.)*

**[Author 2 Name]** *(Placeholder — insert confirmed degree, institution, research interests, and IEEE membership grade prior to IEEE Access submission.)*

**[Author 3 Name]** *(Placeholder — insert confirmed degree, institution, research interests, and IEEE membership grade prior to IEEE Access submission.)*
