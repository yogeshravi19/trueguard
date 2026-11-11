import docx

doc_orig = docx.Document(r"E:\trueguard\CAPSTONE\submitted for finla rview.docx")

print(f"Total paragraphs in submitted for finla rview.docx: {len(doc_orig.paragraphs)}")

for i, p in enumerate(doc_orig.paragraphs):
    xml = p._p.xml
    if "w:drawing" in xml:
        # find nearby caption
        nearby = []
        for offset in range(-2, 4):
            idx = i + offset
            if 0 <= idx < len(doc_orig.paragraphs):
                t = doc_orig.paragraphs[idx].text.strip()
                if t:
                    nearby.append(f"P[{idx}]: {t[:80]}")
        print(f"\nDrawing at P[{i}]:")
        for line in nearby:
            print(f"  {line}")
