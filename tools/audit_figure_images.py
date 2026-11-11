import docx

doc_path = r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx"
doc = docx.Document(doc_path)

print(f"Total paragraphs: {len(doc.paragraphs)}")

for i, p in enumerate(doc.paragraphs):
    for f in range(1, 13):
        txt = p.text.strip()
        if txt.startswith(f"Figure {f}:") or txt.startswith(f"Figure {f} :"):
            # Look backwards up to 30 paragraphs to see where the nearest drawing is
            nearest_img_dist = None
            nearest_img_idx = None
            for back in range(1, 35):
                if i - back >= 0:
                    if "w:drawing" in doc.paragraphs[i - back]._p.xml or "w:pict" in doc.paragraphs[i - back]._p.xml:
                        nearest_img_dist = back
                        nearest_img_idx = i - back
                        break
            
            # Also check if drawing is in the caption paragraph itself
            in_self = "w:drawing" in p._p.xml
            print(f"Fig {f:2d} | Caption P[{i:3d}] | self_has_img={in_self} | nearest_img=P[{nearest_img_idx}] (dist={nearest_img_dist}) | text: {txt[:50]}")
