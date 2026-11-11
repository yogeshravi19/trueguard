import docx
import re
import os

doc_path = r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx"
doc = docx.Document(doc_path)

print(f"Total paragraphs: {len(doc.paragraphs)}")
print(f"Total tables in doc: {len(doc.tables)}")

fig_captions = []
tbl_captions = []

# Check images embedded in paragraphs or tables
images_in_p = []
for i, p in enumerate(doc.paragraphs):
    xml = p._p.xml
    if "w:drawing" in xml or "graphicData" in xml:
        images_in_p.append(i)

print(f"Paragraphs with drawings/images: {images_in_p}")

for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if re.match(r'^(Figure|Fig\.)\s+\d+', text, re.I):
        fig_captions.append((i, text))
    elif re.match(r'^Table\s+\d+', text, re.I):
        tbl_captions.append((i, text))

print("\n=== FIGURE CAPTIONS DETECTED ===")
for idx, c in fig_captions:
    print(f"[{idx}] {c[:100]}")

print("\n=== TABLE CAPTIONS DETECTED ===")
for idx, c in tbl_captions:
    print(f"[{idx}] {c[:100]}")

# Now let's scan all paragraphs to see where Figure 1..N and Table 1..N appear
caption_indices = set([idx for idx, _ in fig_captions] + [idx for idx, _ in tbl_captions])

body_paragraphs = []
for i, p in enumerate(doc.paragraphs):
    if i not in caption_indices:
        body_paragraphs.append((i, p.text.strip()))

# Search for Figure 1 to 15
print("\n=== SEARCHING FOR FIGURE REFERENCES IN BODY ===")
for fig_num in range(1, 15):
    pattern = rf'\b(?:Figure|Fig\.)\s+{fig_num}\b'
    matches = []
    for idx, text in body_paragraphs:
        found = re.findall(pattern, text, re.I)
        if found:
            matches.append((idx, text[:60]))
    if matches or any(re.match(rf'^(Figure|Fig\.)\s+{fig_num}\b', c[1], re.I) for c in fig_captions):
        print(f"Figure {fig_num}: Found {len(matches)} reference(s) in body paragraphs: {matches}")

# Search for Table 1 to 10
print("\n=== SEARCHING FOR TABLE REFERENCES IN BODY ===")
for tbl_num in range(1, 10):
    pattern = rf'\bTable\s+{tbl_num}\b'
    matches = []
    for idx, text in body_paragraphs:
        found = re.findall(pattern, text, re.I)
        if found:
            matches.append((idx, text[:60]))
    if matches or any(re.match(rf'^Table\s+{tbl_num}\b', c[1], re.I) for c in tbl_captions):
        print(f"Table {tbl_num}: Found {len(matches)} reference(s) in body paragraphs: {matches}")
