import docx

doc = docx.Document('FINAL_SUBMISSION/FINAL_REPORT_VERIFIED.docx')

print("=== Embedded Images in Document ===")
img_count = 0
for i, p in enumerate(doc.paragraphs):
    for r in p.runs:
        # check drawing elements
        drawings = r._element.xpath('.//a:blip')
        if drawings:
            r_id = drawings[0].get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
            image_part = doc.part.related_parts[r_id]
            print(f"P{i:3d}: Image {image_part.partname} ({len(image_part.blob)} bytes), text around: '{p.text[:60]}'")
            img_count += 1

print(f"Total embedded images found: {img_count}")
