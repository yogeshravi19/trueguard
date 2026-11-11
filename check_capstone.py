import docx
import re

doc = docx.Document(r'E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx')
full_text = '\n'.join([p.text for p in doc.paragraphs])

print('=== TOTAL WORDS ===')
words = len(full_text.split())
print(f'Total words: {words}')

print('\n=== CHECKING SENSITIVE NUMBERS & CLAIMS ===')
if '65%' in full_text or '65 %' in full_text:
    print('WARNING: Found 65% in text!')
else:
    print('PASS: No 65% claim found.')

if 'loose survey' in full_text.lower():
    print('WARNING: Found loose survey phrase!')
else:
    print('PASS: No loose survey phrase found.')

print('\n=== CHECKING PRISMA NUMBERS ===')
for num in ['688', '196', '492', '324', '168', '128', '40']:
    if num in full_text:
        print(f'PASS: Found PRISMA number {num}')
    else:
        print(f'WARNING: Missing PRISMA number {num}')

print('\n=== CHECKING 6 LANDMARK PAPERS ===')
for paper in ['SelfCheckGPT', 'TruthfulQA', 'FActScore', 'Chain-of-Verification', 'RAG', 'Self-RAG']:
    if paper.lower() in full_text.lower():
        print(f'PASS: Found landmark paper {paper}')
    else:
        print(f'WARNING: Missing landmark paper {paper}')

print('\n=== CHECKING TRUEGUARD CONTROL CONCEPTS ===')
for concept in ['Sensor Layer', 'Signal Fusion', 'Fault Detection', 'Tiered Closed-Loop', 'Explainability']:
    if concept.lower() in full_text.lower():
        print(f'PASS: Found control concept {concept}')
    else:
        print(f'WARNING: Missing control concept {concept}')

print('\n=== CHECKING AI BUZZWORDS / HALLMARKS ===')
buzzwords = ['delve', 'testament', 'tapestry', 'beacon', 'paramount', 'plethora', 'foster', 'revolutionize', 'ever-evolving', 'morsel', 'dyspeptic']
found_buzz = [b for b in buzzwords if re.search(r'\b' + b + r'\b', full_text, re.IGNORECASE)]
print(f'AI buzzwords found: {found_buzz}')

print('\n=== CHECKING TABLES ===')
print(f'Total tables: {len(doc.tables)}')
for i, t in enumerate(doc.tables):
    rows = len(t.rows)
    cols = len(t.columns)
    print(f'Table {i+1}: {rows} rows x {cols} cols')
    header = [c.text.strip().replace("\n", " ") for c in t.rows[0].cells]
    print(f'  Headers: {header}')

print('\n=== CHECKING REFERENCES COUNT ===')
ref_matches = re.findall(r'\[(\d+)\]', full_text)
if ref_matches:
    int_refs = [int(x) for x in ref_matches if int(x) <= 100]
    print(f'Max in-text reference cited: [{max(int_refs)}]')
    print(f'Total citations count: {len(int_refs)}')

print('\n=== CHECKING SECTIONS 7 & 8 & BACK MATTER ===')
for p in doc.paragraphs[-40:]:
    txt = p.text.strip()
    if any(k in txt for k in ['Future Research', 'Conclusion', 'Data Availability', 'Conflict of Interest', 'Funding', 'References']):
        print('  Found:', txt[:80])
