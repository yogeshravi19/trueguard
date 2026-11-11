import zipfile
import xml.etree.ElementTree as ET

docx_path = r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx"

with zipfile.ZipFile(docx_path, 'r') as z:
    rels_xml = z.read("word/_rels/document.xml.rels")
    root = ET.fromstring(rels_xml)
    
    rId_to_target = {}
    for elem in root:
        rId = elem.attrib.get("Id")
        target = elem.attrib.get("Target")
        if target and target.startswith("media/"):
            rId_to_target[rId] = target

print("=== IMAGE RELATIONSHIPS IN DOCX ===")
for rId, target in sorted(rId_to_target.items()):
    print(f"{rId} -> {target}")

# Now let's see which rId are actually referenced in document.xml!
with zipfile.ZipFile(docx_path, 'r') as z:
    doc_xml = z.read("word/document.xml").decode("utf-8")
    for rId, target in sorted(rId_to_target.items()):
        count = doc_xml.count(f'"{rId}"')
        print(f"{rId} ({target}): used {count} times in document.xml")
