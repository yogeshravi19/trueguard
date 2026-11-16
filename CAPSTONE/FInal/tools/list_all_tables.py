import docx

doc = docx.Document('FINAL_SUBMISSION/FINAL_REPORT_VERIFIED.docx')

print(f"Total tables: {len(doc.tables)}")
for idx, table in enumerate(doc.tables):
    # print first cell or row count
    rows = len(table.rows)
    cols = len(table.columns) if rows > 0 else 0
    first_cell = table.rows[0].cells[0].text.strip().replace('\n', ' ')[:70] if rows > 0 and cols > 0 else "EMPTY"
    print(f"Table {idx:2d} ({rows}x{cols}): '{first_cell}'")
