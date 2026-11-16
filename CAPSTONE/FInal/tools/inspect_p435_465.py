import docx

doc = docx.Document('FINAL_SUBMISSION/FINAL_REPORT_VERIFIED.docx')
for i in range(435, 465):
    print(f"P{i:3d}: {doc.paragraphs[i].text[:120]}")

