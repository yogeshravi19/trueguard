import docx
import zipfile
import xml.etree.ElementTree as ET
import os

docx_path = r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx"
doc = docx.Document(docx_path)

# Let's find all paragraphs that have an image
print("=== PARAGRAPHS WITH IMAGES ===")
for i, p in enumerate(doc.paragraphs):
    xml = p._p.xml
    if "w:drawing" in xml or "graphicData" in xml or "w:pict" in xml:
        # Find r:embed or blip
        root = ET.fromstring(xml)
        blips = root.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/main}blip")
        embed_ids = [b.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed", "") for b in blips]
        
        # Check text in paragraph or nearby paragraphs
        nearby_text = [doc.paragraphs[j].text.strip() for j in range(max(0, i-2), min(len(doc.paragraphs), i+4)) if doc.paragraphs[j].text.strip()]
        print(f"P[{i}]: Embed IDs={embed_ids} | Nearby text: {nearby_text[:2]}")
