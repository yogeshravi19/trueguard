import docx
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.style import WD_STYLE_TYPE

def set_margins(doc):
    for section in doc.sections:
        section.left_margin = Cm(3.81)
        section.right_margin = Cm(2.54)
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)

def add_heading_centered(doc, text, size=16, bold=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    return p

def add_title_page(doc):
    doc.add_paragraph('\n\n')
    add_heading_centered(doc, 'TRUEGUARD: A LIGHTWEIGHT REAL-TIME FRAMEWORK FOR HALLUCINATION DETECTION AND MITIGATION IN LARGE LANGUAGE MODELS', 16, True)
    doc.add_paragraph('\n')
    p = doc.add_paragraph('Submitted in partial fulfillment for the award of the degree of')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    add_heading_centered(doc, 'M.Tech. (Integrated) Computer Science and Engineering with Specialization in Business Analytics', 14, False)
    doc.add_paragraph('\nby\n')
    
    add_heading_centered(doc, 'YOGESH RAVI M (22MIA0001)', 14, True)
    
    doc.add_paragraph('\n\nUnder the guidance of\n')
    add_heading_centered(doc, 'Dr. T. S. PRADEEP KUMAR\nAssociate Professor', 12, True)
    
    doc.add_paragraph('\n\n\n\n')
    add_heading_centered(doc, 'SCHOOL OF COMPUTER SCIENCE AND ENGINEERING\nVELLORE INSTITUTE OF TECHNOLOGY, CHENNAI\nSeptember, 2026', 14, True)
    doc.add_page_break()

def add_declaration(doc):
    add_heading_centered(doc, 'DECLARATION', 14, True)
    p = doc.paragraphs[-1]
    p.runs[0].underline = True
    
    p = doc.add_paragraph('\nI hereby declare that the thesis entitled "TRUEGUARD: A LIGHTWEIGHT REAL-TIME FRAMEWORK FOR HALLUCINATION DETECTION AND MITIGATION IN LARGE LANGUAGE MODELS" submitted by me, for the award of the degree of M.Tech. (Integrated) Computer Science and Engineering with Specialization in Business Analytics, Vellore Institute of Technology, Chennai, is a record of bonafide work carried out by me under the supervision of Dr. T. S. PRADEEP KUMAR, Associate Professor, School of Computer Science and Engineering.')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    p = doc.add_paragraph('\nI further declare that the work reported in this thesis has not been submitted and will not be submitted, either in part or in full, for the award of any other degree or diploma in this institute or any other institute or university.\n\n\n')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    doc.add_paragraph('Place: Chennai\nDate: September, 2026                                                                    Signature of the Candidate')
    doc.add_paragraph('                                                                                                    YOGESH RAVI M (22MIA0001)')
    doc.add_page_break()

def add_certificate(doc):
    doc.add_paragraph('School of Computer Science and Engineering\n')
    add_heading_centered(doc, 'CERTIFICATE', 14, True)
    
    p = doc.add_paragraph('\nThis is to certify that the report entitled "TRUEGUARD: A LIGHTWEIGHT REAL-TIME FRAMEWORK FOR HALLUCINATION DETECTION AND MITIGATION IN LARGE LANGUAGE MODELS" is prepared and submitted by YOGESH RAVI M (Reg. No. 22MIA0001) to Vellore Institute of Technology, Chennai, in partial fulfillment of the requirement for the award of the degree of M.Tech. (Integrated) Computer Science and Engineering with Specialization in Business Analytics programme is a bonafide record carried out under my guidance. The project fulfills the requirements as per the regulations of this University and in my opinion meets the necessary standards for submission. The contents of this report have not been submitted and will not be submitted either in part or in full, for the award of any other degree or diploma and the same is certified.\n\n\n')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    doc.add_paragraph('Signature of the Guide: _______________________\nName: Dr. T. S. PRADEEP KUMAR\nDesignation: Associate Professor\nSchool of Computer Science and Engineering\nVellore Institute of Technology, Chennai\nDate: September, 2026\n\n')
    doc.add_paragraph('Signature of Examiner 1: __________________\nName: ________________________________\nDate: ________________________________\n')
    doc.add_paragraph('Signature of Examiner 2: __________________\nName: ________________________________\nDate: ________________________________\n\n')
    doc.add_paragraph('Approved by the Head of Department\nSchool of Computer Science and Engineering\nVellore Institute of Technology, Chennai')
    doc.add_page_break()

def add_abstract(doc):
    add_heading_centered(doc, 'ABSTRACT', 14, True)
    p = doc.add_paragraph('\nLarge Language Models (LLMs) frequently generate fluent yet factually unfounded statements---a phenomenon known as hallucination. Existing detection approaches generally mandate either multi-sample semantic consistency checks (which require 5-10 stochastic forward passes and introduce ~142.3 ms/token overhead) or isolated single-signal white-box metrics that fail to capture heterogeneous hallucination modes. In this paper, we propose TRUEGUARD, an inline, multi-signal framework that monitors autoregressive generation in a single forward pass without disrupting standard decoding.\n\nTRUEGUARD extracts four complementary intrinsic signals at each decoding step: Internal State Probes (ISP), Attention Anomaly Score (AAS), Entropy-Energy Monitor (EEM), and Distribution Shift Tracker (DST). These signals are dynamically standardized via online Z-score normalization and fused through a learned logistic regression layer to produce a calibrated token-level risk score R(t). When the sequence risk exceeds a calibrated safety threshold (tau = 0.50), TRUEGUARD triggers an active closed-loop mitigation pipeline incorporating targeted Retrieval-Augmented Grounding (RAG) and calibrated abstention.\n\nEvaluated across five benchmark distributions (TruthfulQA, HaluEval-QA, HaluEval-Summ, HaluEval-Dial, and HELM), TRUEGUARD achieves an average AUROC of 0.8821 with merely 12.4 ms/token latency overhead---an 11.5x speedup over Semantic Entropy. In human-annotated mitigation evaluations, TRUEGUARD achieves a 63.8% relative reduction in hallucination occurrence while maintaining an 88.0% query answer coverage.\n\nKeywords: Large Language Models, Hallucination Detection, Trustworthy AI, Real-Time Inference, Uncertainty Quantification, Active Mitigation, Explainable AI.')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    doc.add_page_break()

def add_acknowledgement(doc):
    add_heading_centered(doc, 'ACKNOWLEDGEMENT', 14, True)
    p = doc.add_paragraph('\nIt is my pleasure to express with deep sense of gratitude to Dr. T. S. PRADEEP KUMAR, Associate Professor, School of Computer Science and Engineering, Vellore Institute of Technology, Chennai, for his constant guidance, continual encouragement, understanding; more than all, he taught me patience in my endeavour. My association with him is not confined to academics only, but it is a great opportunity for my part of work with an intellectual and expert in the field of Artificial Intelligence and Large Language Models.\n')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p = doc.add_paragraph('It is with gratitude that I would like to extend my thanks to the visionary leader Dr. G. Viswanathan our Honourable Chancellor, Mr. Sankar Viswanathan, Dr. Sekar Viswanathan, Dr. G. V. Selvam Vice Presidents, Dr. Sandhya Pentareddy Executive Director, Ms. Kadhambari S. Viswanathan Assistant Vice-President, Dr. V. S. Kanchana Bhaaskaran Vice-Chancellor, and Dr. T. Thyagarajan Pro-Vice Chancellor, VIT Chennai for providing an exceptional working environment and inspiring all of us during the tenure of the course.\n')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p = doc.add_paragraph('Special mention to Dr. Viswanathan V, Dean, Dr. Nithyanandam P, Dr. Suganya G, and Dr. Sweetlin Hemalatha C, Associate Deans, School of Computer Science and Engineering, Vellore Institute of Technology, Chennai, for spending their valuable time and efforts in sharing their knowledge and for helping us in every aspect.\n')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p = doc.add_paragraph('In jubilant state, I express ingeniously my whole-hearted thanks to the Head of the Department, School of Computer Science and Engineering, Vellore Institute of Technology, Chennai, for their valuable support and encouragement to take up and complete the thesis.\n')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p = doc.add_paragraph('My sincere thanks to all the faculty and staff members at Vellore Institute of Technology, Chennai, who helped me acquire the requisite knowledge. I would like to thank my parents for their unconditional moral support, sacrifices, and prayers. It is indeed a pleasure to thank my peers and friends who encouraged me to take up and complete this research project successfully.\n\n\n')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    doc.add_paragraph('Place: Chennai\nDate: September, 2026                                                                    YOGESH RAVI M (22MIA0001)')
    doc.add_page_break()

def add_lists(doc):
    lists = [
        ('CONTENTS', ['CHAPTER 1 INTRODUCTION', 'CHAPTER 2 BACKGROUND & LITERATURE REVIEW', 'CHAPTER 3 PROBLEM FORMULATION', 'CHAPTER 4 THE TRUEGUARD FRAMEWORK', 'CHAPTER 5 EXPERIMENTAL METHODOLOGY', 'CHAPTER 6 RESULTS AND DISCUSSION', 'CHAPTER 7 CONCLUSION AND FUTURE WORK', 'REFERENCES']),
        ('LIST OF FIGURES', ['Figure 1.1: System Architecture of TRUEGUARD', 'Figure 4.1: Internal State Probes (ISP) Calibration', 'Figure 4.2: Attention Anomaly Score (AAS) Distribution', 'Figure 6.1: ROC Curve for Hallucination Detection across Benchmarks']),
        ('LIST OF TABLES', ['Table 4.1: Base LLM Configurations', 'Table 6.1: Benchmark Performance metrics (TruthfulQA, HaluEval, HELM)', 'Table 6.2: Latency Benchmark comparisons']),
        ('LIST OF ACRONYMS', ['LLM - Large Language Model', 'ISP - Internal State Probes', 'AAS - Attention Anomaly Score', 'EEM - Entropy-Energy Monitor', 'DST - Distribution Shift Tracker', 'RAG - Retrieval-Augmented Generation'])
    ]
    
    for title, items in lists:
        add_heading_centered(doc, title, 14, True)
        doc.add_paragraph()
        for item in items:
            doc.add_paragraph(item)
        doc.add_page_break()

def add_chapters(doc):
    import re
    with open('TRUEGUARD_IEEE_FINAL.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple regex based extraction for mapping
    # Assuming sections in markdown start with ## I., ## II. etc
    sections = re.split(r'\n## [IVX]+\. ', '\n' + content)[1:]
    
    chapter_titles = [
        "INTRODUCTION",
        "BACKGROUND & LITERATURE REVIEW",
        "PROBLEM FORMULATION",
        "THE TRUEGUARD FRAMEWORK",
        "EXPERIMENTAL METHODOLOGY",
        "RESULTS AND EMPIRICAL ANALYSIS",
        "DISCUSSION & LIMITATIONS",
        "CONCLUSION"
    ]
    
    for i, section_content in enumerate(sections):
        lines = section_content.strip().split('\n')
        # Title is the first line
        title = lines[0].strip()
        body = '\n'.join(lines[1:]).strip()
        
        # Add Chapter Heading
        chapter_name = chapter_titles[i] if i < len(chapter_titles) else title.upper()
        
        p = doc.add_paragraph(f"CHAPTER {i+1}")
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].font.size = Pt(16)
        p.runs[0].font.bold = True
        
        p = doc.add_paragraph(chapter_name)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].font.size = Pt(16)
        p.runs[0].font.bold = True
        
        doc.add_paragraph()
        
        for p_text in body.split('\n\n'):
            p_text = p_text.strip()
            if not p_text:
                continue
            if p_text.startswith('### '):
                p = doc.add_paragraph(p_text.replace('###', '').strip().upper())
                p.runs[0].font.size = Pt(14)
                p.runs[0].font.bold = True
            elif p_text.startswith('|'):
                # Format tables roughly as text blocks for now to preserve structure
                p = doc.add_paragraph(p_text)
                p.runs[0].font.name = 'Courier New'
                p.runs[0].font.size = Pt(10)
            else:
                p = doc.add_paragraph(p_text)
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        
        doc.add_page_break()

def main():
    doc = docx.Document()
    set_margins(doc)
    
    add_title_page(doc)
    add_title_page(doc) # Often required twice
    add_declaration(doc)
    add_certificate(doc)
    add_abstract(doc)
    add_acknowledgement(doc)
    add_lists(doc)
    add_chapters(doc)
    
    doc.save('TRUEGUARD_Final_Project_Report_V2.docx')
    print("Full comprehensive report generated successfully.")

if __name__ == '__main__':
    main()
