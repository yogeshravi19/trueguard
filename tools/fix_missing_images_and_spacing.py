import docx
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os
import shutil
import time

MEDIA_DIR = r"E:\trueguard\tools\extracted_media"
DOC_HIGHLIGHTED = r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx"
DOC_NOCOLOUR = r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models_nocolour.docx"

def fix_document(docx_path, out_path=None):
    if out_path is None:
        out_path = docx_path
    print(f"\n==========================================")
    print(f"Processing: {os.path.basename(docx_path)} -> {os.path.basename(out_path)}")
    print(f"==========================================")
    
    # We read from docx_path
    doc = docx.Document(docx_path)

    # Step 1: Insert missing images for Figure 4, Figure 5, Figure 6 if not present
    for f, img_file, w in [
        (4, "image4.png", 6.0),
        (5, "image5.png", 6.0),
        (6, "image6.png", 6.0)
    ]:
        cap_p = None
        for p in doc.paragraphs:
            txt = p.text.strip()
            if txt.startswith(f"Figure {f}:") or txt.startswith(f"Figure {f} :"):
                cap_p = p
                break
        
        if cap_p is not None:
            # Check if any paragraph within 2 steps backward has a drawing
            has_drawing_nearby = False
            curr = cap_p._p.getprevious()
            for _ in range(2):
                if curr is not None:
                    if "w:drawing" in curr.xml or "w:pict" in curr.xml:
                        has_drawing_nearby = True
                        break
                    curr = curr.getprevious()
            
            if has_drawing_nearby:
                print(f"Fig {f}: already has drawing nearby before caption.")
            else:
                print(f"Fig {f}: Inserting {img_file} directly before caption")
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                run = p_img.add_run()
                img_path = os.path.join(MEDIA_DIR, img_file)
                run.add_picture(img_path, width=Inches(w))
                cap_p._p.addprevious(p_img._p)

    # Step 2: For ALL Figures 1 to 12, collapse ANY empty paragraphs between the image and caption
    for f in range(1, 13):
        cap_p = None
        for p in doc.paragraphs:
            txt = p.text.strip()
            if txt.startswith(f"Figure {f}:") or txt.startswith(f"Figure {f} :"):
                cap_p = p
                break
        
        if not cap_p:
            continue
        
        # Traverse backward to find drawing
        curr = cap_p._p.getprevious()
        empty_to_remove = []
        found_drawing = False
        while curr is not None:
            xml = curr.xml
            if "w:drawing" in xml or "w:pict" in xml:
                found_drawing = True
                break
            # check if empty
            p_obj = docx.text.paragraph.Paragraph(curr, doc)
            if len(p_obj.text.strip()) == 0:
                empty_to_remove.append(curr)
            else:
                # Hit text paragraph without finding drawing
                break
            curr = curr.getprevious()
        
        if found_drawing and empty_to_remove:
            print(f"Fig {f:2d}: Removing {len(empty_to_remove)} empty paragraph(s) between image and caption")
            for elem in empty_to_remove:
                elem.getparent().remove(elem)

    # Step 3: Save to out_path
    try:
        doc.save(out_path)
        print(f"Successfully saved to: {out_path}")
    except PermissionError:
        alt_path = out_path.replace(".docx", "_ready_to_replace.docx")
        print(f"WARNING: {out_path} is currently locked! Saving to {alt_path} instead.")
        doc.save(alt_path)
        return alt_path

    # Step 4: Verification
    verify_doc = docx.Document(out_path)
    total_drawings = [p for p in verify_doc.paragraphs if "w:drawing" in p._p.xml]
    print(f"\n--- Verification of {os.path.basename(out_path)} ---")
    print(f"Total drawings in document: {len(total_drawings)}")

    all_ok = True
    for f in range(1, 13):
        for i, p in enumerate(verify_doc.paragraphs):
            txt = p.text.strip()
            if txt.startswith(f"Figure {f}:") or txt.startswith(f"Figure {f} :"):
                prev_p = verify_doc.paragraphs[i-1] if i > 0 else None
                prev_has_img = ("w:drawing" in prev_p._p.xml) if prev_p else False
                self_has_img = "w:drawing" in p._p.xml
                is_paired = prev_has_img or self_has_img
                if not is_paired:
                    all_ok = False
                status = "PASS [Image directly above caption]" if prev_has_img else ("PASS [Image in caption]" if self_has_img else "FAIL [MISSING IMAGE!]")
                print(f"Figure {f:2d} (P[{i:3d}]): {status}")
                break

    print(f"All 12 figures paired with images: {all_ok}")
    return out_path

if __name__ == "__main__":
    fix_document(DOC_HIGHLIGHTED)
    alt = fix_document(DOC_NOCOLOUR)
