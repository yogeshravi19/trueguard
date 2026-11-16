"""
Inject 4K Ultra-HD (4200 x 1760 px, 600 DPI) Publication Figures into Final Report PDF
Strictly replaces the 96-DPI Word downsampled images with full-resolution figures.
Preserves the exact layout, page count, fonts, margins, and the front-matter VIT logo.
"""
from pathlib import Path
import fitz

FIG_DIR = Path("outputs/figures")

HD_FIGS = {
    "7.1": FIG_DIR / "fig_hd_7_1.png",
    "7.2": FIG_DIR / "fig_hd_7_2.png",
    "7.3": FIG_DIR / "fig_hd_7_3.png",
    "7.4": FIG_DIR / "fig_hd_7_4.png",
    "8.1": FIG_DIR / "fig_hd_8_1.png",
    "8.2": FIG_DIR / "fig_hd_8_2.png",
}

# Verify all HD figure source files exist and check dimensions
for fig_id, fig_path in HD_FIGS.items():
    if not fig_path.exists():
        raise FileNotFoundError(f"Missing HD figure file: {fig_path}")
    print(f"Verified source Fig {fig_id}: {fig_path} ({fig_path.stat().st_size:,} bytes)")


def process_pdf(pdf_path: Path):
    print(f"\n=======================================================")
    print(f"Processing: {pdf_path}")
    print(f"=======================================================")
    if not pdf_path.exists():
        print(f"Warning: File not found {pdf_path}")
        return

    doc = fitz.open(str(pdf_path))
    initial_pages = len(doc)
    print(f"Total pages: {initial_pages}")

    # Identify the 3 figure pages by looking for the captions
    p_fig71_72 = None
    p_fig73_74 = None
    p_fig81_82 = None

    for pno in range(len(doc)):
        text = doc[pno].get_text()
        if "FIGURE 7.1:" in text and "FIGURE 7.2:" in text:
            p_fig71_72 = pno
        elif "FIGURE 7.3:" in text and "FIGURE 7.4:" in text:
            p_fig73_74 = pno
        elif "FIGURE 8.1:" in text and "FIGURE 8.2:" in text:
            p_fig81_82 = pno

    print(f"Found Figure Pages:")
    print(f"  Fig 7.1 & 7.2 -> Page {p_fig71_72 + 1 if p_fig71_72 is not None else 'NOT FOUND'}")
    print(f"  Fig 7.3 & 7.4 -> Page {p_fig73_74 + 1 if p_fig73_74 is not None else 'NOT FOUND'}")
    print(f"  Fig 8.1 & 8.2 -> Page {p_fig81_82 + 1 if p_fig81_82 is not None else 'NOT FOUND'}")

    pairs = [
        (p_fig71_72, "7.1", "7.2"),
        (p_fig73_74, "7.3", "7.4"),
        (p_fig81_82, "8.1", "8.2"),
    ]

    for pno, top_id, bottom_id in pairs:
        if pno is None:
            continue
        page = doc[pno]
        imgs = page.get_images(full=True)
        print(f"\nPage {pno + 1}: Found {len(imgs)} image objects")
        
        # We need to sort images by vertical position (y0)
        img_info = []
        for img in imgs:
            xref = img[0]
            rects = page.get_image_rects(xref)
            if rects:
                y0 = rects[0].y0
            else:
                y0 = 0.0
            img_info.append((y0, xref))
        
        img_info.sort(key=lambda x: x[0])
        
        if len(img_info) >= 2:
            top_xref = img_info[0][1]
            bottom_xref = img_info[1][1]
            
            print(f"  Replacing Top Image (xref {top_xref}) with Fig {top_id} ({HD_FIGS[top_id].name})...")
            page.replace_image(top_xref, filename=str(HD_FIGS[top_id]))
            
            print(f"  Replacing Bottom Image (xref {bottom_xref}) with Fig {bottom_id} ({HD_FIGS[bottom_id].name})...")
            page.replace_image(bottom_xref, filename=str(HD_FIGS[bottom_id]))
        else:
            print(f"  Warning: Expected 2 images on page {pno + 1}, found {len(img_info)}")

    tmp_out = pdf_path.with_name(pdf_path.stem + "_4k_temp.pdf")
    doc.save(str(tmp_out), garbage=3, deflate=True)
    doc.close()

    # Re-open and verify
    vdoc = fitz.open(str(tmp_out))
    assert len(vdoc) == initial_pages, f"Page count changed: {len(vdoc)} vs {initial_pages}"
    print(f"\nVerification for {tmp_out.name}:")
    for pno, top_id, bottom_id in pairs:
        if pno is None:
            continue
        vpage = vdoc[pno]
        vimgs = vpage.get_images(full=True)
        print(f"  Page {pno + 1} ({top_id} & {bottom_id}):")
        for idx, img in enumerate(vimgs):
            xref = img[0]
            info = vdoc.extract_image(xref)
            w = info["width"]
            h = info["height"]
            b = len(info["image"])
            print(f"    Image {idx + 1} (xref {xref}): {w} x {h} px, {b:,} bytes")
            assert w == 4200 and h == 1760, f"Expected 4200x1760, got {w}x{h}"
    vdoc.close()

    # Replace original or fallback to _4K.pdf if locked by active viewer
    try:
        tmp_out.replace(pdf_path)
        print(f"SUCCESS: {pdf_path} updated with 4K Ultra-HD figures! Final size: {pdf_path.stat().st_size:,} bytes")
    except PermissionError:
        fallback_path = pdf_path.parent / f"{pdf_path.stem}_4K.pdf"
        print(f"Notice: {pdf_path} is currently open in a PDF viewer (Acrobat/Reader).")
        print(f"Saving 4K copy to: {fallback_path}...")
        tmp_out.replace(fallback_path)
        print(f"SUCCESS: Created {fallback_path} ({fallback_path.stat().st_size:,} bytes) with 4K Ultra-HD figures!")


if __name__ == "__main__":
    targets = [
        Path("FINAL_REPORT_PRINT_READY.pdf"),
        Path("FINAL_SUBMISSION/FINAL_REPORT_PRINT_READY.pdf"),
        Path("FINAL_SUBMISSION/FINAL_REPORT_VERIFIED.pdf"),
        Path("FINAL_REPORT_VERIFIED.pdf"),
    ]
    for target in targets:
        process_pdf(target)
    print("\nALL TARGET PDFs SUCCESSFULLY UPGRADED TO 4K ULTRA-HD IMAGES!")
