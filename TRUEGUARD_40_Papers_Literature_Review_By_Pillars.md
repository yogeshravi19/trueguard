# Comprehensive 40-Paper Literature Review Classified by the Six Pillars

## 2. Literature Review — I

**Pillar 1 · Internal-state based detection.** Hallucination leaves a measurable geometric signature inside hidden transformer activations while the model writes.

*Table 1 — papers 1–8 of 40*

| Paper name | Author(s) & ID | Year | Method | Key contribution | Gap identified |
|:---|:---|:---:|:---|:---|:---|
| **Unsupervised Real-Time Hallucination Detection based on Internal States of LLMs** | Su et al. [1] | 2024 | MIND (Unsupervised Hidden Probing) | Formulated an unsupervised MLP probe over intermediate hidden states and released the HELM internal-state dataset. | Relies solely on hidden states; misses attention dispersion and logit energy; no closed-loop mitigation. |
| **Prompt-Guided Internal States for Hallucination Detection of LLMs** | Zhang et al. [2] | 2024 | PRISM (Prompt-Guided Probing) | Used truth-orienting prompt templates to align truthfulness subspaces across domains before linear probing. | Requires prompt wrapping; passive scoring only with no runtime repair or retrieval grounding. |
| **Detecting Hallucination in LLMs Through Deep Internal Representation Analysis** | Zhang et al. [5] | 2025 | MHAD (Hallucination-Aware Neurons) | Isolated hallucination-sensitive neurons at initial and final decoding steps via layer-wise linear probing. | Static feature concatenation without dynamic multi-sensor calibration or corrective feedback. |
| **HalluShift: Measuring Distribution Shifts Towards Hallucination Detection in LLMs** | Dasgupta et al. [13] | 2025 | HALLUSHIFT (Internal Distribution Shift) | Tracked layer-to-layer cosine and Wasserstein shifts in hidden states across autoregressive trajectories. | Captures macro drift but has modest power on short QA when used without supervised probes. |
| **HalluShift++: Bridging Language and Vision through Internal Representation Shifts** | Nath et al. [16] | 2025 | HALLUSHIFT++ (Hierarchical Shift) | Extended internal representation shift tracking to hierarchical vision-language hallucinations. | Focused on multimodal encoders; provides no closed-loop text retrieval or calibrated abstention. |
| **The Internal State of an LLM Knows When It's Lying** | Azaria & Mitchell [27] | 2023 | SAPLMA (Supervised Hidden Classifier) | Demonstrated that a lightweight classifier trained on middle-layer hidden activations separates true vs. false statements. | Evaluated on synthetic true/false statements; sensitive to domain and answer-length shifts without recalibration. |
| **Inference-Time Intervention: Eliciting Truthful Answers from a Language Model** | Li et al. [28] | 2023 | ITI (Activation Steering along Truthful Heads) | Shifted hidden activations along truthfulness directions during decoding to improve TruthfulQA accuracy. | Fixed steering strength can degrade fluency and cannot supply external facts when model knowledge is absent. |
| **Truth Forest: Toward Multi-Scale Truthfulness in LLMs through Intervention without Tuning** | Chen et al. [38] | 2024 | Truth Forest (Multi-Scale Orthogonal Probes) | Learned orthogonal truthfulness probes (Rap-O) across multiple scales to capture multidimensional truth directions. | Higher probe complexity; still limited to internal knowledge and lacks external retrieval fallback. |

## 2. Literature Review — II

**Pillar 2 · Uncertainty quantification and entropy-based methods.** Token probability dispersion, logit energy, and multi-sample semantic variance quantify when the model is guessing.

*Table 2 — papers 9–14 of 40*

| Paper name | Author(s) & ID | Year | Method | Key contribution | Gap identified |
|:---|:---|:---:|:---|:---|:---|
| **Semantic Energy: Detecting LLM Hallucination Beyond Entropy** | Ma et al. [4] | 2025 | Semantic Energy (Penultimate Logit Energy) | Measured Boltzmann-inspired energy over penultimate logits rather than post-softmax probabilities. | Operates only at the output layer; misses hidden-state truthfulness when the LLM states fluent misconceptions. |
| **Entropy Spike Detection and Self-Confidence Calibration for Hallucination Mitigation** | Anonymous [6] | 2025 | Z-Score Token Entropy Spike + RL Penalty | Detected abrupt token-entropy spikes during reasoning and penalized overconfident spikes during RL training. | Requires RL fine-tuning and lacks inference-time external evidence retrieval. |
| **Uncertainty Quantification for Hallucination Detection in LLMs: Foundations & Methodology** | Kang et al. [7] | 2025 | Epistemic vs. Aleatoric UQ Taxonomy | Formalized epistemic vs. aleatoric uncertainty for LLMs and benchmarked single-pass vs. sampling UQ. | Survey and analytical study; highlights 5x–20x latency bottleneck of multi-sample UQ without a closed-loop fix. |
| **Semantic Entropy Probes: Robust and Cheap Hallucination Detection in LLMs** | Han, Kossen et al. [14] | 2024 | SEPs (Linear Probes for Semantic Entropy) | Trained single-pass linear probes on hidden states to approximate multi-sample semantic entropy at near-zero overhead. | Single-signal approximation; does not integrate attention dispersal, temporal drift, or tiered mitigation. |
| **Learned Hallucination Detection in Black-Box LLMs Using Token-Level Entropy Production Rate** | Moslonka et al. [17] | 2025 | EPR (Thermodynamic Entropy Production Rate) | Estimated non-equilibrium entropy production from top-k token log-probabilities in black-box APIs. | Restricted to surface log-probabilities; cannot inspect hidden states or attention maps. |
| **SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative LLMs** | Manakul et al. [21] | 2023 | SelfCheckGPT (Multi-Sample Consistency) | Checked sentence-level consistency across 5–20 stochastic generations using BERTScore, NLI, and n-gram overlap. | Multiplies inference latency by 5x–20x (169.3 ms/token on T4 GPU) and performs passive detection only. |

## 2. Literature Review — III

**Pillar 3 · Attention-based and multi-signal detection.** Attention head dispersal and combined internal indicators reveal when generation detaches from input context.

*Table 3 — papers 15–18 of 40*

| Paper name | Author(s) & ID | Year | Method | Key contribution | Gap identified |
|:---|:---|:---:|:---|:---|:---|
| **The Map of Misbelief: Tracing Intrinsic and Extrinsic Hallucinations Through Attention Patterns** | Hajji et al. [9] | 2025 | Attention Aggregation (Intrinsic vs. Extrinsic) | Showed attention drop over prompt tokens catches intrinsic contradictions while entropy catches extrinsic errors. | Evaluates attention and entropy separately without a learned multi-sensor fusion controller. |
| **Uncertainty-Aware Attention Heads: Efficient Hallucination Detection for LLMs** | Vazhentsev et al. [11] | 2025 | RAUQ (Recurrent Attention Head UQ) | Identified specific uncertainty-aware attention heads and combined them recurrently with token confidence in one pass. | Ignores deep hidden-state probes and provides no corrective regeneration or retrieval. |
| **LLM-Check: Investigating Detection of Hallucinations in Large Language Models** | Sriramanan et al. [12] | 2024 | LLM-Check (Log-Det Attention + Hidden/Logit) | Combined attention kernel log-determinants, hidden scores, and logit entropy for single-pass white/black-box detection. | Static scoring without grouped out-of-fold probe stacking, calibrated warning/fault regimes, or closed-loop repair. |
| **Self-Contradictory Hallucinations of LLMs: Evaluation, Detection and Mitigation** | Mündler et al. [36] | 2023 | Self-Contradiction Prompting & Critique | Formalized self-contradictory hallucinations and paired contradiction detection with iterative text revision. | Requires multiple extra LLM calls per sentence and misses non-contradictory factual fabrications. |

## 2. Literature Review — IV

**Pillar 4 · Evaluation benchmarks and trustworthiness taxonomies.** Standardized benchmarks and atomic factuality metrics establish ground truth for measuring hallucination detectors.

*Table 4 — papers 19–27 of 40*

| Paper name | Author(s) & ID | Year | Method | Key contribution | Gap identified |
|:---|:---|:---:|:---|:---|:---|
| **TrustLLM: Trustworthiness in Large Language Models** | Huang et al. [3] | 2024 | TrustLLM (8-Dimension Benchmark Suite) | Benchmarked 16+ LLMs across 30+ datasets spanning truthfulness, safety, fairness, robustness, and transparency. | Offline evaluation suite; not a runtime guardrail or low-latency detector. |
| **On a Scale From 1 to 5: Quantifying Hallucination in Faithfulness Evaluation** | Jing et al. [10] | 2025 | Calibrated 1–5 Faithfulness Rubric + NLI | Developed fine-grained 1–5 faithfulness scoring rubrics with LLM-as-judge and fine-tuned NLI evaluators. | Post-generation judge model adds heavy compute overhead unsuitable for token-rate streaming. |
| **Large Language Models Hallucination: A Comprehensive Survey** | Alansari & Luqman [18] | 2024 | Full-Lifecycle Hallucination Taxonomy | Catalogued causes, detection signals, and mitigation stages across pretraining, fine-tuning, and inference. | Narrative survey; documents the disconnect between detection and mitigation without an empirical control architecture. |
| **TruthfulQA: Measuring How Models Mimic Human Falsehoods** | Lin et al. [22] | 2022 | TruthfulQA Benchmark (817 Adversarial Questions) | Created 817 questions targeting popular human misconceptions where scaling model size alone fails. | Static benchmark; requires pairing with internal probes to detect fluent misconceptions at runtime. |
| **FActScore: Fine-Grained Atomic Evaluation of Factual Precision in Long-Form Text** | Min et al. [23] | 2023 | FActScore (Atomic Fact Decomposition + Retrieval) | Decomposed long generations into atomic facts verified individually against Wikipedia. | Offline evaluation requiring multiple LLM decomposition and retrieval calls per paragraph. |
| **HaluEval: A Large-Scale Hallucination Evaluation Benchmark for LLMs** | Li et al. [29] | 2023 | HaluEval (35,000 QA, Dialogue & Summary Samples) | Constructed 35k paired grounded and hallucinated responses across QA, dialogue, and summarization. | QA ground-truth answers are shorter than hallucinated sentences, inducing length shortcuts if uncalibrated. |
| **FacTool: Factuality Detection in Generative AI — A Tool-Augmented Framework** | Chern et al. [34] | 2023 | FacTool (Claim Extraction + External Tools) | Verified LLM claims across QA, code, math, and scientific literature using search, Python, and Scholar tools. | High multi-step tool latency; operates post-hoc rather than reading single-pass internal model states. |
| **Survey of Hallucination in Natural Language Generation** | Ji et al. [35] | 2023 | Intrinsic vs. Extrinsic NLG Hallucination Taxonomy | Established the foundational intrinsic vs. extrinsic hallucination taxonomy across summarization, dialogue, and QA. | Pre-LLM-era focus; does not cover white-box transformer activation probing or closed-loop control. |
| **A Multitask, Multilingual, Multimodal Evaluation of ChatGPT on Reasoning & Hallucination** | Bang et al. [37] | 2023 | Cross-Task Empirical Hallucination Audit | Quantified extrinsic vs. intrinsic hallucination rates across multilingual and multimodal tasks. | Black-box empirical audit; proposes no internal detection or mitigation mechanism. |

## 2. Literature Review — V

**Pillar 5 · Mitigation through calibration, retrieval, and verification.** External evidence retrieval, constrained re-sampling, and calibrated abstention repair or block risky outputs.

*Table 5 — papers 28–38 of 40*

| Paper name | Author(s) & ID | Year | Method | Key contribution | Gap identified |
|:---|:---|:---:|:---|:---|:---|
| **Mitigating LLM Hallucination via Behaviorally Calibrated Reinforcement Learning** | Wu et al. [15] | 2025 | BehCal-RL (Proper Scoring Rule RL Abstention) | Trained LLMs with strictly proper scoring rewards to state calibrated confidence or abstain when uncertain. | Requires RL fine-tuning and immediately abstains without attempting retrieval-grounded correction. |
| **ExpandR: Teaching Dense Retrievers Beyond Queries with LLM Generation Guidance** | Yao et al. [20] | 2025 | ExpandR (Joint LLM-Retriever DPO Alignment) | Optimized query expansion with Direct Preference Optimization so retrieved passages improve downstream generation. | Runs retrieval unconditionally on every query instead of triggering selectively on internal fault signals. |
| **Chain-of-Verification Reduces Hallucination in Large Language Models** | Dhuliawala et al. [24] | 2024 | CoVe (Draft -> Verification Questions -> Revise) | Prompted the LLM to draft an answer, generate verification questions, answer them independently, and revise. | Requires 3–5 sequential generation stages per query and fails when the base LLM lacks the underlying fact. |
| **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** | Lewis et al. [25] | 2020 | RAG (Non-Parametric Dense Passage Retrieval) | Conditioned sequence generation on top-k Wikipedia passages retrieved via Dense Passage Retrieval (DPR). | Always-on retrieval adds latency to easy queries and still hallucinates when retrieved context is noisy. |
| **Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection** | Asai et al. [26] | 2023 | Self-RAG (Special Reflection & Critique Tokens) | Fine-tuned an LLM to emit [Retrieve], [IsRel], and [IsSup] reflection tokens for adaptive retrieval. | Requires full supervised fine-tuning of the base LLM with custom vocabulary tokens. |
| **Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** | Wei et al. [30] | 2022 | CoT (Intermediate Reasoning Traces) | Showed that intermediate natural-language reasoning steps substantially improve multi-step reasoning accuracy. | Reasoning chains themselves can hallucinate intermediate premises without internal uncertainty monitoring. |
| **Improving Factuality and Reasoning in Language Models through Multiagent Debate** | Du et al. [31] | 2024 | Multi-Agent Iterative Debate | Multiple LLM instances critique and refine each other's answers over several rounds to reduce factual errors. | Multiplies token and latency cost by N_agents x N_rounds (typically 6x–15x). |
| **Woodpecker: Hallucination Correction for Multimodal Large Language Models** | Yin et al. [32] | 2024 | Woodpecker (Post-Hoc Visual Claim Verification) | Extracted key concepts from MLLM outputs, verified them with visual detectors, and rewrote hallucinated spans. | Post-processing pipeline tailored to image-caption claims; high multi-model latency. |
| **RARR: Researching and Revising What Language Models Say, Using Language Models** | Gao et al. [33] | 2023 | RARR (Post-Hoc Attribution & Revision) | Generated search queries for unverified claims in an LLM output and edited unsupported statements. | Runs after full generation on every output rather than gating on single-pass internal risk. |
| **CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing** | Gou et al. [39] | 2023 | CRITIC (Tool-Interactive Iterative Self-Correction) | Allowed LLMs to verify and revise their own outputs by interacting with search engines and code interpreters. | Requires multiple iterative tool-invocation loops and provides no calibrated abstention guarantee. |
| **Can Knowledge Graphs Reduce Hallucinations in LLMs? A Survey** | Agrawal et al. [40] | 2024 | KG-Augmented Grounding & Verification Taxonomy | Synthesized knowledge-graph retrieval, graph-guided decoding, and post-hoc KG triple verification. | Survey only; depends on curated domain knowledge graphs that are often incomplete for open-domain queries. |

## 2. Literature Review — VI

**Pillar 6 · Explainability and human trust calibration.** Users need transparent sensor attributions and calibrated confidence cues rather than opaque risk numbers.

*Table 6 — papers 39–40 of 40*

| Paper name | Author(s) & ID | Year | Method | Key contribution | Gap identified |
|:---|:---|:---:|:---|:---|:---|
| **Making Sense of the Unsensible: Survey & Challenges for XAI in LLMs Toward Human-Centered AI** | Herrera [8] | 2025 | Four-Dimension LLM XAI Framework | Defined faithfulness, truthfulness, plausibility, and contrastivity as the four pillars of human-centered LLM XAI. | Conceptual taxonomy; does not provide an algorithmic real-time sensor-attribution engine. |
| **Why Would You Suggest That? Human Trust in Language Model Responses** | Sharma et al. [19] | 2024 | Empirical Study of Explanation Framing & Trust | Demonstrated in human-subject trials that comparative and contrastive explanations improve appropriate trust calibration. | Behavioral study using mocked explanations; not connected to live internal LLM hallucination sensors. |
