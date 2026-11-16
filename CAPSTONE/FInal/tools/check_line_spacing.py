import docx

doc = docx.Document('FINAL_SUBMISSION/FINAL_REPORT_VERIFIED.docx')
spacings = set()
for p in doc.paragraphs:
    if p.text.strip():
        sp = p.paragraph_format.line_spacing
        spacings.add(sp)

print("Unique line spacings in paragraphs:", spacings)

