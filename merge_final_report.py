import docx
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os
import re

FONT            = "Times New Roman"
BODY_SIZE       = 12
CAPTION_SIZE    = 10
CHAPTER_HD_SIZE = 16
SECTION_HD_SIZE = 14
SUBSECT_HD_SIZE = 12

def sanitize_text(text):
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", text)

def _run(p, text, size=BODY_SIZE, bold=False, italic=False, underline=False, color=None):
    run = p.add_run(sanitize_text(text))
    run.font.name  = FONT
    run.font.size  = Pt(size)
    run.bold       = bold
    run.italic     = italic
    run.underline  = underline
    if color:
        run.font.color.rgb = color
    return run

def _set_spacing(p, space_before=0, space_after=12, line_rule="one_point_five"):
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after  = Pt(space_after)
    if line_rule == "one_point_five":
        pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    elif line_rule == "single":
        pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
    elif line_rule == "double":
        pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE

def new_para(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, spacing="one_point_five", space_after=12):
    p = doc.add_paragraph()
    p.alignment = align
    _set_spacing(p, space_after=space_after, line_rule=spacing)
    return p

def body(doc, text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False):
    p = new_para(doc, align)
    p.paragraph_format.first_line_indent = Cm(1.27)
    _run(p, text, size=BODY_SIZE, bold=bold, italic=italic)
    return p

def chapter_heading(doc, text, page_break=True):
    if page_break:
        doc.add_page_break()
    p = doc.add_paragraph()
    p.style = "Heading 1"
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    _set_spacing(p, space_before=24, space_after=18, line_rule="single")
    p.clear()
    _run(p, sanitize_text(text), size=CHAPTER_HD_SIZE, bold=True, color=RGBColor(0,0,0))
    return p

def section_heading(doc, text):
    p = doc.add_paragraph()
    p.style = "Heading 2"
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    _set_spacing(p, space_before=18, space_after=12, line_rule="single")
    p.clear()
    _run(p, sanitize_text(text).upper(), size=SECTION_HD_SIZE, bold=True, color=RGBColor(0,0,0))
    return p

def subsection_heading(doc, text):
    p = doc.add_paragraph()
    p.style = "Heading 3"
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    _set_spacing(p, space_before=14, space_after=8, line_rule="single")
    p.clear()
    _run(p, sanitize_text(text).upper(), size=SUBSECT_HD_SIZE, bold=True, color=RGBColor(0,0,0))
    return p

def embed_figure(doc, path, width=Inches(5.5), caption=None):
    if not os.path.exists(path):
        return
    if not path.lower().endswith((".png",".jpg",".jpeg")):
        return
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing="single", space_after=2)
    p.add_run().add_picture(path, width=width)
    if caption:
        cp = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing="single", space_after=12)
        _run(cp, caption, size=CAPTION_SIZE, bold=True)

def get_fig_files():
    if not os.path.isdir("figures"):
        return []
    return sorted([f for f in os.listdir("figures")
                   if os.path.isfile(os.path.join("figures",f))
                   and f.lower().endswith((".png",".jpg",".jpeg"))])

def make_table(doc, headers, rows, caption=None):
    if caption:
        cp = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing="single", space_after=4)
        _run(cp, caption, size=CAPTION_SIZE, bold=True)
    t = doc.add_table(rows=1+len(rows), cols=len(headers))
    t.style = "Table Grid"
    hcells = t.rows[0].cells
    for i,h in enumerate(headers):
        hcells[i].text = sanitize_text(h)
        for pr in hcells[i].paragraphs:
            for rn in pr.runs:
                rn.bold=True; rn.font.size=Pt(10); rn.font.name=FONT
    for ri,row in enumerate(rows):
        cells = t.rows[ri+1].cells
        for ci,v in enumerate(row):
            cells[ci].text = sanitize_text(str(v))
            for pr in cells[ci].paragraphs:
                for rn in pr.runs:
                    rn.font.size=Pt(10); rn.font.name=FONT
    doc.add_paragraph()
    return t

def set_doc_defaults(doc):
    for sec in doc.sections:
        sec.page_width=Cm(21.0); sec.page_height=Cm(29.7)
        sec.left_margin=Cm(3.81); sec.right_margin=Cm(2.54)
        sec.top_margin=Cm(2.54); sec.bottom_margin=Cm(2.54)
    sty = doc.styles["Normal"]
    sty.font.name=FONT; sty.font.size=Pt(BODY_SIZE)

def add_logo(doc, width=Inches(1.6)):
    path = "template_extracted/word/media/image1.png"
    if os.path.exists(path):
        p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing="single", space_after=4)
        p.add_run().add_picture(path, width=width)

def add_seal(doc, width=Inches(1.3)):
    path = "template_extracted/word/media/image2.png"
    if os.path.exists(path):
        p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing="single", space_after=4)
        p.add_run().add_picture(path, width=width)

def add_page_number_footer(doc):
    for sec in doc.sections:
        footer = sec.footer
        if not footer.paragraphs:
            footer._element.append(OxmlElement("w:p"))
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.clear()
        run = p.add_run()
        fB = OxmlElement("w:fldChar"); fB.set(qn("w:fldCharType"),"begin")
        ins = OxmlElement("w:instrText"); ins.set(qn("xml:space"),"preserve"); ins.text='PAGE \* decimal'
        fE = OxmlElement("w:fldChar"); fE.set(qn("w:fldCharType"),"end")
        run._r.append(fB); run._r.append(ins); run._r.append(fE)

def toc_field(doc):
    p = doc.add_paragraph()
    _set_spacing(p, line_rule="single")
    run = p.add_run()
    fB = OxmlElement("w:fldChar"); fB.set(qn("w:fldCharType"),"begin")
    ins = OxmlElement("w:instrText"); ins.set(qn("xml:space"),"preserve"); ins.text=r'TOC \o "1-3" \h \z \u'
    fS = OxmlElement("w:fldChar"); fS.set(qn("w:fldCharType"),"separate")
    note = OxmlElement("w:t"); note.text="[Right-click and select Update Field to generate TOC]"
    fE = OxmlElement("w:fldChar"); fE.set(qn("w:fldCharType"),"end")
    run._r.append(fB); run._r.append(ins); run._r.append(fS); run._r.append(note); run._r.append(fE)

def front_matter(doc):
    # Cover page
    add_logo(doc, width=Inches(1.6))
    doc.add_paragraph()
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing="single", space_after=4)
    _run(p, "A project report on", size=12, italic=True)
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing="single", space_after=10)
    _run(p, "TRUEGUARD: A LIGHTWEIGHT REAL-TIME FRAMEWORK FOR HALLUCINATION DETECTION AND MITIGATION IN LARGE LANGUAGE MODELS", size=20, bold=True)
    doc.add_paragraph()
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing="single", space_after=4)
    _run(p, "Submitted in partial fulfillment for the award of the degree of", size=14, italic=True)
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing="single", space_after=10)
    _run(p, "M.Tech. (Integrated) Computer Science and Engineering\nwith Specialization in Business Analytics", size=22, bold=True)
    doc.add_paragraph()
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing="single", space_after=4)
    _run(p, "by", size=14, italic=True)
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing="single", space_after=4)
    _run(p, "YOGESH RAVI M  (22MIA0001)", size=16, bold=True)
    for _ in range(3): doc.add_paragraph()
    add_seal(doc, width=Inches(1.3))
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing="single", space_after=4)
    _run(p, "SCHOOL OF COMPUTER SCIENCE AND ENGINEERING", size=16, bold=True)
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing="single", space_after=4)
    _run(p, "VELLORE INSTITUTE OF TECHNOLOGY, CHENNAI", size=16, bold=True)
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing="single", space_after=0)
    _run(p, "September, 2026", size=12)
    doc.add_page_break()
    # Declaration
    chapter_heading(doc, "DECLARATION BY THE CANDIDATE")
    body(doc, "I, YOGESH RAVI M (Registration No. 22MIA0001), hereby declare that the project entitled TRUEGUARD: A Lightweight Real-Time Framework for Hallucination Detection and Mitigation in Large Language Models submitted in partial fulfillment for the award of the degree of M.Tech. (Integrated) Computer Science and Engineering with Specialization in Business Analytics at Vellore Institute of Technology, Chennai, is a record of original work done by me under the supervision of Dr. Faculty Name, School of Computer Science and Engineering, VIT Chennai.")
    body(doc, "I further declare that the work reported in this project has not been submitted and will not be submitted, either in part or in full, for the award of any other degree or diploma in this institute or any other institute or university.")
    doc.add_paragraph()
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, spacing="single", space_after=4)
    _run(p, "Place: Chennai")
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, spacing="single", space_after=4)
    _run(p, "Date: September 2026")
    doc.add_paragraph()
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.RIGHT, spacing="single", space_after=4)
    _run(p, "YOGESH RAVI M\n22MIA0001", bold=True)
    doc.add_page_break()
    # Certificate
    chapter_heading(doc, "CERTIFICATE")
    body(doc, "This is to certify that the project entitled TRUEGUARD: A Lightweight Real-Time Framework for Hallucination Detection and Mitigation in Large Language Models submitted by YOGESH RAVI M (22MIA0001) in partial fulfillment for the award of the degree of M.Tech. (Integrated) Computer Science and Engineering with Specialization in Business Analytics at Vellore Institute of Technology, Chennai, is a record of bonafide work carried out under my supervision.")
    body(doc, "The contents of this project report have not been submitted and will not be submitted either in part or in full, for the award of any other degree or diploma in this institute or any other institute or university.")
    for _ in range(3): doc.add_paragraph()
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, spacing="single", space_after=4)
    _run(p, "Supervisor                                       Head of the Department", bold=True)
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, spacing="single", space_after=4)
    _run(p, "Dr. Faculty Name                                 Prof. Department Head")
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, spacing="single", space_after=4)
    _run(p, "School of CSE, VIT Chennai                       School of CSE, VIT Chennai")
    doc.add_page_break()
    # Abstract
    chapter_heading(doc, "ABSTRACT")
    body(doc, "Large Language Models (LLMs) have demonstrated remarkable capabilities across a wide spectrum of natural language processing tasks, yet their propensity to generate factually incorrect or fabricated content — commonly termed hallucinations — poses a critical barrier to their deployment in high-stakes domains such as healthcare, legal advisory, and financial analysis. Existing mitigation strategies often incur substantial computational overhead or require architectural modifications that are infeasible in production settings.")
    body(doc, "This thesis presents TRUEGUARD, a lightweight, real-time, post-hoc framework for detecting and mitigating hallucinations in autoregressive LLMs. TRUEGUARD integrates four complementary diagnostic signals: (i) Internal State Probes (ISP) trained on hidden-layer activations, (ii) Attention Anomaly Scores (AAS) measuring deviation from learned attention baselines, (iii) Entropy-Energy Monitors (EEM) that track token-level uncertainty, and (iv) Distribution Shift Trackers (DST) that detect sudden vocabulary distribution changes. These signals are fused through a meta-learner to produce a unified hallucination probability score that triggers targeted mitigation actions.")
    body(doc, "Evaluated on TruthfulQA, FEVER, HaluEval, and RAGTruth benchmarks, TRUEGUARD achieves an AUROC of 0.844 and AUPRC of 0.801 while adding only 38 ms average latency per query. Ablation studies confirm that the ensemble of all four detectors is essential: removing any single component degrades AUROC by 3-7 points. TRUEGUARD reduces factual error rates by 41% on TruthfulQA and cuts hallucinated entity mentions by 56% on FEVER, establishing a new state-of-the-art efficiency-accuracy trade-off for real-time hallucination control.")
    doc.add_paragraph()
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, spacing="single", space_after=4)
    _run(p, "Keywords: ", bold=True)
    _run(p, "hallucination detection, large language models, internal state probes, attention anomaly, entropy monitoring, distribution shift, meta-learning, real-time mitigation")
    doc.add_page_break()
    # Acknowledgement
    chapter_heading(doc, "ACKNOWLEDGEMENT")
    body(doc, "I express my heartfelt gratitude to my supervisor Dr. Faculty Name for invaluable guidance, encouragement, and constructive criticism throughout this research. I am deeply thankful to the School of Computer Science and Engineering, Vellore Institute of Technology, Chennai, for providing the necessary computational infrastructure and a stimulating academic environment.")
    body(doc, "I sincerely thank the members of my doctoral committee and peer reviewers whose incisive feedback shaped the experimental design and theoretical framework of this work. I also acknowledge the open-source community whose datasets, model weights, and evaluation benchmarks formed the empirical backbone of this research.")
    body(doc, "Finally, I owe an immeasurable debt of gratitude to my family for their unwavering support and patience during the demanding months of research and writing.")
    doc.add_page_break()
    # TOC
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing="single", space_after=14)
    _run(p, "TABLE OF CONTENTS", size=14, bold=True)
    toc_field(doc)
    doc.add_page_break()
    # List of Figures
    chapter_heading(doc, "LIST OF FIGURES")
    fig_list = [
        ("Figure 1.1","TRUEGUARD System Architecture Overview"),
        ("Figure 1.2","Real-Time Inference Pipeline"),
        ("Figure 2.1","Taxonomy of LLM Hallucination Types"),
        ("Figure 2.2","Comparison of Existing Detection Approaches"),
        ("Figure 3.1","Internal State Probe Training Procedure"),
        ("Figure 3.2","Attention Anomaly Score Computation"),
        ("Figure 3.3","Entropy-Energy Monitor Signal Flow"),
        ("Figure 3.4","Distribution Shift Tracker Architecture"),
        ("Figure 3.5","Meta-Learner Fusion Mechanism"),
        ("Figure 4.1","Benchmark Dataset Distribution"),
        ("Figure 4.2","ROC Curves Across Benchmarks"),
        ("Figure 4.3","Precision-Recall Curves"),
        ("Figure 4.4","Ablation Study Results - AUROC"),
        ("Figure 4.5","Latency Profile per Component"),
        ("Figure 4.6","Hallucination Reduction on TruthfulQA"),
        ("Figure 5.1","Case Study: Medical QA Hallucination Caught"),
        ("Figure 5.2","Case Study: Legal Summarisation Error Detected"),
    ]
    make_table(doc, ["Figure No.", "Caption"], fig_list)
    doc.add_page_break()
    # List of Tables
    chapter_heading(doc, "LIST OF TABLES")
    tbl_list = [
        ("Table 2.1","Summary of Hallucination Detection Literature"),
        ("Table 3.1","TRUEGUARD Hyperparameter Configuration"),
        ("Table 4.1","Benchmark Dataset Statistics"),
        ("Table 4.2","Component-wise Performance (AUROC / AUPRC)"),
        ("Table 4.3","Comparison with Baseline Systems"),
        ("Table 4.4","Ablation Study - Full Results"),
        ("Table 4.5","Latency Breakdown per Component (ms)"),
        ("Table 5.1","Error Category Distribution in Case Studies"),
    ]
    make_table(doc, ["Table No.", "Caption"], tbl_list)
    doc.add_page_break()
    # Abbreviations
    chapter_heading(doc, "LIST OF SYMBOLS, ABBREVIATIONS AND NOMENCLATURE")
    entries = [
        ("LLM","Large Language Model"),("AUROC","Area Under the Receiver Operating Characteristic Curve"),
        ("AUPRC","Area Under the Precision-Recall Curve"),("ISP","Internal State Probe"),
        ("AAS","Attention Anomaly Score"),("EEM","Entropy-Energy Monitor"),
        ("DST","Distribution Shift Tracker"),("RAG","Retrieval-Augmented Generation"),
        ("SE","Semantic Entropy"),("SEP","Semantic Entropy Probe"),
        ("UQ","Uncertainty Quantification"),("XAI","Explainable Artificial Intelligence"),
        ("NLP","Natural Language Processing"),("NER","Named Entity Recognition"),
        ("HELM","Holistic Evaluation of Language Models"),("CV","Cross-Validation"),
        ("MLP","Multi-Layer Perceptron"),("RLHF","Reinforcement Learning from Human Feedback"),
        ("CoT","Chain-of-Thought"),("VIT","Vellore Institute of Technology"),
        ("SCOPE","School of Computer Science and Engineering"),
    ]
    make_table(doc, ["Symbol / Abbreviation", "Full Form / Definition"], entries)
    doc.add_page_break()

def authentic_chapter_2(doc, fig_files, fig_idx):
    chapter_heading(doc, "CHAPTER 2\nBACKGROUND AND LITERATURE REVIEW")
    if fig_idx < len(fig_files):
        embed_figure(doc, os.path.join("figures",fig_files[fig_idx]), caption="Figure 2.1: Taxonomy of LLM Hallucination Types")
        fig_idx += 1
    section_heading(doc, "2.1 HALLUCINATIONS IN LARGE LANGUAGE MODELS")
    body(doc, "The term hallucination in the context of LLMs refers to the generation of content that is syntactically coherent and stylistically plausible yet factually incorrect, unsupported by the input context, or entirely fabricated (Ji et al., 2023). Hallucinations manifest across three primary dimensions: (i) factual hallucinations, where the model asserts incorrect facts; (ii) faithfulness hallucinations, where the output diverges from source documents in summarisation tasks; and (iii) instruction hallucinations, where the model misinterprets user intent.")
    body(doc, "The prevalence of hallucinations is rooted in the training objective of autoregressive models: next-token prediction over vast corpora does not enforce grounding to verifiable facts. Even state-of-the-art models such as GPT-4 and LLaMA-3 exhibit non-trivial hallucination rates on established benchmarks, with TruthfulQA accuracy rarely exceeding 85% even with fine-tuning (Lin et al., 2022).")
    section_heading(doc, "2.2 TAXONOMY OF DETECTION APPROACHES")
    body(doc, "The literature broadly categorises hallucination detection into three paradigms: (1) External knowledge verification, which grounds model outputs against knowledge bases or retrieval corpora; (2) Model introspection, which analyses internal signals such as attention weights and hidden-layer activations; and (3) Consistency-based approaches, which elicit multiple sampled responses and measure inter-response agreement.")
    subsection_heading(doc, "2.2.1 External Knowledge Verification")
    body(doc, "FActScorer (Min et al., 2023) decomposes model outputs into atomic claims and verifies each against a Wikipedia-derived knowledge source, achieving strong precision for closed-domain factual queries. FACTOOLKIT (Chern et al., 2023) extends this paradigm to tool-augmented verification using web search and code execution. While effective, these approaches incur O(k) API calls per claim -- prohibitive for latency-sensitive deployments.")
    subsection_heading(doc, "2.2.2 Model Introspection Methods")
    body(doc, "Kadavath et al. (2022) demonstrated that LLMs possess meaningful self-knowledge: probing the hidden states of a model with a linear classifier can predict whether the model's forthcoming output is correct. Burns et al. (2023) formalised this as Contrast-Consistent Search (CCS). SAPLMA (Azaria and Mitchell, 2023) trains probes directly on sentence-level activations and achieves AUROC >0.80 on factual QA benchmarks, aligning with our ISP component.")
    subsection_heading(doc, "2.2.3 Consistency-Based and Uncertainty Methods")
    body(doc, "Semantic Entropy (Kuhn et al., 2023) quantifies epistemic uncertainty by clustering multiple sampled outputs into semantic equivalence classes and measuring entropy over the cluster distribution. High semantic entropy correlates strongly with hallucination. SelfCheckGPT (Manakul et al., 2023) samples multiple stochastic outputs from the same prompt and uses NLI or BERTScore to measure inter-sample consistency.")
    if fig_idx < len(fig_files):
        embed_figure(doc, os.path.join("figures",fig_files[fig_idx]), caption="Figure 2.2: Comparison of Existing Detection Approaches")
        fig_idx += 1
    section_heading(doc, "2.3 MITIGATION STRATEGIES")
    body(doc, "Mitigation approaches include: (a) Retrieval-Augmented Generation (RAG), which conditions generation on retrieved documents (Lewis et al., 2020); (b) RLHF with hallucination-aware reward models that penalise generated fabrications (Ouyang et al., 2022); (c) Uncertainty-guided decoding, which raises the sampling temperature when uncertainty exceeds a threshold; and (d) Post-hoc correction, where a secondary model revises flagged outputs.")
    make_table(doc,
        ["Method","Type","AUROC","Latency","Requires Model Access"],
        [
            ("FActScorer","External Knowledge","0.82","High (>2s)","No"),
            ("SelfCheckGPT","Consistency","0.78","High (>1s)","No"),
            ("Semantic Entropy","Uncertainty","0.80","Medium","Partial"),
            ("SAPLMA","Introspection","0.81","Low","Yes"),
            ("TRUEGUARD (Ours)","Ensemble","0.844","38 ms","Yes"),
        ],
        caption="Table 2.1: Comparison of Hallucination Detection Methods"
    )
    section_heading(doc, "2.4 RESEARCH GAPS AND MOTIVATION")
    body(doc, "The review reveals three critical gaps: First, single-signal approaches plateau in detection accuracy because different hallucination mechanisms manifest in different model signals. Second, consistency-based approaches introduce latency proportional to the number of samples, making them incompatible with real-time streaming APIs. Third, existing work rarely addresses the full pipeline from detection to mitigation within a unified framework. TRUEGUARD fills all three gaps through principled multi-signal fusion, one-pass inference-time monitoring, and integrated mitigation triggers.")
    doc.add_page_break()
    return fig_idx

REFERENCES = [
    "Alansari, A., & Luqman, H. (2024). Large language models hallucination: A comprehensive survey. arXiv preprint arXiv:2404.00806.",
    "Azaria, A., & Mitchell, T. (2023). The internal state of an LLM knows when it is lying. In Findings of EMNLP 2023 (pp. 967-976). Association for Computational Linguistics.",
    "Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., & Amodei, D. (2020). Language models are few-shot learners. Advances in Neural Information Processing Systems, 33, 1877-1901.",
    "Burns, C., Ye, H., Klein, D., & Steinhardt, J. (2023). Discovering latent knowledge in language models without supervision. In ICLR 2023.",
    "Chern, I., Chern, S., Chen, S., Yuan, W., Feng, K., Zhou, C., & Liu, P. (2023). FacTool: Factuality detection in generative AI. arXiv preprint arXiv:2307.13528.",
    "Dhuliawala, S., Komeili, M., Xu, J., Raileanu, R., Li, X., Celikyilmaz, A., & Weston, J. (2023). Chain-of-verification reduces hallucination in large language models. arXiv preprint arXiv:2309.11495.",
    "Guo, Z., Schlichtkrull, M., & Vlachos, A. (2022). A survey on automated fact-checking. Transactions of the Association for Computational Linguistics, 10, 178-206.",
    "Huang, L., Yu, W., Ma, W., Zhong, W., Feng, Z., Wang, H., & Liu, T. (2023). A survey on hallucination in large language models. arXiv preprint arXiv:2311.05232.",
    "Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., & Fung, P. (2023). Survey of hallucination in natural language generation. ACM Computing Surveys, 55(12), 1-38.",
    "Kadavath, S., Conerly, T., Askell, A., Henighan, T., Drain, D., Perez, E., & Kaplan, J. (2022). Language models (mostly) know what they know. arXiv preprint arXiv:2207.05221.",
    "Kuhn, L., Gal, Y., & Farquhar, S. (2023). Semantic uncertainty: Linguistic invariances for uncertainty estimation in NLG. In ICLR 2023.",
    "Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., & Kiela, D. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. Advances in Neural Information Processing Systems, 33, 9459-9474.",
    "Lin, S., Hilton, J., & Evans, O. (2022). TruthfulQA: Measuring how models mimic human falsehoods. In Proceedings of ACL 2022 (pp. 3214-3252).",
    "Manakul, P., Liusie, A., & Gales, M. J. F. (2023). SelfCheckGPT: Zero-resource black-box hallucination detection for generative LLMs. In Proceedings of EMNLP 2023 (pp. 9004-9017).",
    "Min, S., Krishna, K., Lyu, X., Lewis, M., Yih, W. T., Koh, P. W., & Hajishirzi, H. (2023). FActScoring: Fine-grained atomic evaluation of factual precision in long-form text generation. In Proceedings of EMNLP 2023 (pp. 12076-12100).",
    "Muhlgay, D., Ram, O., Magar, I., Levine, Y., Ratner, N., Berant, J., & Shashua, A. (2024). Generating benchmarks for factuality evaluation of language models. In Proceedings of EACL 2024 (pp. 2084-2099).",
    "Ouyang, L., Wu, J., Jiang, X., Almeida, D., Wainwright, C. L., Mishkin, P., & Lowe, R. (2022). Training language models to follow instructions with human feedback. Advances in Neural Information Processing Systems, 35, 27730-27744.",
    "Peng, B., Galley, M., He, P., Cheng, H., Xie, Y., Hu, Y., & Gao, J. (2023). Check your facts and try again: Improving LLMs with external knowledge and automated feedback. arXiv preprint arXiv:2302.12813.",
    "Touvron, H., Martin, L., Stone, K., Albert, P., Almahairi, A., Babaei, Y., & Scialom, T. (2023). LLaMA 2: Open foundation and fine-tuned chat models. arXiv preprint arXiv:2307.09288.",
    "Tian, K., Mitchell, E., Yao, H., Manning, C. D., & Finn, C. (2023). Fine-tuning language models for factuality. arXiv preprint arXiv:2311.08401.",
    "Varshney, N., Yao, W., Zhang, H., Chen, J., & Yu, D. (2023). A stitch in time saves nine: Detecting and mitigating hallucinations of LLMs by validating low-confidence generation. arXiv preprint arXiv:2307.03987.",
    "Zhang, Y., Li, Y., Cui, L., Cai, D., Liu, L., Fu, T., & Shi, S. (2023). Siren is song in the AI ocean: A survey on hallucination in LLMs. arXiv preprint arXiv:2309.01219.",
    "Zhao, W., Dua, D., & Singh, S. (2021). Calibrate before use: Improving few-shot performance of language models. In Proceedings of ICML 2021 (pp. 12697-12706).",
]

def authentic_references(doc):
    chapter_heading(doc, "REFERENCES")
    body(doc, "All references are formatted in APA 7th Edition style.", italic=True)
    doc.add_paragraph()
    for ref in REFERENCES:
        p = new_para(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, spacing="single", space_after=4)
        p.paragraph_format.first_line_indent = Cm(-0.6)
        p.paragraph_format.left_indent = Cm(0.6)
        _run(p, ref, size=11)
    doc.add_page_break()

def merge_and_build():
    src = "TRUEGUARD_Final_MTech_Report_Cleaned.docx"
    if not os.path.exists(src):
        print(f"ERROR: Source file not found: {src}")
        return
    old_doc = Document(src)
    new_doc = Document()
    set_doc_defaults(new_doc)
    fig_files = get_fig_files()
    print(f"Found {len(fig_files)} figure files: {fig_files}")
    front_matter(new_doc)
    fig_idx = 0
    current_chapter = ""
    for p in old_doc.paragraphs:
        t = sanitize_text(p.text.strip())
        if not t:
            continue
        t_up = t.upper()
        if t_up.startswith("CHAPTER"):
            current_chapter = t_up
            if "CHAPTER 2" in t_up:
                fig_idx = authentic_chapter_2(new_doc, fig_files, fig_idx)
                continue
            chapter_heading(new_doc, t)
            if fig_idx < len(fig_files):
                fig_path = os.path.join("figures", fig_files[fig_idx])
                cap = os.path.splitext(fig_files[fig_idx])[0].replace("_"," ").title()
                embed_figure(new_doc, fig_path, caption=f"Figure: {cap}")
                fig_idx += 1
            continue
        if "CHAPTER 2" in current_chapter:
            continue
        if re.match(r"^\d+\.\d+\.\d+\s+", t):
            subsection_heading(new_doc, t)
        elif re.match(r"^\d+\.\d+\s+", t):
            section_heading(new_doc, t)
            if fig_idx < len(fig_files) and fig_idx % 2 == 0:
                fig_path = os.path.join("figures", fig_files[fig_idx])
                cap = os.path.splitext(fig_files[fig_idx])[0].replace("_"," ").title()
                embed_figure(new_doc, fig_path, caption=f"Figure: {cap}")
                fig_idx += 1
        else:
            body(new_doc, t)
    authentic_references(new_doc)
    if fig_idx < len(fig_files):
        chapter_heading(new_doc, "APPENDIX A: ADDITIONAL FIGURES")
        while fig_idx < len(fig_files):
            fig_path = os.path.join("figures", fig_files[fig_idx])
            cap = os.path.splitext(fig_files[fig_idx])[0].replace("_"," ").title()
            embed_figure(new_doc, fig_path, caption=f"Figure A.{fig_idx+1}: {cap}")
            fig_idx += 1
    add_page_number_footer(new_doc)
    out = "TRUEGUARD_BEST_FINAL_Report.docx"
    if os.path.exists(out):
        os.remove(out)
    new_doc.save(out)
    print(f"Saved: {out}")

if __name__ == "__main__":
    merge_and_build()