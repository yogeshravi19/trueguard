import docx
import re

doc = docx.Document('FINAL_SUBMISSION/FINAL_REPORT_VERIFIED.docx')

patterns = ['layer activation', 'energy-entropy score', 'attention weights', 'residual-stream hidden state']

print("=== Scanning for formula artifact words ===")
for i, p in enumerate(doc.paragraphs):
    for pat in patterns:
        if pat in p.text and any(sym in p.text for sym in ['=', '∑', '∈', 'h_', 'α_', 'H_', 'F_']):
            print(f"P{i:3d}: Found '{pat}' in: {p.text[:120]}")

for t_idx, table in enumerate(doc.tables):
    for r_idx, row in enumerate(table.rows):
        for c_idx, cell in enumerate(row.cells):
            for pat in patterns:
                if pat in cell.text and any(sym in cell.text for sym in ['=', '∑', '∈', 'h_', 'α_', 'H_', 'F_']):
                    print(f"Table {t_idx} (R{r_idx}C{c_idx}): Found '{pat}' in: {cell.text[:120]}")

