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
        "Pillar 1 investigates internal hidden activation manifolds to detect hallucinations during autoregressive decoding. Early supervised probing (SAPLMA, Azaria & Mitchell [27]) demonstrated that multilayer perceptrons on middle-layer residual streams separate truth from falsehood far more reliably than surface probabilities. Subsequent work extended this to activation steering (ITI, Li et al. [28]), unsupervised uncertainty probing (MIND, Su et al. [1]), prompt-aligned truth subspaces (PRISM, Zhang et al. [2]), polysemantic neuron isolation (MHAD, Zhang et al. [5]; Truth Forest, Chen et al. [38]), and representational distribution shift tracking (HalluShift, Dasgupta et al. [13]; Nath et al. [16]). As detailed in Table 3.2, while internal hidden probes achieve high within-domain discrimination, existing frameworks evaluate them in isolation without out-of-fold multi-sensor calibration or closed-loop corrective actuation."
    ],
    2: [
        "Pillar 2 addresses predictive vocabulary entropy, logit energy, and semantic uncertainty quantification (UQ). Black-box multi-sample consistency approaches such as SelfCheckGPT (Manakul et al. [21]) evaluate agreement across 5 to 20 stochastic samples but multiply decoding latency by 5x to 20x. Single-pass alternatives include Semantic Entropy Probes (SEPs, Han et al. [14]), Boltzmann-inspired free energy over pre-softmax logits (Ma et al. [4]), localized token-entropy Z-score spikes (Anonymous [6]), and thermodynamic token-level entropy production rate (Moslonka et al. [17]). As shown in Table 3.3, raw entropy and negative log-likelihood (NLL) invert polarity under answer-length asymmetry, which TRUEGUARD resolves by pairing hybrid Shannon/Renyi-2 entropy with supervised hidden probes in a signed logistic fusion layer."
    ],
    3: [
        "Pillar 3 examines causal self-attention matrices and multi-signal white-box indicators. Hajji et al. [9] (The Map of Misbelief) proved that intrinsic hallucinations manifest as attention collapse on prompt source context, whereas extrinsic fabrications correlate with elevated predictive entropy. Vazhentsev et al. [11] (RAUQ) identified attention heads whose recurrently aggregated entropy tracks reliability in a single pass. Sriramanan et al. [12] (LLM-Check) combined attention kernel log-determinants with hidden-state scores, while Mundler et al. [36] analyzed self-contradictory generations. Table 3.4 synthesizes these findings, motivating TRUEGUARD's extraction of final-quartile normalized attention entropy (AAS) alongside ISP, EEM, and DST within the same forward pass."
    ],
    4: [
        "Pillar 4 establishes quantitative hallucination benchmarks and trustworthiness taxonomies. Canonical foundations distinguish intrinsic contradictions from extrinsic fabrications (Ji et al. [35]; Alansari & Luqman [18]; Bang et al. [37]). For evaluation, Lin et al. [22] developed TruthfulQA (817 adversarial questions testing popular human misconceptions), while Li et al. [29] introduced HaluEval (35,000 paired answers across QA, Dialogue, and Summarization). Long-form biography auditing was formalized via atomic fact decomposition in FActScore (Min et al. [23]), claim-level verification in FacTool (Chern et al. [34]), 1-to-5 faithfulness rubrics (Jing et al. [10]), and multi-dimensional trust rubrics in TrustLLM (Huang et al. [3]). As shown in Table 3.5, length-confounded benchmarks require question-grouped cross-validation to prevent optimistic data leakage."
    ],
    5: [
        "Pillar 5 investigates hallucination mitigation through retrieval-augmented generation (RAG), claim verification, and reinforcement learning. Lewis et al. [25] introduced standard RAG, while ExpandR (Yao et al. [20]) and Agrawal et al. [40] enhanced retrieval coverage via query expansion. To eliminate unneeded retrieval latency on simple prompts, Self-RAG (Asai et al. [26]) trained models to emit adaptive reflection tokens, though requiring full parameter fine-tuning. Post-hoc verification pipelines—including Chain-of-Verification (CoVe, Dhuliawala et al. [24]), RARR (Gao et al. [33]), CRITIC (Gou et al. [39]), Woodpecker (Yin et al. [32]), and Multiagent Debate (Du et al. [31])—execute 3 to 15 sequential calls per query. At the abstention boundary, BehCal-RL (Wu et al. [15]) trained models to abstain via proper scoring rules. Table 3.6 synthesizes Pillar 5, demonstrating that no prior framework uses single-pass internal states to drive a graded 3-tier corrective actuator."
    ],
    6: [
        "Pillar 6 addresses explainable AI (XAI) and human-AI trust calibration. Herrera [8] formulated a four-dimensional human-centered XAI taxonomy comprising faithfulness, truthfulness, plausibility, and contrastivity, arguing that scalar risk scores fail to support high-stakes decision-making without mechanistic attributions. Sharma et al. [19] showed through controlled human-subject trials that comparative explanations significantly improve trust calibration, enabling users to accept valid outputs while rejecting false suggestions. Table 3.7 highlights this gap, which TRUEGUARD resolves by decomposing the fused risk logit into exact per-sensor signed log-odds contributions (ISP, AAS, EEM, DST) alongside a 3-tier audit trace."
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

