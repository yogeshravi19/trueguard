import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

doc = docx.Document()

# Page Margins
for s in doc.sections:
    s.top_margin = Inches(1.0)
    s.bottom_margin = Inches(1.0)
    s.left_margin = Inches(1.0)
    s.right_margin = Inches(1.0)

# Styles
normal_style = doc.styles['Normal']
normal_style.font.name = 'Times New Roman'
normal_style.font.size = Pt(11)
normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

# Title
title_p = doc.add_paragraph()
title_p.paragraph_format.space_before = Pt(0)
title_p.paragraph_format.space_after = Pt(4)
r = title_p.add_run("RESPONSE TO REVIEWERS' COMMENTS")
r.bold = True
r.font.size = Pt(16)
r.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

meta_p = doc.add_paragraph()
meta_p.paragraph_format.space_before = Pt(0)
meta_p.paragraph_format.space_after = Pt(16)
r_meta = meta_p.add_run(
    "Manuscript Number: Ms. No. 269790004\n"
    "Title: Toward Trustworthy Large Language Models: A Comprehensive Review of Hallucination Detection, Explainability, and Mitigation Strategies\n"
    "Journal: Systems Science & Control Engineering (Taylor & Francis)\n"
    "Authors: Yogesh Ravi M, Pradeep Kumar T S\n"
    "Corresponding Author: Yogesh Ravi M (yogeshravi.m2022@vitstudent.ac.in)\n"
    "Academic Editor: Dr. Zidong Wang"
)
r_meta.font.size = Pt(10)
r_meta.font.italic = True
r_meta.font.color.rgb = RGBColor(0x44, 0x44, 0x44)

# Intro Letter
p_intro = doc.add_paragraph()
p_intro.paragraph_format.space_after = Pt(12)
p_intro.paragraph_format.line_spacing = 1.15
p_intro.add_run(
    "Dear Academic Editor Dr. Zidong Wang and Reviewers,\n\n"
    "Thank you for reviewing our manuscript and for providing detailed, constructive feedback. "
    "We have revised the paper carefully to address every comment. "
    "All changes in the revised manuscript have been highlighted in colored text so they are easy to locate.\n\n"
    "Below is our point-by-point response to each reviewer comment, quoting the exact words of the reviewers followed by our response and the exact section where the changes were made."
)

# Helper function to add QA blocks
def add_qa(reviewer_label, comment_exact, response_simple, location_text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(14)
    h.paragraph_format.space_after = Pt(4)
    r_h = h.add_run(reviewer_label)
    r_h.bold = True
    r_h.font.size = Pt(12)
    r_h.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
    
    # Table for Exact Reviewer Comment
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.cell(0, 0)
    set_cell_background(c, "F4F6F8")
    set_cell_margins(c, 100, 100, 150, 150)
    cp = c.paragraphs[0]
    cp.paragraph_format.space_after = Pt(0)
    r_clbl = cp.add_run("Reviewer Comment (Exact Words):\n")
    r_clbl.bold = True
    r_clbl.font.size = Pt(10)
    r_clbl.font.color.rgb = RGBColor(0x33, 0x41, 0x55)
    r_ctxt = cp.add_run(f'"{comment_exact}"')
    r_ctxt.font.italic = True
    r_ctxt.font.size = Pt(10)
    r_ctxt.font.color.rgb = RGBColor(0x1E, 0x29, 0x3B)
    
    # Simple Response
    rp = doc.add_paragraph()
    rp.paragraph_format.space_before = Pt(8)
    rp.paragraph_format.space_after = Pt(4)
    rp.paragraph_format.line_spacing = 1.15
    r_rlbl = rp.add_run("Author's Response:\n")
    r_rlbl.bold = True
    r_rlbl.font.color.rgb = RGBColor(0x0D, 0x6E, 0x38)
    rp.add_run(response_simple)
    
    # Location
    lp = doc.add_paragraph()
    lp.paragraph_format.space_before = Pt(2)
    lp.paragraph_format.space_after = Pt(10)
    r_llbl = lp.add_run("Location of Changes: ")
    r_llbl.bold = True
    r_llbl.font.size = Pt(10)
    r_ltxt = lp.add_run(location_text)
    r_ltxt.font.size = Pt(10)
    r_ltxt.font.italic = True

# Reviewer 1
add_qa(
    "Reviewer 1 — Comment 1",
    "The review is described as comprehensive/systematic, but the search strategy and study selection process are not sufficiently explained. The authors should specify the databases, search terms, time period, inclusion/exclusion criteria, and screening procedure. Important works such as SelfCheckGPT, TruthfulQA, FActScore, Chain-of-Verification, RAG, and Self-RAG should also be discussed to support the claimed coverage.",
    "We agree completely. We have made two major additions to the paper:\n"
    "1. Added a full Methodology Section (Section 2) using PRISMA guidelines: We explicitly list the five databases searched (Scopus, Web of Science, IEEE Xplore, ACM Digital Library, and arXiv), the exact search query, the date window (January 1, 2020 to February 28, 2026), 6 inclusion criteria (IC1–IC6), and 4 exclusion criteria (EC1–EC4). We also document the screening numbers at each stage (688 retrieved -> 196 duplicates removed -> 492 screened -> 324 excluded -> 168 assessed -> 128 excluded -> 40 final included papers) in Table 1 and in the Figure 2 PRISMA flow diagram.\n"
    "2. Included all six requested landmark papers: We expanded the literature review to 40 papers and added detailed discussions of all six suggested studies:\n"
    "   - SelfCheckGPT [21] is added to Section 3.2 (black-box consistency testing).\n"
    "   - TruthfulQA [22] and FActScore [23] are added to Section 3.4 (benchmarks for factuality and atomic facts).\n"
    "   - RAG [25], Self-RAG [26], and Chain-of-Verification (CoVe) [24] are added to Section 3.5 (mitigation through retrieval and verification).",
    "Section 2 (Methodology), Subsections 2.1–2.6; Table 1; Figure 2; Section 3, Subsections 3.2, 3.4, and 3.5; Table 2 and Table 3."
)

add_qa(
    "Reviewer 1 — Comment 2",
    "The manuscript is often descriptive rather than critical. The authors should discuss the assumptions, limitations, generalizability, computational requirements, and model-access requirements of the reviewed approaches. In addition, the six-pillar taxonomy contains overlaps, particularly among internal-state analysis, uncertainty estimation, and attention-based methods. The taxonomy should be better justified or refined.",
    "We agree with this advice. We have made the review much more critical and justified the taxonomy:\n"
    "1. Taxonomy Justification: At the start of Section 3, we added an explanation for boundary-crossing papers. We explain that some methods naturally combine signals (for example, SEPs uses internal hidden states to predict semantic entropy in one step, and LLM-Check uses both attention and hidden states). We clarify that our six pillars categorize each method based on its primary signal source and where it acts in the model's generation process.\n"
    "2. Critical Trade-offs (Section 4): We expanded Section 4 to directly compare operational trade-offs across all methods:\n"
    "   - Computing cost and latency: We compare multi-pass methods (SelfCheckGPT takes 5 to 10 passes) against single-pass methods (SEPs, RAUQ) and fast engineering (LLM-Check gives up to 450x speedup).\n"
    "   - Model access: We contrast open-weight white-box methods against commercial black-box APIs (like OpenAI or Anthropic).\n"
    "   - Table 4 compares all detection methods across model access, extra passes, supervision, and performance on intrinsic vs. extrinsic errors.",
    "Section 3 (Boundary Crossings text); Section 4 (Comparative Analysis); Table 4; Figures 7 and 8."
)

add_qa(
    "Reviewer 1 — Comment 3",
    "TRUEGUARD is an interesting idea, but its current presentation is largely conceptual. More detail is needed on signal fusion, mitigation thresholds, decision mechanisms, evaluation, and system architecture. Given the journal scope, the framework should also be connected more explicitly to control concepts such as sensing, feedback, actuation, robustness, fault detection, and adaptive control.",
    "We thank the reviewer for this guidance. To fit the scope of Systems Science & Control Engineering, we created a dedicated Section 6 titled 'TRUEGUARD: A Closed-Loop Control Architecture'. We explain TRUEGUARD using standard control systems principles:\n"
    "1. Sensor Layer (6.1): Monitors the model in a single forward pass across 4 non-redundant sensors: State Sensor (hidden layers [1], [2], [14]), Observation Sensor (attention heads [9], [11]), Output Sensor (logit energy and entropy [4], [17]), and Temporal Sensor (distribution drift [13], [16]).\n"
    "2. Signal Fusion & Conflict Resolution (6.2): Combines the four signals into an aggregate Risk Score R (0 to 1). Attention is prioritized for internal self-contradictions, while logit entropy is prioritized for fabricated external facts.\n"
    "3. Fault Detection Thresholds (6.3): Establishes clear operating regimes: Normal Regime (Risk Score below Warning Threshold), Warning Regime (between Warning and Fault Thresholds), and Fault Regime (exceeding Fault Threshold).\n"
    "4. Tiered Closed-Loop Actuation (6.4): Applies feedback in three stages: Tier 1 (local constrained re-sampling [24]), Tier 2 (targeted claim retrieval [20], [25], [26]), and Tier 3 (calibrated abstention [15] when facts are missing).\n"
    "5. Explainability and Trust Feedback (6.5): Converts technical sensor data into user-facing explanations using Herrera's 4 XAI dimensions [8] and Sharma's comparative trust calibration [19].",
    "Section 6 (TRUEGUARD: A Closed-Loop Control Architecture), Subsections 6.1 through 6.5."
)

add_qa(
    "Reviewer 1 — Comment 4",
    "The discussion of hallucination detection for API-based or black-box LLMs should be strengthened. The authors should also consider evaluation criteria beyond detection accuracy, including false-positive/false-negative trade-offs, calibration, latency, computational overhead, mitigation effectiveness, and robustness across models.",
    "We have strengthened our discussion of black-box models and multi-metric evaluations:\n"
    "1. Black-Box Methods: In Subsections 3.2, 4.3, and 7, we analyze commercial API models where internal weights cannot be seen. We evaluate token-level Entropy Production Rate (EPR [17]), companion output sampling (SelfCheckGPT [21]), and the black-box version of LLM-Check [12] (which achieves a 450x speedup with minimal accuracy loss).\n"
    "2. Multi-Metric Evaluation: In Section 4 and Table 4, we evaluate methods across multiple criteria beyond accuracy: F1-score (balancing false positives and false negatives), calibration error (Brier score / ECE), inference passes, latency speedup, and cross-domain robustness.",
    "Section 3, Subsections 3.2 and 3.4; Section 4 (The Efficiency Question and The Access Problem); Section 7; Table 4."
)

# Reviewer 2
add_qa(
    "Reviewer 2 — Point 1",
    "A description of the databases/search engines used, complete search strings, search period, inclusion and exclusion criteria, screening procedure, number of initially retrieved studies, duplicate removal, full text assessment, and the final selection procedure should be provided by the authors. Transparency can be greatly enhanced by a flow diagram similar to the one used in the PRISMA project.",
    "We agree completely. In Section 2, we have documented the entire literature search in detail:\n"
    "- Databases: Scopus, Web of Science, IEEE Xplore, ACM Digital Library, and arXiv.\n"
    "- Search Dates & Query: January 2020 to February 2026, using an exact Boolean search query.\n"
    "- Selection Pipeline: 688 initial records retrieved -> 196 duplicates removed -> 492 screened on title and abstract -> 324 excluded -> 168 assessed in full text -> 128 excluded with documented reasons -> 40 final included papers.\n"
    "- Table 1: Summarizes the entire search strategy and criteria.\n"
    "- Figure 2 (PRISMA Flow Diagram): We created and included a clean, high-resolution (300 DPI) PRISMA flow diagram showing every step and exact count.",
    "Section 2 (Methodology and Literature Search), Subsections 2.1–2.5; Table 1; Figure 2."
)

add_qa(
    "Reviewer 2 — Point 2",
    "Explain how the 20 studies were selected. For a 'comprehensive' review of such a fast-growing field, 20 is a fairly small number of studies. Why these studies were chosen by the authors should be explained and the 20 main studies should be clearly identified from supporting/background studies should be clearly distinguished.",
    "Thank you for pointing this out. In our original draft, the phrase 'loose survey of twenty current sources' in the abstract was misleading. We have resolved this in the revised manuscript:\n"
    "1. Expanded Corpus: We expanded our formal review to 40 representative papers selected under strict quality criteria (algorithmic formulation, standard benchmarks, reliable metrics, and model access disclosure).\n"
    "2. Removed 'loose survey': We completely removed the phrase 'loose survey' from the Abstract and Introduction.\n"
    "3. Clear Two-Tier Corpus Structure (Subsection 2.6): We explain how the 40 papers are structured:\n"
    "   - 20 Core Architectural Studies: Advanced technical papers testing internal probing, entropy, attention heads, distribution shifts, and calibrated RL ([1]–[20]).\n"
    "   - 20 Foundational Benchmarks and Mitigation Frameworks: Landmark papers defining evaluation baselines (TruthfulQA, HaluEval, FActScore), mitigation methods (RAG, Self-RAG, CoVe), and black-box sampling (SelfCheckGPT) ([21]–[40]).",
    "Abstract; Section 1; Section 2 (Subsection 2.6); Section 3."
)

add_qa(
    "Reviewer 2 — Point 3",
    "Conduct an overall citation and reference check. The name of the author, method names and citation numbers do not seem to match up. For instance, there is a reference [18] to a 'Comprehensive Hallucination Survey' by Alansari and Luqman, as part of the manuscript, but the bibliography needs to be checked. Reference to the original publication must be made for each citation.",
    "We have conducted a complete audit of every in-text citation and reference entry:\n"
    "- Reference [18]: Alansari and Luqman ('Large language models hallucination: A comprehensive survey') is now placed at entry [18] in the References list, matching all citations in Section 1 and Section 3.4.\n"
    "- Reference [2]: Zhang et al. (PRISM) is placed at entry [2], matching the in-text citation in Section 3.1.\n"
    "- References [21]–[40]: All landmark papers (SelfCheckGPT [21], TruthfulQA [22], FActScore [23], CoVe [24], RAG [25], Self-RAG [26], etc.) are verified against official published metadata and numbered in exact sequence.\n"
    "- Every single citation in the text now maps strictly 1-to-1 to the bibliography.",
    "Section 3, Section 4, Section 8, and the References list ([1] through [40])."
)

add_qa(
    "Reviewer 2 — Point 4",
    "Use the appropriate unit of measurement for every number in figures and tables which bear a numerical value. Indicate if each value has been copied from an original article, calculated by the authors, approximated from a figure, or transformed/normalized. Quantitative comparisons should be accompanied by a dataset, a model, a definition of the metric, an experimental setting, and a source citation.",
    "We have updated all tables and figures to make the origin of all data completely clear:\n"
    "- Source Citations: Every number in Table 2, Table 3, and Table 4 now directly cites the original published paper, listing the exact dataset (e.g., HaluEval, TruthfulQA, WikiBio), the model family and size (LLaMA-2 7B/70B, GPT-4, Mistral-7B), and the standardized metric units (AUROC, Precision %, Accuracy %, Consistency %).\n"
    "- Qualitative Ratings: In Table 4, ratings for Intrinsic and Extrinsic detection efficacy are explicitly labeled as qualitative author assessments based on reported findings in the primary papers.",
    "Table 1, Table 2, Table 3, and Table 4; captions of Figures 1–8."
)

add_qa(
    "Reviewer 2 — Point 5",
    "Do not compare methods tested in different contexts. AUROC, F1, accuracy, calibration error, retrieval performance and percentage improvements should not be directly compared for different models and datasets without a defensible normalization or common evaluation methodology.",
    "We fully agree with this principle. In Section 4, we now clearly contextualize all method comparisons:\n"
    "- We evaluate methods grouped by task and access type (white-box vs. black-box) rather than ranking raw numbers across mismatched benchmarks.\n"
    "- Table 2 explicitly describes the limitations of each benchmark (e.g., synthetic generation templates in HaluEval, short-answer format in TruthfulQA, external retrieval quality in FActScore) to prevent misleading direct comparisons.",
    "Section 4 (Comparative Analysis); Table 2; Table 4."
)

add_qa(
    "Reviewer 2 — Point 6",
    "Eliminate or substantiate the reported TRUEGUARD performance by experimentation. The manuscript outlines the conceptual framework TRUEGUARD, but the comparison table shows a success rate of around 65%. This number should be deleted if a protocol for the full evaluation or empirical evidence of TRUEGUARD implementation / experiment is not provided.",
    "We accept this critique completely. Including the '~65% success rate' was an error in our previous draft:\n"
    "- Completely Deleted: We have 100% deleted the '~65%' number and removed the 'Success Rate %' column from all comparison tables.\n"
    "- Honest Conceptual Framing: TRUEGUARD is now clearly presented throughout the Abstract, Section 1, Section 5, and Section 6 strictly as a conceptual closed-loop architecture that unifies existing methods, without claiming unverified experimental test scores.",
    "Abstract; Section 1; Section 5; Section 6; Table 3 and Table 4."
)

add_qa(
    "Reviewer 2 — Point 7",
    "Improve TRUEGUARD in the form of a conceptual architecture. Describe the fusion of the four signals, the determination of thresholds, how conflicting signals are dealt with, how explanations are generated, when retrieval and abstention is triggered, what kind of model access is needed and what kind of computational overhead is expected. A forward pass is currently proposed to extract several signals from the manuscript but this assumption needs to be carefully qualified.",
    "We have completely rewritten Section 6 to provide technical details for every question raised:\n"
    "1. Single Forward-Pass Extraction (6.1): We qualify this assumption by explaining that hidden states, attention maps, and logits are already produced during standard transformer decoding. By attaching lightweight linear probes and caching attention tensors during the forward pass, extracting multiple signals adds negligible delay compared to multi-sample generation.\n"
    "2. Signal Fusion & Conflict Resolution (6.2): We explain how the system resolves conflicting signals. Attention tracking is prioritized for detecting internal self-contradictions, while logit entropy is prioritized for detecting fabricated external facts, producing an aggregate Risk Score between 0 and 1.\n"
    "3. Determining Thresholds (6.3): We define calibrated decision rules using a Warning Threshold and a Fault Threshold to separate Normal, Warning, and Fault operating regimes.\n"
    "4. Actuation Triggers (6.4): Explains when each corrective action is triggered: Tier 1 (local constrained re-sampling) under mild warnings; Tier 2 (targeted claim retrieval) when factual knowledge is missing; and Tier 3 (calibrated abstention) when uncertainty cannot be resolved below the fault threshold.\n"
    "5. Explanation Generation (6.5): Grounded in Herrera's 4 XAI dimensions [8], explaining how sensor data is translated into token risk highlights, alarm attribution, and contrastive rationales.",
    "Section 6 (TRUEGUARD: A Closed-Loop Control Architecture), Subsections 6.1 through 6.5."
)

# Closing
p_close = doc.add_paragraph()
p_close.paragraph_format.space_before = Pt(14)
p_close.paragraph_format.space_after = Pt(4)
p_close.paragraph_format.line_spacing = 1.15
p_close.add_run(
    "Conclusion and Acknowledgments:\n"
    "We once again thank Dr. Zidong Wang and both reviewers for their constructive comments. "
    "Their feedback has helped us significantly improve the quality and technical clarity of this paper. "
    "We hope that the revised manuscript meets the standards of Systems Science & Control Engineering, and we look forward to your decision.\n\n"
    "Sincerely,\n\n"
    "Yogesh Ravi M & Dr. Pradeep Kumar T S\n"
    "Department of Computer Science\n"
    "Vellore Institute of Technology (VIT), Chennai, Tamil Nadu, India\n"
    "Corresponding Author Email: yogeshravi.m2022@vitstudent.ac.in"
)

output_path = r'E:\trueguard\CAPSTONE\Response_to_Reviewers_269790004.docx'
doc.save(output_path)
print(f'Successfully updated: {output_path}')
