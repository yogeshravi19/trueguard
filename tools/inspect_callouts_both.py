import docx
import re

for name in ['Toward Trustworthy Large Language Models_coloured.docx', 'Toward Trustworthy Large Language Models_standard.docx']:
    path = rf'E:\trueguard\CAPSTONE\{name}'
    doc = docx.Document(path)
    print("=" * 60)
    print(f"VERIFYING IN-TEXT REFERENCES IN: {name}")
    print("=" * 60)
    
    # Figures 1 to 12
    for f in range(1, 13):
        callouts = []
        caption = None
        for i, p in enumerate(doc.paragraphs):
            t = p.text.strip()
            if t.startswith(f"Figure {f}:") or t.startswith(f"Figure {f} :"):
                caption = (i, t[:60])
            elif re.search(rf"\bFigure\s+{f}\b", t, re.IGNORECASE):
                callouts.append((i, t))
        cap_str = f"P[{caption[0]}]" if caption else "MISSING"
        print(f"Figure {f:2d}: Caption at {cap_str} | In-Text Callouts: {len(callouts)}")
        for c in callouts:
            # Extract sentence containing Figure X
            sentences = [s.strip() for s in c[1].split(".") if re.search(rf"\bFigure\s+{f}\b", s, re.IGNORECASE)]
            for s in sentences:
                print(f"   -> Callout [P{c[0]}]: \"{s}.\"")

    print("\n" + "-" * 40)
    # Tables 1 to 4
    for t in range(1, 5):
        callouts = []
        caption = None
        for i, p in enumerate(doc.paragraphs):
            txt = p.text.strip()
            if txt.startswith(f"Table {t}:") or txt.startswith(f"Table {t} :"):
                caption = (i, txt[:60])
            elif re.search(rf"\bTable\s+{t}\b", txt, re.IGNORECASE):
                callouts.append((i, txt))
        cap_str = f"P[{caption[0]}]" if caption else "MISSING"
        print(f"Table {t:2d}: Caption at {cap_str} | In-Text Callouts: {len(callouts)}")
        for c in callouts:
            sentences = [s.strip() for s in c[1].split(".") if re.search(rf"\bTable\s+{t}\b", s, re.IGNORECASE)]
            for s in sentences:
                print(f"   -> Callout [P{c[0]}]: \"{s}.\"")
    print("\n")
