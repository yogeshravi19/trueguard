import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex="F2F4F7"):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_table_borders(table, color="CCCCCC"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="{color}"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>
            <w:left w:val="single" w:sz="6" w:space="0" w:color="{color}"/>
            <w:right w:val="single" w:sz="6" w:space="0" w:color="{color}"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
            <w:insideV w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def build_response_document(out_path):
    doc = Document()

    # Set 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Base Styles
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = RGBColor(0, 0, 0) # Fully black
    style_normal.paragraph_format.line_spacing = 1.15
    style_normal.paragraph_format.space_after = Pt(6)

    # Helper function for title & headings
    def add_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(15)
        run.font.color.rgb = RGBColor(0, 0, 0)
        p.paragraph_format.space_after = Pt(4)
        return p

    def add_meta_line(label, value):
        p = doc.add_paragraph()
        run_l = p.add_run(label + ": ")
        run_l.bold = True
        run_l.font.name = 'Times New Roman'
        run_l.font.size = Pt(11)
        run_l.font.color.rgb = RGBColor(0, 0, 0)
        
        run_v = p.add_run(value)
        run_v.font.name = 'Times New Roman'
        run_v.font.size = Pt(11)
        run_v.font.color.rgb = RGBColor(0, 0, 0)
        p.paragraph_format.space_after = Pt(3)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(8)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.5)
        run.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_comment_response_block(comment_title, exact_comment_text, author_response_text, location_text):
        add_h2(comment_title)
        
        tbl = doc.add_table(rows=3, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl, color="A0A0A0")

        # Row 0: Exact Comment
        cell0 = tbl.cell(0, 0)
        set_cell_margins(cell0, top=120, bottom=120, left=160, right=160)
        set_cell_shading(cell0, "F5F5F5")
        p0 = cell0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0_lbl = p0.add_run("Comment / Requirement (Exact Words):\n")
        r0_lbl.bold = True
        r0_lbl.font.name = 'Times New Roman'
        r0_lbl.font.size = Pt(10.5)
        r0_lbl.font.color.rgb = RGBColor(0, 0, 0)
        r0_txt = p0.add_run(f'"{exact_comment_text}"')
        r0_txt.italic = True
        r0_txt.font.name = 'Times New Roman'
        r0_txt.font.size = Pt(10.5)
        r0_txt.font.color.rgb = RGBColor(0, 0, 0)

        # Row 1: Author Response
        cell1 = tbl.cell(1, 0)
        set_cell_margins(cell1, top=140, bottom=140, left=160, right=160)
        p1 = cell1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(4)
        r1_lbl = p1.add_run("Author's Response:\n")
        r1_lbl.bold = True
        r1_lbl.font.name = 'Times New Roman'
        r1_lbl.font.size = Pt(11)
        r1_lbl.font.color.rgb = RGBColor(0, 0, 0)
        
        # Add response paragraphs
        resp_lines = author_response_text.strip().split("\n\n")
        for idx, line in enumerate(resp_lines):
            if idx == 0:
                p_curr = p1
            else:
                p_curr = cell1.add_paragraph()
                p_curr.paragraph_format.space_after = Pt(4)
            r = p_curr.add_run(line.strip())
            r.font.name = 'Times New Roman'
            r.font.size = Pt(11)
            r.font.color.rgb = RGBColor(0, 0, 0)

        # Row 2: Location of Changes
        cell2 = tbl.cell(2, 0)
        set_cell_margins(cell2, top=100, bottom=100, left=160, right=160)
        set_cell_shading(cell2, "FAFAFA")
        p2 = cell2.paragraphs[0]
        p2.paragraph_format.space_after = Pt(2)
        r2_lbl = p2.add_run("Location of Changes: ")
        r2_lbl.bold = True
        r2_lbl.font.name = 'Times New Roman'
        r2_lbl.font.size = Pt(10.5)
        r2_lbl.font.color.rgb = RGBColor(0, 0, 0)
        r2_txt = p2.add_run(location_text)
        r2_txt.font.name = 'Times New Roman'
        r2_txt.font.size = Pt(10.5)
        r2_txt.font.color.rgb = RGBColor(0, 0, 0)

        # Space after table
        p_sp = doc.add_paragraph()
        p_sp.paragraph_format.space_before = Pt(0)
        p_sp.paragraph_format.space_after = Pt(6)

    # -------------------------------------------------------------
    # DOCUMENT HEADER
    # -------------------------------------------------------------
    add_title("POINT-BY-POINT RESPONSE TO EDITORIAL TECHNICAL CHECKS & REVIEWER COMMENTS")
    doc.add_paragraph() # blank line

    add_meta_line("Journal", "Systems Science & Control Engineering (Taylor & Francis)")
    add_meta_line("Manuscript Number", "Ms. No. 269790004")
    add_meta_line("Manuscript Title", "Toward Trustworthy Large Language Models: A Comprehensive Review of Hallucination Detection, Explainability, and Mitigation")
    add_meta_line("Authors", "Yogesh Ravi M, Pradeep Kumar T S")
    add_meta_line("Institution", "School of Computer Science and Engineering, Vellore Institute of Technology (VIT), Chennai, India")
    add_meta_line("Date of Resubmission", "October 2026")

    # Cover Letter Opening
    p_cov = doc.add_paragraph()
    p_cov.paragraph_format.space_before = Pt(8)
    p_cov.paragraph_format.space_after = Pt(8)
    p_cov.add_run(
        "Dear Dr. Ajith Kumar BS, Academic Editor Dr. Zidong Wang, and Respected Reviewers,\n\n"
        "Thank you for reviewing our manuscript and for providing the constructive technical checks and peer review feedback. "
        "We have carefully addressed every item raised in the editorial decision and technical check notice. "
        "Below, we provide an exact, itemized point-by-point response detailing the specific revisions made to our manuscript. "
        "To facilitate verification, all modifications are highlighted in yellow within the accompanying marked manuscript "
        "('Toward Trustworthy Large Language Models_coloured.docx'), while a completely clean copy "
        "('Toward Trustworthy Large Language Models_standard.docx') is provided for publication."
    )

    # -------------------------------------------------------------
    # PART A: EDITORIAL TECHNICAL CHECKS
    # -------------------------------------------------------------
    add_h1("PART A: RESPONSE TO EDITORIAL TECHNICAL CHECKS")

    add_comment_response_block(
        "Editorial Office — Technical Check Point 1",
        "Please include a complete point-by-point response to the reviewer's comments included in your decision letter. This can be in the form of track changes or a separate document.",
        "We have prepared this comprehensive, itemized document providing an explicit response to every reviewer comment and editorial request from our decision letter.\n\n"
        "Along with this response document, we are submitting two complete versions of our revised manuscript:\n"
        "1. A marked revision document ('Toward Trustworthy Large Language Models_coloured.docx') with all newly added and updated prose highlighted in yellow for rapid verification.\n"
        "2. A clean, unhighlighted manuscript ('Toward Trustworthy Large Language Models_standard.docx') completely prepared for final production processing.",
        "This response document (Response_to_Reviewers_269790004.docx), Part B and Part C below; Marked manuscript (Toward Trustworthy Large Language Models_coloured.docx); Clean manuscript (Toward Trustworthy Large Language Models_standard.docx)."
    )

    add_comment_response_block(
        "Editorial Office — Technical Check Point 2",
        "We note that the information on 'Abstract' does not match the information you entered for your manuscript in the Submission Portal. Please update this to reflect the manuscript.",
        "We apologize for the discrepancy between the submission portal metadata and the manuscript. Our initial submission portal profile contained an earlier draft abstract that mentioned an outdated preliminary estimate ('~65%').\n\n"
        "We have completely synchronized the abstract text. The abstract is now exactly 214 words (well within the journal's 250-word limit), confirms our 40 PRISMA-compliant synthesized studies, explicitly outlines our six-pillar taxonomy, completely removes the unverified '~65%' claim, and introduces TRUEGUARD as a closed-loop control architecture. We have pasted this exact 214-word text into the submission portal Abstract field so that the portal and manuscript match word-for-word.",
        "Manuscript Abstract (Page 1, Paragraph 11); Submission Portal Metadata field ('Abstract')."
    )

    add_comment_response_block(
        "Editorial Office — Technical Check Point 3",
        "While conducting checks on your manuscript we noted that some of the figures and tables have not been referenced in the text. All figures/tables included in the manuscript should be referenced in the body of the text.",
        "We conducted a systematic, paragraph-by-paragraph audit of the entire manuscript to ensure that every single display item is explicitly introduced and discussed in the narrative.\n\n"
        "1. Figures: All 12 figures (Figure 1 through Figure 12) now possess explicit in-text citations in the body prose immediately preceding or adjacent to their placement. In addition, all 12 figures have their visual image files properly embedded directly above their respective captions, eliminating any empty paragraphs or formatting detachments.\n\n"
        "2. Tables: All 4 tables (Table 1 through Table 4) are explicitly called out by name in the body text (Table 1 in Section 2; Table 2 in Pillar 4; Table 3 in Pillar 5; Table 4 in Section 4).",
        "Throughout body prose: Figure 1 (P[15]), Figure 2 & Table 1 (P[80]), Figure 3 (P[125]), Figure 4 (P[153]), Figures 5 & 6 (P[166]), Table 2 (P[186]), Figures 7 & 8 (P[208]), Table 3 (P[216]), Figure 9 (P[222]), Figures 10, 11, 12 & Table 4 (P[251])."
    )

    # -------------------------------------------------------------
    # PART B: REVIEWER 1 COMMENTS
    # -------------------------------------------------------------
    add_h1("PART B: POINT-BY-POINT RESPONSE TO REVIEWER 1")

    add_comment_response_block(
        "Reviewer 1 — Comment 1",
        "The review is described as comprehensive/systematic, but the search strategy and study selection process are not sufficiently explained. The authors should specify the databases, search terms, time period, inclusion/exclusion criteria, and screening procedure. Important works such as SelfCheckGPT, TruthfulQA, FActScore, Chain-of-Verification, RAG, and Self-RAG should also be discussed to support the claimed coverage.",
        "We thank the reviewer for highlighting the need for greater methodological transparency. We have expanded Section 2 into a formal PRISMA 2020 systematic review protocol:\n\n"
        "1. Databases & Search Strategy: We searched five major databases—Scopus, Web of Science, IEEE Xplore, ACM Digital Library, and Google Scholar/arXiv—spanning January 2020 through December 2024. Table 1 lists our exact boolean search queries, eligibility filters, and screening criteria.\n\n"
        "2. Key Baseline & Benchmark Integration: We expanded our literature synthesis to comprehensively discuss and contextualize the pivotal baseline methods suggested by the reviewer:\n"
        "   - SelfCheckGPT (Manakul et al. [21]): Evaluated in Pillar 2 as a zero-resource, sampling-based black-box consistency checker.\n"
        "   - TruthfulQA (Lin et al. [22]) & FActScore (Min et al. [23]): Analyzed in Pillar 4 and Table 2 as standard evaluation benchmarks for factuality and myth-resistance.\n"
        "   - Chain-of-Verification (Dhuliawala et al. [24]): Examined in Pillar 5 as a self-corrective multi-step reasoning protocol.\n"
        "   - Standard RAG (Lewis et al. [25]) & Self-RAG (Asai et al. [26]): Evaluated in Pillar 5 as retrieval-grounded mitigation mechanisms, contrasted with adaptive approaches like ExpandR [20].",
        "Section 2 (PRISMA Methodology, Pages 3–5, Table 1, Figure 2); Section 3 (Pillars 2, 4, 5, Pages 7–16, References [21]–[26])."
    )

    add_comment_response_block(
        "Reviewer 1 — Comment 2",
        "The manuscript is often descriptive rather than critical. The authors should discuss the assumptions, limitations, generalizability, computational requirements, and model-access requirements of the reviewed approaches. In addition, the six-pillar taxonomy contains overlaps, particularly among internal-state analysis, uncertainty estimation, and attention-based methods. The taxonomy should be better justified or refined.",
        "We appreciate this constructive critique and have substantially revised our analysis across Sections 3 and 4 to provide a critical, comparative assessment rather than passive summaries:\n\n"
        "1. Critical Dimensions Added: For each technique, we now explicitly analyze model-access constraints (white-box versus black-box/API), computational runtime requirements, and generalization boundaries across model scales. These trade-offs are systematically compiled in Table 4.\n\n"
        "2. Taxonomy Boundaries Clarified: We clarified the conceptual and operational distinctions among Pillars 1, 2, and 3:\n"
        "   - Pillar 1 (Internal States): Probes latent feature representations and residual stream activations across intermediate layers (e.g., SAPLMA, INSIDE).\n"
        "   - Pillar 2 (Uncertainty Quantification): Operates on output probability distributions and semantic clustering over sampled token sequences (e.g., Semantic Entropy, SEP, SelfCheckGPT).\n"
        "   - Pillar 3 (Attention Mechanisms): Tracks routing weights across self-attention heads to detect when context tokens are being ignored (e.g., RAUQ, LLM-Check).\n"
        "We explain that these three pillars capture fundamentally different failure modes: internal states reflect latent truthfulness, entropy reflects output certainty, and attention maps reflect context grounding.",
        "Section 3 (Pillars 1, 2, 3 Introductions and Summaries, Pages 6–13); Section 4 (Comparative Analysis & Trade-Offs, Pages 17–20, Table 4)."
    )

    add_comment_response_block(
        "Reviewer 1 — Comment 3",
        "TRUEGUARD is an interesting idea, but its current presentation is largely conceptual. More detail is needed on signal fusion, mitigation thresholds, decision mechanisms, evaluation, and system architecture. Given the journal scope, the framework should also be connected more explicitly to control concepts such as sensing, feedback, actuation, robustness, fault detection, and adaptive control.",
        "We thank the reviewer for this invaluable guidance. In Section 6, we have restructured TRUEGUARD around classical closed-loop control and fault detection principles, directly aligning the work with the scope of Systems Science & Control Engineering:\n\n"
        "1. Plant & Sensors: The generative LLM is treated as the open-loop plant. Multi-modal internal probes (attention monitors, logit entropy trackers, hidden activation classifiers) act as sensors measuring system state during generation without extra sampling overhead.\n\n"
        "2. Fusion & Comparator Logic: A logistic fusion module combines sensor outputs into a normalized fault signal S_error = sigma(sum w_i * s_i), which is compared against dual calibrated decision boundaries (tau_warn and tau_fault).\n\n"
        "3. Tiered Actuation (Corrective Feedback): Instead of binary blocking, the controller applies proportional corrective control across three stages:\n"
        "   - Tier 1 (Activation Steering): Subtle steering vectors nudge internal layer representations when S_error is near tau_warn.\n"
        "   - Tier 2 (Targeted Retrieval): Query expansion and factual retrieval are triggered when uncertainty stems from missing evidence.\n"
        "   - Tier 3 (Supervised Abstention): The system abstains and generates a structured explanation when S_error exceeds tau_fault.\n\n"
        "4. Control Stability: We analyze closed-loop stability, preventing cascading error propagation in multi-turn reasoning workflows.",
        "Section 6 (A Closed-Loop Control Architecture: TRUEGUARD, Pages 22–26, Subsections 6.1–6.5)."
    )

    add_comment_response_block(
        "Reviewer 1 — Comment 4",
        "The discussion of hallucination detection for API-based or black-box LLMs should be strengthened. The authors should also consider evaluation criteria beyond detection accuracy, including false-positive/false-negative trade-offs, calibration, latency, computational overhead, mitigation effectiveness, and robustness across models.",
        "We have expanded our evaluation beyond conventional classification accuracy to address real-world deployment challenges:\n\n"
        "1. Black-Box & API Coverage: In Section 4 and Table 4, we evaluate methods that function strictly without internal access (SelfCheckGPT, LLM-Check black-box, SEP). We analyze the cost and latency implications of repeated API sampling passes.\n\n"
        "2. Multi-Metric Evaluation: We now analyze detection methods across Expected Calibration Error (ECE), F1-score balance, and runtime speedup factors. Figures 10, 11, and 12 map AUROC against F1 and runtime speedup, showing that LLM-Check's black-box variant delivers up to a 450x speedup over brute-force sampling while maintaining an AUROC within 0.02 of white-box baselines.",
        "Section 4 (Pages 17–20, Table 4, Figures 10, 11, 12)."
    )

    # -------------------------------------------------------------
    # PART C: REVIEWER 2 POINTS
    # -------------------------------------------------------------
    add_h1("PART C: POINT-BY-POINT RESPONSE TO REVIEWER 2")

    add_comment_response_block(
        "Reviewer 2 — Point 1",
        "A description of the databases/search engines used, complete search strings, search period, inclusion and exclusion criteria, screening procedure, number of initially retrieved studies, duplicate removal, full text assessment, and the final selection procedure should be provided by the authors. Transparency can be greatly enhanced by a flow diagram similar to the one used in the PRISMA project.",
        "We have incorporated a full PRISMA 2020 literature selection methodology in Section 2:\n\n"
        "1. Systematic Search Details: We documented our search across five primary academic databases (Scopus, Web of Science, IEEE Xplore, ACM Digital Library, and Google Scholar/arXiv) from January 2020 to December 2024. Table 1 lists the exact boolean queries, date windows, and selection rules.\n\n"
        "2. PRISMA Flow Diagram: We generated and added Figure 2 (PRISMA 2020 Flow Diagram) showing our exact study counts at every phase:\n"
        "   - Identification: 688 candidate records identified across databases.\n"
        "   - De-duplication: 168 duplicate records removed.\n"
        "   - Title/Abstract Screening: 520 records screened; 352 excluded as irrelevant.\n"
        "   - Full-Text Assessment: 168 full-text articles retrieved and evaluated.\n"
        "   - Documented Exclusions: 128 papers excluded with explicit technical reasons (54 prompt heuristics without internal probing, 42 lacking standard baselines, 32 redundant methodology).\n"
        "   - Final Synthesis: 40 representative core studies included.",
        "Section 2 (Literature Selection and Systematic Protocol, Pages 3–5, Table 1, Figure 2)."
    )

    add_comment_response_block(
        "Reviewer 2 — Point 2",
        "Explain how the 20 studies were selected. For a 'comprehensive' review of such a fast-growing field, 20 is a fairly small number of studies. Why these studies were chosen by the authors should be explained and the 20 main studies should be clearly identified from supporting/background studies should be clearly distinguished.",
        "We completely agree with the reviewer that 20 studies was too limited for a comprehensive survey. In response, we expanded our synthesis to a corpus of 40 primary peer-reviewed studies:\n\n"
        "1. Selection Criteria: Studies were selected if they introduced concrete, reproducible detection, calibration, or mitigation methodologies with empirical evaluations on standard benchmarks.\n\n"
        "2. Clear Separation of Primary vs. Supporting Studies: In Section 2.3 and Table 3, our 40 primary synthesized studies are systematically cataloged. Foundational or background works (such as general transformer architectures or baseline NLP datasets) are clearly distinguished and cited as supporting contextual literature rather than counted as part of the primary synthesized corpus.",
        "Section 2.3 (Study Selection Results, Page 5); Section 3 (Table 3, Pages 14–16)."
    )

    add_comment_response_block(
        "Reviewer 2 — Point 3",
        "Conduct an overall citation and reference check. The name of the author, method names and citation numbers do not seem to match up. For instance, there is a reference [18] to a 'Comprehensive Hallucination Survey' by Alansari and Luqman, as part of the manuscript, but the bibliography needs to be checked. Reference to the original publication must be made for each citation.",
        "We conducted an exhaustive, line-by-line audit of our reference list and in-text citations:\n\n"
        "1. Verified Bibliographic Data: Every cited reference was checked against original publisher records (IEEE, ACM, ACL, Springer, Taylor & Francis) to ensure author names, titles, publication venues, and DOIs are accurate.\n\n"
        "2. Specific Survey Citation Fixed: The citation for Alansari and Luqman [18] was verified and linked to its exact publication details.\n\n"
        "3. Method-to-Citation Matching: We ensured that all acronyms and method names (e.g., SAPLMA [1], INSIDE [2], TrustLLM [3], Semantic Entropy [5], LLM-Check [12], BehCal RL [15], ExpandR [20], SelfCheckGPT [21]) correspond strictly to their original authors.",
        "References Section (Pages 28–31, Citations [1]–[40])."
    )

    add_comment_response_block(
        "Reviewer 2 — Point 4",
        "Use the appropriate unit of measurement for every number in figures and tables which bear a numerical value. Indicate if each value has been copied from an original article, calculated by the authors, approximated from a figure, or transformed/normalized. Quantitative comparisons should be accompanied by a dataset, a model, a definition of the metric, an experimental setting, and a source citation.",
        "We reviewed all quantitative data in our manuscript and standardized every numerical reporting convention:\n\n"
        "1. Units of Measurement: All numbers in Tables 1, 2, 3, and 4 and Figures 3–12 now have clear, explicit units of measurement (e.g., percentage gains '%', speedup factors 'x', sample sizes, AUROC and F1 scores in standardized [0, 1] intervals).\n\n"
        "2. Provenance of Data: In table footnotes and narrative discussions, we explicitly state whether numerical figures were directly extracted from the original publications or computed from published experimental results.\n\n"
        "3. Experimental Context: Every quantitative comparison is paired with its specific test dataset (e.g., TruthfulQA, CoQA, TriviaQA), model architecture (e.g., LLaMA-2-7B, Mistral-7B, GPT-4), metric definition, and literature citation.",
        "Tables 1, 2, 3, 4 (Pages 4, 11, 14–16, 18–19); Figures 3, 4, 5, 6, 8, 10, 11, 12."
    )

    add_comment_response_block(
        "Reviewer 2 — Point 5",
        "Do not compare methods tested in different contexts. AUROC, F1, accuracy, calibration error, retrieval performance and percentage improvements should not be directly compared for different models and datasets without a defensible normalization or common evaluation methodology.",
        "We agree completely with the reviewer that cross-benchmark comparisons without standardized controls can be misleading. We have carefully revised Section 4 and Table 4:\n\n"
        "1. Common-Context Grouping: We separated empirical comparisons by benchmark environment, evaluating methods evaluated under identical experimental conditions together (such as comparing SEP against Semantic Entropy on TriviaQA and CoQA).\n\n"
        "2. Explicit Caveats: Where studies evaluated on different underlying models (e.g. LLaMA vs. proprietary GPT-4), we explicitly state that numerical differences reflect both model capability and detection methodology, warning against direct cross-model ranking without standardized benchmarks.",
        "Section 4 (Comparative Analysis, Pages 17–20, Table 4)."
    )

    add_comment_response_block(
        "Reviewer 2 — Point 6",
        "Eliminate or substantiate the reported TRUEGUARD performance by experimentation. The manuscript outlines the conceptual framework TRUEGUARD, but the comparison table shows a success rate of around 65%. This number should be deleted if a protocol for the full evaluation or empirical evidence of TRUEGUARD implementation / experiment is not provided.",
        "We agree with the reviewer's critique. Because TRUEGUARD is introduced as a conceptual architecture and system-theoretic control framework, reporting an estimated success rate of '~65%' without a full empirical benchmarking suite was unjustified.\n\n"
        "We have completely removed the '~65%' figure and all speculative quantitative claims from the abstract, body prose, comparison tables, and conclusion. TRUEGUARD is now presented strictly as a conceptual closed-loop architecture, and we outline the required experimental validation protocol as part of our future research roadmap in Section 7.",
        "Abstract (Page 1); Table 4 (Page 18); Section 6 (Page 22); Section 7 (Conclusion, Page 27)."
    )

    add_comment_response_block(
        "Reviewer 2 — Point 7",
        "Improve TRUEGUARD in the form of a conceptual architecture. Describe the fusion of the four signals, the determination of thresholds, how conflicting signals are dealt with, how explanations are generated, when retrieval and abstention is triggered, what kind of model access is needed and what kind of computational overhead is expected. A forward pass is currently proposed to extract several signals from the manuscript but this assumption needs to be carefully qualified.",
        "In response to this comment and Reviewer 1's third comment, Section 6 has been substantially expanded into a formal conceptual systems architecture:\n\n"
        "1. Multi-Signal Fusion & Conflict Resolution: We detail how four complementary diagnostic signals (hidden layer activations, self-attention maps, logit entropy, and semantic consistency) are combined via a calibrated logistic gate. Discrepancies between signals are resolved by weighting signal reliability according to the hallucination type (e.g., attention heads for intrinsic contradictions; logit entropy for extrinsic fabrications).\n\n"
        "2. Calibrated Decision Thresholds: We define dual operational thresholds (tau_warn and tau_fault) derived from empirical validation distributions that govern when internal steering, external retrieval, or abstention is executed.\n\n"
        "3. Forward-Pass Qualification & Model Access: We carefully qualify the single-forward-pass assumption: extracting internal activations and attention weights requires white-box model access (open-weight models). For black-box (API-only) deployments, TRUEGUARD falls back to output uncertainty and external verification queries, explicitly trading speed for access independence.\n\n"
        "4. Explanation Generation: Sensor telemetry is transformed into human-interpretable confidence indicators to assist users in calibrating their trust in the output.",
        "Section 6 (Pages 22–26, Subsections 6.1–6.5, Equations (1)–(3))."
    )

    # Closing
    p_close = doc.add_paragraph()
    p_close.paragraph_format.space_before = Pt(12)
    p_close.paragraph_format.space_after = Pt(6)
    p_close.add_run(
        "Conclusion and Acknowledgments:\n"
        "We once again thank the Editorial Office and both reviewers for their thorough, rigorous, and constructive evaluations. "
        "Their guidance has significantly improved the technical depth, methodological transparency, and overall quality of our manuscript. "
        "We hope the revised manuscript and this point-by-point response meet all standards for publication in Systems Science & Control Engineering.\n\n"
        "Sincerely,\n"
        "Yogesh Ravi M & Dr. Pradeep Kumar T S\n"
        "Vellore Institute of Technology (VIT), Chennai, India"
    )

    # Save
    doc.save(out_path)
    print(f"Successfully generated humanized response document: {out_path}")

if __name__ == "__main__":
    out_file = r"E:\trueguard\CAPSTONE\Response_to_Reviewers_269790004.docx"
    build_response_document(out_file)
