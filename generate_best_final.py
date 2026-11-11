"""
TRUEGUARD — Final M.Tech Project Report
Strictly conforming to VIT Chennai MIA-Project format specification.
Ground truth content from TRUEGUARD_IEEE_FINAL.tex and Mini_Project_Literature_Review.md only.
"""

import docx
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

# ─────────────────────────────────────────────────────────────────────────────
#  GLOBAL STYLE CONSTANTS (per VIT spec)
# ─────────────────────────────────────────────────────────────────────────────
FONT = 'Times New Roman'
BODY_SIZE        = 12
CAPTION_SIZE     = 10
CHAPTER_HD_SIZE  = 16   # Chapter heading: 16, Bold
SECTION_HD_SIZE  = 14   # Section heading:  14, CAPS
SUBSECT_HD_SIZE  = 12   # Subsection:       12, CAPS
LINE_SPACING_VAL = Pt(18)   # ~1.5 for 12pt text

# ─────────────────────────────────────────────────────────────────────────────
#  LOW-LEVEL HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _run(p, text, size=BODY_SIZE, bold=False, italic=False, underline=False, color=None):
    run = p.add_run(text)
    run.font.name  = FONT
    run.font.size  = Pt(size)
    run.bold       = bold
    run.italic     = italic
    run.underline  = underline
    if color:
        run.font.color.rgb = color
    return run

def _set_spacing(p, space_before=0, space_after=6, line_rule='one_point_five'):
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after  = Pt(space_after)
    if line_rule == 'one_point_five':
        pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    elif line_rule == 'single':
        pf.line_spacing_rule = WD_LINE_SPACING.SINGLE

def new_para(doc, align=WD_ALIGN_PARAGRAPH.JUSTIFY, spacing='one_point_five', space_after=6):
    p = doc.add_paragraph()
    p.alignment = align
    _set_spacing(p, space_after=space_after, line_rule=spacing)
    return p

def body(doc, text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False):
    p = new_para(doc, align)
    _run(p, text, size=BODY_SIZE, bold=bold, italic=italic)
    return p

def chapter_heading(doc, text):
    """Chapter heading: 16pt, Bold, Centered, Times New Roman."""
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=18)
    _set_spacing(p, space_before=12, space_after=12, line_rule='single')
    _run(p, text, size=CHAPTER_HD_SIZE, bold=True)
    return p

def section_heading(doc, text):
    """Section heading: 14pt, CAPS, Times New Roman."""
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, spacing='single', space_after=6)
    _set_spacing(p, space_before=10, space_after=6, line_rule='single')
    _run(p, text.upper(), size=SECTION_HD_SIZE, bold=True)
    return p

def subsection_heading(doc, text):
    """Subsection heading: 12pt, CAPS, Times New Roman."""
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, spacing='single', space_after=4)
    _set_spacing(p, space_before=6, space_after=4, line_rule='single')
    _run(p, text.upper(), size=SUBSECT_HD_SIZE, bold=True)
    return p

def fig_caption(doc, text):
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=8)
    _run(p, text, size=CAPTION_SIZE, italic=True)
    return p

def tbl_caption(doc, text):
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=4)
    _run(p, text, size=CAPTION_SIZE, bold=True)
    return p

def embed_figure(doc, path, width=Inches(5.5)):
    if os.path.exists(path):
        p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=2)
        p.add_run().add_picture(path, width=width)
    else:
        body(doc, f'[Figure file not found: {path}]', align=WD_ALIGN_PARAGRAPH.CENTER, italic=True)

def make_table(doc, headers, rows):
    t = doc.add_table(rows=1+len(rows), cols=len(headers))
    t.style = 'Table Grid'
    hcells = t.rows[0].cells
    for i, h in enumerate(headers):
        hcells[i].text = h
        for pr in hcells[i].paragraphs:
            for rn in pr.runs:
                rn.bold = True; rn.font.size = Pt(10); rn.font.name = FONT
    for ri, row in enumerate(rows):
        cells = t.rows[ri+1].cells
        for ci, v in enumerate(row):
            cells[ci].text = str(v)
            for pr in cells[ci].paragraphs:
                for rn in pr.runs:
                    rn.font.size = Pt(10); rn.font.name = FONT
    return t

def bullet_item(doc, text):
    p = doc.add_paragraph(style='List Bullet')
    _set_spacing(p, space_after=3, line_rule='one_point_five')
    _run(p, text)
    return p

def numbered_item(doc, text):
    p = doc.add_paragraph(style='List Number')
    _set_spacing(p, space_after=3, line_rule='one_point_five')
    _run(p, text)
    return p

def add_logo(doc, width=Inches(1.6)):
    paths = ['template_extracted/word/media/image1.png',
             'template_extracted/word/media/image2.png']
    for path in paths:
        if os.path.exists(path):
            p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=4)
            p.add_run().add_picture(path, width=width)
            return
    body(doc, '[VIT Logo — template_extracted/word/media/image1.png]',
         align=WD_ALIGN_PARAGRAPH.CENTER, italic=True)

def add_seal(doc, width=Inches(1.3)):
    path = 'template_extracted/word/media/image2.png'
    if os.path.exists(path):
        p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=4)
        p.add_run().add_picture(path, width=width)

def add_page_number_footer(doc, roman=False):
    """Add bottom-center page number to all section footers."""
    for sec in doc.sections:
        footer = sec.footer
        if not footer.paragraphs:
            footer._element.append(OxmlElement('w:p'))
        p = footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.clear()
        run = p.add_run()
        if roman:
            fmt = 'lowerRoman'
        else:
            fmt = 'decimal'
        fB = OxmlElement('w:fldChar'); fB.set(qn('w:fldCharType'), 'begin')
        ins = OxmlElement('w:instrText')
        ins.set(qn('xml:space'), 'preserve')
        ins.text = f'PAGE \\* {fmt}'
        fE = OxmlElement('w:fldChar'); fE.set(qn('w:fldCharType'), 'end')
        run._r.append(fB); run._r.append(ins); run._r.append(fE)

def toc_field(doc):
    p = doc.add_paragraph()
    _set_spacing(p, line_rule='single')
    run = p.add_run()
    fB = OxmlElement('w:fldChar'); fB.set(qn('w:fldCharType'), 'begin')
    ins = OxmlElement('w:instrText')
    ins.set(qn('xml:space'), 'preserve')
    ins.text = 'TOC \\o "1-3" \\h \\z \\u'
    fS = OxmlElement('w:fldChar'); fS.set(qn('w:fldCharType'), 'separate')
    note = OxmlElement('w:t')
    note.text = '[Right-click this line and select Update Field to generate the Table of Contents]'
    fE = OxmlElement('w:fldChar'); fE.set(qn('w:fldCharType'), 'end')
    run._r.append(fB); run._r.append(ins); run._r.append(fS); run._r.append(note); run._r.append(fE)

def set_doc_defaults(doc):
    for sec in doc.sections:
        sec.page_width    = Cm(21.0)
        sec.page_height   = Cm(29.7)
        sec.left_margin   = Cm(3.81)
        sec.right_margin  = Cm(2.54)
        sec.top_margin    = Cm(2.54)
        sec.bottom_margin = Cm(2.54)
    sty = doc.styles['Normal']
    sty.font.name = FONT
    sty.font.size = Pt(BODY_SIZE)

# ─────────────────────────────────────────────────────────────────────────────
#  1. COVER PAGE  (spec: exact font hierarchy as given)
# ─────────────────────────────────────────────────────────────────────────────

def cover_page(doc):
    add_logo(doc, width=Inches(1.6))
    doc.add_paragraph()

    # "A project report on"  — 12pt Italic
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=4)
    _run(p, 'A project report on', size=12, italic=True)

    # TITLE — 20pt Bold CAPS
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=10)
    _run(p, 'TRUEGUARD: A LIGHTWEIGHT REAL-TIME FRAMEWORK FOR HALLUCINATION DETECTION AND MITIGATION IN LARGE LANGUAGE MODELS',
         size=20, bold=True)

    doc.add_paragraph()

    # "Submitted in partial fulfillment..." — 14pt Italic
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=4)
    _run(p, 'Submitted in partial fulfillment for the award of the degree of', size=14, italic=True)

    # Degree name — 22pt Bold
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=10)
    _run(p, 'M.Tech. (Integrated) Computer Science and Engineering with Specialization in Business Analytics',
         size=22, bold=True)

    doc.add_paragraph()

    # "by" — 14pt Italic
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=4)
    _run(p, 'by', size=14, italic=True)

    # NAME (Reg. No.) — 16pt Bold CAPS
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=4)
    _run(p, 'YOGESH RAVI M (22MIA0001)', size=16, bold=True)

    for _ in range(3):
        doc.add_paragraph()

    add_seal(doc, width=Inches(1.3))

    # School name — 16pt Bold CAPS
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=4)
    _run(p, 'SCHOOL OF COMPUTER SCIENCE AND ENGINEERING', size=16, bold=True)

    # Vellore Institute of Technology — 16pt Bold CAPS
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=4)
    _run(p, 'VELLORE INSTITUTE OF TECHNOLOGY, CHENNAI', size=16, bold=True)

    # Date — 12pt
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=0)
    _run(p, 'September, 2026', size=12)

    doc.add_page_break()

# ─────────────────────────────────────────────────────────────────────────────
#  2. TITLE PAGE  (identical text to cover page per spec)
# ─────────────────────────────────────────────────────────────────────────────

def title_page(doc):
    add_logo(doc, width=Inches(1.6))
    doc.add_paragraph()

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=4)
    _run(p, 'A project report on', size=12, italic=True)

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=10)
    _run(p, 'TRUEGUARD: A LIGHTWEIGHT REAL-TIME FRAMEWORK FOR HALLUCINATION DETECTION AND MITIGATION IN LARGE LANGUAGE MODELS',
         size=20, bold=True)

    doc.add_paragraph()

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=4)
    _run(p, 'Submitted in partial fulfillment for the award of the degree of', size=14, italic=True)

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=10)
    _run(p, 'M.Tech. (Integrated) Computer Science and Engineering with Specialization in Business Analytics',
         size=22, bold=True)

    doc.add_paragraph()

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=4)
    _run(p, 'by', size=14, italic=True)

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=4)
    _run(p, 'YOGESH RAVI M (22MIA0001)', size=16, bold=True)

    doc.add_paragraph()

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=4)
    _run(p, 'Under the guidance of', size=12, italic=True)

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=4)
    _run(p, 'Dr. T. S. PRADEEP KUMAR', size=14, bold=True)

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=14)
    _run(p, 'Associate Professor, SCOPE', size=12)

    for _ in range(2):
        doc.add_paragraph()

    add_seal(doc, width=Inches(1.3))

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=4)
    _run(p, 'SCHOOL OF COMPUTER SCIENCE AND ENGINEERING', size=16, bold=True)

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=4)
    _run(p, 'VELLORE INSTITUTE OF TECHNOLOGY, CHENNAI', size=16, bold=True)

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=0)
    _run(p, 'September, 2026', size=12)

    doc.add_page_break()

# ─────────────────────────────────────────────────────────────────────────────
#  3. DECLARATION
# ─────────────────────────────────────────────────────────────────────────────

def declaration_page(doc):
    doc.add_paragraph()
    # Heading: 14pt, Underlined, Bold, CAPS
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=18)
    _run(p, 'DECLARATION', size=14, bold=True, underline=True)

    body(doc, 'I hereby declare that the thesis entitled "TRUEGUARD: A LIGHTWEIGHT REAL-TIME FRAMEWORK FOR HALLUCINATION DETECTION AND MITIGATION IN LARGE LANGUAGE MODELS" submitted by me, for the award of the degree of M.Tech. (Integrated) Computer Science and Engineering with Specialization in Business Analytics, Vellore Institute of Technology, Chennai, is a record of bonafide work carried out by me under the supervision of Dr. T. S. Pradeep Kumar, Associate Professor, School of Computer Science and Engineering, Vellore Institute of Technology, Chennai.')

    body(doc, 'I further declare that the work reported in this thesis has not been submitted and will not be submitted, either in part or in full, for the award of any other degree or diploma in this institute or any other institute or university.')

    for _ in range(3):
        doc.add_paragraph()

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, spacing='single', space_after=4)
    _run(p, 'Place: Chennai', size=14, bold=True)

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, spacing='single', space_after=4)
    _run(p, 'Date:', size=14, bold=True)

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.RIGHT, spacing='single', space_after=4)
    _run(p, 'Signature of the Candidate', size=14, bold=True)

    for _ in range(3):
        doc.add_paragraph()

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.RIGHT, spacing='single', space_after=2)
    _run(p, 'YOGESH RAVI M', size=14, bold=True)

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.RIGHT, spacing='single', space_after=2)
    _run(p, 'Reg. No.: 22MIA0001', size=12)

    doc.add_page_break()

# ─────────────────────────────────────────────────────────────────────────────
#  4. CERTIFICATE
# ─────────────────────────────────────────────────────────────────────────────

def certificate_page(doc):
    add_logo(doc, width=Inches(1.6))

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=4)
    _run(p, 'School of Computer Science and Engineering', size=14, bold=True)

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=4)
    _run(p, 'Vellore Institute of Technology, Chennai', size=12)

    doc.add_paragraph()

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=14)
    _run(p, 'CERTIFICATE', size=14, bold=True, underline=True)

    body(doc, 'This is to certify that the report entitled "TRUEGUARD: A LIGHTWEIGHT REAL-TIME FRAMEWORK FOR HALLUCINATION DETECTION AND MITIGATION IN LARGE LANGUAGE MODELS" is prepared and submitted by YOGESH RAVI M (Reg. No.: 22MIA0001) to Vellore Institute of Technology, Chennai, in partial fulfillment of the requirement for the award of the degree of M.Tech. (Integrated) Computer Science and Engineering with Specialization in Business Analytics programme, and is a bonafide record carried out under my guidance. The project fulfills the requirements as per the regulations of this University and in my opinion meets the necessary standards for submission. The contents of this report have not been submitted and will not be submitted either in part or in full, for the award of any other degree or diploma and the same is certified.')

    for _ in range(2):
        doc.add_paragraph()

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, spacing='single', space_after=2)
    _run(p, 'Signature of the Guide:  _____________________________', size=12)

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, spacing='single', space_after=2)
    _run(p, 'Name: Dr. T. S. Pradeep Kumar', size=12)

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, spacing='single', space_after=2)
    _run(p, 'Date:', size=12)

    for _ in range(2):
        doc.add_paragraph()

    # Two examiner signatures side by side using a 2-col table
    t = doc.add_table(rows=4, cols=2)
    t.style = 'Table Grid'
    rows_data = [
        ['Signature of the Examiner 1:', 'Signature of the Examiner 2:'],
        ['Name: ________________________________', 'Name: ________________________________'],
        ['Date: ________________________________', 'Date: ________________________________'],
        ['', ''],
    ]
    for ri, row in enumerate(rows_data):
        for ci, val in enumerate(row):
            t.rows[ri].cells[ci].text = val
            for pr in t.rows[ri].cells[ci].paragraphs:
                for rn in pr.runs:
                    rn.font.size = Pt(11); rn.font.name = FONT

    doc.add_paragraph()
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=2)
    _run(p, 'Approved by the Head of Department', size=12, bold=True)

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=2)
    _run(p, 'School of Computer Science and Engineering', size=12)

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=0)
    _run(p, 'Vellore Institute of Technology, Chennai', size=12)

    doc.add_page_break()

# ─────────────────────────────────────────────────────────────────────────────
#  5. ABSTRACT  (front matter, roman numeral i)
# ─────────────────────────────────────────────────────────────────────────────

def abstract_page(doc):
    doc.add_paragraph()
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=14)
    _run(p, 'ABSTRACT', size=14, bold=True, underline=True)

    body(doc, 'Large Language Models (LLMs) frequently generate fluent yet factually unfounded statements — a phenomenon known as hallucination. Existing detection approaches generally mandate either multi-sample semantic consistency checks, which require 5–10 stochastic forward passes and introduce approximately 142.3 ms/token overhead, or isolated single-signal white-box metrics that fail to capture heterogeneous hallucination modes. This project proposes TRUEGUARD, an inline, multi-signal framework that monitors autoregressive generation in a single forward pass without disrupting standard decoding.')
    body(doc, 'TRUEGUARD extracts four complementary intrinsic signals at each decoding step: Internal State Probes (ISP), Attention Anomaly Score (AAS), Entropy-Energy Monitor (EEM), and Distribution Shift Tracker (DST). These signals are dynamically standardized via online Z-score normalization and fused through a learned logistic regression layer to produce a calibrated token-level risk score R(t). When the sequence risk exceeds a calibrated safety threshold (tau = 0.50), TRUEGUARD triggers an active closed-loop mitigation pipeline incorporating targeted Retrieval-Augmented Grounding and calibrated abstention.')
    body(doc, 'Evaluated across five benchmark distributions — TruthfulQA, HaluEval-QA, HaluEval-Summ, HaluEval-Dial, and HELM — TRUEGUARD achieves an average AUROC of 0.8821 ± 0.0170 while imposing merely 12.4 ± 0.5 ms/token latency overhead, representing an 11.5× speedup over Semantic Entropy. In human-annotated mitigation evaluations (n = 300, Cohen\'s kappa = 0.82), TRUEGUARD achieves a 63.8% relative reduction in hallucination occurrence while maintaining an 88.0% query answer coverage.')

    doc.add_paragraph()
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, spacing='single', space_after=4)
    _run(p, 'Keywords: ', size=12, bold=True)
    p.runs[-1]  # existing run
    _run(p, 'Large Language Models, Hallucination Detection, Trustworthy AI, Real-Time Inference, Uncertainty Quantification, Active Mitigation, Explainable AI.', size=12, italic=True)

    doc.add_page_break()

# ─────────────────────────────────────────────────────────────────────────────
#  6. ACKNOWLEDGEMENT  (roman numeral ii)
# ─────────────────────────────────────────────────────────────────────────────

def acknowledgement_page(doc):
    doc.add_paragraph()
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=14)
    _run(p, 'ACKNOWLEDGEMENT', size=14, bold=True, underline=True)

    body(doc, 'It is my pleasure to express with deep sense of gratitude to Dr. T. S. Pradeep Kumar, Associate Professor, School of Computer Science and Engineering, Vellore Institute of Technology, Chennai, for his constant guidance, continual encouragement, and understanding throughout the course of this project. His expertise in Artificial Intelligence and Natural Language Processing significantly shaped the technical direction and research rigor of this work.')
    body(doc, 'It is with gratitude that I would like to extend my thanks to the visionary leader Dr. G. Viswanathan, our Honourable Chancellor, Mr. Sankar Viswanathan, Dr. Sekar Viswanathan, Dr. G. V. Selvam, Vice Presidents, Dr. Sandhya Pentareddy, Executive Director, Ms. Kadhambari S. Viswanathan, Assistant Vice-President, Dr. V. S. Kanchana Bhaaskaran, Vice-Chancellor, and Dr. T. Thyagarajan, Pro-Vice Chancellor, VIT Chennai, for providing an exceptional working environment and inspiring all of us during the tenure of the course.')
    body(doc, 'Special mention to Dr. Viswanathan V, Dean, Dr. Nithyanandam P, Dr. Suganya G, and Dr. Sweetlin Hemalatha C, Associate Deans, School of Computer Science and Engineering, Vellore Institute of Technology, Chennai, for spending their valuable time and efforts in sharing their knowledge and for helping us in every aspect.')
    body(doc, 'My sincere thanks to all the faculty and staff members at Vellore Institute of Technology, Chennai, who helped me acquire the requisite knowledge. I would like to thank my parents for their unwavering support throughout this project. It is indeed a pleasure to thank my friends and colleagues who encouraged me to take up and complete this task.')

    for _ in range(2):
        doc.add_paragraph()

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, spacing='single', space_after=2)
    _run(p, 'Place: Chennai', size=12)

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.LEFT, spacing='single', space_after=2)
    _run(p, 'Date:', size=12)

    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.RIGHT, spacing='single', space_after=0)
    _run(p, 'Yogesh Ravi M', size=12, bold=True)

    doc.add_page_break()

# ─────────────────────────────────────────────────────────────────────────────
#  7. TABLE OF CONTENTS  (roman iii)
# ─────────────────────────────────────────────────────────────────────────────

def toc_page(doc):
    doc.add_paragraph()
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=14)
    _run(p, 'CONTENTS', size=14, bold=True)
    toc_field(doc)
    doc.add_page_break()

# ─────────────────────────────────────────────────────────────────────────────
#  8. LIST OF FIGURES  (roman iv)
# ─────────────────────────────────────────────────────────────────────────────

def lof_page(doc):
    doc.add_paragraph()
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=14)
    _run(p, 'LIST OF FIGURES', size=14, bold=True)
    entries = [
        ('4.1', 'Overall architecture of the TRUEGUARD framework', '35'),
        ('6.1', 'Hallucination detection AUROC comparison across benchmark methods', '49'),
        ('6.2', 'Ablation study — AUROC degradation when removing individual signals', '52'),
        ('6.3', 'Detection AUROC vs. latency efficiency tradeoff (log scale)', '55'),
        ('6.4', 'Mitigation waterfall — hallucination rate reduction across pipeline stages', '58'),
        ('6.5', 'Token-level risk trace during induced hallucination sequence generation', '60'),
    ]
    make_table(doc, ['Figure No.', 'Title', 'Page No.'], entries)
    doc.add_page_break()

# ─────────────────────────────────────────────────────────────────────────────
#  9. LIST OF TABLES  (roman v)
# ─────────────────────────────────────────────────────────────────────────────

def lot_page(doc):
    doc.add_paragraph()
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=14)
    _run(p, 'LIST OF TABLES', size=14, bold=True)
    entries = [
        ('2.1', 'Thematic summary of 20 surveyed works', '19'),
        ('4.1', 'TRUEGUARD signal formulations summary', '40'),
        ('6.1', 'Cross-validation AUROC across five benchmarks (5-Fold CV)', '49'),
        ('6.2', 'Ablation study — signal contribution to AUROC', '52'),
        ('6.3', 'Comparative performance and inference latency across methods', '55'),
        ('6.4', 'Mitigation pipeline impact on hallucination rate (n = 300)', '58'),
    ]
    make_table(doc, ['Table No.', 'Title', 'Page No.'], entries)
    doc.add_page_break()

# ─────────────────────────────────────────────────────────────────────────────
#  11. LIST OF SYMBOLS, ABBREVIATIONS AND NOMENCLATURE
# ─────────────────────────────────────────────────────────────────────────────

def abbreviations_page(doc):
    doc.add_paragraph()
    p = new_para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, spacing='single', space_after=14)
    _run(p, 'LIST OF SYMBOLS, ABBREVIATIONS AND NOMENCLATURE', size=14, bold=True)
    entries = [
        ('LLM', 'Large Language Model'),
        ('AUROC', 'Area Under the Receiver Operating Characteristic Curve'),
        ('AUPRC', 'Area Under the Precision-Recall Curve'),
        ('ISP', 'Internal State Probe'),
        ('AAS', 'Attention Anomaly Score'),
        ('EEM', 'Entropy-Energy Monitor'),
        ('DST', 'Distribution Shift Tracker'),
        ('RAG', 'Retrieval-Augmented Generation'),
        ('SE', 'Semantic Entropy'),
        ('SEP', 'Semantic Entropy Probe'),
        ('UQ', 'Uncertainty Quantification'),
        ('XAI', 'Explainable Artificial Intelligence'),
        ('NLP', 'Natural Language Processing'),
        ('NER', 'Named Entity Recognition'),
        ('HELM', 'Holistic Evaluation of Language Models'),
        ('CV', 'Cross-Validation'),
        ('VIT', 'Vellore Institute of Technology'),
        ('SCOPE', 'School of Computer Science and Engineering'),
        ('R(t)', 'Token-level hallucination risk score at step t'),
        ('tau', 'Decision threshold for mitigation trigger (default 0.50)'),
        ('kappa', 'Cohen\'s kappa — inter-rater agreement coefficient'),
        ('h_t^L', 'Hidden state at generation step t, layer L'),
        ('A_t^L', 'Attention matrix at generation step t, layer L'),
        ('z_t', 'Output logit vector at generation step t'),
    ]
    make_table(doc, ['Symbol / Abbreviation', 'Full Form / Definition'], entries)
    doc.add_page_break()

# ─────────────────────────────────────────────────────────────────────────────
#  CHAPTER 1 — INTRODUCTION
# ─────────────────────────────────────────────────────────────────────────────

def chapter1(doc):
    chapter_heading(doc, 'CHAPTER 1\nINTRODUCTION')

    section_heading(doc, '1.1 Introduction')
    body(doc, 'Large Language Models (LLMs) such as GPT-4, LLaMA, and Mistral have demonstrated remarkable empirical capabilities in language generation, reasoning, and synthesis. Trained on internet-scale corpora using the autoregressive Transformer architecture, these models have achieved state-of-the-art performance across diverse benchmarks encompassing question answering, document summarization, machine translation, code generation, and open-domain dialogue. Their apparent fluency and breadth of knowledge have made them attractive candidates for deployment in high-stakes professional environments, including healthcare information retrieval, legal document analysis, and automated financial advisory systems.')
    body(doc, 'Despite their widespread adoption, the deployment of LLMs in safety-critical domains remains severely constrained by a fundamental and well-documented failure mode: hallucination. Hallucinations occur when an LLM produces outputs that appear syntactically coherent and contextually plausible but are factually false, unfaithful to the prompt context, or logically contradictory. Unlike traditional software failures, which produce obvious crashes or error codes, LLM hallucinations are insidious — they are smooth, confident, and stylistically indistinguishable from accurate responses. A hallucinating LLM can cite non-existent research papers, fabricate medical dosing guidelines, misquote legal statutes, or invent historical events, all with the same linguistic authority as a factually correct response.')

    section_heading(doc, '1.2 Overview of Hallucination in LLMs')
    body(doc, 'The phenomenon of hallucination in autoregressive LLMs stems from the model\'s training objective: next-token prediction on human-generated text. This objective creates a model that is optimized for linguistic plausibility rather than factual accuracy. When a model encounters a query that lies at the boundary of its training data distribution — or requires compositional reasoning that exceeds its emergent capabilities — it continues to generate plausible-sounding text by extrapolating from statistical patterns rather than grounding its response in verified factual knowledge.')
    body(doc, 'Research has systematically classified hallucinations along two major axes. Intrinsic hallucinations directly contradict information present in the user\'s prompt context, for example, misstating an entity attribute that was explicitly provided. Extrinsic hallucinations introduce assertions that are absent from both the prompt context and ground-truth world knowledge — fabricated facts that cannot be verified from any available source. These two hallucination subtypes are particularly important because they respond to different detection signals: attention-based monitoring is most sensitive to intrinsic contradictions, while entropy-based uncertainty quantification is most effective for detecting extrinsic fabrications.')
    body(doc, 'The real-world consequences of undetected hallucinations are severe. In a medical context, a hallucinated drug interaction warning could lead to patient harm or clinical negligence. In a legal context, fabricated case citations — a documented phenomenon termed "hallucinated legal citations" — could undermine judicial proceedings. In financial advisory, hallucinated earnings projections could cause material investment losses. The field of AI safety has increasingly recognized hallucination as one of the most critical unsolved challenges in the practical deployment of generative AI systems.')

    section_heading(doc, '1.3 Challenges Present in Existing Approaches')
    body(doc, 'Prior research in hallucination detection has largely pursued two contrasting design philosophies, each with fundamental limitations:')
    body(doc, 'Black-Box Multi-Sample Consistency Checks: Methods such as SelfCheckGPT and Semantic Entropy sample multiple stochastic completions per prompt and evaluate their semantic variance. While these methods achieve reliable detection accuracy, generating 5–10 stochastic responses per query consumes significant memory bandwidth and compute time, incurring approximately 142.3 ms/token overhead. This makes them entirely impractical for low-latency streaming applications that require sub-50 ms response times.', bold=False)
    body(doc, 'Single-Signal White-Box Probes: To bypass multi-pass latency, recent works monitor internal model activations in a single forward pass. Representative examples include internal representation probes (MIND, MHAD), attention pattern tracking, semantic energy logits analysis, and distribution shift trackers (HaluShift). However, individual internal signals capture only specific facets of uncertainty. Attention dispersion effectively flags intrinsic contradictions but often misses extrinsic fabrications, whereas predictive output entropy exhibits the inverse behavior. No existing single-pass method achieves coverage across both hallucination subtypes.')
    body(doc, 'Furthermore, a persistent disconnect exists between detection engines and downstream intervention: most systems operate as post-hoc diagnostic monitors rather than active mitigation controllers. Detection of a hallucinated response after complete generation provides no mechanism for correction.')

    section_heading(doc, '1.4 Project Statement')
    body(doc, 'To resolve these limitations, this project introduces TRUEGUARD — Trustworthy, Unified, Real-time, Explainable Guard — a lightweight, production-deployable framework that unifies multi-signal intrinsic uncertainty tracking, learned signal fusion, token-level explainability, and active closed-loop mitigation within a single transformer forward pass. TRUEGUARD concurrently extracts four orthogonal intrinsic signals directly from the model\'s internal tensor graph at each autoregressive step, standardizes them via online Z-score normalization, fuses them through a learned logistic regression layer to produce a calibrated token-level risk score R(t), and triggers a two-tier active mitigation response when R(t) exceeds a decision threshold tau = 0.50.')

    section_heading(doc, '1.5 Objectives')
    numbered_item(doc, 'To develop a multi-signal hallucination detection system fusing Internal State Probes (ISP), Attention Anomaly Score (AAS), Entropy-Energy Monitor (EEM), and Distribution Shift Tracker (DST) within a single transformer forward pass.')
    numbered_item(doc, 'To implement online Welford Z-score normalization for domain-agnostic signal standardization, ensuring calibrated detection across heterogeneous query distributions.')
    numbered_item(doc, 'To train and evaluate a learned logistic regression fusion layer that optimally combines the four normalized signals into a calibrated token-level risk score with < 0.1 ms overhead.')
    numbered_item(doc, 'To design and evaluate a two-tier active closed-loop mitigation pipeline using Retrieval-Augmented Grounding (Tier 1) and Calibrated Abstention (Tier 2).')
    numbered_item(doc, 'To benchmark TRUEGUARD across five hallucination detection benchmarks using 5-fold cross-validation with statistical reporting of AUROC, AUPRC, F1 Score, Precision, and Recall.')
    numbered_item(doc, 'To evaluate mitigation effectiveness through a double-blind human annotation study (n = 300, two domain experts) measuring relative hallucination reduction and answer coverage.')

    section_heading(doc, '1.6 Scope of the Project')
    body(doc, 'The scope of this project is confined to software-based hallucination detection and mitigation within open-source, white-box causal language models. The framework is validated on three model families: LLaMA-2-7B-Chat, Mistral-7B-Instruct-v0.2, and TinyLlama-1.1B-Chat. All evaluation benchmarks (TruthfulQA, HaluEval, HELM) are publicly available English-language datasets. The project does not extend to proprietary black-box API models, multimodal models, or non-English language settings in the current scope. Complete reproducible code, Google Colab notebooks, and pre-computed metrics are provided at https://github.com/yogeshravi19/trueguard.')
    doc.add_page_break()

# ─────────────────────────────────────────────────────────────────────────────
#  CHAPTER 2 — LITERATURE REVIEW
# ─────────────────────────────────────────────────────────────────────────────

def chapter2(doc):
    chapter_heading(doc, 'CHAPTER 2\nLITERATURE REVIEW')

    section_heading(doc, '2.1 Introduction')
    body(doc, 'This chapter presents a systematic review of 20 foundational and recent works that directly motivated the design decisions of the TRUEGUARD framework. The literature is organized into six thematic clusters: hallucination taxonomy and benchmarking; white-box internal state probing; entropy and uncertainty quantification; attention-based detection; distribution shift analysis; and active mitigation strategies. Each paper is reviewed with particular attention to its primary signal, experimental scope, and key limitations that TRUEGUARD addresses.')

    section_heading(doc, '2.2 Hallucination Taxonomy, Benchmarking, and Trust')
    subsection_heading(doc, '2.2.1 TrustLLM: Trustworthiness in Large Language Models (Huang et al., 2024)')
    body(doc, 'Huang et al. proposed TrustLLM, a unified framework for studying LLM trustworthiness across eight key dimensions: truthfulness, safety, fairness, robustness, privacy, machine ethics, transparency, and accountability. The paper introduced a comprehensive benchmark encompassing over 30 datasets evaluated across 16+ mainstream LLMs. The study revealed that trustworthiness and functional capability are positively correlated, that proprietary models generally outperform open-source models in trustworthiness, and that excessive safety measures can compromise model utility. This work forms the conceptual foundation for TRUEGUARD by establishing that hallucination is part of a broader trustworthiness challenge that demands unified, principled solutions.')
    body(doc, 'Limitation: TrustLLM provides evaluation metrics but does not offer a real-time detection or mitigation mechanism, leaving the implementation gap that TRUEGUARD fills.')

    subsection_heading(doc, '2.2.2 LLM Hallucination: A Comprehensive Survey (Alansari & Luqman, 2024)')
    body(doc, 'Alansari and Luqman presented a comprehensive survey reviewing hallucination research across the entire LLM lifecycle, introducing a taxonomy of hallucination types and root causes spanning data collection biases, architectural limitations, and inference-time stochasticity. The survey identified open challenges including computational efficiency of detection, domain transfer robustness, and calibration quality of detection scores. TRUEGUARD directly addresses the computational efficiency and domain transfer challenges identified in this survey through its single-pass multi-signal architecture and online normalization.')

    subsection_heading(doc, '2.2.3 Quantifying Hallucination in Faithfulness Evaluation (Jing et al., Expedia Group)')
    body(doc, 'Jing et al. investigated automated faithfulness evaluation in guided NLG using rubric templates and LLM-as-judge scoring. Results on four travel-domain industry datasets showed that GPT-4 provides accurate faithfulness judgments and that fine-tuning NLI models on synthetic hallucinated data improves detection. This work informed TRUEGUARD\'s mitigation evaluation methodology, particularly the design of the double-blind human annotation protocol with structured faithfulness scoring rubrics.')

    subsection_heading(doc, '2.2.4 Human Trust in Language Model Responses (Sharma et al., MIT Lincoln Laboratory)')
    body(doc, 'Sharma et al. demonstrated through human studies that adding explanations to LLM responses significantly increases user trust in comparative evaluation contexts, but this trust gain disappears when responses are shown in isolation. This finding directly motivated TRUEGUARD\'s design decision to provide explicit, human-readable token-level risk annotations rather than opaque binary hallucination flags, ensuring that trust-relevant information is presented in contexts where comparative evaluation is possible.')

    section_heading(doc, '2.3 White-Box Internal State Probing Methods')
    subsection_heading(doc, '2.3.1 MIND: Unsupervised Real-Time Hallucination Detection (Su et al., Tsinghua University, 2024)')
    body(doc, 'Su et al. introduced MIND, an unsupervised training framework that leverages the internal hidden states of LLMs for real-time hallucination detection without requiring manual annotations. The key insight is that hallucination-related information leaves distinct footprints in intermediate representations. MIND also presented the HELM benchmark for multi-LLM hallucination evaluation. TRUEGUARD\'s Internal State Probe (ISP) signal is directly inspired by MIND, extending it to multi-layer averaging for improved generalization. Limitation: MIND is a single-signal system that does not capture attentional or temporal uncertainty dimensions.')

    subsection_heading(doc, '2.3.2 PRISM: Prompt-Guided Internal States (Zhang et al., Nankai University)')
    body(doc, 'Zhang et al. proposed PRISM, which uses carefully designed prompts to guide structural changes in LLMs\' internal states related to text truthfulness, enhancing cross-domain hallucination detection. The cross-domain generalization challenge identified by PRISM informed TRUEGUARD\'s use of online Z-score normalization — a domain-agnostic standardization technique — to ensure calibrated signal fusion across diverse query domains. Limitation: PRISM requires domain-specific prompt engineering, introducing deployment overhead.')

    subsection_heading(doc, '2.3.3 MHAD: Deep Internal Representation Analysis (Zhang et al., Beijing Institute of Technology, 2025)')
    body(doc, 'Zhang et al. proposed MHAD using linear probing to identify hallucination-aware neurons and layers within LLMs, establishing that truthfulness-related information is concentrated in specific intermediate transformer layers. This finding directly shaped TRUEGUARD\'s ISP signal design, which probes layers at relative depth percentiles {0.45, 0.60, 0.75, 0.90}. Limitation: MHAD monitors only hidden states and does not address the temporal trajectory of hallucinated generation.')

    subsection_heading(doc, '2.3.4 LLM-Check: Single-Pass Hidden State Classification (Sriramanan et al., University of Maryland, 2024)')
    body(doc, 'Sriramanan et al. demonstrated that a single-pass hidden state classifier combining logit and hidden state features can achieve up to 45× and 450× speedup over sampling-based baselines while improving detection accuracy. This work validated the architectural philosophy of TRUEGUARD and serves as a key single-signal baseline in experimental comparisons.')

    section_heading(doc, '2.4 Entropy and Uncertainty Quantification')
    subsection_heading(doc, '2.4.1 Semantic Energy: Beyond Standard Entropy (Ma et al., Tianjin University, 2025)')
    body(doc, 'Ma et al. introduced Semantic Energy, combining semantic clustering with a Boltzmann-inspired energy distribution to capture uncertainty in cases where standard entropy fails — when a softmax distribution is dominated by a single high-probability token despite underlying factual uncertainty. TRUEGUARD\'s EEM signal synthesizes this insight by combining Shannon entropy with Renyi-2 energy, providing complementary measures of distribution tail uncertainty and mode sharpness.')

    subsection_heading(doc, '2.4.2 UQ for Hallucination Detection — Survey (Kang et al., University of Southern California)')
    body(doc, 'Kang et al. provided a comprehensive survey of uncertainty quantification for LLM hallucination, reviewing confidence-based, sampling-based, and ensemble-based methods and identifying open challenges including computational efficiency and calibration quality. This survey provided TRUEGUARD with a principled framework for understanding the complementarity of its four signals across epistemic, aleatoric, contextual, and temporal uncertainty dimensions.')

    subsection_heading(doc, '2.4.3 Semantic Entropy Probes (Kossen et al., University of Oxford, 2024)')
    body(doc, 'Kossen et al. proposed SEPs, which approximate semantic entropy from single-generation hidden states, eliminating the 5–10× computation cost of traditional semantic entropy. This work validated the feasibility of deriving rich uncertainty information from a single forward pass, directly supporting TRUEGUARD\'s architectural decision and serving as the primary latency baseline (142.3 ms/token) in computational efficiency experiments.')

    subsection_heading(doc, '2.4.4 Entropy Production Rate for Black-Box Detection (Moslonka et al., 2025)')
    body(doc, 'Moslonka et al. introduced EPR, derived from token log-probabilities during non-greedy decoding, for black-box hallucination detection. This work extended TRUEGUARD\'s theoretical understanding of temporal entropy dynamics during hallucinated generation, complementing the DST signal conceptually.')

    section_heading(doc, '2.5 Attention-Based Detection Methods')
    subsection_heading(doc, '2.5.1 Map of Misbelief: Attention-Based Hallucination Tracing (Hajji et al., Universite Paris-Saclay, 2025)')
    body(doc, 'Hajji et al. demonstrated that attention-based uncertainty quantification can differentiate intrinsic from extrinsic hallucinations, finding that sampling-based methods (Semantic Entropy) excel at extrinsic detection while attention-based aggregation is better suited for intrinsic hallucinations. This complementarity result provides the primary empirical justification for TRUEGUARD\'s multi-signal fusion: the AAS (attention) and EEM (entropy) signals target orthogonal hallucination subtypes, ensuring comprehensive coverage.')

    subsection_heading(doc, '2.5.2 RAUQ: Uncertainty-Aware Attention Heads (Anonymous, ICLR 2026 submission)')
    body(doc, 'RAUQ demonstrated that when incorrect information is generated, specific "uncertainty-aware" attention heads reduce their focus on preceding tokens. The method automatically identifies these heads and combines their patterns with token-level confidence measures in a single forward pass. RAUQ validated TRUEGUARD\'s AAS signal design, which monitors attention entropy specifically in the final layer quartile where uncertainty-sensitive attention heads are most concentrated.')

    section_heading(doc, '2.6 Distribution Shift and Temporal Drift Detection')
    subsection_heading(doc, '2.6.1 HALLUSHIFT: Distribution Shifts in LLM Hallucination (Dasgupta et al., 2025)')
    body(doc, 'Dasgupta et al. hypothesized and demonstrated that hallucinations manifest as progressive geometric displacement in hidden activation space — the model\'s internal representation gradually drifts away from the factual trajectory. Their cosine distance metric between successive hidden state vectors provided a reliable temporal signal for hallucination onset. TRUEGUARD\'s DST signal is directly grounded in HALLUSHIFT, adapted to compute cumulative average cosine divergence for more stable sequential tracking.')

    subsection_heading(doc, '2.6.2 HALLUSHIFT++: Multimodal Extension (Nath et al.)')
    body(doc, 'Nath et al. extended HALLUSHIFT to multimodal LLMs, demonstrating that similar distribution shift patterns manifest in vision-language models during hallucinated generation. This validated the generalizability of the distribution shift detection paradigm across architectures and modalities, supporting the long-term applicability of TRUEGUARD\'s DST signal.')

    section_heading(doc, '2.7 Active Mitigation Strategies')
    subsection_heading(doc, '2.7.1 Chain-of-Verification (Dhuliawala et al., 2024)')
    body(doc, 'Dhuliawala et al. demonstrated that generating auxiliary verification queries to challenge potentially hallucinated claims meaningfully reduces hallucination rates, establishing the principle of active verification-based mitigation. TRUEGUARD\'s Tier-1 RAG mitigation is inspired by this principle but avoids multi-pass overhead by triggering retrieval conditionally based on token-level risk scores rather than universally.')

    subsection_heading(doc, '2.7.2 Retrieval-Augmented Generation (Lewis et al., NeurIPS 2020)')
    body(doc, 'Lewis et al. introduced RAG, demonstrating significant factual accuracy improvements by conditioning generation on retrieved documents. TRUEGUARD\'s Tier-1 mitigation implements a targeted variant of RAG that activates selectively when R(t) > tau, preserving computational efficiency while maximizing mitigation effectiveness.')

    subsection_heading(doc, '2.7.3 Behaviorally Calibrated Reinforcement Learning (Wu et al., 2025)')
    body(doc, 'Wu et al. demonstrated that training LLMs to abstain when uncertain via proper scoring rules can align model confidence with actual accuracy. This work motivated TRUEGUARD\'s Tier-2 calibrated abstention mechanism, implemented as an epistemically honest disclaimer triggered when Tier-1 retrieval fails to provide sufficient factual grounding.')

    section_heading(doc, '2.8 Summary of Literature Survey')
    body(doc, 'Table 2.1 provides a thematic summary of all 20 surveyed works, mapping each paper\'s primary signal, experimental scope, and key limitation to the corresponding TRUEGUARD design decision.')
    rows = [
        ('MIND (Su et al., 2024)', 'Internal State', 'HELM, HaluEval', 'Single signal; no fusion'),
        ('PRISM (Zhang et al.)', 'Internal State', 'Multi-domain QA', 'Prompt engineering overhead'),
        ('TrustLLM (Huang et al., 2024)', 'Benchmark', '30+ datasets', 'No real-time detection'),
        ('Semantic Energy (Ma et al., 2025)', 'Logit UQ', 'TruthfulQA, HaluEval', 'Single signal'),
        ('MHAD (Zhang et al., 2025)', 'Internal State', 'QA benchmarks', 'No temporal signal'),
        ('Entropy Spike + RL (Ext. Abs.)', 'RL Calibration', 'GSM8K, MATH', 'RL training overhead'),
        ('UQ Survey (Kang et al.)', 'Survey', 'Comprehensive', 'No implementation'),
        ('XAI Survey (Herrera)', 'Survey/XAI', 'Healthcare, Law', 'No implementation'),
        ('Map of Misbelief (Hajji, 2025)', 'Attention', 'HaluEval, XSum', 'Single signal'),
        ('Faithfulness Eval (Jing et al.)', 'Faithfulness', 'Travel industry', 'Domain-specific'),
        ('RAUQ (Anonymous, 2026)', 'Attention', '12 tasks, 4 LLMs', 'No mitigation'),
        ('LLM-Check (Sriramanan, 2024)', 'Internal State', 'TruthfulQA, NQ', 'White-box only'),
        ('HALLUSHIFT (Dasgupta, 2025)', 'Dist. Shift', 'HaluEval', 'Single signal'),
        ('SEP (Kossen et al., 2024)', 'Hidden State UQ', 'TriviaQA, NQ', 'Single signal proxy'),
        ('Behav. Calib. RL (Wu, 2025)', 'RL/Abstention', 'GSM8K, ARC', 'Requires fine-tuning'),
        ('HALLUSHIFT++ (Nath et al.)', 'Dist. Shift/Multi', 'POPE, MMBench', 'Multimodal focus'),
        ('EPR (Moslonka, 2025)', 'UQ/Black-box', 'HaluEval, NQ', 'Black-box only'),
        ('LLM Hallucination Survey (Alansari)', 'Survey', 'Comprehensive', 'No implementation'),
        ('Human Trust (Sharma et al.)', 'Human Study', 'LaMP, News', 'Human studies only'),
        ('ExpandR (Yao et al., 2025)', 'Retrieval/RAG', 'MSMARCO, NQ', 'Retrieval focus'),
    ]
    make_table(doc, ['Paper', 'Primary Signal', 'Dataset(s)', 'Key Limitation'], rows)
    doc.add_page_break()

# ─────────────────────────────────────────────────────────────────────────────
#  CHAPTER 3 — RESEARCH GAP & OBJECTIVES
# ─────────────────────────────────────────────────────────────────────────────

def chapter3(doc):
    chapter_heading(doc, 'CHAPTER 3\nRESEARCH GAP AND PROBLEM FORMULATION')

    section_heading(doc, '3.1 Identified Research Gaps')
    body(doc, 'The systematic review presented in Chapter 2 reveals five critical gaps in the existing hallucination detection and mitigation literature:')

    subsection_heading(doc, '3.1.1 Signal Isolation')
    body(doc, 'Every existing single-pass detection method monitors exactly one category of intrinsic signal. As demonstrated by Hajji et al., these signal categories exhibit complementary blind spots — attention-based methods miss extrinsic fabrications that entropy-based methods detect, and vice versa. No existing system integrates multiple orthogonal signals into a unified, learned detection architecture, resulting in coverage gaps that allow specific hallucination categories to evade any single detector.')

    subsection_heading(doc, '3.1.2 Computational Overhead vs. Coverage Trade-off')
    body(doc, 'Multi-sample methods achieve reliable detection accuracy but incur approximately 142.3 ms/token latency — 5–10 redundant forward passes — rendering them impractical for streaming applications requiring sub-50 ms response times. Single-pass methods address the latency constraint but sacrifice detection coverage. No existing system simultaneously achieves single-pass computational efficiency and multi-signal coverage.')

    subsection_heading(doc, '3.1.3 Detection-Mitigation Disconnect')
    body(doc, 'All existing hallucination detection systems (except Chain-of-Verification, which introduces its own multi-pass overhead) operate as post-hoc diagnostic monitors. They analyze a completed response and flag it as potentially hallucinated but provide no mechanism to intercept generation mid-sentence and actively correct or prevent the hallucinated output. A closed-loop detection-mitigation architecture remains an open problem in the literature.')

    subsection_heading(doc, '3.1.4 Explainability Deficit')
    body(doc, 'Detection systems produce binary hallucination labels or scalar aggregate confidence scores that provide no interpretable explanation for why a specific claim is flagged as unreliable. As established by Sharma et al. and Herrera, explanation faithfulness and specificity are critical for user trust calibration. A token-level, signal-attributed explainability layer is absent from all existing single-pass detection frameworks.')

    subsection_heading(doc, '3.1.5 Calibration Drift Under Domain Shift')
    body(doc, 'Most existing detectors use fixed decision thresholds calibrated on homogeneous benchmark distributions. When deployed on new query types or domain distributions, raw signal magnitudes shift, causing inflated false positive or false negative rates. Online normalization of signals to a stable distribution is rarely considered in the detection literature.')

    section_heading(doc, '3.2 Formal Problem Formulation')
    body(doc, 'Let an autoregressive language model M parameterized by theta generate a sequence Y = (y_1, ..., y_T) given prompt C = (c_1, ..., c_M). At generation step t, the model produces logit vector z_t over vocabulary V, hidden states {h_t^L} across all transformer layers, and attention matrices {A_t^L}.')
    body(doc, 'The TRUEGUARD problem is defined as learning an inline mapping f: (z_t, {h_t^L}, {A_t^L}) -> R(t) in [0,1] such that R(t) accurately reflects the probability that token y_t constitutes a factual hallucination, computed with latency overhead much less than the model\'s base forward pass. Furthermore, when R(t) exceeds threshold tau, TRUEGUARD must trigger an active mitigation response M(t) that reduces the expected hallucination rate below that of the unguarded baseline model while preserving maximum answer coverage.')
    doc.add_page_break()

# ─────────────────────────────────────────────────────────────────────────────
#  CHAPTER 4 — FRAMEWORK DESIGN
# ─────────────────────────────────────────────────────────────────────────────

def chapter4(doc):
    chapter_heading(doc, 'CHAPTER 4\nTRUEGUARD FRAMEWORK DESIGN AND ARCHITECTURE')

    section_heading(doc, '4.1 Overall Architecture')
    body(doc, 'TRUEGUARD operates as an inline tensor monitor that intercepts the model\'s internal activations at each autoregressive generation step without modifying the model\'s weights, architecture, or decoding procedure. At each step t, TRUEGUARD extracts a 4-dimensional feature vector X_t = [ISP_t, AAS_t, EEM_t, DST_t]^T directly from the ongoing forward execution graph.')
    embed_figure(doc, 'figures/fig1_architecture.png')
    fig_caption(doc, 'Figure 4.1: Overall architecture of the TRUEGUARD framework. Four complementary intrinsic signals (ISP, AAS, EEM, DST) are extracted concurrently in a single forward pass, standardized online, and fused via logistic regression to trigger active closed-loop mitigation.')

    body(doc, 'The framework consists of four sequential processing stages: (1) parallel signal extraction from the model\'s internal tensors, (2) online Z-score normalization of the extracted signals, (3) learned logistic regression fusion into a scalar risk score R(t), and (4) threshold-triggered closed-loop mitigation. Each stage is computationally minimal, contributing negligible overhead relative to the base model\'s forward pass time.')

    rows = [
        ('ISP', 'sigma(w_L^T h_t^L + b_L) averaged over layers {0.45, 0.60, 0.75, 0.90}', '0.49 ms'),
        ('AAS', 'Normalized Shannon entropy of attention over prompt context (final quartile)', '1.26 ms'),
        ('EEM', '0.6 * H_norm(t) + 0.4 * E_norm(t)  (Shannon + Renyi-2)', '0.47 ms'),
        ('DST', 'Cumulative average cosine distance between successive hidden centroids', '0.26 ms'),
        ('Normalization', 'Online Welford Z-score: (X_t - mu_t) / (sigma_t + eps)', '< 0.01 ms'),
        ('Fusion', 'R(t) = sigma(W^T X_hat_t + b)  — logistic regression', '< 0.10 ms'),
    ]
    make_table(doc, ['Component', 'Formulation', 'Overhead'], rows)
    tbl_caption(doc, 'Table 4.1: TRUEGUARD signal formulations and per-component inference overhead on NVIDIA T4 GPU.')

    section_heading(doc, '4.2 Signal 1: Internal State Probes (ISP)')
    body(doc, 'Following MHAD (Zhang et al., 2025) and MIND (Su et al., 2024), truthfulness-related information is concentrated in middle-to-late transformer layers. For a 32-layer model, probe layers L_ISP = {15, 20, 25, 30} are selected at relative depth percentiles {0.45, 0.60, 0.75, 0.90}. For each probe layer L, a linear classification probe projects the hidden state to a scalar hallucination probability via the sigmoid function: ISP_t^L = sigma(w_L^T h_t^L + b_L). The aggregated ISP score is the arithmetic mean: ISP_t = (1/|L_ISP|) * sum_{L} ISP_t^L. Probes are trained using binary cross-entropy loss with L2 regularization (lambda = 1e-4).')
    body(doc, 'The averaging across multiple layers provides robustness against layer-specific noise. The probes are shallow (single linear layer with less than 4096 parameters per probe) and require 0.49 ms to evaluate at each generation step, contributing minimal overhead.')

    section_heading(doc, '4.3 Signal 2: Attention Anomaly Score (AAS)')
    body(doc, 'When generating factually accurate tokens, attention heads attend predominantly to relevant context tokens. During hallucinated generation, attention weights disperse across irrelevant tokens, reflecting loss of contextual grounding. TRUEGUARD quantifies this dispersal using normalized Shannon entropy of attention matrices in the final layer quartile L_AAS = {25, ..., 31}.')
    body(doc, 'For head h at layer L, the normalized attention entropy from position t to prior positions is: H_norm^{h,L}(t) = [-sum_{i=1}^t A_{t,i}^{h,L} * log(A_{t,i}^{h,L} + eps)] / log(t). The composite AAS averages across all heads and monitored layers. Values approaching 1 denote dispersed attention indicative of ungrounded generation. Normalization by log(t) ensures comparability across different sequence lengths.')

    section_heading(doc, '4.4 Signal 3: Entropy-Energy Monitor (EEM)')
    body(doc, 'Standard Shannon entropy measures overall predictive dispersion but can underestimate uncertainty when a softmax is dominated by a single high-probability token. TRUEGUARD augments it with Renyi-2 entropy, which specifically quantifies probability concentration. The normalized Shannon entropy and Renyi-2 energy are computed from softmax distribution p_t = softmax(z_t): H_norm(t) = [-sum_k p_{t,k} * log(p_{t,k} + eps)] / log(|V|); E_norm(t) = [-log(sum_k p_{t,k}^2 + eps)] / log(|V|).')
    body(doc, 'The EEM score is a convex combination: EEM_t = w_e * H_norm(t) + (1 - w_e) * E_norm(t), where w_e = 0.6, selected via grid search on validation data. This formulation provides complementary uncertainty signals that capture both distribution tail uncertainty and mode sharpness, addressing the failure modes of standard entropy alone.')

    section_heading(doc, '4.5 Signal 4: Distribution Shift Tracker (DST)')
    body(doc, 'Drawing on HALLUSHIFT (Dasgupta et al., 2025), factual hallucination manifests as progressive geometric displacement in activation space. TRUEGUARD tracks this temporal drift by computing the centroid hidden state as the average across deep layers L_DST = {20, 25, 30}: h_bar_t = (1/|L_DST|) * sum_{L} h_t^L. The instantaneous distribution shift is the normalized cosine distance: d_t = [1 - cos(h_bar_t, h_bar_{t-1})] / 2, with d_1 = 0. The running DST score accumulates: DST_t = (1/(t-1)) * sum_{t\'=2}^t d_{t\'}, providing a stable trajectory-level signal less sensitive to transient single-step fluctuations.')

    section_heading(doc, '4.6 Online Normalization and Fusion')
    body(doc, 'Because the four signals operate across distinct numerical scales, TRUEGUARD applies an online Welford Z-score scaler: X_hat_t = (X_t - mu_t) / (sigma_t + eps_s), where mu_t and sigma_t denote running empirical mean and standard deviation vectors updated at each step. This domain-agnostic normalization ensures that signal scales remain consistent even as domain characteristics shift across queries.')
    body(doc, 'The standardized vector X_hat_t is mapped to risk score R(t) via logistic regression: R(t) = sigma(W^T X_hat_t + b), where W and b are optimized using binary cross-entropy on validation data. The full-sequence risk incorporates a frequency penalty: R_seq = min(1.0, max_t R(t) * [1 + gamma * (high-risk token fraction)]), where threshold tau = 0.50 and gamma = 0.20 penalizes multi-token hallucination cascades.')

    section_heading(doc, '4.7 Two-Tier Active Closed-Loop Mitigation')
    body(doc, 'When R(t) exceeds tau = 0.50, TRUEGUARD immediately halts generation mid-sentence and initiates a two-tier mitigation response.')
    subsection_heading(doc, '4.7.1 Tier 1: Targeted Retrieval-Augmented Grounding')
    body(doc, 'Key entities from the prompt context are extracted using lightweight NER to formulate a targeted retrieval query submitted to an external factual knowledge store (Wikipedia API by default, configurable to domain-specific corpora). Retrieved passages are injected into an augmented prompt and generation is restarted with factual grounding. If the regenerated sequence risk remains below tau, the grounded response is emitted.')
    subsection_heading(doc, '4.7.2 Tier 2: Calibrated Abstention')
    body(doc, 'If retrieval fails to locate high-confidence evidence, or if regenerated sequence risk remains above tau after Tier 1, TRUEGUARD executes calibrated abstention, emitting: "I do not have sufficient verified evidence to answer this query reliably without risk of factual inaccuracy." This response is logged with the triggering risk score and failed retrieval context for diagnostic transparency.')
    doc.add_page_break()

# ─────────────────────────────────────────────────────────────────────────────
#  CHAPTER 5 — EXPERIMENTAL METHODOLOGY
# ─────────────────────────────────────────────────────────────────────────────

def chapter5(doc):
    chapter_heading(doc, 'CHAPTER 5\nEXPERIMENTAL METHODOLOGY')

    section_heading(doc, '5.1 Models and Hardware Environment')
    subsection_heading(doc, '5.1.1 Primary Evaluation Models')
    body(doc, 'LLaMA-2-7B-Chat and Mistral-7B-Instruct-v0.2 serve as the primary evaluation models. Both share a 32-layer Transformer architecture with 4096-dimensional hidden states and 32 attention heads. These models were selected due to their widespread adoption in open-source deployments and their representative scale for practical production environments.')
    subsection_heading(doc, '5.1.2 Lightweight Validation Model')
    body(doc, 'TinyLlama-1.1B-Chat (22 layers, 2048 hidden dimension, 32 heads) provides a lightweight validation platform for testing cross-scale generalization of TRUEGUARD\'s signal extraction and fusion components.')
    subsection_heading(doc, '5.1.3 Hardware Configuration')
    body(doc, 'Inference experiments were conducted in both cloud environments (NVIDIA T4 GPU, 16 GB VRAM, CUDA 11.8, PyTorch 2.0) and local CPU workstations (Intel Core i7-12700K, 32 GB RAM). All latency measurements are means of 100 repeated trials with standard deviations reported. Models were loaded in bfloat16 precision on GPU.')

    section_heading(doc, '5.2 Evaluation Benchmarks')
    numbered_item(doc, 'TruthfulQA (Lin et al., 2022): 817 questions spanning 38 categories designed to induce common misconceptions. Particularly challenging because correct answers are often counterintuitive.')
    numbered_item(doc, 'HaluEval-QA (Li et al., 2023): 10,000 question-answer pairs with paired factual and hallucinated responses generated by ChatGPT. Provides balanced large-sample evaluation.')
    numbered_item(doc, 'HaluEval-Summ: Knowledge-grounded text summarization with synthetic entity fabrications injected, testing detection in abstractive summarization contexts.')
    numbered_item(doc, 'HaluEval-Dial: Dialogue completion evaluating conversational consistency, where hallucinations manifest as factual contradictions with earlier dialogue context.')
    numbered_item(doc, 'HELM (Liang et al., 2022): Open-domain knowledge retrieval and multi-step reasoning queries requiring broad factual knowledge across diverse domains.')

    section_heading(doc, '5.3 Baseline Methods')
    bullet_item(doc, 'Token Entropy (Black-Box): Predictive entropy of output softmax distribution — requires no hidden state access.')
    bullet_item(doc, 'Semantic Entropy (Kossen et al., 2024): Multi-sample clustering baseline, 5–10 stochastic completions per prompt. Primary latency benchmark.')
    bullet_item(doc, 'MIND (Su et al., 2024): Unsupervised probing of a single intermediate hidden state layer.')
    bullet_item(doc, 'LLM-Check (Sriramanan et al., 2024): Single-pass hidden state and logit classifier.')
    bullet_item(doc, 'HaluShift (Dasgupta et al., 2025): Single-signal instantaneous cosine state distance tracker.')

    section_heading(doc, '5.4 Evaluation Metrics')
    body(doc, 'All detection metrics are computed via 5-fold cross-validation with sample standard deviation and 95% confidence intervals: CI_95% = x_bar ± 1.96 * (s / sqrt(5)).')
    bullet_item(doc, 'AUROC: Primary detection metric — probability that a hallucinated token receives higher risk score than an accurate token. Threshold-independent.')
    bullet_item(doc, 'AUPRC: Supplementary metric for class-imbalanced settings where hallucinated tokens are a minority.')
    bullet_item(doc, 'F1 Score, Precision, Recall: Reported at operating threshold tau = 0.50.')
    bullet_item(doc, 'False Positive Rate (FPR): Fraction of accurate tokens incorrectly flagged, characterizing disruption to normal generation.')
    body(doc, 'Mitigation efficacy is measured by relative hallucination reduction: Reduction (%) = [(Rate_before - Rate_after) / Rate_before] x 100%, and answer coverage percentage.')
    doc.add_page_break()

# ─────────────────────────────────────────────────────────────────────────────
#  CHAPTER 6 — RESULTS
# ─────────────────────────────────────────────────────────────────────────────

def chapter6(doc):
    chapter_heading(doc, 'CHAPTER 6\nRESULTS AND EMPIRICAL ANALYSIS')

    section_heading(doc, '6.1 Overall Benchmark Performance')
    body(doc, 'Table 6.1 presents 5-fold cross-validation performance across all five benchmarks. TRUEGUARD achieves an overall average AUROC of 0.8821 ± 0.0170, consistently outperforming all baseline methods.')
    rows = [
        ('TruthfulQA',    '0.8533 ± 0.0533', '[0.8066, 0.9001]', '0.8140', '0.7186'),
        ('HaluEval-QA',   '0.8840 ± 0.0185', '[0.8678, 0.9003]', '0.8739', '0.7874'),
        ('HaluEval-Summ', '0.8797 ± 0.0440', '[0.8411, 0.9184]', '0.8459', '0.7252'),
        ('HaluEval-Dial', '0.8872 ± 0.0387', '[0.8533, 0.9212]', '0.8484', '0.7373'),
        ('HELM',          '0.9063 ± 0.0454', '[0.8665, 0.9461]', '0.8552', '0.7545'),
        ('Overall Mean',  '0.8821 ± 0.0170', '—',                '0.8475', '0.7446'),
    ]
    make_table(doc, ['Benchmark', 'AUROC', '95% CI', 'AUPRC', 'F1 Score'], rows)
    tbl_caption(doc, 'Table 6.1: Cross-Validation Detection Performance Across Five Benchmarks (5-Fold CV).')

    embed_figure(doc, 'figures/fig2_auroc_benchmark_comparison.png')
    fig_caption(doc, 'Figure 6.1: Hallucination detection AUROC comparison across baseline methods and TRUEGUARD. Multi-signal fusion consistently outperforms all single-signal and multi-pass baselines.')

    body(doc, 'On TruthfulQA, TRUEGUARD achieves 0.8533 ± 0.0533, significantly outperforming Token Entropy (0.712) and Semantic Entropy (0.776). On HELM — the most challenging benchmark due to multi-step reasoning queries — TRUEGUARD achieves its highest AUROC of 0.9063, demonstrating that multi-signal fusion provides particular advantages on complex factual reasoning tasks where single-signal detectors underperform.')

    section_heading(doc, '6.2 Ablation Study')
    body(doc, 'Table 6.2 details the AUROC degradation when each signal is systematically excluded, verifying that all four signals contribute complementary, non-redundant information.')
    rows = [
        ('Full TRUEGUARD (4 Signals)', '0.8475', '±0.0324', 'Reference'),
        ('- EEM (No Entropy/Energy)',  '0.7957', '±0.0316', '-0.0518'),
        ('- ISP (No Hidden Probes)',   '0.8093', '±0.0465', '-0.0382'),
        ('- DST (No Dist. Shift)',     '0.8320', '±0.0237', '-0.0155'),
        ('- AAS (No Attention)',       '0.8370', '±0.0395', '-0.0105'),
        ('EEM Only',                  '0.7516', '±0.0395', '-0.0959'),
        ('ISP Only',                  '0.7445', '±0.0537', '-0.1030'),
        ('DST Only',                  '0.6812', '±0.0626', '-0.1663'),
        ('AAS Only',                  '0.6317', '±0.0345', '-0.2158'),
    ]
    make_table(doc, ['Configuration', 'AUROC', 'Std', 'Delta from Full'], rows)
    tbl_caption(doc, 'Table 6.2: Ablation Study — AUROC Contribution of Each Signal.')

    embed_figure(doc, 'figures/fig3_ablation_study.png')
    fig_caption(doc, 'Figure 6.2: Ablation study — AUROC degradation when removing individual signals. EEM removal causes the sharpest drop (-0.0518), proving it is the dominant detection signal.')

    body(doc, 'Removing EEM produces the largest degradation (delta = -0.0518), confirming that predictive probability distributions provide the primary factual uncertainty signal. ISP removal degrades AUROC by -0.0382, confirming that intermediate hidden representations encode semantic truthfulness cues that logits alone cannot capture. All single-signal models operate substantially below full 4-signal fusion — EEM alone achieves 0.7516 versus 0.8475 — proving mutual complementarity.')

    section_heading(doc, '6.3 Latency and Computational Efficiency')
    rows = [
        ('Semantic Entropy', '5–10', '142.3 ± 3.8', '1.0× (Baseline)'),
        ('LLM-Check',        '1',    '31.5 ± 1.2',  '4.5×'),
        ('HaluShift',        '1',    '18.2 ± 0.6',  '7.8×'),
        ('TRUEGUARD (Ours)', '1',    '12.4 ± 0.5',  '11.5×'),
    ]
    make_table(doc, ['Method', 'Passes/Token', 'Overhead (ms/token)', 'Speedup vs SE'], rows)
    tbl_caption(doc, 'Table 6.3: Inference Latency and Computational Overhead Per Token (NVIDIA T4 GPU).')

    embed_figure(doc, 'figures/fig4_latency_efficiency_tradeoff.png')
    fig_caption(doc, 'Figure 6.3: Detection AUROC vs. latency overhead. TRUEGUARD occupies the optimal low-latency, high-accuracy quadrant, achieving 11.5x speedup over Semantic Entropy.')

    body(doc, 'TRUEGUARD executes in 12.4 ± 0.5 ms/token — an 11.5× speedup over Semantic Entropy (142.3 ms/token). Component profiling: ISP 0.49 ms, AAS 1.26 ms, EEM 0.47 ms, DST 0.26 ms, fusion < 0.10 ms. Total overhead remains well within the sub-50 ms constraint required for streaming LLM deployment.')

    section_heading(doc, '6.4 Mitigation Effectiveness')
    body(doc, 'The two-tier mitigation pipeline was evaluated via double-blind human annotation on n = 300 responses sampled evenly across TruthfulQA, HaluEval, and HELM. Two domain experts evaluated factual faithfulness independently, achieving high inter-rater agreement (Cohen\'s kappa = 0.82). Discrepancies were resolved via consensus adjudication.')
    rows = [
        ('Base LLM (No Guard)',           '31.2%', '68.8%', '100.0%'),
        ('Detection Flag Only',           '31.2%', '68.8%', '100.0%'),
        ('+ Targeted RAG (Tier 1)',        '18.4%', '79.3%', '100.0%'),
        ('+ Calibrated Abstention (T2)',   '12.7%', '84.1%', '95.0%'),
        ('Full TRUEGUARD Closed-Loop',     '11.3%', '85.6%', '88.0%'),
    ]
    make_table(doc, ['Mitigation Stage', 'Hallucination Rate', 'Accuracy', 'Coverage'], rows)
    tbl_caption(doc, 'Table 6.4: Mitigation Pipeline Impact (n=300, Cohen\'s kappa=0.82).')

    embed_figure(doc, 'figures/fig5_mitigation_waterfall.png')
    fig_caption(doc, 'Figure 6.4: Hallucination rate waterfall across mitigation stages. Full TRUEGUARD achieves 63.8% relative reduction while maintaining 88.0% answer coverage.')

    body(doc, 'Tier-1 RAG alone reduces the 31.2% baseline hallucination rate to 18.4% — a 41.0% relative reduction. Adding Tier-2 Abstention drives the final rate to 11.3%, yielding a 63.8% relative reduction: (31.2 - 11.3) / 31.2 = 63.78%. TRUEGUARD achieves this while maintaining 88.0% coverage — abstaining on only 12.0% of queries.')

    section_heading(doc, '6.5 Token-Level Risk Visualization')
    embed_figure(doc, 'figures/fig6_token_risk_heatmap.png')
    fig_caption(doc, 'Figure 6.5: Real-time token-level risk trace during induced hallucination. R(t) surges above tau=0.50 at the fabricated entity, triggering mid-sentence interception at step 6.')

    body(doc, 'During initial context processing (tokens 1–5), all signals remain low with R(t) approximately 0.11–0.21. At the fabricated entity in token step 6, EEM spikes to 0.88, AAS increases to 0.74, and the fused risk score reaches 0.83 > tau. TRUEGUARD halts generation mid-sentence, intercepting the hallucinated cascade before the fabricated assertion completes.')
    doc.add_page_break()

# ─────────────────────────────────────────────────────────────────────────────
#  CHAPTER 7 — DISCUSSION
# ─────────────────────────────────────────────────────────────────────────────

def chapter7(doc):
    chapter_heading(doc, 'CHAPTER 7\nDISCUSSION')

    section_heading(doc, '7.1 Complementarity of Detection Signals')
    body(doc, 'The ablation study confirms that hallucination in autoregressive LLMs is not a monolithic phenomenon. Each TRUEGUARD signal targets an orthogonal mathematical subspace: EEM captures output vocabulary uncertainty; ISP identifies latent truthfulness discrepancies in intermediate representations; AAS isolates attentional deanchoring from prompt context; and DST tracks progressive temporal drift from the factual activation trajectory. Because these signals target distinct subspaces, linear fusion provides robust cross-domain generalization, with each signal compensating for the blind spots of the others.')

    section_heading(doc, '7.2 Computational Efficiency Analysis')
    body(doc, 'The 11.5× speedup over Semantic Entropy is achieved primarily by eliminating the multi-pass sampling loop. Within TRUEGUARD itself, AAS computation (1.26 ms) dominates, requiring iteration over attention matrices in the final layer quartile. Potential optimizations include caching pre-computed attention entropy statistics across common query prefixes and applying sparse attention monitoring that selects only uncertainty-sensitive attention heads identified via the RAUQ methodology, potentially reducing total overhead below 8 ms/token.')

    section_heading(doc, '7.3 Mitigation Effectiveness Analysis')
    body(doc, 'The residual 11.3% hallucination rate after full closed-loop mitigation reflects cases where: (1) retrieved documents lack sufficient factual specificity for the query, (2) the hallucination is subtle enough that token-level risk scores do not exceed tau = 0.50, or (3) compositional reasoning errors occur where individual token risks remain sub-threshold despite the overall response containing a factual error. Adaptive threshold calibration based on query category and retrieval confidence is a high-priority future direction.')

    section_heading(doc, '7.4 Ethical Considerations')
    body(doc, 'Deploying active hallucination mitigation introduces epistemic trade-offs. While calibrated abstention reduces false assertions, overly conservative thresholds reduce system utility by abstracting on queries the model would have answered correctly. Users must be explicitly informed when a response was grounded via Tier-1 RAG or altered via Tier-2 Abstention to preserve appropriate trust calibration. The construction of ISP probe training data requires careful annotation protocols to avoid labeling biases that could cause disparate detection accuracy across query domains or demographic groups.')
    doc.add_page_break()

# ─────────────────────────────────────────────────────────────────────────────
#  CONCLUSION AND FUTURE WORK  (per spec: "Conclusion & Future Work" section)
# ─────────────────────────────────────────────────────────────────────────────

def conclusion_chapter(doc):
    chapter_heading(doc, 'CONCLUSION AND FUTURE WORK')

    section_heading(doc, 'Conclusion')
    body(doc, 'This project presented TRUEGUARD, a unified, lightweight, and production-deployable framework for real-time hallucination detection and active mitigation in Large Language Models. The core innovation lies in the principled integration of four complementary intrinsic uncertainty signals — Internal State Probes (ISP), Attention Anomaly Score (AAS), Entropy-Energy Monitor (EEM), and Distribution Shift Tracker (DST) — within a single transformer forward pass, eliminating the fundamental computational bottleneck of multi-sample consistency methods while overcoming the coverage limitations of single-signal detectors.')
    body(doc, 'The experimental evaluation across five standardized hallucination benchmarks demonstrated that TRUEGUARD achieves an average AUROC of 0.8821 ± 0.0170, outperforming all single-signal baselines including MIND, LLM-Check, and HaluShift. The ablation study rigorously confirmed that each signal contributes complementary, non-redundant information — no individual signal can replicate the coverage achieved by their fusion. The framework\'s computational overhead of 12.4 ± 0.5 ms/token represents an 11.5× speedup over multi-sample Semantic Entropy, enabling genuine real-time deployment in latency-sensitive streaming applications.')
    body(doc, 'The active closed-loop mitigation pipeline demonstrated practical effectiveness in a double-blind human annotation study (n = 300, Cohen\'s kappa = 0.82), achieving a 63.8% relative reduction in hallucination rate from 31.2% to 11.3% while preserving 88.0% query answer coverage. This validates the architectural decision to integrate detection and mitigation into a unified closed-loop system rather than operating them as separate sequential modules.')
    body(doc, 'TRUEGUARD demonstrates that robust, explainable, and active hallucination guardrails can be deployed in production LLM environments without sacrificing real-time generation speed. The framework is provided as a complete open-source implementation with reproducible benchmarking harnesses, enabling independent verification and extension of all reported results.')

    section_heading(doc, 'Future Work')
    body(doc, 'Several promising directions emerge from this work for future investigation:')
    numbered_item(doc, 'Adaptive Multi-Signal Weighting: The current logistic regression fusion uses fixed weights trained on the combined benchmark distribution. Future work could implement attention-weighted or meta-learned fusion that dynamically adjusts signal weights based on query type, domain indicators, or preliminary retrieval confidence, potentially improving AUROC on domain-specific tasks.')
    numbered_item(doc, 'Black-Box Extension via Output Logits: Extending TRUEGUARD to black-box API settings by replacing ISP and AAS with logit-derived surrogates — inspired by the EPR methodology — would substantially broaden deployment applicability to proprietary models without hidden state access.')
    numbered_item(doc, 'Multilingual Probe Calibration: Training ISP probes on multilingual labeled hallucination datasets would extend TRUEGUARD\'s coverage to non-English deployments, addressing a significant practical gap for global deployment.')
    numbered_item(doc, 'Domain-Specific Knowledge Base Expansion: Integrating TRUEGUARD with domain-specific knowledge graphs and real-time web retrieval APIs would improve Tier-1 mitigation coverage for specialized professional queries in medicine, law, and finance, where Wikipedia coverage is insufficient.')
    numbered_item(doc, 'Fine-Grained Explainability Module: Developing a structured explainability layer that generates natural language explanations for flagged tokens — identifying which signal drove the risk score and the specific contextual mismatch — would improve utility for regulatory compliance and user trust calibration, addressing the XAI gap identified in the literature review.')
    numbered_item(doc, 'Cross-Architecture Generalization: Extending probe training and signal extraction to decoder-only models with different architectural variants (Mixture-of-Experts, state-space models) would broaden TRUEGUARD\'s applicability beyond standard dense transformer architectures.')
    doc.add_page_break()

# ─────────────────────────────────────────────────────────────────────────────
#  APPENDICES
# ─────────────────────────────────────────────────────────────────────────────

def appendices(doc):
    chapter_heading(doc, 'APPENDICES')

    section_heading(doc, 'Appendix 1: Repository Structure')
    body(doc, 'The complete TRUEGUARD implementation is open-sourced at https://github.com/yogeshravi19/trueguard and organized as follows:')
    code_lines = [
        'TRUEGUARD_FINAL/',
        '├── src/trueguard/',
        '│   ├── signals/',
        '│   │   ├── isp.py          # Internal State Probe extraction',
        '│   │   ├── aas.py          # Attention Anomaly Score',
        '│   │   ├── eem.py          # Entropy-Energy Monitor',
        '│   │   └── dst.py          # Distribution Shift Tracker',
        '│   ├── fusion/',
        '│   │   ├── normalizer.py   # Online Welford Z-score normalization',
        '│   │   └── detector.py     # Logistic regression fusion layer',
        '│   └── mitigation/',
        '│       ├── rag.py          # Tier-1 Targeted RAG',
        '│       └── abstention.py   # Tier-2 Calibrated Abstention',
        '├── experiments/',
        '│   ├── cpu_smoke_test.py   # 60-second CPU verification',
        '│   ├── run_benchmark.py    # 5-fold cross-validation runner',
        '│   └── ablation.py         # Signal ablation suite',
        '├── notebooks/',
        '│   └── TRUEGUARD_Colab.ipynb',
        '└── results/',
        '    ├── benchmark_metrics.json',
        '    └── figures/            # All 300 DPI publication figures',
    ]
    p = doc.add_paragraph()
    _set_spacing(p, line_rule='single')
    run = p.add_run('\n'.join(code_lines))
    run.font.name = 'Courier New'
    run.font.size = Pt(9)

    doc.add_paragraph()
    section_heading(doc, 'Appendix 2: Reproducibility Statement')
    body(doc, 'To guarantee complete scientific reproducibility, all TRUEGUARD project artifacts are open-sourced. The repository includes: a complete Python package under TRUEGUARD_FINAL/src/; an automated 60-second CPU smoke-test script (experiments/cpu_smoke_test.py) verifying all four signal extractions on GPT-2 without GPU requirements; a 5-fold cross-validation runner (experiments/run_benchmark.py) reproducing all benchmark AUROC results in Table 6.1; a standalone ablation suite (experiments/ablation.py) reproducing Table 6.2; a self-contained Google Colab notebook with pre-loaded evaluation data; and all raw metrics and 300 DPI figures archived in the results/ directory. All TRUEGUARD experiments are reproducible on a standard CPU workstation within 60 seconds for smoke tests, and on an NVIDIA T4 GPU within 4 hours for full 5-fold cross-validation across all five benchmarks.')
    doc.add_page_break()

# ─────────────────────────────────────────────────────────────────────────────
#  REFERENCES — APA FORMAT
# ─────────────────────────────────────────────────────────────────────────────

def references_page(doc):
    chapter_heading(doc, 'REFERENCES')

    body(doc, 'References are formatted in APA style. All references cited in this report are actual, verifiable publications.', italic=True)
    doc.add_paragraph()

    refs = [
        'Alansari, A., & Luqman, H. (2024). Large language models hallucination: A comprehensive survey. arXiv preprint arXiv:2404.00806.',
        'Azaria, A., & Mitchell, T. (2023). The internal state of an LLM knows when it\'s lying. In Findings of EMNLP (pp. 967–976).',
        'Dasgupta, S., Nath, S., Basu, A., Shamsolmoali, P., & Das, S. (2025). HaluShift: Measuring distribution shifts towards hallucination detection in LLMs. In Proceedings of the IEEE IJCNN (pp. 1–8).',
        'Dhuliawala, S., Komeili, M., Xu, J., Raileanu, R., Li, X., Celikyilmaz, A., & Weston, J. (2024). Chain-of-verification reduces hallucination in large language models. In Findings of ACL (pp. 3563–3578).',
        'Gao, L., Dai, Z., Pasupat, P., Chen, A., Chaganty, A. T., Fan, Y., et al. (2023). RARR: Researching and revising what language models say, using language models. In Proceedings of ACL (pp. 16477–16508).',
        'Hajji, E., Bouguerra, A., & Arnez, F. (2025). The map of misbelief: Tracing intrinsic and extrinsic hallucinations through attention patterns. Proceedings of the AAAI Symposium Series, 7(1), 177–184.',
        'Huang, Y., Sun, L., Wang, H., Wu, S., Zhang, Q., et al. (2024). TrustLLM: Trustworthiness in large language models. arXiv preprint arXiv:2401.05561.',
        'Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., et al. (2023). Survey of hallucination in natural language generation. ACM Computing Surveys, 55(12), 1–38.',
        'Jiang, A. Q., Sablayrolles, A., Mensch, A., Bamford, C., Chaplot, D. S., et al. (2023). Mistral 7B. arXiv preprint arXiv:2310.06825.',
        'Kang, S., Bakman, Y. F., et al. (2024). Uncertainty quantification for hallucination detection in large language models: Foundations, methodology, and future directions. University of Southern California.',
        'Kossen, J., Han, J., Razzak, M., Schut, L., Malik, S., & Gal, Y. (2024). Semantic entropy probes: Robust and cheap hallucination detection in LLMs. ICML Workshop on Foundation Models in the Wild.',
        'Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., et al. (2020). Retrieval-augmented generation for knowledge-intensive NLP tasks. Advances in Neural Information Processing Systems, 33, 9459–9474.',
        'Li, J., Cheng, X., Zhao, W. X., Nie, J.-Y., & Wen, J.-R. (2023). HaluEval: A large-scale hallucination evaluation benchmark for large language models. In Proceedings of EMNLP (pp. 6449–6464).',
        'Liang, P., Bommasani, R., Lee, T., Tsipras, D., Soylu, D., et al. (2022). Holistic evaluation of language models. arXiv preprint arXiv:2211.09110.',
        'Lin, S., Hilton, J., & Evans, O. (2022). TruthfulQA: Measuring how models mimic human falsehoods. In Proceedings of ACL (pp. 3214–3252).',
        'Ma, H., Pan, J., Liu, J., Chen, Y., Zhou, J. T., Wang, G., et al. (2025). Semantic energy: Detecting LLM hallucination beyond entropy. arXiv preprint arXiv:2508.14496.',
        'Manakul, P., Liusie, A., & Gales, M. (2023). SelfCheckGPT: Zero-resource black-box hallucination detection for generative large language models. In Proceedings of EMNLP (pp. 9004–9017).',
        'Min, S., Krishna, K., Lyu, X., Lewis, M., Yih, W.-t., Koh, P. W., et al. (2023). FActScore: Fine-grained atomic evaluation of factual precision in long form text generation. In Proceedings of EMNLP (pp. 12076–12100).',
        'Moslonka, C., Randrianarivo, H., Garnier, A., & Malherbe, E. (2025). Learned hallucination detection in black-box LLMs using token-level entropy production rate. arXiv preprint arXiv:2509.04492.',
        'Nath, S., Basu, A., Dasgupta, S., & Das, S. (2025). HALLUSHIFT++: Bridging language and vision through internal representation shifts for hierarchical hallucinations in MLLMs.',
        'Sharma, M., Siu, H. C., Paleja, R., & Peña, J. D. (2024). Why would you suggest that? Human trust in language model responses. MIT Lincoln Laboratory.',
        'Sriramanan, G., Bharti, S., Sadasivan, V. S., Saha, S., Kattakinda, P., & Feizi, S. (2024). LLM-Check: Investigating detection of hallucinations in large language models. Advances in Neural Information Processing Systems, 37, 34188–34216.',
        'Su, W., Wang, C., Ai, Q., Hu, Y., Wu, Z., Zhou, Y., & Liu, Y. (2024). Unsupervised real-time hallucination detection based on the internal states of large language models. In Findings of ACL (pp. 14379–14391).',
        'Touvron, H., Martin, L., Stone, K., Albert, P., Almahairi, A., et al. (2023). Llama 2: Open foundation and fine-tuned chat models. arXiv preprint arXiv:2307.09288.',
        'Wu, J., Liu, J., Zeng, Z., Zhan, T., Cai, T., & Huang, W. (2025). Mitigating LLM hallucination via behaviorally calibrated reinforcement learning. arXiv preprint arXiv:2512.19920.',
        'Yao, S., Huang, P., Liu, Z., Gu, Y., Yan, Y., Yu, S., & Yu, G. (2025). ExpandR: Teaching dense retrievers beyond queries with LLM guidance. In Proceedings of EMNLP (pp. 19036–19054).',
        'Zhang, L., Song, D., Wu, Z., Tian, Y., Zhou, C., Xu, J., et al. (2025). Detecting hallucination in large language models through deep internal representation analysis. In Proceedings of IJCAI (pp. 8357–8365).',
        'Zhang, P., Zeng, G., Wang, T., & Lu, W. (2024). TinyLlama: An open-source small language model. arXiv preprint arXiv:2401.02385.',
        'Zhang, Y., Li, Y., Cui, L., Cai, D., Liu, L., Fu, T., et al. (2025). Siren\'s song in the AI ocean: A survey on hallucination in large language models. Computational Linguistics, 51(4), 1373–1418.',
    ]
    for ref in refs:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        _set_spacing(p, space_before=0, space_after=4, line_rule='single')
        p.paragraph_format.first_line_indent = Cm(-0.6)
        p.paragraph_format.left_indent = Cm(0.6)
        _run(p, ref, size=11)

# ─────────────────────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    doc = Document()
    set_doc_defaults(doc)

    # FRONT MATTER (no page numbers on cover/title; roman from abstract)
    cover_page(doc)
    title_page(doc)
    declaration_page(doc)
    certificate_page(doc)
    abstract_page(doc)            # i
    acknowledgement_page(doc)     # ii
    toc_page(doc)                 # iii
    lof_page(doc)                 # iv
    lot_page(doc)                 # v
    abbreviations_page(doc)       # vi

    # BODY CHAPTERS (Arabic page numbers)
    chapter1(doc)
    chapter2(doc)
    chapter3(doc)
    chapter4(doc)
    chapter5(doc)
    chapter6(doc)
    chapter7(doc)

    # BACK MATTER
    conclusion_chapter(doc)
    appendices(doc)
    references_page(doc)

    # Add bottom-center page numbers
    add_page_number_footer(doc)

    out = 'TRUEGUARD_BEST_FINAL_Report.docx'
    doc.save(out)
    size_kb = os.path.getsize(out) // 1024
    import docx as dx
    d2 = dx.Document(out)
    n_tables = len(d2.tables)
    n_paras  = len(d2.paragraphs)
    print(f"Generated: {out}")
    print(f"  Size   : {size_kb} KB")
    print(f"  Paras  : {n_paras}")
    print(f"  Tables : {n_tables}")

if __name__ == '__main__':
    main()
