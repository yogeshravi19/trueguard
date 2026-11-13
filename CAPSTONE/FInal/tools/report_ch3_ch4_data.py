"""
Chapter 3 (PRISMA 40-Study Literature Review across 6 Pillars) and
Chapter 4 (System Analysis, Requirements, and Closed-Loop Control Architecture)
data and narrative generator for FINAL_REPORT.docx.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(r"E:\trueguard\CAPSTONE\FInal\tools")))
from build_40paper_literature_review import PILLARS

PILLAR_NARRATIVES = {
    1: [
        "Pillar 1 encompasses eight primary investigations that interrogate the internal hidden activation manifolds of transformer language models to detect hallucinations during or immediately following sequence generation. The central theoretical premise of this research stream is that an autoregressive language model's intermediate residual-stream representations encode a linearly separable or geometrically structured 'truthfulness subspace' that diverges when the model fabricates ungrounded claims, even when the final vocabulary softmax layer assigns high surface probability to the hallucinated tokens [1, 27].",
        "Azaria and Mitchell [27] pioneered supervised internal-state probing with SAPLMA (Statement Accuracy Prediction based on Language Model Activations), demonstrating that a lightweight multilayer perceptron trained on middle-layer hidden representations separates true from false declarative statements significantly more accurately than surface token probabilities. Li et al. [28] extended this insight from passive detection to active intervention via Inference-Time Intervention (ITI), identifying a sparse subset of attention heads with high linear probing accuracy for truthfulness and shifting activations along truth-correlated directions during decoding. While ITI improved TruthfulQA performance without parameter fine-tuning, fixed directional steering vectors can degrade linguistic fluency when applied unconditionally and cannot inject missing external facts that lie outside the model's parametric memory.",
        "Subsequent studies between 2024 and 2025 refined internal representation probing along three dimensions: unsupervised probing, prompt-aligned subspace projection, and multi-layer representation shift tracking. Su et al. [1] proposed MIND, an unsupervised internal-state framework paired with the HELM internal activation benchmark, showing that internal states carry real-time uncertainty signatures without requiring human-annotated truthfulness labels. Zhang et al. [2] introduced PRISM, demonstrating that truth-orienting prompt templates align internal truthfulness directions across domain shifts prior to linear classification. Zhang et al. [5] developed MHAD, isolating hallucination-sensitive neurons at initial and terminal decoding positions, whereas Chen et al. [38] proposed Truth Forest, learning orthogonal multi-scale probes (Rap-O) to capture polysemantic truthfulness directions.",
        "In parallel, Dasgupta et al. [13] (HalluShift) and Nath et al. [16] (HalluShift++) analyzed layer-to-layer and token-to-token representational distribution shifts across autoregressive trajectories. Despite their strong discriminative accuracy on in-domain benchmarks, Pillar 1 methods exhibit two persistent limitations when deployed in isolation: (i) supervised hidden probes are rarely combined with surface uncertainty, attention dispersion, and directional trajectory drift inside a leakage-free out-of-fold stacking pipeline, and (ii) existing probing frameworks terminate at passive risk scoring rather than driving a graded closed-loop corrective actuator."
    ],
    2: [
        "Pillar 2 comprises six primary studies focused on uncertainty quantification (UQ), predictive vocabulary entropy, logit free energy, and multi-sample semantic consistency. Unlike internal hidden-state probes, Pillar 2 methods operate primarily on the pre-softmax logit vector or the post-softmax predictive token distribution, seeking to distinguish epistemic uncertainty (knowledge gaps) from aleatoric ambiguity (valid linguistic paraphrases) [7].",
        "At the multi-sample end of the spectrum, Manakul et al. [21] introduced SelfCheckGPT, a zero-resource black-box detector that generates K = 5 to 20 stochastic candidate responses for the same prompt and measures sentence-level consistency against the primary answer using BERTScore, natural language inference (NLI), or n-gram overlap. Although multi-sample consistency reliably flags stochastic fabrications, Kang et al. [7] and Han, Kossen et al. [14] emphasize that generating 5 to 20 full trajectories multiplies inference latency and GPU compute cost by 5x to 20x (reaching 169.31 ms/token on an NVIDIA Tesla T4 GPU in our empirical profiling), rendering multi-sample verification impractical for interactive streaming systems.",
        "To eliminate multi-sample overhead, Han, Kossen et al. [14] proposed Semantic Entropy Probes (SEPs), training linear probes on single-pass hidden states to approximate multi-sample semantic entropy at near-zero runtime cost. Ma et al. [4] introduced Semantic Energy, showing that Boltzmann-inspired free energy computed over pre-softmax logits preserves magnitude information discarded by the shift-invariant softmax normalization. Anonymous [6] examined localized token-entropy Z-score spikes during multi-step reasoning, while Moslonka et al. [17] formulated thermodynamic token-level Entropy Production Rate (EPR) for black-box APIs.",
        "Our empirical audit in Chapter 7 reveals a critical failure mode of uncalibrated single-pass entropy and negative log-likelihood (NLL) baselines that has been largely overlooked in Pillar 2 literature: on paired question-answering benchmarks such as HaluEval-QA, concise ground-truth entity answers naturally exhibit higher per-token entropy than verbose, template-wrapped hallucinated sentences, causing raw entropy and NLL to point in the opposite direction (raw AUROC < 0.50). TRUEGUARD resolves this vulnerability by pairing scale-invariant hybrid Shannon/Renyi-2 entropy (EEM) with supervised internal-state probes inside a sign-adaptive logistic fusion layer."
    ],
    3: [
        "Pillar 3 investigates causal self-attention matrices and multi-signal white-box indicators across four primary studies [9, 11, 12, 36]. Whereas hidden-state probes inspect the residual stream after feed-forward blocks, attention-based detectors examine how strongly the autoregressive decoder attends to grounding tokens in the prompt or retrieved context versus dispersing attention mass across uninformative sink positions.",
        "Hajji et al. [9] ('The Map of Misbelief') demonstrated that intrinsic hallucinations—where the model directly contradicts facts stated in the input prompt—manifest as a measurable collapse in attention weight allocated to source context spans, whereas extrinsic hallucinations—where the model fabricates unsupported details beyond the context—correlate more strongly with elevated predictive entropy. Vazhentsev et al. [11] proposed RAUQ, identifying a subset of uncertainty-aware attention heads whose recurrently aggregated entropy tracks generation reliability in a single forward pass.",
        "Sriramanan et al. [12] introduced LLM-Check, combining log-determinants of attention kernels, hidden-state scores, and logit entropy for single-pass hallucination detection, while Mundler et al. [36] analyzed self-contradictory hallucinations across multi-sentence generations. However, existing Pillar 3 frameworks either combine raw signals via heuristic summation without inner out-of-fold probe calibration or require multiple iterative critique passes [36]. In TRUEGUARD, final-quartile normalized attention Shannon entropy (AAS) is extracted alongside ISP, EEM, and DST within the same forward pass and calibrated via grouped cross-validation."
    ],
    4: [
        "Pillar 4 encompasses nine foundational benchmark, metric, and taxonomic studies that define how hallucinations and broader trustworthiness properties are measured across natural language generation systems [3, 10, 18, 22, 23, 29, 34, 35, 37]. Ji et al. [35] and Alansari and Luqman [18] established the canonical distinction between intrinsic hallucinations (direct contradictions of source context) and extrinsic hallucinations (unverifiable fabrications absent from source context), while Bang et al. [37] audited empirical hallucination rates across multilingual and multitask deployments.",
        "For quantitative evaluation, Lin et al. [22] created TruthfulQA (817 adversarial questions across 38 categories designed to trigger human-mimicked misconceptions), demonstrating that larger language models frequently assign higher probability to popular falsehoods than smaller models. Li et al. [29] released HaluEval, providing 35,000 paired grounded and hallucinated responses across knowledge-grounded Question Answering, knowledge-grounded Dialogue, and document Summarization. Min et al. [23] introduced FActScore to evaluate long-form biographies via atomic fact decomposition against Wikipedia, Chern et al. [34] proposed FacTool for multi-tool claim verification, Jing et al. [10] developed calibrated 1-to-5 faithfulness rubrics, and Huang et al. [3] synthesized eight trustworthiness dimensions in TrustLLM.",
        "A crucial methodological insight emerging from our synthesis of Pillar 4 benchmarks is that different datasets probe fundamentally distinct failure mechanisms: TruthfulQA tests short-form adversarial misconceptions where both correct and hallucinated answers have matched lengths, whereas HaluEval-QA pairs concise entity answers against longer, plausible-sounding fabricated sentences. Consequently, rigorous detector evaluation requires question-grouped cross-validation (keeping paired responses for the same question in the same fold), explicit length-confound diagnostics, and cross-dataset transfer matrices."
    ],
    5: [
        "Pillar 5 surveys eleven primary studies addressing hallucination mitigation through non-parametric retrieval-augmented generation (RAG), post-hoc claim verification, multi-agent debate, and behaviorally calibrated reinforcement learning [15, 20, 24, 25, 26, 30, 31, 32, 33, 39, 40]. Lewis et al. [25] established the RAG paradigm by conditioning generation on dense-retrieved Wikipedia passages, while Yao et al. [20] (ExpandR) and Agrawal et al. [40] enhanced retrieval coverage via query expansion and knowledge graphs.",
        "Recognising that unconditional ('always-on') retrieval introduces unnecessary latency on simple queries and can inject noisy distractors, Asai et al. [26] proposed Self-RAG, training the language model to emit special reflection tokens ([Retrieve], [IsRel], [IsSup]) to trigger retrieval adaptively. However, Self-RAG requires full parameter fine-tuning of the base LLM with an expanded vocabulary. Post-hoc verification pipelines—including Chain-of-Verification (CoVe) [24], RARR [33], CRITIC [39], Woodpecker [32], and Multiagent Debate [31]—avoid base-model retraining by prompting the LLM to draft an answer, generate verification queries, consult external tools or peer agents, and revise unsupported claims. Yet these post-hoc pipelines execute 3 to 15 sequential LLM calls per query.",
        "At the abstention boundary, Wu et al. [15] (BehCal-RL) trained models via reinforcement learning with strictly proper scoring rules to abstain when uncertain, sacrificing answer coverage on queries that could have been repaired via retrieval. Across all eleven Pillar 5 studies, no existing framework uses fast, single-pass white-box internal sensors on a frozen LLM to drive a graded three-tier escalation controller (local temperature-annealed re-sampling -> targeted Wikipedia retrieval -> calibrated abstention)."
    ],
    6: [
        "Pillar 6 examines explainability (XAI) and human-AI trust calibration across two dedicated studies [8, 19]. Herrera [8] formulated a four-dimensional human-centered XAI taxonomy for large language models comprising faithfulness, truthfulness, plausibility, and contrastivity, arguing that black-box risk scores fail to support high-stakes human decision-making unless users can inspect why a response was flagged.",
        "Complementing this theoretical framework, Sharma et al. [19] conducted controlled human-subject experiments demonstrating that comparative and transparent explanations significantly improve users' ability to calibrate trust—accepting accurate model outputs while overriding hallucinated suggestions. In existing hallucination detectors, however, the output is an opaque scalar probability or binary flag. TRUEGUARD directly operationalizes Pillar 6 by decomposing the fused logit risk score into exact signed per-sensor log-odds contributions (ISP, AAS, EEM, and DST) alongside a transparent tier-actuation audit trail."
    ],
}

PILLAR_SECTION_TITLES = [
    "3.2 PILLAR 1: INTERNAL-STATE BASED HALLUCINATION DETECTION",
    "3.3 PILLAR 2: UNCERTAINTY QUANTIFICATION AND ENTROPY-BASED METHODS",
    "3.4 PILLAR 3: ATTENTION-BASED AND MULTI-SIGNAL DETECTION",
    "3.5 PILLAR 4: EVALUATION BENCHMARKS AND TRUSTWORTHINESS TAXONOMIES",
    "3.6 PILLAR 5: MITIGATION THROUGH CALIBRATION, RETRIEVAL AND VERIFICATION",
    "3.7 PILLAR 6: EXPLAINABILITY AND HUMAN TRUST CALIBRATION",
]

PILLAR_TABLE_CAPTIONS = [
    "TABLE 3.2: PILLAR 1 LITERATURE REVIEW MATRIX — INTERNAL-STATE BASED DETECTION (PAPERS 1–8 OF 40)",
    "TABLE 3.3: PILLAR 2 LITERATURE REVIEW MATRIX — UNCERTAINTY QUANTIFICATION AND ENTROPY METHODS (PAPERS 9–14 OF 40)",
    "TABLE 3.4: PILLAR 3 LITERATURE REVIEW MATRIX — ATTENTION-BASED AND MULTI-SIGNAL DETECTION (PAPERS 15–18 OF 40)",
    "TABLE 3.5: PILLAR 4 LITERATURE REVIEW MATRIX — EVALUATION BENCHMARKS AND TAXONOMIES (PAPERS 19–27 OF 40)",
    "TABLE 3.6: PILLAR 5 LITERATURE REVIEW MATRIX — MITIGATION VIA CALIBRATION, RETRIEVAL AND VERIFICATION (PAPERS 28–38 OF 40)",
    "TABLE 3.7: PILLAR 6 LITERATURE REVIEW MATRIX — EXPLAINABILITY AND HUMAN TRUST CALIBRATION (PAPERS 39–40 OF 40)",
]

CROSS_PILLAR_SYNTHESIS_ROWS = [
    ("Pillar 1: Internal States\n[1, 2, 5, 13, 16, 27, 28, 38]",
     "Intermediate hidden layers (45%–90% depth) encode linear truthfulness directions and representation drift.",
     "Probes are evaluated in isolation without out-of-fold multi-sensor stacking or closed-loop corrective actuation.",
     "Sensor 1 (ISP: 4-layer OOF-stacked logistic probes) + Sensor 4 (DST: consecutive-token cosine drift).",
     "0.935 macro AUROC on TinyLlama-1.1B; ISP contributes +0.188 to +0.251 AUROC over surface signals."),
    ("Pillar 2: Uncertainty & Entropy\n[4, 6, 7, 14, 17, 21]",
     "Logit free energy and multi-sample semantic entropy flag uncertain generations.",
     "Multi-sample UQ costs 5x–20x latency; single-pass logit entropy fails on fluent misconceptions and length confounds.",
     "Sensor 3 (EEM: 0.6 Shannon + 0.4 Renyi-2 normalized entropy) fused with supervised ISP.",
     "36.41 ms/tok post-pass and 39.30 ms/tok online on Tesla T4 GPU (4.31x–4.65x faster than 5-sample consistency)."),
    ("Pillar 3: Attention & Multi-Signal\n[9, 11, 12, 36]",
     "Final-quartile attention head dispersal catches prompt and context detachment.",
     "Heuristic aggregation without grouped OOF calibration or thresholded corrective escalation.",
     "Sensor 2 (AAS: final-quartile attention Shannon entropy) + leakage-free L2 Logistic Fusion.",
     "When ISP is withheld (-ISP), AAS+EEM+DST provide a 0.626–0.918 training-free fallback detector."),
    ("Pillar 4: Benchmarks & Taxonomies\n[3, 10, 18, 22, 23, 29, 34, 35, 37]",
     "Paired and open-ended benchmarks quantify intrinsic and extrinsic hallucinations.",
     "Answer-length asymmetries across QA benchmarks invert uncalibrated entropy and NLL baselines.",
     "Question-grouped 5-fold CV + automated polarity diagnostics + 4x4 cross-dataset transfer audit.",
     "0.986 (HaluEval-Summ), 0.975 (HaluEval-QA), 0.903 (HaluEval-Dial), 0.876 (TruthfulQA); ECE 0.024–0.042."),
    ("Pillar 5: Mitigation & Retrieval\n[15, 20, 24, 25, 26, 30, 31, 32, 33, 39, 40]",
     "Re-sampling, RAG, and RL abstention each repair only one failure regime.",
     "Detection and mitigation operate as disconnected silos; always-on RAG wastes compute on low-risk queries.",
     "Two calibrated thresholds (tau_warn=0.611, tau_fault=0.898) + 3-Tier Actuator (Resample, Wikipedia RAG, Abstain).",
     "TriviaQA answered hallucination rate drops 62.0% -> 40.0% (-35.5% relative; -72.0% system-wide); AURC = 0.412."),
    ("Pillar 6: Explainability & Trust\n[8, 19]",
     "Human operators require faithful, contrastive explanations to calibrate trust.",
     "Existing detectors emit opaque scalar scores with no per-sensor attribution.",
     "Exact per-sensor log-odds decomposition (TrueGuardDetector.explain) + tier decision audit trace.",
     "Every prediction outputs signed log-odds contributions c_k = w_k * z_k for ISP, AAS, EEM, and DST."),
]

