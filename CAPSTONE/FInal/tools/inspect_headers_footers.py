import docx

doc = docx.Document('FINAL_SUBMISSION/FINAL_REPORT_VERIFIED.docx')

print(f"Total sections: {len(doc.sections)}")
for i, s in enumerate(doc.sections):
    footer_text = ""
    for p in s.footer.paragraphs:
        if p.text.strip():
            footer_text += p.text.strip() + " | "
    header_text = ""
    for p in s.header.paragraphs:
        if p.text.strip():
            header_text += p.text.strip() + " | "
    
    start_type = s.start_type
    diff_first = s.different_first_page_header_footer
    print(f"Section {i:2d}: start={start_type}, diff_first={diff_first}, header='{header_text}', footer='{footer_text}'")

