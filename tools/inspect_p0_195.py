import docx

doc = docx.Document(r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx")

print("=== CHECKING ALL PARAGRAPHS 0 TO 195 WITH DRAWINGS OR CAPTIONS ===")
for i in range(0, 195):
    t = doc.paragraphs[i].text.strip()
    xml = doc.paragraphs[i]._p.xml
    has_img = "w:drawing" in xml or "graphicData" in xml
    if has_img or "figure" in t.lower() or "fig." in t.lower() or "table" in t.lower():
        print(f"P[{i}] (img={has_img}): {t[:120]}")
