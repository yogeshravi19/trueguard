import docx
import re

doc = docx.Document('FINAL_SUBMISSION/FINAL_REPORT_VERIFIED.docx')

print(f"Total Paragraphs: {len(doc.paragraphs)}")
print(f"Total Tables: {len(doc.tables)}")

print("\n=== Paragraphs 0 to 40 (Front Matter) ===")
for i, p in enumerate(doc.paragraphs[:40]):
    text = p.text.strip()
    if text:
        print(f"{i:2d}: [{p.style.name}] {text[:90]}")

print("\n=== Headings in Document ===")
for i, p in enumerate(doc.paragraphs):
    if p.style.name.startswith("Heading") or (p.runs and p.runs[0].bold and len(p.text.strip()) < 80 and not p.text.strip().startswith("Figure") and not p.text.strip().startswith("Table")):
        text = p.text.strip()
        if text and len(text) < 70:
            print(f"P{i:3d}: [{p.style.name}] {text}")

print("\n=== Checking for Placeholders (bracketed text, XXX, TODO, TBD, etc.) ===")
placeholder_pattern = re.compile(r'(\[.*?\]|TODO|TBD|XXX|<.*?>|\bplaceholder\b)', re.IGNORECASE)
for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    # exclude references like [1], [2-5]
    cleaned = re.sub(r'\[\d+(?:[,\s–-]+\d+)*\]', '', text)
    matches = placeholder_pattern.findall(cleaned)
    if matches:
        # filter out simple brackets that are math or standard citation
        suspicious = [m for m in matches if not re.match(r'^\[\w+\]$', m) or len(m) > 4 or any(k in m.lower() for k in ['name', 'date', 'insert', 'todo', 'tbd', 'xxx', 'guide', 'dr', 'reg'])]
        if suspicious:
            print(f"P{i:3d}: Suspicious placeholders {suspicious} in: {text[:100]}")

print("\n=== Checking Tables for Placeholders ===")
for t_idx, table in enumerate(doc.tables):
    for r_idx, row in enumerate(table.rows):
        for c_idx, cell in enumerate(row.cells):
            text = cell.text.strip()
            cleaned = re.sub(r'\[\d+(?:[,\s–-]+\d+)*\]', '', text)
            matches = placeholder_pattern.findall(cleaned)
            suspicious = [m for m in matches if any(k in m.lower() for k in ['name', 'todo', 'tbd', 'xxx', 'insert', 'placeholder'])]
            if suspicious:
                print(f"Table {t_idx} (R{r_idx}C{c_idx}): Suspicious {suspicious} in: {text[:80]}")

