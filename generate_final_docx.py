import docx
from docx.shared import Pt, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import re

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

def add_cover_page(doc):
    doc.add_paragraph('\n\n')
    add_heading_centered(doc, 'TRUEGUARD: A LIGHTWEIGHT REAL-TIME FRAMEWORK FOR HALLUCINATION DETECTION AND MITIGATION IN LARGE LANGUAGE MODELS', 16, True)
    doc.add_paragraph('\n')
    
    # Add logo image
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_img = p_img.add_run()
    try:
        run_img.add_picture('template_extracted/word/media/image1.png', width=Inches(1.5))
    except:
        pass
        
    doc.add_paragraph('\n')
    p = doc.add_paragraph('Submitted in partial fulfillment for the award of the degree of')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    add_heading_centered(doc, 'M.Tech. (Integrated) Computer Science and Engineering with Specialization in Business Analytics', 14, False)
    doc.add_paragraph('\nby\n')
    
    add_heading_centered(doc, 'YOGESH RAVI M (22MIA0001)', 14, True)
    
    doc.add_paragraph('\n\nUnder the guidance of\n')
    add_heading_centered(doc, 'Dr. T. S. PRADEEP KUMAR\nAssociate Professor', 12, True)
    
    doc.add_paragraph('\n\n')
    # Add Seal image
    p_seal = doc.add_paragraph()
    p_seal.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_seal = p_seal.add_run()
    try:
        run_seal.add_picture('template_extracted/word/media/image2.png', width=Inches(1.5))
    except:
        pass
        
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
    
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_img = p_img.add_run()
    try:
        run_img.add_picture('template_extracted/word/media/image1.png', width=Inches(1.5))
    except:
        pass
        
    add_heading_centered(doc, 'CERTIFICATE', 14, True)
    
    p = doc.add_paragraph('\nThis is to certify that the report entitled "TRUEGUARD: A LIGHTWEIGHT REAL-TIME FRAMEWORK FOR HALLUCINATION DETECTION AND MITIGATION IN LARGE LANGUAGE MODELS" is prepared and submitted by YOGESH RAVI M (Reg. No. 22MIA0001) to Vellore Institute of Technology, Chennai, in partial fulfillment of the requirement for the award of the degree of M.Tech. (Integrated) Computer Science and Engineering with Specialization in Business Analytics programme is a bonafide record carried out under my guidance. The project fulfills the requirements as per the regulations of this University and in my opinion meets the necessary standards for submission. The contents of this report have not been submitted and will not be submitted either in part or in full, for the award of any other degree or diploma and the same is certified.\n\n\n')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    doc.add_paragraph('Signature of the Guide: _______________________\nName: Dr. T. S. PRADEEP KUMAR\nDesignation: Associate Professor\nSchool of Computer Science and Engineering\nVellore Institute of Technology, Chennai\nDate: September, 2026\n\n')
    doc.add_paragraph('Signature of Examiner 1: __________________\nName: ________________________________\nDate: ________________________________\n')
    doc.add_paragraph('Signature of Examiner 2: __________________\nName: ________________________________\nDate: ________________________________\n\n')
    doc.add_paragraph('Approved by the Head of Department\nSchool of Computer Science and Engineering\nVellore Institute of Technology, Chennai')
    doc.add_page_break()

def parse_markdown_to_docx(doc, md_file_path):
    with open(md_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # Skip the # TITLE line if present at the top
    start_idx = 0
    for i, line in enumerate(lines):
        if line.startswith('## CHAPTER 1'):
            start_idx = i
            break
            
    for line in lines[start_idx:]:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('---'):
            doc.add_page_break()
            continue
            
        if line.startswith('## '):
            # Chapter heading
            text = line.replace('##', '').strip()
            p = doc.add_paragraph(text)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].font.size = Pt(16)
            p.runs[0].font.bold = True
        elif line.startswith('### '):
            # Section heading
            text = line.replace('###', '').strip().upper()
            p = doc.add_paragraph(text)
            p.runs[0].font.size = Pt(14)
            p.runs[0].font.bold = True
        elif line.startswith('#### '):
            # Subsection
            text = line.replace('####', '').strip().upper()
            p = doc.add_paragraph(text)
            p.runs[0].font.size = Pt(12)
            p.runs[0].font.bold = True
        elif line.startswith('*[FLAG:'):
            # Flag needs input
            p = doc.add_paragraph(line)
            p.runs[0].font.color.rgb = docx.shared.RGBColor(255, 0, 0) # Red
            p.runs[0].bold = True
        elif line.startswith('- '):
            p = doc.add_paragraph(line.replace('- ', ''), style='List Bullet')
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        elif line.startswith('1. ') or line.startswith('2. '):
            p = doc.add_paragraph(line, style='List Number')
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        else:
            # Normal paragraph
            # Strip bold/italic markdown for simple import, or parse them
            clean_line = line.replace('**', '').replace('*', '').replace('__', '')
            p = doc.add_paragraph(clean_line)
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

def main():
    doc = docx.Document()
    set_margins(doc)
    
    add_cover_page(doc) # Cover
    add_cover_page(doc) # Title page
    add_declaration(doc)
    add_certificate(doc)
    
    # Optional: add lists (contents, figures) 
    doc.add_paragraph("TABLE OF CONTENTS [TO BE GENERATED IN WORD]").runs[0].font.bold = True
    doc.add_page_break()
    
    # Parse draft markdown
    parse_markdown_to_docx(doc, 'TRUEGUARD_Expanded_Draft.md')
    
    doc.save('TRUEGUARD_Final_MTech_Report_Expanded.docx')
    print("M.Tech Project Report generated successfully.")

if __name__ == '__main__':
    main()
