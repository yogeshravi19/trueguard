import docx

doc = docx.Document('FINAL_SUBMISSION/FINAL_REPORT_VERIFIED.docx')

print("=== Table of Contents (Paragraphs 51 to 127) ===")
for i in range(51, 128):
    p = doc.paragraphs[i]
    if p.text.strip():
        print(f"P{i:3d}: {p.text.strip()}")

print("\n=== List of Figures (Paragraphs 128 to 135) ===")
for i in range(128, 136):
    p = doc.paragraphs[i]
    if p.text.strip():
        print(f"P{i:3d}: {p.text.strip()}")

print("\n=== List of Tables (Paragraphs 136 to 175) ===")
for i in range(136, 175):
    p = doc.paragraphs[i]
    if p.text.strip():
        print(f"P{i:3d}: {p.text.strip()}")

