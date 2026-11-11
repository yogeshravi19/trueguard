import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
import os

def build_final_response(out_path):
    doc = Document()

    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    normal = doc.styles['Normal']
    normal.font.name = 'Times New Roman'
    normal.font.size = Pt(11)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(6)

    # Title Block
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

    def add_meta(lbl, val):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(lbl + ": ")
        r1.bold = True
        r1.font.size = Pt(10.5)
        r2 = p.add_run(val)
        r2.font.size = Pt(10.5)

    add_meta("Title", "Toward Trustworthy Large Language Models: A Comprehensive Review of Hallucination Detection, Explainability, and Mitigation")
    add_meta("Authors", "Yogesh Ravi M, Pradeep Kumar T S")
    add_meta("Affiliation", "School of Computer Science and Engineering, Vellore Institute of Technology (VIT), Chennai, India")
    add_meta("Date", "October 2026")

    doc.add_paragraph()

    # Cover Greeting
    p_cov = doc.add_paragraph()
    p_cov.paragraph_format.space_after = Pt(12)
    p_cov.add_run(
        "Dear Dr. Ajith Kumar BS, Academic Editor Dr. Zidong Wang, and Reviewers,\n\n"
        "Thank you for reviewing our manuscript and for providing these helpful comments. "
        "We have addressed all three technical check points from the editorial office and every comment from both reviewers. "
        "Below is our point-by-point response. For clear reading, every editorial and reviewer comment is highlighted in bright yellow, "
        "followed directly by our response and the exact location of the change in the revised manuscript.\n\n"
        "We have also submitted a marked copy showing all changes in yellow highlight "
        "('Toward Trustworthy Large Language Models_coloured.docx') and a clean copy ('Toward Trustworthy Large Language Models_standard.docx')."
    )

    def add_sec(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        r = p.add_run(title)
        r.bold = True
        r.font.size = Pt(13)

    def add_qa(title, comment, response, location):
        p_h = doc.add_paragraph()
        p_h.paragraph_format.space_before = Pt(12)
        p_h.paragraph_format.space_after = Pt(3)
        r_h = p_h.add_run(title)
        r_h.bold = True
        r_h.font.size = Pt(11)

        p_c = doc.add_paragraph()
        p_c.paragraph_format.space_before = Pt(0)
        p_c.paragraph_format.space_after = Pt(4)
        rc1 = p_c.add_run("Comment: ")
        rc1.bold = True
        rc1.font.size = Pt(10.5)
        rc1.font.highlight_color = WD_COLOR_INDEX.YELLOW
        rc2 = p_c.add_run(f'"{comment}"')
        rc2.italic = True
        rc2.font.size = Pt(10.5)
        rc2.font.highlight_color = WD_COLOR_INDEX.YELLOW

        p_r = doc.add_paragraph()
        p_r.paragraph_format.space_before = Pt(0)
        p_r.paragraph_format.space_after = Pt(4)
        rr1 = p_r.add_run("Response: ")
        rr1.bold = True
        rr1.font.size = Pt(10.5)
        rr2 = p_r.add_run(response)
        rr2.font.size = Pt(10.5)

        p_l = doc.add_paragraph()
        p_l.paragraph_format.space_before = Pt(0)
        p_l.paragraph_format.space_after = Pt(10)
        rl1 = p_l.add_run("Location in Manuscript: ")
        rl1.bold = True
        rl1.font.size = Pt(10)
        rl2 = p_l.add_run(location)
        rl2.font.size = Pt(10)

    # PART A
    add_sec("PART A: EDITORIAL TECHNICAL CHECKS")

    add_qa(
        "Technical Check Point 1: Response Document",
        "Please include a complete point-by-point response to the reviewer’s comments included in your decision letter. This can be in the form of track changes or a separate document.",
        "We have written this standalone point-by-point document responding to all comments from the decision letter and the editorial check. We are also submitting a marked manuscript with all revised text highlighted in yellow (Toward Trustworthy Large Language Models_coloured.docx) and a clean manuscript (Toward Trustworthy Large Language Models_standard.docx).",
        "Submitted files: Response_to_Reviewers_269790004.docx, Toward Trustworthy Large Language Models_coloured.docx, and Toward Trustworthy Large Language Models_standard.docx."
    )

    add_qa(
        "Technical Check Point 2: Abstract Mismatch",
        "We note that the information on “Abstract” does not match the information you entered for your manuscript in the Submission Portal. Please update this to reflect the manuscript.",
        "We updated the portal abstract to match our manuscript abstract word-for-word. The revised abstract contains exactly 214 words, confirms our 40 PRISMA-screened studies, outlines the six-pillar taxonomy and TRUEGUARD framework, and removes the outdated ~65% claim.",
        "Manuscript Abstract (Page 1, Paragraph 11) and Submission Portal Abstract field."
    )

    add_qa(
        "Technical Check Point 3: In-Text Figure and Table References",
        "While conducting checks on your manuscript we noted that some of the figures and tables have not been referenced in the text. All figures/tables included in the manuscript should be referenced in the body of the text.",
        "We went through the entire paper and added clear in-text citations for all 12 figures and all 4 tables in the body text. Each figure and table is introduced in the prose before it appears, and every image is positioned directly above its caption.",
        "Referenced throughout the manuscript: Figures 1–12 and Tables 1–4."
    )

    # PART B
    add_sec("PART B: REVIEWER 1 COMMENTS")

    add_qa(
        "Reviewer 1 — Comment 1: Systematic Search Strategy and Baseline Works",
        "The review is described as comprehensive/systematic, but the search strategy and study selection process are not sufficiently explained. The authors should specify the databases, search terms, time period, inclusion/exclusion criteria, and screening procedure. Important works such as SelfCheckGPT, TruthfulQA, FActScore, Chain-of-Verification, RAG, and Self-RAG should also be discussed to support the claimed coverage.",
        "We added our complete PRISMA 2020 search protocol in Section 2, covering five databases (Scopus, Web of Science, IEEE Xplore, ACM Digital Library, and Google Scholar/arXiv) from January 2020 to December 2024. Table 1 lists our exact boolean search queries, eligibility filters, and screening steps. We also added in-depth discussions of the requested baseline works: SelfCheckGPT in Pillar 2; TruthfulQA and FActScore in Pillar 4 (Table 2); and Chain-of-Verification, standard RAG, and Self-RAG in Pillar 5.",
        "Section 2 (Pages 3–5, Table 1, Figure 2); Section 3 (Pages 7–16, References [21]–[26])."
    )

    add_qa(
        "Reviewer 1 — Comment 2: Critical Evaluation and Taxonomy Justification",
        "The manuscript is often descriptive rather than critical. The authors should discuss the assumptions, limitations, generalizability, computational requirements, and model-access requirements of the reviewed approaches. In addition, the six-pillar taxonomy contains overlaps, particularly among internal-state analysis, uncertainty estimation, and attention-based methods. The taxonomy should be better justified or refined.",
        "We revised Sections 3 and 4 to critically evaluate each method’s practical assumptions, limitations, computational overhead, and model-access needs (summarized in Table 4). We also clarified why Pillars 1, 2, and 3 are distinct: Pillar 1 analyzes hidden layer activations (internal latent truthfulness), Pillar 2 calculates entropy over output token distributions (lexical certainty), and Pillar 3 tracks attention weights (whether the model is attending to context). Each pillar catches a different type of error.",
        "Section 3 (Pages 6–13); Section 4 (Pages 17–20, Table 4)."
    )

    add_qa(
        "Reviewer 1 — Comment 3: Grounding TRUEGUARD in Control Theory",
        "TRUEGUARD is an interesting idea, but its current presentation is largely conceptual. More detail is needed on signal fusion, mitigation thresholds, decision mechanisms, evaluation, and system architecture. Given the journal scope, the framework should also be connected more explicitly to control concepts such as sensing, feedback, actuation, robustness, fault detection, and adaptive control.",
        "In Section 6, we grounded TRUEGUARD directly in closed-loop control and fault detection principles: the LLM is treated as the plant; internal probing, logit entropy, and attention monitoring act as real-time diagnostic sensors; a fusion module compares the error signal against calibrated decision thresholds; and tiered actuation applies proportional corrective feedback (activation steering, targeted retrieval, or abstention with explanations). We also analyze closed-loop stability.",
        "Section 6 (Pages 22–26, Subsections 6.1–6.5)."
    )

    add_qa(
        "Reviewer 1 — Comment 4: Black-Box Models and Multi-Metric Evaluations",
        "The discussion of hallucination detection for API-based or black-box LLMs should be strengthened. The authors should also consider evaluation criteria beyond detection accuracy, including false-positive/false-negative trade-offs, calibration, latency, computational overhead, mitigation effectiveness, and robustness across models.",
        "We expanded our analysis of black-box/API methods (SelfCheckGPT, black-box LLM-Check, SEP) in Section 4 and Table 4, focusing on latency and query costs. Beyond raw accuracy, we evaluate Expected Calibration Error (ECE), F1 balance, and speedup factor. Figures 10, 11, and 12 illustrate these trade-offs, showing that LLM-Check’s black-box version achieves up to a 450x speedup with minimal loss in AUROC compared to full white-box probing.",
        "Section 4 (Pages 17–20, Table 4, Figures 10, 11, 12)."
    )

    # PART C
    add_sec("PART C: REVIEWER 2 POINTS")

    add_qa(
        "Reviewer 2 — Point 1: PRISMA Flow Diagram and Search Protocol",
        "A description of the databases/search engines used, complete search strings, search period, inclusion and exclusion criteria, screening procedure, number of initially retrieved studies, duplicate removal, full text assessment, and the final selection procedure should be provided by the authors. Transparency can be greatly enhanced by a flow diagram similar to the one used in the PRISMA project.",
        "We added a full PRISMA 2020 protocol in Section 2 and included Figure 2 (PRISMA flow diagram). It shows our exact numbers: 688 candidate records found across five databases, 168 duplicates removed, 352 excluded during title/abstract screening, and 128 excluded with documented reasons during full-text review (54 prompt heuristics, 42 lacking standard baselines, 32 redundant methodology), leaving 40 core studies. Table 1 details our search strings and selection criteria.",
        "Section 2 (Pages 3–5, Table 1, Figure 2)."
    )

    add_qa(
        "Reviewer 2 — Point 2: Corpus Size (20 vs. 40 Studies)",
        "Explain how the 20 studies were selected. For a “comprehensive” review of such a fast-growing field, 20 is a fairly small number of studies. Why these studies were chosen by the authors should be explained and the 20 main studies should be clearly identified from supporting/background studies should be clearly distinguished.",
        "We expanded our synthesized corpus from 20 to 40 core peer-reviewed studies. In Section 2.3 and Table 3, all 40 primary studies are systematically cataloged with their methodology, model access, and benchmark outcomes. Foundational papers and general background citations are cited separately as context.",
        "Section 2.3 (Page 5); Section 3 (Table 3, Pages 14–16)."
    )

    add_qa(
        "Reviewer 2 — Point 3: Citation Audit and Author Verification",
        "Conduct an overall citation and reference check. The name of the author, method names and citation numbers do not seem to match up. For instance, there is a reference [18] to a “Comprehensive Hallucination Survey” by Alansari and Luqman, as part of the manuscript, but the bibliography needs to be checked. Reference to the original publication must be made for each citation.",
        "We conducted a complete audit of our bibliography. We verified all author names, article titles, DOIs, and venues against original publisher records. The Alansari and Luqman survey citation [18] was corrected to its original published source, and all method names throughout the text correctly match their primary citations.",
        "References Section (Pages 28–31, Citations [1]–[40])."
    )

    add_qa(
        "Reviewer 2 — Point 4: Units of Measurement and Provenance of Numbers",
        "Use the appropriate unit of measurement for every number in figures and tables which bear a numerical value. Indicate if each value has been copied from an original article, calculated by the authors, approximated from a figure, or transformed/normalized. Quantitative comparisons should be accompanied by a dataset, a model, a definition of the metric, an experimental setting, and a source citation.",
        "We standardized units across all tables and figures (e.g., speedup factors in 'x', percentage gains in '%', error metrics in normalized [0, 1] scales). In table notes, we specify whether numbers were directly extracted from original papers or computed from reported data, and we specify the test dataset (TruthfulQA, CoQA, etc.), the model used, and the metric definition.",
        "Tables 1, 2, 3, 4 (Pages 4, 11, 14–16, 18–19); Figures 3, 4, 5, 6, 8, 10, 11, 12."
    )

    add_qa(
        "Reviewer 2 — Point 5: Fair Comparisons Across Experimental Contexts",
        "Do not compare methods tested in different contexts. AUROC, F1, accuracy, calibration error, retrieval performance and percentage improvements should not be directly compared for different models and datasets without a defensible normalization or common evaluation methodology.",
        "In Section 4 and Table 4, we grouped comparisons strictly by common benchmark setups (such as methods evaluated on the same dataset and baseline model). We added explicit notes warning against directly comparing numbers across different models or prompt setups.",
        "Section 4 (Pages 17–20, Table 4)."
    )

    add_qa(
        "Reviewer 2 — Point 6: Deletion of the Unsubstantiated ~65% Claim",
        "Eliminate or substantiate the reported TRUEGUARD performance by experimentation. The manuscript outlines the conceptual framework TRUEGUARD, but the comparison table shows a success rate of around 65%. This number should be deleted if a protocol for the full evaluation or empirical evidence of TRUEGUARD implementation / experiment is not provided.",
        "We completely removed the '~65%' figure and any speculative performance claims from the abstract, main text, tables, and conclusion. TRUEGUARD is now presented strictly as a conceptual control architecture, and experimental validation is framed as future work in Section 7.",
        "Abstract (Page 1); Table 4 (Page 18); Section 6 (Page 22); Section 7 (Page 27)."
    )

    add_qa(
        "Reviewer 2 — Point 7: Detailed TRUEGUARD Conceptual Architecture",
        "Improve TRUEGUARD in the form of a conceptual architecture. Describe the fusion of the four signals, the determination of thresholds, how conflicting signals are dealt with, how explanations are generated, when retrieval and abstention is triggered, what kind of model access is needed and what kind of computational overhead is expected. A forward pass is currently proposed to extract several signals from the manuscript but this assumption needs to be carefully qualified.",
        "In Section 6, we expanded TRUEGUARD’s architecture: we explain the logistic fusion gate, how conflicting signals are resolved (weighting attention for intrinsic contradictions vs. logit entropy for extrinsic fabrications), the dual operational thresholds (tau_warn and tau_fault), and tiered mitigation. We also clearly state that single-pass extraction requires white-box model access, whereas black-box deployments use output uncertainty and verification queries.",
        "Section 6 (Pages 22–26, Subsections 6.1–6.5)."
    )

    # Closing
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
    print("SUCCESS: saved to", out_path)

if __name__ == "__main__":
    p = r"E:\trueguard\CAPSTONE\Response_to_Reviewers_269790004.docx"
    build_final_response(p)
