import docx

doc = docx.Document(r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx")

# Let's inspect where each drawing is and what text is before and after it
for i, p in enumerate(doc.paragraphs):
    xml = p._p.xml
    has_img = "w:drawing" in xml or "graphicData" in xml
    text = p.text.strip()
    if has_img:
        print(f"\n=================== IMAGE AT P[{i}] ===================")
        for offset in range(-2, 4):
            idx = i + offset
            if 0 <= idx < len(doc.paragraphs):
                p_text = doc.paragraphs[idx].text.strip()
                print(f"  P[{idx}]: {p_text[:120]}")
