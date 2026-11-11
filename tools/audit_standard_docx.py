import docx
import re
import os

path = r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models_standard.docx"
doc = docx.Document(path)

print("==================================================")
print("COMPREHENSIVE AUDIT OF Toward Trustworthy Large Language Models_standard.docx")
print("==================================================")

# 1. Title and Abstract
print("\n--- 1. TITLE & ABSTRACT ---")
for i in range(min(15, len(doc.paragraphs))):
    t = doc.paragraphs[i].text.strip()
    if t:
        print(f"P[{i}]: {t[:100]}...")

# Extract abstract text
abstract_text = ""
for i, p in enumerate(doc.paragraphs[:15]):
    if p.text.strip().startswith("Abstract"):
        abstract_text = p.text.strip()
        break

print(f"\nAbstract Word Count: {len(abstract_text.split())} words")
print(f"Contains '~65%' claim: {'65%' in abstract_text}")
print(f"Contains '40' papers: {'40' in abstract_text}")
print(f"Abstract preview: {abstract_text[:200]}...")

# 2. Figures & Images
print("\n--- 2. FIGURES & DRAWINGS AUDIT ---")
drawings = [p for p in doc.paragraphs if "w:drawing" in p._p.xml or "w:pict" in p._p.xml]
print(f"Total drawings in document: {len(drawings)}/12")

for f in range(1, 13):
    cap_idx = None
    cap_text = ""
    for i, p in enumerate(doc.paragraphs):
        t = p.text.strip()
        if t.startswith(f"Figure {f}:") or t.startswith(f"Figure {f} :"):
            cap_idx = i
            cap_text = t
            break
    
    if cap_idx is not None:
        prev_p = doc.paragraphs[cap_idx - 1] if cap_idx > 0 else None
        prev_has_img = ("w:drawing" in prev_p._p.xml or "w:pict" in prev_p._p.xml) if prev_p else False
        self_has_img = "w:drawing" in doc.paragraphs[cap_idx]._p.xml
        
        # Check callout in body prose
        # Search all paragraphs except caption
        body_callouts = []
        for i, p in enumerate(doc.paragraphs):
            if i != cap_idx and re.search(rf"\bFigure\s+{f}\b", p.text):
                body_callouts.append((i, p.text.strip()[:70]))
        
        status_img = "IMAGE OK" if (prev_has_img or self_has_img) else "MISSING IMAGE!"
        status_callout = f"CALLOUT OK (P[{body_callouts[0][0]}])" if body_callouts else "MISSING CALLOUT!"
        print(f"Fig {f:2d} | Caption P[{cap_idx:3d}] | {status_img} | {status_callout} | Caption: {cap_text[:50]}...")
    else:
        print(f"Fig {f:2d} | CAPTION NOT FOUND!")

# 3. Tables Audit
print("\n--- 3. TABLES & CALLOUTS AUDIT ---")
print(f"Total document tables: {len(doc.tables)}/4")
for t in range(1, 5):
    # Check table caption paragraph or callout
    callouts = []
    for i, p in enumerate(doc.paragraphs):
        if re.search(rf"\bTable\s+{t}\b", p.text):
            callouts.append((i, p.text.strip()[:70]))
    print(f"Table {t} mentions ({len(callouts)}): {[f'P[{c[0]}]: {c[1]}' for c in callouts]}")

# 4. Highlight check
hl_count = sum(1 for p in doc.paragraphs for r in p.runs if r.font.highlight_color is not None)
print(f"\n--- 4. HIGHLIGHTS AUDIT ---")
print(f"Total highlighted runs: {hl_count} (Standard clean submission version should have 0)")

# 5. Reviewer Points Audit
print("\n--- 5. REVIEWER POINTS / CRITICAL CONTENT CHECK ---")
full_text = " ".join(p.text for p in doc.paragraphs)

checks = {
    "PRISMA 40 papers corpus": "40" in full_text and "PRISMA" in full_text,
    "168 candidate articles screened": "168" in full_text,
    "128 excluded articles documented": "128" in full_text,
    "Exclusion reasons (prompt heuristics, baseline, redundant)": "prompt heuristics" in full_text.lower(),
    "LLM-Check 450x speedup": "450" in full_text and "LLM-Check" in full_text or "LLM Check" in full_text,
    "TrustLLM eight dimensions": "TrustLLM" in full_text and "eight" in full_text.lower(),
    "ExpandR joint optimization": "ExpandR" in full_text,
    "BehCal RL calibration error": "BehCal" in full_text,
    "Human trust explanation framing": "trust" in full_text.lower() and "explanation" in full_text.lower(),
    "TRUEGUARD control architecture": "TRUEGUARD" in full_text or "TrueGuard" in full_text,
    "Pillar 1: Internal States": "Pillar 1" in full_text,
    "Pillar 2: Uncertainty Quantification": "Pillar 2" in full_text,
    "Pillar 3: Attention Based Detection": "Pillar 3" in full_text,
    "Pillar 4: Evaluation and Benchmarking": "Pillar 4" in full_text,
    "Pillar 5: Mitigation": "Pillar 5" in full_text,
    "Pillar 6: Explainability and Human Trust": "Pillar 6" in full_text,
}

for k, v in checks.items():
    print(f"  [{'PASS' if v else 'FAIL'}] {k}")

# 6. Word Count & Structure
word_count = len(full_text.split())
print(f"\n--- 6. TOTAL MANUSCRIPT WORD COUNT ---")
print(f"Total Words: {word_count}")
