import docx
import re
import os
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

def clean_markdown_bold(paragraph):
    # Highly simplified bold replacement:
    # If '**' exists, we just strip it from the text since doing complex run splitting in python-docx is error-prone.
    # We apply bold to any run that contained the asterisks if it was fully enclosed.
    # To be safe and clean, we will just strip all asterisks from the text.
    if '**' in paragraph.text or '*' in paragraph.text:
        for run in paragraph.runs:
            if '**' in run.text:
                run.bold = True
                run.text = run.text.replace('**', '')
            if '*' in run.text:
                run.text = run.text.replace('*', '')

def strip_markdown_headers_and_lists(paragraph):
    text = paragraph.text.strip()
    if text.startswith('### '):
        paragraph.text = text.replace('### ', '')
    elif text.startswith('## '):
        paragraph.text = text.replace('## ', '')
    elif text.startswith('# '):
        paragraph.text = text.replace('# ', '')
    elif text.startswith('- '):
        paragraph.style = 'List Bullet'
        paragraph.text = text[2:]

def purge_red_flags(doc):
    # We will identify paragraphs that contain the RED flag or [FLAG:
    # We collect them and delete them.
    paragraphs_to_delete = []
    for p in doc.paragraphs:
        if '[FLAG:' in p.text:
            paragraphs_to_delete.append(p)
            continue
        # Check for red runs
        is_red = False
        for run in p.runs:
            if run.font.color and run.font.color.rgb == RGBColor(255, 0, 0):
                is_red = True
                break
        if is_red:
            paragraphs_to_delete.append(p)
            
    for p in paragraphs_to_delete:
        p._element.getparent().remove(p._element)

def rebuild_tables(doc):
    # Find contiguous blocks of paragraphs starting with '|'
    table_blocks = []
    current_block = []
    
    for p in doc.paragraphs:
        if p.text.strip().startswith('|') and p.text.strip().endswith('|'):
            current_block.append(p)
        else:
            if len(current_block) > 0:
                table_blocks.append(current_block)
                current_block = []
                
    if len(current_block) > 0:
        table_blocks.append(current_block)
        
    for block in table_blocks:
        # Ignore markdown separator rows like |---|---|
        valid_rows = [p.text for p in block if '---' not in p.text]
        if not valid_rows:
            continue
            
        # Parse data
        table_data = []
        for row in valid_rows:
            cols = [c.strip() for c in row.split('|')[1:-1]]
            table_data.append(cols)
            
        if not table_data:
            continue
            
        # Insert table before the first paragraph of the block
        first_p = block[0]
        table = doc.add_table(rows=len(table_data), cols=len(table_data[0]))
        table.style = 'Table Grid'
        
        # Populate table
        for r_idx, row_data in enumerate(table_data):
            for c_idx, cell_text in enumerate(row_data):
                if c_idx < len(table.columns):
                    cell = table.cell(r_idx, c_idx)
                    cell.text = cell_text
                    # Set 10pt font
                    for p in cell.paragraphs:
                        for run in p.runs:
                            run.font.size = Pt(10)
                            if r_idx == 0:
                                run.bold = True
        
        # Move table to correct location
        first_p._p.addprevious(table._tbl)
        
        # Delete original text paragraphs
        for p in block:
            p._element.getparent().remove(p._element)

def insert_additional_figures(doc):
    image_map = {
        'fig3_ablation': 'figures/fig3_ablation_study.png',
        'fig4_latency': 'figures/fig4_latency_efficiency_tradeoff.png',
        'fig5_waterfall': 'figures/fig5_mitigation_waterfall.png'
    }
    
    # We will search for chapter 6 Results and inject these figures
    for i, p in enumerate(doc.paragraphs):
        text = p.text.upper()
        if '6.3 ABLATION STUDY' in text:
            if os.path.exists(image_map['fig3_ablation']):
                run = doc.paragraphs[i].add_run()
                run.add_picture(image_map['fig3_ablation'], width=Inches(5.5))
        if '6.4 LATENCY' in text:
            if os.path.exists(image_map['fig4_latency']):
                run = doc.paragraphs[i].add_run()
                run.add_picture(image_map['fig4_latency'], width=Inches(5.5))
        if '6.5 MITIGATION EFFECTIVENESS' in text:
            if os.path.exists(image_map['fig5_waterfall']):
                run = doc.paragraphs[i].add_run()
                run.add_picture(image_map['fig5_waterfall'], width=Inches(5.5))

def main():
    filepath = 'TRUEGUARD_Final_MTech_Report_Fixed.docx'
    doc = docx.Document(filepath)
    
    # 1. Purge red text / flags
    purge_red_flags(doc)
    
    # 2. Markdown Cleanup
    for p in doc.paragraphs:
        clean_markdown_bold(p)
        strip_markdown_headers_and_lists(p)
        
    # 3. Rebuild Tables
    rebuild_tables(doc)
    
    # 4. Insert remaining figures
    insert_additional_figures(doc)
    
    doc.save('TRUEGUARD_Final_MTech_Report_Cleaned.docx')
    print("Final formatting cleanup applied successfully.")

if __name__ == '__main__':
    main()
