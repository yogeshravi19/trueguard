from pypdf import PdfReader
import re

reader = PdfReader('FINAL_SUBMISSION/small changes/FINAL_REPORT_VERIFIED.pdf')
print(f"Total pages in PDF: {len(reader.pages)}")

# Print footer and top of each page
page_map = []
for p_idx, page in enumerate(reader.pages):
    text = page.extract_text()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    first_line = lines[0] if lines else "EMPTY"
    last_line = lines[-1] if lines else "EMPTY"
    
    # Check if there is a chapter or section heading on this page
    headings = []
    for l in lines:
        if re.match(r'^(CHAPTER\s+\d+|\d+\.\d+|\bTABLE\s+\d+|\bFIGURE\s+\d+|\bREFERENCES\b|\bAPPENDICES\b|\bABSTRACT\b|\bACKNOWLEDGEMENT\b|\bCONTENTS\b|\bLIST OF\b)', l, re.IGNORECASE):
            if len(l) < 90:
                headings.append(l)
    
    page_map.append({
        'pdf_page': p_idx + 1,
        'first_line': first_line[:60],
        'last_line': last_line,
        'headings': headings
    })

print("\n=== Sample of Page Map ===")
for p in page_map[:20]:
    print(f"PDF P{p['pdf_page']:2d} (footer: '{p['last_line']}'): headings={p['headings']}")

print("\n=== Main Chapters (from PDF page 14 onwards) ===")
for p in page_map[13:]:
    if p['headings']:
        print(f"PDF P{p['pdf_page']:2d} (footer: '{p['last_line']}'): headings={p['headings']}")
