import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
import os

def build_ultra_humanized_response(out_path):
    doc = Document()

    # 1-inch margins
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

    def add_meta(lbl, val):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        r1 = p.add_run(lbl + ": ")
        r1.bold = True
        r1.font.size = Pt(10.5)
        r2 = p.add_run(val)
        r2.font.size = Pt(10.5)

    add_meta("Title", "Toward Trustworthy Large Language Models: A Comprehensive Review of Hallucination Detection, Explainability, and Mitigation Strategies")
    add_meta("Authors", "Yogesh Ravi M, Pradeep Kumar T S")
    add_meta("Affiliation", "School of Computer Science and Engineering, Vellore Institute of Technology (VIT), Chennai, India")
    add_meta("Date", "October 2026")

    doc.add_paragraph()

    # Cover Letter
    p_cov = doc.add_paragraph()
    p_cov.paragraph_format.space_after = Pt(12)
    p_cov.add_run(
        "Dear Professor Zidong Wang (Editor-in-Chief), Dr. Ajith Kumar BS (Editorial Office), and Reviewers,\n\n"
        "Thank you for reviewing our manuscript and for providing these helpful comments. "
        "We have addressed all three technical check points from the editorial office and every comment from both reviewers. "
        "Below is our point-by-point response. For clear visual tracking, every editorial and reviewer comment is highlighted in bright yellow, "
        "followed directly by our response and the exact location of the change in the revised manuscript.\n\n"
        "We have also submitted a marked copy showing all changes in yellow highlight ('Toward Trustworthy Large Language Models_coloured.docx') "
        "alongside the clean version ('Toward Trustworthy Large Language Models_standard.docx')."
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
        "Please include a complete point-by-point response to the reviewer's comments included in your decision letter. This can be in the form of track changes or a separate document.",
        "We put together this separate response file covering every single editorial check and reviewer point. Along with this letter, we uploaded both the marked paper with yellow highlights and the clean final manuscript.",
        "Submitted files: Response_to_Reviewers_269790004.docx, Toward Trustworthy Large Language Models_coloured.docx, and Toward Trustworthy Large Language Models_standard.docx."
    )

    add_qa(
        "Technical Check Point 2: Abstract Mismatch",
        "We note that the information on “Abstract” does not match the information you entered for your manuscript in the Submission Portal. Please update this to reflect the manuscript.",
        "Our portal profile still had an old draft that mentioned an estimated '65%' figure. We updated the portal abstract to match the paper word-for-word. The new abstract is 214 words, mentions the 40 PRISMA papers, outlines TRUEGUARD, and drops the 65% claim.",
        "Manuscript Abstract (Page 1, Paragraph 11) and Submission Portal Abstract field."
    )

    add_qa(
        "Technical Check Point 3: In-Text Figure and Table References",
        "While conducting checks on your manuscript we noted that some of the figures and tables have not been referenced in the text. All figures/tables included in the manuscript should be referenced in the body of the text.",
        "We went through the whole paper and added direct in-text mentions for all 12 figures and all 4 tables right in the prose before they appear. We also fixed the layout so every figure image sits directly above its caption without large blank gaps.",
        "Referenced throughout body text: Figures 1–12 and Tables 1–4."
    )

    # PART B
    add_sec("PART B: REVIEWER 1 COMMENTS")

    add_qa(
        "Reviewer 1 — Comment 1: Search Strategy and Key Baselines",
        "The review is described as comprehensive/systematic, but the search strategy and study selection process are not sufficiently explained. The authors should specify the databases, search terms, time period, inclusion/exclusion criteria, and screening procedure. Important works such as SelfCheckGPT, TruthfulQA, FActScore, Chain-of-Verification, RAG, and Self-RAG should also be discussed to support the claimed coverage.",
        "We wrote out our full PRISMA 2020 search steps in Section 2. We searched Scopus, Web of Science, IEEE Xplore, ACM, and Google Scholar/arXiv from 2020 to 2024, and listed our exact search queries and screening rules in Table 1. As suggested, we also added dedicated discussions and comparisons for SelfCheckGPT (Pillar 2), TruthfulQA and FActScore (Pillar 4), and Chain-of-Verification, standard RAG, and Self-RAG (Pillar 5).",
        "Section 2 (Pages 3–5, Table 1, Figure 2) and Section 3 (Pages 7–16, References [21]–[26])."
    )

    add_qa(
        "Reviewer 1 — Comment 2: Critical Evaluation and Taxonomy Justification",
        "The manuscript is often descriptive rather than critical. The authors should discuss the assumptions, limitations, generalizability, computational requirements, and model-access requirements of the reviewed approaches. In addition, the six-pillar taxonomy contains overlaps, particularly among internal-state analysis, uncertainty estimation, and attention-based methods. The taxonomy should be better justified or refined.",
        "We reworked Sections 3 and 4 to be more critical instead of just summarizing papers. We added Table 4 to compare runtime costs, limitations, and whether each method needs full model weights (white-box) or just API access (black-box). We also clarified the difference between Pillars 1, 2, and 3: Pillar 1 probes hidden layer activations inside the model, Pillar 2 measures entropy over output token probabilities, and Pillar 3 checks attention weights to see if context was ignored. Each pillar catches a distinct type of error.",
        "Section 3 (Pages 6–13) and Section 4 (Pages 17–20, Table 4)."
    )

    add_qa(
        "Reviewer 1 — Comment 3: Grounding TRUEGUARD in Control Theory",
        "TRUEGUARD is an interesting idea, but its current presentation is largely conceptual. More detail is needed on signal fusion, mitigation thresholds, decision mechanisms, evaluation, and system architecture. Given the journal scope, the framework should also be connected more explicitly to control concepts such as sensing, feedback, actuation, robustness, fault detection, and adaptive control.",
        "To fit the scope of Systems Science & Control Engineering, we rebuilt Section 6 around feedback control and fault detection principles. We treat the LLM as the plant; internal probing, logit entropy, and attention monitoring serve as sensors; a fusion module compares the error signal against set thresholds; and tiered actuation applies corrective feedback (activation steering, targeted retrieval, or abstaining with an explanation). We also discuss stability in multi-step reasoning.",
        "Section 6 (Pages 22–26, Subsections 6.1–6.5)."
    )

    add_qa(
        "Reviewer 1 — Comment 4: Black-Box Models and Multi-Metric Evaluations",
        "The discussion of hallucination detection for API-based or black-box LLMs should be strengthened. The authors should also consider evaluation criteria beyond detection accuracy, including false-positive/false-negative trade-offs, calibration, latency, computational overhead, mitigation effectiveness, and robustness across models.",
        "We expanded our coverage of black-box methods (SelfCheckGPT, black-box LLM-Check, SEP) in Section 4 and Table 4, looking specifically at latency and API query costs. Instead of just looking at accuracy, we also look at calibration error (ECE), F1 balance, and speedup. In Figures 10, 11, and 12, we plot these trade-offs, showing that black-box LLM-Check runs up to 450 times faster with only a slight drop in AUROC compared to white-box methods.",
        "Section 4 (Pages 17–20, Table 4, Figures 10, 11, 12)."
    )

    # PART C
    add_sec("PART C: REVIEWER 2 POINTS")

    add_qa(
        "Reviewer 2 — Point 1: PRISMA Flow Diagram and Search Protocol",
        "A description of the databases/search engines used, complete search strings, search period, inclusion and exclusion criteria, screening procedure, number of initially retrieved studies, duplicate removal, full text assessment, and the final selection procedure should be provided by the authors. Transparency can be greatly enhanced by a flow diagram similar to the one used in the PRISMA project.",
        "We added a PRISMA 2020 flow diagram in Figure 2 showing our exact screening numbers: 688 records found, 168 duplicates removed, 352 dropped at title/abstract screening, and 128 excluded during full-text reading (54 prompt heuristics, 42 lacking standard baselines, 32 redundant), leaving 40 core studies. Table 1 lists all search strings and criteria.",
        "Section 2 (Pages 3–5, Table 1, Figure 2)."
    )

    add_qa(
        "Reviewer 2 — Point 2: Corpus Organization (20 Core vs. 40 Total Studies)",
        "Explain how the 20 studies were selected. For a “comprehensive” review of such a fast-growing field, 20 is a fairly small number of studies. Why these studies were chosen by the authors should be explained and the 20 main studies should be clearly identified from supporting/background studies should be clearly distinguished.",
        "We apologize for the confusion in our previous draft. Our full corpus actually includes 40 peer-reviewed studies. In the earlier draft, we had emphasized 20 detection papers in the text, which made it look like only 20 studies were reviewed in total. To make this completely transparent, we added Section 2.6 and Table 3, which organize the 40 studies into two clear groups: (1) 20 Core Architectural Studies focusing on internal probing, token entropy, and attention monitoring, and (2) 20 Foundational Benchmarks and Mitigation Frameworks (such as TruthfulQA, FActScore, RAG, Self-RAG, and SelfCheckGPT). In Section 2.3 and Table 1, we detail our PRISMA eligibility criteria and explain exactly why each study was chosen.",
        "Section 2.3 (Page 5), Section 2.6 (Page 6), and Table 3 (Pages 14–16)."
    )

    add_qa(
        "Reviewer 2 — Point 3: Citation Audit and Author Verification",
        "Conduct an overall citation and reference check. The name of the author, method names and citation numbers do not seem to match up. For instance, there is a reference [18] to a “Comprehensive Hallucination Survey” by Alansari and Luqman, as part of the manuscript, but the bibliography needs to be checked. Reference to the original publication must be made for each citation.",
        "We checked every single citation in the reference list against original publisher records (IEEE, ACM, ACL, Taylor & Francis). We corrected author spellings, paper titles, DOIs, and citation numbers. Specifically, we updated reference [18] (Alansari and Luqman) to its verified publication details and made sure all method names match their original papers.",
        "References Section (Pages 28–31, Citations [1]–[40])."
    )

    add_qa(
        "Reviewer 2 — Point 4: Units of Measurement and Provenance of Numbers",
        "Use the appropriate unit of measurement for every number in figures and tables which bear a numerical value. Indicate if each value has been copied from an original article, calculated by the authors, approximated from a figure, or transformed/normalized. Quantitative comparisons should be accompanied by a dataset, a model, a definition of the metric, an experimental setting, and a source citation.",
        "We checked all numbers across our tables and figures to make sure units are clear (such as 'x' for speedup, '%' for gains, and normalized [0, 1] scales for errors). In the table notes and text, we explicitly state where each number came from, the dataset used (TruthfulQA, CoQA, etc.), the base model, and the metric definition.",
        "Tables 1–4 and Figures 3–12."
    )

    add_qa(
        "Reviewer 2 — Point 5: Fair Comparisons Across Experimental Contexts",
        "Do not compare methods tested in different contexts. AUROC, F1, accuracy, calibration error, retrieval performance and percentage improvements should not be directly compared for different models and datasets without a defensible normalization or common evaluation methodology.",
        "We reorganized our comparisons in Section 4 and Table 4 so numbers are only compared when tested under the same benchmark setup. We also added explicit notes warning readers that differences in test sets, prompt lengths, and base models prevent direct head-to-head rankings.",
        "Section 4 (Pages 17–20, Table 4)."
    )

    add_qa(
        "Reviewer 2 — Point 6: Deletion of the Unsubstantiated ~65% Claim",
        "Eliminate or substantiate the reported TRUEGUARD performance by experimentation. The manuscript outlines the conceptual framework TRUEGUARD, but the comparison table shows a success rate of around 65%. This number should be deleted if a protocol for the full evaluation or empirical evidence of TRUEGUARD implementation / experiment is not provided.",
        "We completely removed the '65%' figure and all related claims from the abstract, text, tables, and conclusion. You are right that giving an estimated success rate for a conceptual architecture without full experimental data was premature. TRUEGUARD is now presented strictly as a conceptual control framework.",
        "Abstract (Page 1), Table 4 (Page 18), Section 6 (Page 22), and Section 7 (Page 27)."
    )

    add_qa(
        "Reviewer 2 — Point 7: Detailed TRUEGUARD Conceptual Architecture",
        "Improve TRUEGUARD in the form of a conceptual architecture. Describe the fusion of the four signals, the determination of thresholds, how conflicting signals are dealt with, how explanations are generated, when retrieval and abstention is triggered, what kind of model access is needed and what kind of computational overhead is expected. A forward pass is currently proposed to extract several signals from the manuscript but this assumption needs to be carefully qualified.",
        "We expanded Section 6 to detail TRUEGUARD's system design: how the four signals are combined using a logistic gate, how conflicting signals are handled (e.g., using attention for internal self-contradictions and logit entropy for external fabrications), how the warning and fault thresholds are set, and how tiered corrections work. We also clarified that extracting internal signals in a single forward pass requires open-weight white-box access, while black-box setups use output entropy and verification queries instead.",
        "Section 6 (Pages 22–26, Subsections 6.1–6.5)."
    )

    # Formal Closing
    p_close = doc.add_paragraph()
    p_close.paragraph_format.space_before = Pt(16)
    p_close.paragraph_format.space_after = Pt(6)
    p_close.add_run(
        "Conclusion:\n"
        "We thank the editor and reviewers again for these helpful recommendations. They have made our survey much stronger, clearer, and more rigorous.\n\n"
        "Sincerely,\n"
        "Yogesh Ravi M & Dr. Pradeep Kumar T S\n"
        "Vellore Institute of Technology (VIT), Chennai, India"
    )

    doc.save(out_path)
    print("SUCCESS: saved ultra-humanized docx to", out_path)

if __name__ == "__main__":
    out1 = r"E:\trueguard\CAPSTONE\Response_to_Reviewers_269790004.docx"
    out2 = r"E:\trueguard\CAPSTONE\Response_to_Reviewers_269790004_humanized.docx"
    build_ultra_humanized_response(out1)
    try:
        build_ultra_humanized_response(out2)
    except Exception as e:
        print("Note: out2 is currently open in Word, skipping lock:", e)
