"""
Build the standalone 40-paper Literature Review document classified by the 6 Pillars of
`E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models_standard.docx`, formatted in the exact visual layout
of the user's screenshot:
  - Navy serif heading (`2. Literature Review — I`, etc.) with navy bottom border rule
  - Bold pillar title + one-sentence summary (`Pillar k · ...`)
  - Grey caption (`Table k — papers a–b of 40`)
  - 6-column navy-bordered table:
      Paper name | Author(s) & ID | Year | Method | Key contribution | Gap identified
Outputs:
  - E:\trueguard\TRUEGUARD_40_Papers_Literature_Review_By_Pillars.docx
  - E:\trueguard\CAPSTONE\FInal\paper\TRUEGUARD_40_Papers_Literature_Review_By_Pillars.docx
  - E:\trueguard\TRUEGUARD_40_Papers_Literature_Review_By_Pillars.md
"""
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

PILLARS = [
    (
        "2. Literature Review — I",
        "Pillar 1 · Internal-state based detection.",
        "Hallucination leaves a measurable geometric signature inside hidden transformer activations while the model writes.",
        [
            ("Unsupervised Real-Time Hallucination Detection based on Internal States of LLMs",
             "Su et al. [1]", "2024", "MIND (Unsupervised Hidden Probing)",
             "Formulated an unsupervised MLP probe over intermediate hidden states and released the HELM internal-state dataset.",
             "Relies solely on hidden states; misses attention dispersion and logit energy; no closed-loop mitigation."),
            ("Prompt-Guided Internal States for Hallucination Detection of LLMs",
             "Zhang et al. [2]", "2024", "PRISM (Prompt-Guided Probing)",
             "Used truth-orienting prompt templates to align truthfulness subspaces across domains before linear probing.",
             "Requires prompt wrapping; passive scoring only with no runtime repair or retrieval grounding."),
            ("Detecting Hallucination in LLMs Through Deep Internal Representation Analysis",
             "Zhang et al. [5]", "2025", "MHAD (Hallucination-Aware Neurons)",
             "Isolated hallucination-sensitive neurons at initial and final decoding steps via layer-wise linear probing.",
             "Static feature concatenation without dynamic multi-sensor calibration or corrective feedback."),
            ("HalluShift: Measuring Distribution Shifts Towards Hallucination Detection in LLMs",
             "Dasgupta et al. [13]", "2025", "HALLUSHIFT (Internal Distribution Shift)",
             "Tracked layer-to-layer cosine and Wasserstein shifts in hidden states across autoregressive trajectories.",
             "Captures macro drift but has modest power on short QA when used without supervised probes."),
            ("HalluShift++: Bridging Language and Vision through Internal Representation Shifts",
             "Nath et al. [16]", "2025", "HALLUSHIFT++ (Hierarchical Shift)",
             "Extended internal representation shift tracking to hierarchical vision-language hallucinations.",
             "Focused on multimodal encoders; provides no closed-loop text retrieval or calibrated abstention."),
            ("The Internal State of an LLM Knows When It's Lying",
             "Azaria & Mitchell [27]", "2023", "SAPLMA (Supervised Hidden Classifier)",
             "Demonstrated that a lightweight classifier trained on middle-layer hidden activations separates true vs. false statements.",
             "Evaluated on synthetic true/false statements; sensitive to domain and answer-length shifts without recalibration."),
            ("Inference-Time Intervention: Eliciting Truthful Answers from a Language Model",
             "Li et al. [28]", "2023", "ITI (Activation Steering along Truthful Heads)",
             "Shifted hidden activations along truthfulness directions during decoding to improve TruthfulQA accuracy.",
             "Fixed steering strength can degrade fluency and cannot supply external facts when model knowledge is absent."),
            ("Truth Forest: Toward Multi-Scale Truthfulness in LLMs through Intervention without Tuning",
             "Chen et al. [38]", "2024", "Truth Forest (Multi-Scale Orthogonal Probes)",
             "Learned orthogonal truthfulness probes (Rap-O) across multiple scales to capture multidimensional truth directions.",
             "Higher probe complexity; still limited to internal knowledge and lacks external retrieval fallback."),
        ],
    ),
    (
        "2. Literature Review — II",
        "Pillar 2 · Uncertainty quantification and entropy-based methods.",
        "Token probability dispersion, logit energy, and multi-sample semantic variance quantify when the model is guessing.",
        [
            ("Semantic Energy: Detecting LLM Hallucination Beyond Entropy",
             "Ma et al. [4]", "2025", "Semantic Energy (Penultimate Logit Energy)",
             "Measured Boltzmann-inspired energy over penultimate logits rather than post-softmax probabilities.",
             "Operates only at the output layer; misses hidden-state truthfulness when the LLM states fluent misconceptions."),
            ("Entropy Spike Detection and Self-Confidence Calibration for Hallucination Mitigation",
             "Anonymous [6]", "2025", "Z-Score Token Entropy Spike + RL Penalty",
             "Detected abrupt token-entropy spikes during reasoning and penalized overconfident spikes during RL training.",
             "Requires RL fine-tuning and lacks inference-time external evidence retrieval."),
            ("Uncertainty Quantification for Hallucination Detection in LLMs: Foundations & Methodology",
             "Kang et al. [7]", "2025", "Epistemic vs. Aleatoric UQ Taxonomy",
             "Formalized epistemic vs. aleatoric uncertainty for LLMs and benchmarked single-pass vs. sampling UQ.",
             "Survey and analytical study; highlights 5x–20x latency bottleneck of multi-sample UQ without a closed-loop fix."),
            ("Semantic Entropy Probes: Robust and Cheap Hallucination Detection in LLMs",
             "Han, Kossen et al. [14]", "2024", "SEPs (Linear Probes for Semantic Entropy)",
             "Trained single-pass linear probes on hidden states to approximate multi-sample semantic entropy at near-zero overhead.",
             "Single-signal approximation; does not integrate attention dispersal, temporal drift, or tiered mitigation."),
            ("Learned Hallucination Detection in Black-Box LLMs Using Token-Level Entropy Production Rate",
             "Moslonka et al. [17]", "2025", "EPR (Thermodynamic Entropy Production Rate)",
             "Estimated non-equilibrium entropy production from top-k token log-probabilities in black-box APIs.",
             "Restricted to surface log-probabilities; cannot inspect hidden states or attention maps."),
            ("SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative LLMs",
             "Manakul et al. [21]", "2023", "SelfCheckGPT (Multi-Sample Consistency)",
             "Checked sentence-level consistency across 5–20 stochastic generations using BERTScore, NLI, and n-gram overlap.",
             "Multiplies inference latency by 5x–20x (169.3 ms/token on T4 GPU) and performs passive detection only."),
        ],
    ),
    (
        "2. Literature Review — III",
        "Pillar 3 · Attention-based and multi-signal detection.",
        "Attention head dispersal and combined internal indicators reveal when generation detaches from input context.",
        [
            ("The Map of Misbelief: Tracing Intrinsic and Extrinsic Hallucinations Through Attention Patterns",
             "Hajji et al. [9]", "2025", "Attention Aggregation (Intrinsic vs. Extrinsic)",
             "Showed attention drop over prompt tokens catches intrinsic contradictions while entropy catches extrinsic errors.",
             "Evaluates attention and entropy separately without a learned multi-sensor fusion controller."),
            ("Uncertainty-Aware Attention Heads: Efficient Hallucination Detection for LLMs",
             "Vazhentsev et al. [11]", "2025", "RAUQ (Recurrent Attention Head UQ)",
             "Identified specific uncertainty-aware attention heads and combined them recurrently with token confidence in one pass.",
             "Ignores deep hidden-state probes and provides no corrective regeneration or retrieval."),
            ("LLM-Check: Investigating Detection of Hallucinations in Large Language Models",
             "Sriramanan et al. [12]", "2024", "LLM-Check (Log-Det Attention + Hidden/Logit)",
             "Combined attention kernel log-determinants, hidden scores, and logit entropy for single-pass white/black-box detection.",
             "Static scoring without grouped out-of-fold probe stacking, calibrated warning/fault regimes, or closed-loop repair."),
            ("Self-Contradictory Hallucinations of LLMs: Evaluation, Detection and Mitigation",
             "Mündler et al. [36]", "2023", "Self-Contradiction Prompting & Critique",
             "Formalized self-contradictory hallucinations and paired contradiction detection with iterative text revision.",
             "Requires multiple extra LLM calls per sentence and misses non-contradictory factual fabrications."),
        ],
    ),
    (
        "2. Literature Review — IV",
        "Pillar 4 · Evaluation benchmarks and trustworthiness taxonomies.",
        "Standardized benchmarks and atomic factuality metrics establish ground truth for measuring hallucination detectors.",
        [
            ("TrustLLM: Trustworthiness in Large Language Models",
             "Huang et al. [3]", "2024", "TrustLLM (8-Dimension Benchmark Suite)",
             "Benchmarked 16+ LLMs across 30+ datasets spanning truthfulness, safety, fairness, robustness, and transparency.",
             "Offline evaluation suite; not a runtime guardrail or low-latency detector."),
            ("On a Scale From 1 to 5: Quantifying Hallucination in Faithfulness Evaluation",
             "Jing et al. [10]", "2025", "Calibrated 1–5 Faithfulness Rubric + NLI",
             "Developed fine-grained 1–5 faithfulness scoring rubrics with LLM-as-judge and fine-tuned NLI evaluators.",
             "Post-generation judge model adds heavy compute overhead unsuitable for token-rate streaming."),
            ("Large Language Models Hallucination: A Comprehensive Survey",
             "Alansari & Luqman [18]", "2024", "Full-Lifecycle Hallucination Taxonomy",
             "Catalogued causes, detection signals, and mitigation stages across pretraining, fine-tuning, and inference.",
             "Narrative survey; documents the disconnect between detection and mitigation without an empirical control architecture."),
            ("TruthfulQA: Measuring How Models Mimic Human Falsehoods",
             "Lin et al. [22]", "2022", "TruthfulQA Benchmark (817 Adversarial Questions)",
             "Created 817 questions targeting popular human misconceptions where scaling model size alone fails.",
             "Static benchmark; requires pairing with internal probes to detect fluent misconceptions at runtime."),
            ("FActScore: Fine-Grained Atomic Evaluation of Factual Precision in Long-Form Text",
             "Min et al. [23]", "2023", "FActScore (Atomic Fact Decomposition + Retrieval)",
             "Decomposed long generations into atomic facts verified individually against Wikipedia.",
             "Offline evaluation requiring multiple LLM decomposition and retrieval calls per paragraph."),
            ("HaluEval: A Large-Scale Hallucination Evaluation Benchmark for LLMs",
             "Li et al. [29]", "2023", "HaluEval (35,000 QA, Dialogue & Summary Samples)",
             "Constructed 35k paired grounded and hallucinated responses across QA, dialogue, and summarization.",
             "QA ground-truth answers are shorter than hallucinated sentences, inducing length shortcuts if uncalibrated."),
            ("FacTool: Factuality Detection in Generative AI — A Tool-Augmented Framework",
             "Chern et al. [34]", "2023", "FacTool (Claim Extraction + External Tools)",
             "Verified LLM claims across QA, code, math, and scientific literature using search, Python, and Scholar tools.",
             "High multi-step tool latency; operates post-hoc rather than reading single-pass internal model states."),
            ("Survey of Hallucination in Natural Language Generation",
             "Ji et al. [35]", "2023", "Intrinsic vs. Extrinsic NLG Hallucination Taxonomy",
             "Established the foundational intrinsic vs. extrinsic hallucination taxonomy across summarization, dialogue, and QA.",
             "Pre-LLM-era focus; does not cover white-box transformer activation probing or closed-loop control."),
            ("A Multitask, Multilingual, Multimodal Evaluation of ChatGPT on Reasoning & Hallucination",
             "Bang et al. [37]", "2023", "Cross-Task Empirical Hallucination Audit",
             "Quantified extrinsic vs. intrinsic hallucination rates across multilingual and multimodal tasks.",
             "Black-box empirical audit; proposes no internal detection or mitigation mechanism."),
        ],
    ),
    (
        "2. Literature Review — V",
        "Pillar 5 · Mitigation through calibration, retrieval, and verification.",
        "External evidence retrieval, constrained re-sampling, and calibrated abstention repair or block risky outputs.",
        [
            ("Mitigating LLM Hallucination via Behaviorally Calibrated Reinforcement Learning",
             "Wu et al. [15]", "2025", "BehCal-RL (Proper Scoring Rule RL Abstention)",
             "Trained LLMs with strictly proper scoring rewards to state calibrated confidence or abstain when uncertain.",
             "Requires RL fine-tuning and immediately abstains without attempting retrieval-grounded correction."),
            ("ExpandR: Teaching Dense Retrievers Beyond Queries with LLM Generation Guidance",
             "Yao et al. [20]", "2025", "ExpandR (Joint LLM-Retriever DPO Alignment)",
             "Optimized query expansion with Direct Preference Optimization so retrieved passages improve downstream generation.",
             "Runs retrieval unconditionally on every query instead of triggering selectively on internal fault signals."),
            ("Chain-of-Verification Reduces Hallucination in Large Language Models",
             "Dhuliawala et al. [24]", "2024", "CoVe (Draft -> Verification Questions -> Revise)",
             "Prompted the LLM to draft an answer, generate verification questions, answer them independently, and revise.",
             "Requires 3–5 sequential generation stages per query and fails when the base LLM lacks the underlying fact."),
            ("Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
             "Lewis et al. [25]", "2020", "RAG (Non-Parametric Dense Passage Retrieval)",
             "Conditioned sequence generation on top-k Wikipedia passages retrieved via Dense Passage Retrieval (DPR).",
             "Always-on retrieval adds latency to easy queries and still hallucinates when retrieved context is noisy."),
            ("Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection",
             "Asai et al. [26]", "2023", "Self-RAG (Special Reflection & Critique Tokens)",
             "Fine-tuned an LLM to emit [Retrieve], [IsRel], and [IsSup] reflection tokens for adaptive retrieval.",
             "Requires full supervised fine-tuning of the base LLM with custom vocabulary tokens."),
            ("Chain-of-Thought Prompting Elicits Reasoning in Large Language Models",
             "Wei et al. [30]", "2022", "CoT (Intermediate Reasoning Traces)",
             "Showed that intermediate natural-language reasoning steps substantially improve multi-step reasoning accuracy.",
             "Reasoning chains themselves can hallucinate intermediate premises without internal uncertainty monitoring."),
            ("Improving Factuality and Reasoning in Language Models through Multiagent Debate",
             "Du et al. [31]", "2024", "Multi-Agent Iterative Debate",
             "Multiple LLM instances critique and refine each other's answers over several rounds to reduce factual errors.",
             "Multiplies token and latency cost by N_agents x N_rounds (typically 6x–15x)."),
            ("Woodpecker: Hallucination Correction for Multimodal Large Language Models",
             "Yin et al. [32]", "2024", "Woodpecker (Post-Hoc Visual Claim Verification)",
             "Extracted key concepts from MLLM outputs, verified them with visual detectors, and rewrote hallucinated spans.",
             "Post-processing pipeline tailored to image-caption claims; high multi-model latency."),
            ("RARR: Researching and Revising What Language Models Say, Using Language Models",
             "Gao et al. [33]", "2023", "RARR (Post-Hoc Attribution & Revision)",
             "Generated search queries for unverified claims in an LLM output and edited unsupported statements.",
             "Runs after full generation on every output rather than gating on single-pass internal risk."),
            ("CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing",
             "Gou et al. [39]", "2023", "CRITIC (Tool-Interactive Iterative Self-Correction)",
             "Allowed LLMs to verify and revise their own outputs by interacting with search engines and code interpreters.",
             "Requires multiple iterative tool-invocation loops and provides no calibrated abstention guarantee."),
            ("Can Knowledge Graphs Reduce Hallucinations in LLMs? A Survey",
             "Agrawal et al. [40]", "2024", "KG-Augmented Grounding & Verification Taxonomy",
             "Synthesized knowledge-graph retrieval, graph-guided decoding, and post-hoc KG triple verification.",
             "Survey only; depends on curated domain knowledge graphs that are often incomplete for open-domain queries."),
        ],
    ),
    (
        "2. Literature Review — VI",
        "Pillar 6 · Explainability and human trust calibration.",
        "Users need transparent sensor attributions and calibrated confidence cues rather than opaque risk numbers.",
        [
            ("Making Sense of the Unsensible: Survey & Challenges for XAI in LLMs Toward Human-Centered AI",
             "Herrera [8]", "2025", "Four-Dimension LLM XAI Framework",
             "Defined faithfulness, truthfulness, plausibility, and contrastivity as the four pillars of human-centered LLM XAI.",
             "Conceptual taxonomy; does not provide an algorithmic real-time sensor-attribution engine."),
            ("Why Would You Suggest That? Human Trust in Language Model Responses",
             "Sharma et al. [19]", "2024", "Empirical Study of Explanation Framing & Trust",
             "Demonstrated in human-subject trials that comparative and contrastive explanations improve appropriate trust calibration.",
             "Behavioral study using mocked explanations; not connected to live internal LLM hallucination sensors."),
        ],
    ),
]


def set_cell_border(cell, **kwargs):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement("w:tcBorders")
        tcPr.append(tcBorders)
    for edge, val in kwargs.items():
        edge_el = tcBorders.find(qn(f"w:{edge}"))
        if edge_el is None:
            edge_el = OxmlElement(f"w:{edge}")
            tcBorders.append(edge_el)
        for k, v in val.items():
            edge_el.set(qn(f"w:{k}"), str(v))


def add_bottom_rule(paragraph, color="1F3A60", sz="12"):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), sz)
    bottom.set(qn("w:space"), "4")
    bottom.set(qn("w:color"), color)
    pBdr.append(bottom)
    pPr.append(pBdr)


def build_docx(paths):
    doc = docx.Document()
    for sec in doc.sections:
        sec.top_margin = Inches(0.65)
        sec.bottom_margin = Inches(0.65)
        sec.left_margin = Inches(0.6)
        sec.right_margin = Inches(0.6)

    navy = RGBColor(0x1F, 0x3A, 0x60)
    grey = RGBColor(0x59, 0x59, 0x59)
    dark = RGBColor(0x1A, 0x1A, 0x1A)

    headers = ["Paper name", "Author(s) & ID", "Year", "Method", "Key contribution", "Gap identified"]
    widths = [Inches(1.65), Inches(1.05), Inches(0.48), Inches(1.25), Inches(1.65), Inches(1.62)]

    idx_start = 1
    for t_idx, (sec_title, pillar_title, pillar_desc, rows) in enumerate(PILLARS, 1):
        idx_end = idx_start + len(rows) - 1

        # Navy section title with bottom rule (exact screenshot style)
        p_head = doc.add_paragraph()
        p_head.paragraph_format.space_before = Pt(10 if t_idx > 1 else 0)
        p_head.paragraph_format.space_after = Pt(6)
        r_head = p_head.add_run(sec_title)
        r_head.bold = True
        r_head.font.name = "Georgia"
        r_head.font.size = Pt(18)
        r_head.font.color.rgb = navy
        add_bottom_rule(p_head, color="1F3A60", sz="12")

        # Pillar title + 1-sentence description
        p_pil = doc.add_paragraph()
        p_pil.paragraph_format.space_before = Pt(4)
        p_pil.paragraph_format.space_after = Pt(2)
        r1 = p_pil.add_run(pillar_title + " ")
        r1.bold = True
        r1.font.name = "Calibri"
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = dark
        r2 = p_pil.add_run(pillar_desc)
        r2.font.name = "Calibri"
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = dark

        # Grey table caption: "Table k — papers a–b of 40"
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(0)
        p_cap.paragraph_format.space_after = Pt(4)
        rc = p_cap.add_run(f"Table {t_idx} — papers {idx_start}–{idx_end} of 40")
        rc.font.name = "Calibri"
        rc.font.size = Pt(9.5)
        rc.font.color.rgb = grey

        # 6-column navy-bordered table
        tbl = doc.add_table(rows=len(rows) + 1, cols=6)
        tbl.autofit = False
        bspec = {"val": "single", "sz": "6", "space": "0", "color": "1F3A60"}

        for j, htext in enumerate(headers):
            c = tbl.cell(0, j)
            c.width = widths[j]
            set_cell_border(c, top=bspec, bottom=bspec, left=bspec, right=bspec)
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            rn = p.add_run(htext)
            rn.bold = True
            rn.font.name = "Calibri"
            rn.font.size = Pt(9.5)
            rn.font.color.rgb = navy

        for i, row in enumerate(rows, 1):
            for j, val in enumerate(row):
                c = tbl.cell(i, j)
                c.width = widths[j]
                set_cell_border(c, top=bspec, bottom=bspec, left=bspec, right=bspec)
                p = c.paragraphs[0]
                p.paragraph_format.space_before = Pt(2.5)
                p.paragraph_format.space_after = Pt(2.5)
                rn = p.add_run(val)
                rn.bold = (j == 0)
                rn.font.name = "Calibri"
                rn.font.size = Pt(9)
                rn.font.color.rgb = dark

        idx_start = idx_end + 1

    # Section VII: Cross-Pillar Synthesis & How TRUEGUARD Resolves the 5 Gaps Across All 40 Papers
    p_head = doc.add_paragraph()
    p_head.paragraph_format.space_before = Pt(12)
    p_head.paragraph_format.space_after = Pt(6)
    r_head = p_head.add_run("2. Literature Review — VII (Cross-Pillar Synthesis & TRUEGUARD Mapping)")
    r_head.bold = True
    r_head.font.name = "Georgia"
    r_head.font.size = Pt(18)
    r_head.font.color.rgb = navy
    add_bottom_rule(p_head, color="1F3A60", sz="12")

    p_pil = doc.add_paragraph()
    p_pil.paragraph_format.space_before = Pt(4)
    p_pil.paragraph_format.space_after = Pt(2)
    r1 = p_pil.add_run("Synthesis of Research Gaps Across Pillars 1–6. ")
    r1.bold = True
    r1.font.name = "Calibri"
    r1.font.size = Pt(10.5)
    r1.font.color.rgb = dark
    r2 = p_pil.add_run("How each pillar and identified research gap maps to a verified module in TRUEGUARD v2.")
    r2.font.name = "Calibri"
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = dark

    p_cap = doc.add_paragraph()
    p_cap.paragraph_format.space_before = Pt(0)
    p_cap.paragraph_format.space_after = Pt(4)
    rc = p_cap.add_run("Table 7 — Cross-pillar gap synthesis and empirical resolution in TRUEGUARD v2 (40-study corpus)")
    rc.font.name = "Calibri"
    rc.font.size = Pt(9.5)
    rc.font.color.rgb = grey

    syn_headers = ["Pillar & Paper IDs", "Core Literature Finding", "Cross-Corpus Gap Identified",
                   "TRUEGUARD v2 Architectural Module", "Verified Tesla T4 GPU Result"]
    syn_widths = [Inches(1.25), Inches(1.45), Inches(1.55), Inches(1.65), Inches(1.80)]
    syn_rows = [
        ("Pillar 1: Internal States\n[1, 2, 5, 13, 16, 27, 28, 38]",
         "Middle-to-late hidden layers encode linear truthfulness directions and representation drift.",
         "Probes are evaluated in isolation without out-of-fold fusion or closed-loop repair.",
         "Sensor 1 (ISP — 4-layer OOF-stacked logistic probes) + Sensor 4 (DST cosine drift).",
         "0.935 macro AUROC across 4 benchmarks; ISP adds +0.188 to +0.251 AUROC over surface signals."),
        ("Pillar 2: Uncertainty & Entropy\n[4, 6, 7, 14, 17, 21]",
         "Logit energy and multi-sample semantic entropy flag uncertain generations.",
         "Multi-sample UQ costs 5x–20x latency; single-pass logit entropy fails on fluent lies.",
         "Sensor 3 (EEM — 0.6 Shannon + 0.4 Renyi-2 logit monitor) fused with supervised ISP.",
         "36.41–39.30 ms/tok on T4 GPU (4.31x–4.65x faster than 169.31 ms/tok 5-sample baseline)."),
        ("Pillar 3: Attention & Multi-Signal\n[9, 11, 12, 36]",
         "Final-quartile attention head dispersal catches context detachment.",
         "Static scoring without grouped OOF stacking or thresholded corrective actuation.",
         "Sensor 2 (AAS — final-quartile attention entropy) + leakage-free Logistic Fusion.",
         "When ISP is unavailable (-ISP), AAS+EEM+DST provide a 0.626–0.918 training-free fallback."),
        ("Pillar 4: Benchmarks & Metrics\n[3, 10, 18, 22, 23, 29, 34, 35, 37]",
         "Paired and open-ended benchmarks quantify factuality and calibration.",
         "Answer-length differences between QA benchmarks invert uncalibrated entropy/NLL scores.",
         "Grouped 5-fold CV + automated polarity diagnostics + target-domain threshold calibration.",
         "0.986 (HaluEval-Summ), 0.975 (HaluEval-QA), 0.903 (HaluEval-Dial), 0.876 (TruthfulQA); ECE 0.024–0.042."),
        ("Pillar 5: Mitigation & Retrieval\n[15, 20, 24, 25, 26, 30, 31, 32, 33, 39, 40]",
         "Re-sampling, RAG, and RL abstention each fix only one failure mode.",
         "Detection and mitigation are disconnected; always-on RAG wastes compute on easy queries.",
         "Two calibrated thresholds (tau_warn=0.611, tau_fault=0.898) + 3-Tier Controller (Resample, Wikipedia RAG, Abstain).",
         "TriviaQA answered hallucination rate drops 62.0% -> 40.0% (-35.5% relative; -72.0% system-wide); AURC 0.412."),
        ("Pillar 6: Explainability & Trust\n[8, 19]",
         "Users require faithful, contrastive explanations to calibrate trust.",
         "Existing detectors emit opaque scalar numbers without per-sensor attribution.",
         "Signed per-sensor log-odds attribution (TrueGuardDetector.explain) + full tier decision trace.",
         "Every prediction outputs exact log-odds contributions of ISP, AAS, EEM, and DST."),
    ]
    tbl = doc.add_table(rows=len(syn_rows) + 1, cols=5)
    tbl.autofit = False
    bspec = {"val": "single", "sz": "6", "space": "0", "color": "1F3A60"}
    for j, htext in enumerate(syn_headers):
        c = tbl.cell(0, j); c.width = syn_widths[j]
        set_cell_border(c, top=bspec, bottom=bspec, left=bspec, right=bspec)
        p = c.paragraphs[0]; p.paragraph_format.space_before = Pt(3); p.paragraph_format.space_after = Pt(3)
        rn = p.add_run(htext); rn.bold = True; rn.font.name = "Calibri"; rn.font.size = Pt(9.5); rn.font.color.rgb = navy
    for i, row in enumerate(syn_rows, 1):
        for j, val in enumerate(row):
            c = tbl.cell(i, j); c.width = syn_widths[j]
            set_cell_border(c, top=bspec, bottom=bspec, left=bspec, right=bspec)
            p = c.paragraphs[0]; p.paragraph_format.space_before = Pt(2.5); p.paragraph_format.space_after = Pt(2.5)
            rn = p.add_run(val); rn.bold = (j == 0); rn.font.name = "Calibri"; rn.font.size = Pt(9); rn.font.color.rgb = dark

    for p in paths:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        doc.save(p)
        print("wrote", p)


def build_md(path):
    lines = ["# Comprehensive 40-Paper Literature Review Classified by the Six Pillars\n"]
    idx_start = 1
    for t_idx, (sec_title, pillar_title, pillar_desc, rows) in enumerate(PILLARS, 1):
        idx_end = idx_start + len(rows) - 1
        lines.append(f"## {sec_title}\n")
        lines.append(f"**{pillar_title}** {pillar_desc}\n")
        lines.append(f"*Table {t_idx} — papers {idx_start}–{idx_end} of 40*\n")
        lines.append("| Paper name | Author(s) & ID | Year | Method | Key contribution | Gap identified |")
        lines.append("|:---|:---|:---:|:---|:---|:---|")
        for r in rows:
            lines.append(f"| **{r[0]}** | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} |")
        lines.append("")
        idx_start = idx_end + 1
    open(path, "w", encoding="utf8").write("\n".join(lines))
    print("wrote", path)


if __name__ == "__main__":
    build_docx([
        r"E:\trueguard\TRUEGUARD_40_Papers_Literature_Review_By_Pillars.docx",
        r"E:\trueguard\CAPSTONE\FInal\paper\TRUEGUARD_40_Papers_Literature_Review_By_Pillars.docx",
    ])
    build_md(r"E:\trueguard\TRUEGUARD_40_Papers_Literature_Review_By_Pillars.md")

