import docx

doc = docx.Document('FINAL_SUBMISSION/FINAL_REPORT_VERIFIED.docx')
eq_table_indices = [1, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

for idx in eq_table_indices:
    table = doc.tables[idx]
    c0 = table.rows[0].cells[0].text.strip().replace('\n', ' ')
    c1 = table.rows[0].cells[1].text.strip().replace('\n', ' ') if len(table.rows[0].cells) > 1 else ""
    print(f"Table {idx:2d}: [{c1}] {c0}")

