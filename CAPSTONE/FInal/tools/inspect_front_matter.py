import docx

doc = docx.Document('FINAL_SUBMISSION/FINAL_REPORT_VERIFIED.docx')
for i in range(25, 52):
    p = doc.paragraphs[i]
    print(f"P{i:2d}: {p.text}")
