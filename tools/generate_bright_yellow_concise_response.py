import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
import os

def build_bright_yellow_response_doc(out_path):
    doc = Document()

    # 1-inch margins
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # Base Normal Style
    normal = doc.styles['Normal']
    normal.font.name = 'Times New Roman'
    normal.font.size = Pt(11)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(6)

    # Document Header
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    r_t = p_title.add_run("Response to Reviewers and Editorial Technical Checks")
    r_t.bold = True
    r_t.font.size = Pt(15)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(12)
    r_s = p_sub.add_run("Manuscript: Ms. No. 269790004 | Systems Science & Control Engineering (Taylor & Francis)")
    r_s.italic = True
    r_s.font.size = Pt(10.5)

    # Metadata lines
    def add_meta(label, val):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(label + ": ")
        r1.bold = True
        r1.font.size = Pt(10.5)
        r2 = p.add_run(val)
        r2.font.size = Pt(10.5)

    add_meta("Title", "Toward Trustworthy Large Language Models: A Comprehensive Review of Hallucination Detection, Explainability, and Mitigation")
    add_meta("Authors", "Yogesh Ravi M, Pradeep Kumar T S")
    add_meta("Affiliation", "School of Computer Science and Engineering, Vellore Institute of Technology (VIT), Chennai, India")
    add_meta("Date", "October 2026")

    doc.add_paragraph() # blank line

    # Cover Letter Opening
    p_cov = doc.add_paragraph()
    p_cov.paragraph_format.space_after = Pt(12)
    p_cov.add_run(
        "Dear Dr. Ajith Kumar BS, Academic Editor Dr. Zidong Wang, and Reviewers,\n\n"
        "Thank you for reviewing our manuscript and for the constructive feedback. We have addressed all points raised in the technical check and the decision letter. "
        "Below is our point-by-point response. For clear visual tracking, every reviewer and editorial comment is highlighted in bright yellow, "
        "followed directly by our response and the exact location of changes in the revised manuscript.\n\n"
        "All updates in the manuscript are also highlighted in yellow in the submitted marked copy ('Toward Trustworthy Large Language Models_coloured.docx'), "
        "and a clean copy ('Toward Trustworthy Large Language Models_standard.docx') is provided for publication."
    )

    def add_section_heading(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(13)
        return p

    def add_item(item_num_title, exact_question, response_text, location_text):
        # 1. Item Title
        p_hdr = doc.add_paragraph()
        p_hdr.paragraph_format.space_before = Pt(12)
        p_hdr.paragraph_format.space_after = Pt(3)
        r_h = p_hdr.add_run(item_num_title)
        r_h.bold = True
        r_h.font.size = Pt(11)

        # 2. Bright Yellow Highlighted Question
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(0)
        p_q.paragraph_format.space_after = Pt(4)
        
        r_q_lbl = p_q.add_run("Comment: ")
        r_q_lbl.bold = True
        r_q_lbl.font.size = Pt(10.5)
        r_q_lbl.font.highlight_color = WD_COLOR_INDEX.YELLOW

        r_q_txt = p_q.add_run(f'"{exact_question}"')
        r_q_txt.italic = True
        r_q_txt.font.size = Pt(10.5)
        r_q_txt.font.highlight_color = WD_COLOR_INDEX.YELLOW

        # 3. Direct Humanized Response
        p_resp = doc.add_paragraph()
        p_resp.paragraph_format.space_before = Pt(0)
        p_resp.paragraph_format.space_after = Pt(4)
        
        r_resp_lbl = p_resp.add_run("Response: ")
        r_resp_lbl.bold = True
        r_resp_lbl.font.size = Pt(10.5)

        r_resp_txt = p_resp.add_run(response_text)
        r_resp_txt.font.size = Pt(10.5)

        # 4. Location of Changes
        p_loc = doc.add_paragraph()
        p_loc.paragraph_format.space_before = Pt(0)
        p_loc.paragraph_format.space_after = Pt(10)
        
        r_loc_lbl = p_loc.add_run("Location in Manuscript: ")
        r_loc_lbl.bold = True
        r_loc_lbl.font.size = Pt(10)
        
        r_loc_txt = p_loc.add_run(location_text)
        r_loc_txt.font.size = Pt(10)

    # -------------------------------------------------------------
    # PART A: EDITORIAL TECHNICAL CHECKS
    # -------------------------------------------------------------
    add_section_heading("PART A: EDITORIAL TECHNICAL CHECKS")

    add_item(
        "Technical Check Point 1 (Response Document & Rebuttal)",
        "Please include a complete point-by-point response to the reviewer's comments included in your decision letter. This can be in the form of track changes or a separate document.",
        "We have provided this separate point-by-point response addressing every comment from the decision letter and technical check. Along with this file, we have submitted both a marked manuscript with changes highlighted in yellow ('Toward Trustworthy Large Language Models_coloured.docx') and a clean manuscript ('Toward Trustworthy Large Language Models_standard.docx').",
        "Submitted files: Response_to_Reviewers_269790004.docx, Toward Trustworthy Large Language Models_coloured.docx, and Toward Trustworthy Large Language Models_standard.docx."
    )

    add_item(
        "Technical Check Point 2 (Abstract Metadata Mismatch)",
        "We note that the information on 'Abstract' does not match the information you entered for your manuscript in the Submission Portal. Please update this to reflect the manuscript.",
        "We updated the portal metadata to match our revised manuscript abstract word-for-word. The revised abstract has 214 words, confirms the 40 PRISMA-screened studies, outlines our six-pillar review and TRUEGUARD framework, and completely removes the outdated '~65%' claim.",
        "Manuscript Abstract (Page 1, Paragraph 11) and Submission Portal Abstract field."
    )

    add_item(
        "Technical Check Point 3 (Figures & Tables In-Text References)",
        "While conducting checks on your manuscript we noted that some of the figures and tables have not been referenced in the text. All figures/tables included in the manuscript should be referenced in the body of the text.",
        "We added explicit in-text references for all 12 figures and all 4 tables in the body prose. Every figure and table is now introduced before it appears, and each image is placed directly above its caption without large gaps.",
        "Referenced throughout body text: Figures 1–12 and Tables 1–4."
    )

    # -------------------------------------------------------------
    # PART B: REVIEWER 1
    # -------------------------------------------------------------
    add_section_heading("PART B: REVIEWER 1 COMMENTS")

    add_item(
        "Reviewer 1 — Comment 1 (Search Strategy & Key Baselines)",
        "The review is described as comprehensive/systematic, but the search strategy and study selection process are not sufficiently explained. The authors should specify the databases, search terms, time period, inclusion/exclusion criteria, and screening procedure. Important works such as SelfCheckGPT, TruthfulQA, FActScore, Chain-of-Verification, RAG, and Self-RAG should also be discussed to support the claimed coverage.",
        "We added our full PRISMA 2020 search protocol in Section 2, covering five databases (Scopus, Web of Science, IEEE Xplore, ACM, Google Scholar/arXiv) from 2020 to 2024. Table 1 lists our exact search queries and criteria. We also added and analyzed the requested key works: SelfCheckGPT (Pillar 2), TruthfulQA and FActScore (Pillar 4, Table 2), Chain-of-Verification, RAG, and Self-RAG (Pillar 5).",
        "Section 2 (Pages 3–5, Table 1, Figure 2); Section 3 (Pages 7–16, References [21]–[26])."
    )

    add_item(
        "Reviewer 1 — Comment 2 (Critical Evaluation & Taxonomy Overlap)",
        "The manuscript is often descriptive rather than critical. The authors should discuss the assumptions, limitations, generalizability, computational requirements, and model-access requirements of the reviewed approaches. In addition, the six-pillar taxonomy contains overlaps, particularly among internal-state analysis, uncertainty estimation, and attention-based methods. The taxonomy should be better justified or refined.",
        "We revised Sections 3 and 4 to critically evaluate each method's assumptions, limitations, runtime costs, and model access (summarized in Table 4). We also clarified the boundaries between Pillars 1, 2, and 3: Pillar 1 looks at hidden layer activations (internal representation), Pillar 2 calculates probability entropy over output tokens (predictive confidence), and Pillar 3 checks attention weights to see if context was ignored.",
        "Section 3 (Pages 6–13); Section 4 (Pages 17–20, Table 4)."
    )

    add_item(
        "Reviewer 1 — Comment 3 (TRUEGUARD Control Theory Grounding)",
        "TRUEGUARD is an interesting idea, but its current presentation is largely conceptual. More detail is needed on signal fusion, mitigation thresholds, decision mechanisms, evaluation, and system architecture. Given the journal scope, the framework should also be connected more explicitly to control concepts such as sensing, feedback, actuation, robustness, fault detection, and adaptive control.",
        "In Section 6, we grounded TRUEGUARD directly in closed-loop control and fault detection principles: the LLM is the plant; internal probing, logit entropy, and attention tracking act as real-time sensors; a fusion module compares the error signal against calibrated thresholds; and tiered actuation applies corrective feedback (activation steering, targeted retrieval, or abstention with explanations).",
        "Section 6 (Pages 22–26, Subsections 6.1–6.5)."
    )

    add_item(
        "Reviewer 1 — Comment 4 (Black-box LLMs & Multi-Metric Evaluation)",
        "The discussion of hallucination detection for API-based or black-box LLMs should be strengthened. The authors should also consider evaluation criteria beyond detection accuracy, including false-positive/false-negative trade-offs, calibration, latency, computational overhead, mitigation effectiveness, and robustness across models.",
        "We expanded our evaluation of black-box/API methods (SelfCheckGPT, black-box LLM-Check, SEP) in Section 4 and Table 4. Beyond raw accuracy, we now evaluate calibration error (ECE), F1 balance, and speedup factor. Figures 10, 11, and 12 plot these trade-offs, highlighting that black-box LLM-Check achieves up to a 450x speedup with minimal accuracy loss.",
        "Section 4 (Pages 17–20, Table 4, Figures 10, 11, 12)."
    )

    # -------------------------------------------------------------
    # PART C: REVIEWER 2
    # -------------------------------------------------------------
    add_section_heading("PART C: REVIEWER 2 POINTS")

    add_item(
        "Reviewer 2 — Point 1 (PRISMA Flow Diagram & Search Strings)",
        "A description of the databases/search engines used, complete search strings, search period, inclusion and exclusion criteria, screening procedure, number of initially retrieved studies, duplicate removal, full text assessment, and the final selection procedure should be provided by the authors. Transparency can be greatly enhanced by a flow diagram similar to the one used in the PRISMA project.",
        "We added a PRISMA 2020 flow diagram (Figure 2) detailing our selection numbers: 688 records identified across 5 databases, 168 duplicates removed, 352 excluded at title/abstract screening, and 128 excluded with specific reasons during full-text review, leaving 40 core studies. Table 1 lists all search strings, dates, and screening criteria.",
        "Section 2 (Pages 3–5, Table 1, Figure 2)."
    )

    add_item(
        "Reviewer 2 — Point 2 (Corpus Size: 20 vs 40 Studies)",
        "Explain how the 20 studies were selected. For a 'comprehensive' review of such a fast-growing field, 20 is a fairly small number of studies. Why these studies were chosen by the authors should be explained and the 20 main studies should be clearly identified from supporting/background studies should be clearly distinguished.",
        "We expanded our synthesized corpus from 20 to 40 core peer-reviewed studies. In Section 2.3 and Table 3, we catalog all 40 primary studies with their methods, benchmarks, and results, clearly separating them from general background references.",
        "Section 2.3 (Page 5); Section 3 (Table 3, Pages 14–16)."
    )

    add_item(
        "Reviewer 2 — Point 3 (Citation Check & Author Names)",
        "Conduct an overall citation and reference check. The name of the author, method names and citation numbers do not seem to match up. For instance, there is a reference [18] to a 'Comprehensive Hallucination Survey' by Alansari and Luqman, as part of the manuscript, but the bibliography needs to be checked. Reference to the original publication must be made for each citation.",
        "We verified every citation in the bibliography against its original published version. We corrected author names, publication venues, DOIs, and method-to-citation links. The Alansari and Luqman survey citation [18] was checked and updated to its correct published source.",
        "References Section (Pages 28–31, Citations [1]–[40])."
    )

    add_item(
        "Reviewer 2 — Point 4 (Units of Measurement & Numerical Provenance)",
        "Use the appropriate unit of measurement for every number in figures and tables which bear a numerical value. Indicate if each value has been copied from an original article, calculated by the authors, approximated from a figure, or transformed/normalized. Quantitative comparisons should be accompanied by a dataset, a model, a definition of the metric, an experimental setting, and a source citation.",
        "We standardized units across all tables and figures (e.g., speedup in 'x', percentages in '%', error scales in [0, 1]). In table notes and text, we specify the source of each number, the evaluation dataset (TruthfulQA, CoQA, etc.), the tested model, and the metric definition.",
        "Tables 1, 2, 3, 4 (Pages 4, 11, 14–16, 18–19); Figures 3, 4, 5, 6, 8, 10, 11, 12."
    )

    add_item(
        "Reviewer 2 — Point 5 (Fair Comparisons Across Contexts)",
        "Do not compare methods tested in different contexts. AUROC, F1, accuracy, calibration error, retrieval performance and percentage improvements should not be directly compared for different models and datasets without a defensible normalization or common evaluation methodology.",
        "In Section 4 and Table 4, we grouped performance figures strictly by common benchmark settings (such as comparing methods tested on the same dataset and baseline model). We added explicit notes warning against directly ranking numbers from different test setups.",
        "Section 4 (Pages 17–20, Table 4)."
    )

    add_item(
        "Reviewer 2 — Point 6 (Eliminate ~65% Claim)",
        "Eliminate or substantiate the reported TRUEGUARD performance by experimentation. The manuscript outlines the conceptual framework TRUEGUARD, but the comparison table shows a success rate of around 65%. This number should be deleted if a protocol for the full evaluation or empirical evidence of TRUEGUARD implementation / experiment is not provided.",
        "We completely removed the '~65%' number and any speculative claims from the abstract, body text, tables, and conclusion. TRUEGUARD is now presented strictly as a conceptual control architecture.",
        "Abstract (Page 1); Table 4 (Page 18); Section 6 (Page 22); Section 7 (Page 27)."
    )

    add_item(
        "Reviewer 2 — Point 7 (TRUEGUARD Conceptual Architecture Details)",
        "Improve TRUEGUARD in the form of a conceptual architecture. Describe the fusion of the four signals, the determination of thresholds, how conflicting signals are dealt with, how explanations are generated, when retrieval and abstention is triggered, what kind of model access is needed and what kind of computational overhead is expected. A forward pass is currently proposed to extract several signals from the manuscript but this assumption needs to be carefully qualified.",
        "In Section 6, we expanded TRUEGUARD's system architecture: we describe the logistic fusion gate, how conflicting signals are handled (e.g. weighting attention for internal self-contradictions vs. logit entropy for extrinsic fabrications), the dual decision thresholds, and tiered corrections. We also clarify that single-pass internal extraction requires white-box access, while black-box setups rely on output uncertainty.",
        "Section 6 (Pages 22–26, Subsections 6.1–6.5)."
    )

    # Formal Closing
    p_close = doc.add_paragraph()
    p_close.paragraph_format.space_before = Pt(16)
    p_close.paragraph_format.space_after = Pt(6)
    p_close.add_run(
        "Conclusion:\n"
        "We thank the editor and reviewers for their constructive comments. These revisions have strengthened the clarity, methodology, and theoretical grounding of our paper.\n\n"
        "Sincerely,\n"
        "Yogesh Ravi M & Dr. Pradeep Kumar T S\n"
        "Vellore Institute of Technology (VIT), Chennai, India"
    )

    doc.save(out_path)
    print(f"Successfully generated bright-yellow concise response document: {out_path}")

if __name__ == "__main__":
    out_file = r"E:\trueguard\CAPSTONE\Response_to_Reviewers_269790004.docx"
    build_bright_yellow_response_doc(out_file)
