import docx
import zipfile
import xml.etree.ElementTree as ET

orig_path = r"E:\trueguard\CAPSTONE\submitted for finla rview.docx"
curr_path = r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx"

doc_orig = docx.Document(orig_path)
doc_curr = docx.Document(curr_path)

# Let's inspect each drawing in orig_path
print("=== DRAWINGS IN ORIGINAL SUBMITTED DOCX ===")
orig_drawings = []
for i, p in enumerate(doc_orig.paragraphs):
    xml = p._p.xml
    if "w:drawing" in xml:
        # get blip embed id
        root = ET.fromstring(xml)
        blip = root.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}blip")
        embed_id = blip.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed", "") if blip is not None else ""
        
        # find caption
        cap = ""
        for off in range(-3, 4):
            idx = i + off
            if 0 <= idx < len(doc_orig.paragraphs):
                t = doc_orig.paragraphs[idx].text.strip()
                if t.startswith("Figure ") or t.startswith("Fig."):
                    cap = f"P[{idx}]: {t}"
                    break
        print(f"Orig Drawing at P[{i}]: embed={embed_id} | Caption: {cap}")
        orig_drawings.append((i, embed_id, cap, xml))
