import docx

doc = docx.Document('FINAL_SUBMISSION/FINAL_REPORT_VERIFIED.docx')

in_ref = False
ref_paragraphs = []
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "REFERENCES":
        in_ref = True
        continue
    if in_ref:
        if p.text.strip():
            ref_paragraphs.append((i, p.text.strip()))

print(f"Total reference paragraphs found: {len(ref_paragraphs)}")
for i, text in ref_paragraphs:
    if any(text.startswith(f"[{k}]") for k in [1, 2, 3, 4, 5, 8, 9, 10, 37, 38, 39, 40]):
        print(f"P{i:3d}: {text}")

