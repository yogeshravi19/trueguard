import docx

doc = docx.Document('FINAL_SUBMISSION/FINAL_REPORT_VERIFIED.docx')
indices = [181, 231, 232, 320, 326, 330, 340]
for idx in indices:
    print(f"=== P{idx} ===")
    print(doc.paragraphs[idx].text)
    print()
