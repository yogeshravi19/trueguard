import docx
import re

doc = docx.Document('FINAL_SUBMISSION/FINAL_REPORT_VERIFIED.docx')

print(f"Total paragraphs: {len(doc.paragraphs)}")

# Check P388
print("\n=== Paragraph 385 to 395 ===")
for i in range(385, min(395, len(doc.paragraphs))):
    print(f"P{i:3d}: {doc.paragraphs[i].text}")

# Check figures mentioned or captions
print("\n=== Figure Captions in Body ===")
for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if re.match(r'^Figure\s+\d+\.\d+', text, re.IGNORECASE):
        print(f"P{i:3d}: {text}")

# Check Table Captions in Body
print("\n=== Table Captions in Body ===")
for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if re.match(r'^Table\s+\d+\.\d+', text, re.IGNORECASE) or re.match(r'^Table\s+A\d+\.\d+', text, re.IGNORECASE):
        print(f"P{i:3d}: {text}")

# Check math equations / broken symbols
print("\n=== Checking for Broken Math / Artifacts ===")
for i, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if any(k in text for k in ['\\frac', '\\sum', '\\sigma', '\\tau', '$$', '', 'TODO', 'TBD', 'XXX']):
        print(f"P{i:3d} has math/symbol artifact: {text[:100]}")
