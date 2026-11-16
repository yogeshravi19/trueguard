import docx
import re

doc = docx.Document('FINAL_SUBMISSION/FINAL_REPORT_VERIFIED.docx')

latex_cmd_pattern = re.compile(r'\\[a-zA-Z]+|\^\{|\_\{')

print("=== Scanning for unrendered LaTeX syntax ===")
found = 0
for i, p in enumerate(doc.paragraphs):
    text = p.text
    matches = latex_cmd_pattern.findall(text)
    if matches:
        print(f"P{i:3d}: Found {matches} in: {text[:100]}")
        found += 1

print(f"\nTotal paragraphs with unrendered LaTeX: {found}")

# Also check tables
print("\n=== Scanning Tables for unrendered LaTeX syntax ===")
t_found = 0
for t_idx, table in enumerate(doc.tables):
    for r_idx, row in enumerate(table.rows):
        for c_idx, cell in enumerate(row.cells):
            text = cell.text
            matches = latex_cmd_pattern.findall(text)
            if matches:
                print(f"Table {t_idx} (R{r_idx}C{c_idx}): Found {matches} in: {text[:80]}")
                t_found += 1
