import docx

doc = docx.Document('FINAL_SUBMISSION/FINAL_REPORT_VERIFIED.docx')

print("=== Checking Abstract (P37 to P41) ===")
for i in range(37, 42):
    p = doc.paragraphs[i]
    fonts = set()
    sizes = set()
    for r in p.runs:
        fonts.add(r.font.name)
        sizes.add(r.font.size.pt if r.font.size else None)
    print(f"P{i:2d}: font={fonts}, size={sizes}, text='{p.text[:60]}'")

print("\n=== Checking Sample Chapter Body Paragraphs (P180 to P190) ===")
for i in range(180, 186):
    p = doc.paragraphs[i]
    fonts = set()
    sizes = set()
    for r in p.runs:
        fonts.add(r.font.name)
        sizes.add(r.font.size.pt if r.font.size else None)
    print(f"P{i:2d}: font={fonts}, size={sizes}, text='{p.text[:60]}'")

print("\n=== Checking References (P482 to P490) ===")
for i in range(482, 490):
    p = doc.paragraphs[i]
    fonts = set()
    sizes = set()
    for r in p.runs:
        fonts.add(r.font.name)
        sizes.add(r.font.size.pt if r.font.size else None)
    print(f"P{i:2d}: font={fonts}, size={sizes}, text='{p.text[:60]}'")

print("\n=== Checking Tables Font Sizes ===")
for t_idx in [0, 2, 4, 11, 15, 37, 45, 47]:
    table = doc.tables[t_idx]
    fonts = set()
    sizes = set()
    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    fonts.add(r.font.name)
                    sizes.add(r.font.size.pt if r.font.size else None)
    print(f"Table {t_idx:2d}: fonts={fonts}, sizes={sizes}")
