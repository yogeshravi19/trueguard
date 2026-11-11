import docx
import re
import os

files = [
    r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models_coloured.docx",
    r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models_standard.docx"
]

for fpath in files:
    fname = os.path.basename(fpath)
    print("=" * 70)
    print(f"AUDITING (READ-ONLY): {fname}")
    print("=" * 70)
    doc = docx.Document(fpath)
    full_text = " ".join(p.text for p in doc.paragraphs)
    
    # 1. Total paragraphs, tables, drawings, highlights
    drawings = [p for p in doc.paragraphs if "w:drawing" in p._p.xml or "w:pict" in p._p.xml]
    hl_count = sum(1 for p in doc.paragraphs for r in p.runs if r.font.highlight_color is not None)
    print(f"Paragraphs: {len(doc.paragraphs)} | Tables: {len(doc.tables)} | Drawings: {len(drawings)} | Highlights: {hl_count}")
    
    # 2. Check Abstract
    abs_p = ""
    for p in doc.paragraphs[:15]:
        if len(p.text) > 100 and ("hallucination" in p.text.lower() or "large language models" in p.text.lower()):
            abs_p = p.text
            break
    print(f"Abstract length: {len(abs_p.split())} words")
    print(f"  Contains ~65%: {'65%' in abs_p}")
    print(f"  Contains 40 studies: {'40' in abs_p}")
    print(f"  Contains PRISMA: {'PRISMA' in abs_p}")
    print(f"  Contains TRUEGUARD: {'TRUEGUARD' in abs_p}")
    
    # 3. Check Point 3: Figures 1-12
    print("\n--- FIGURE AUDIT (Point 3) ---")
    fig_ok = True
    for f in range(1, 13):
        cap_p = None
        callouts = []
        for i, p in enumerate(doc.paragraphs):
            t = p.text.strip()
            if t.startswith(f"Figure {f}:") or t.startswith(f"Figure {f} :"):
                cap_p = (i, t[:50])
            elif re.search(rf"\bFigure\s+{f}\b", t):
                callouts.append((i, t[:50]))
        
        has_img_above = False
        if cap_p and cap_p[0] > 0:
            has_img_above = ("w:drawing" in doc.paragraphs[cap_p[0]-1]._p.xml or "w:pict" in doc.paragraphs[cap_p[0]-1]._p.xml)
            if not has_img_above and cap_p[0] > 1:
                has_img_above = ("w:drawing" in doc.paragraphs[cap_p[0]-2]._p.xml or "w:pict" in doc.paragraphs[cap_p[0]-2]._p.xml)
        
        call_ok = len(callouts) > 0
        status = "PASS" if (call_ok and cap_p and (has_img_above or "w:drawing" in doc.paragraphs[cap_p[0]]._p.xml)) else "FAIL"
        if status == "FAIL": fig_ok = False
        print(f"  Fig {f:2d}: [{status}] Callouts in prose={len(callouts)} (P{[c[0] for c in callouts]}) | Caption at P[{cap_p[0] if cap_p else 'None'}] | ImgPresent={has_img_above}")
    
    # 4. Check Point 3: Tables 1-4
    print("\n--- TABLE AUDIT (Point 3) ---")
    tbl_ok = True
    for t in range(1, 5):
        cap_p = None
        callouts = []
        for i, p in enumerate(doc.paragraphs):
            txt = p.text.strip()
            if txt.startswith(f"Table {t}:") or txt.startswith(f"Table {t} :"):
                cap_p = (i, txt[:50])
            elif re.search(rf"\bTable\s+{t}\b", txt):
                callouts.append((i, txt[:50]))
        call_ok = len(callouts) > 0
        status = "PASS" if (call_ok and cap_p) else "FAIL"
        if status == "FAIL": tbl_ok = False
        print(f"  Table {t}: [{status}] Callouts in prose={len(callouts)} (P{[c[0] for c in callouts]}) | Caption at P[{cap_p[0] if cap_p else 'None'}]")

    # 5. Check Reviewer Points
    print("\n--- REVIEWER POINTS AUDIT ---")
    rev_checks = {
        "R1.1 Control Architecture / TRUEGUARD": "TRUEGUARD" in full_text and "closed-loop" in full_text,
        "R1.2 PRISMA 40 corpus and 128 exclusions": "40" in full_text and "128" in full_text and "168" in full_text,
        "R1.3 Computational latency and LLM-Check 450x": "450" in full_text and "latency" in full_text.lower(),
        "R1.4 AUROC vs F1 trade-offs": "AUROC" in full_text and "F1" in full_text,
        "R2.1 54 prompt heuristics excluded": "prompt heuristics" in full_text.lower() and "54" in full_text,
        "R2.2 Six-pillar taxonomy": all(f"Pillar {i}" in full_text for i in range(1, 7)),
        "R2.3 Operational definitions (intrinsic/extrinsic)": "intrinsic" in full_text.lower() and "extrinsic" in full_text.lower(),
        "R2.4 Evaluation benchmarks (Table 2 / TrustLLM)": "TrustLLM" in full_text and "Table 2" in full_text,
        "R2.5 Mitigation and BehCal / ExpandR (Table 3)": "BehCal" in full_text and "ExpandR" in full_text and "Table 3" in full_text,
        "R2.6 Explainability and User Trust (Figure 9)": "Figure 9" in full_text and "user trust" in full_text.lower(),
        "R2.7 Five Research Gaps": "Research Gap" in full_text or "five major research gaps" in full_text.lower(),
    }
    all_rev_ok = True
    for k, v in rev_checks.items():
        if not v: all_rev_ok = False
        print(f"  [{ 'PASS' if v else 'FAIL' }] {k}")
    
    print(f"\nOVERALL VERDICT FOR {fname}:")
    print(f"  Figures Point 3: {'ALL REFERENCED AND PAIRED' if fig_ok else 'NEEDS ATTENTION'}")
    print(f"  Tables Point 3: {'ALL REFERENCED AND CAPTIONED' if tbl_ok else 'NEEDS ATTENTION'}")
    print(f"  Reviewer Points: {'ALL 11 REVIEWER POINTS SATISFIED' if all_rev_ok else 'NEEDS ATTENTION'}\n")
