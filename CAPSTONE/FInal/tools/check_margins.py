import docx

doc = docx.Document('FINAL_SUBMISSION/FINAL_REPORT_VERIFIED.docx')
for i, sec in enumerate(doc.sections):
    print(f"Section {i}: W={sec.page_width.inches:.2f}\", H={sec.page_height.inches:.2f}\", Top={sec.top_margin.inches:.2f}\", Bottom={sec.bottom_margin.inches:.2f}\", Left={sec.left_margin.inches:.2f}\", Right={sec.right_margin.inches:.2f}\"")

