import docx

doc = docx.Document(r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx")

print("=== CHECKING PARAGRAPHS 195 TO 305 ===")
for i in range(195, 305):
    t = doc.paragraphs[i].text.strip()
    xml = doc.paragraphs[i]._p.xml
    has_img = "w:drawing" in xml or "graphicData" in xml
    if t or has_img:
        print(f"P[{i}] (img={has_img}): {t}")
