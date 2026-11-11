import docx
import re

doc = docx.Document(r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx")

print("=== ALL TABLES IN DOCX ===")
for t_idx, tbl in enumerate(doc.tables):
    rows = len(tbl.rows)
    cols = len(tbl.columns)
    first_row_text = [c.text.strip() for c in tbl.rows[0].cells]
    print(f"Table index {t_idx}: {rows} rows x {cols} cols | Header: {first_row_text[:4]}")

print("\n=== PARAGRAPHS 15 TO 45 (Near Fig 1) ===")
for i in range(15, 36):
    print(f"P[{i}]: {doc.paragraphs[i].text[:90]}")

print("\n=== PARAGRAPHS 110 TO 145 (Near Fig 2 / Table 1) ===")
for i in range(110, 145):
    t = doc.paragraphs[i].text.strip()
    if t:
        print(f"P[{i}]: {t[:90]}")

print("\n=== SCANNING ALL PARAGRAPHS WITH 'Figure' or 'Table' ===")
for i, p in enumerate(doc.paragraphs):
    t = p.text.strip()
    if "figure" in t.lower() or "table" in t.lower():
        print(f"P[{i}]: {t[:110]}")
