import docx
import re
import os
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt, Inches

def replace_text_in_paragraph(paragraph, old_text, new_text):
    if old_text in paragraph.text:
        for run in paragraph.runs:
            if old_text in run.text:
                run.text = run.text.replace(old_text, new_text)

def clean_latex_and_metrics(doc):
    for p in doc.paragraphs:
        # Fix AUROC 0.8821 to 0.844
        replace_text_in_paragraph(p, '0.8821', '0.844')
        replace_text_in_paragraph(p, '88.21', '84.4')
        
        # Strip basic LaTeX math wrappers
        if '$' in p.text:
            for run in p.runs:
                if '$' in run.text:
                    run.text = run.text.replace('$', '')
                    
        # Replace \textbf{} and \rho
        if '\\' in p.text:
            for run in p.runs:
                if '\\rho' in run.text:
                    run.text = run.text.replace('\\rho', 'p')
                if '\\textbf{' in run.text:
                    run.text = re.sub(r'\\textbf{([^}]+)}', r'\1', run.text)

def add_page_numbers(doc):
    # Standard python-docx doesn't easily expose bottom-center page numbers directly, 
    # but we can add the required XML field to the footer of every section
    for section in doc.sections:
        footer = section.footer
        if len(footer.paragraphs) == 0:
            p = footer.add_paragraph()
        else:
            p = footer.paragraphs[0]
            
        p.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
        
        # Add PAGE field
        run = p.add_run()
        fldChar1 = OxmlElement('w:fldChar')
        fldChar1.set(qn('w:fldCharType'), 'begin')
        
        instrText = OxmlElement('w:instrText')
        instrText.set(qn('xml:space'), 'preserve')
        instrText.text = "PAGE"
        
        fldChar2 = OxmlElement('w:fldChar')
        fldChar2.set(qn('w:fldCharType'), 'end')
        
        run._r.append(fldChar1)
        run._r.append(instrText)
        run._r.append(fldChar2)

def inject_toc(doc):
    for p in doc.paragraphs:
        if 'TABLE OF CONTENTS [TO BE GENERATED IN WORD]' in p.text:
            p.text = ''
            run = p.add_run()
            
            # Insert native TOC field
            fldChar1 = OxmlElement('w:fldChar')
            fldChar1.set(qn('w:fldCharType'), 'begin')
            
            instrText = OxmlElement('w:instrText')
            instrText.set(qn('xml:space'), 'preserve')
            instrText.text = 'TOC \\o "1-3" \\h \\z \\u'
            
            fldChar2 = OxmlElement('w:fldChar')
            fldChar2.set(qn('w:fldCharType'), 'separate')
            
            fldChar3 = OxmlElement('w:fldChar')
            fldChar3.set(qn('w:fldCharType'), 'end')
            
            run._r.append(fldChar1)
            run._r.append(instrText)
            run._r.append(fldChar2)
            run._r.append(fldChar3)

def insert_figures(doc):
    # Look for captions and insert matching images
    image_map = {
        'fig1_architecture': 'figures/fig1_architecture.png',
        'fig2_overview': 'figures/fig2_overview.png',
        'fig3_ablation': 'figures/fig3_ablation_study.png',
        'fig4_latency': 'figures/fig4_latency_efficiency_tradeoff.png'
    }
    
    # We will just insert these figures at the start of Chapter 3, 4, 6 respectively for now 
    # to guarantee they are embedded
    for i, p in enumerate(doc.paragraphs):
        text = p.text.upper()
        if 'CHAPTER 3' in text and i+1 < len(doc.paragraphs) and 'RESEARCH GAP' in doc.paragraphs[i+1].text.upper():
            if os.path.exists(image_map['fig1_architecture']):
                run = doc.paragraphs[i+2].add_run()
                run.add_picture(image_map['fig1_architecture'], width=Inches(5.5))
                
        if 'CHAPTER 4' in text and i+1 < len(doc.paragraphs) and 'METHODOLOGY' in doc.paragraphs[i+1].text.upper():
            if os.path.exists(image_map['fig2_overview']):
                run = doc.paragraphs[i+2].add_run()
                run.add_picture(image_map['fig2_overview'], width=Inches(5.5))

def main():
    filepath = 'TRUEGUARD_Final_MTech_Report_Expanded.docx'
    doc = docx.Document(filepath)
    
    # 1. Clean LaTeX and enforce 0.844 AUROC
    clean_latex_and_metrics(doc)
    
    # 2. Add Page Numbers
    add_page_numbers(doc)
    
    # 3. Add TOC field
    inject_toc(doc)
    
    # 4. Insert real figures
    insert_figures(doc)
    
    doc.save('TRUEGUARD_Final_MTech_Report_Fixed.docx')
    print("QA pass and fixes applied successfully.")

if __name__ == '__main__':
    main()
