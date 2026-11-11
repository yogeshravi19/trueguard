import docx

doc_before = docx.Document(r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx.bak_tech_check")
doc_after = docx.Document(r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx")

# Let's inspect each item we targeted:
# 1. Figure 1 reference & caption
# 2. Figure 2 & Table 1 reference & caption
# 3. Figure 3 caption
# 4. Figure 4 reference & caption
# 5. Figure 5 & 6 reference & captions
# 6. Table 2 caption
# 7. Figure 7 & 8 reference & captions
# 8. Table 3 reference & caption
# 9. Figure 9 reference & caption
# 10. Figure 10, 11, 12 & Table 4 references & captions

items = [
    ("Figure 1 in-text reference", "phenomenon commonly termed hallucination"),
    ("Figure 1 caption", "Semantic Entropy excels at detecting extrinsic hallucinations"),
    ("Figure 2 & Table 1 in-text reference", "Included: A final corpus of 40 representative studies"),
    ("Figure 2 caption", "PRISMA flow diagram showing the literature selection process"),
    ("Figure 3 caption", "SEP matches or exceeds Semantic Entropy accuracy"),
    ("Figure 4 in-text reference", "At their fundamental level, transformers are attention machineries"),
    ("Figure 4 caption", "LLM-Check's black-box variant achieves" if True else "LLM Check's black box variant"),
    ("Figure 5 & 6 in-text reference", "Rigorous benchmarking is essential" if True else "The thesaurus of any body of research"),
    ("Figure 5 caption", "Proprietary models outscore open"),
    ("Figure 6 caption", "Percentage performance gains achieved" if True else "Figure 6:"),
    ("Table 2 caption & reference", "What this pillar tells us. Benchmarks are improving"),
    ("Figure 7 & 8 in-text reference", "Behaviorally Calibrated Reinforcement Learning: Wu"),
    ("Figure 7 caption", "ExpandR's joint LLM"),
    ("Figure 8 caption", "Expected calibration error across three benchmarks" if True else "Figure 8:"),
    ("Table 3 in-text reference", "What this pillar tells us. Mitigating hallucinations is not just about"),
    ("Figure 9 in-text reference", "All the above is geared towards the end result"),
    ("Figure 9 caption", "Impact of explanation framing on human user trust" if True else "Figure 9:"),
    ("Figure 10, 11, 12 & Table 4 in-text reference", "Where Are the Explanations? The most notable weakness"),
    ("Figure 10 caption", "AUROC versus F1 score scatter distribution" if True else "Figure 10:"),
    ("Table 4 caption", "Table 4: Comparative analysis"),
    ("Figure 11 caption", "Figure 11: AUROC vs. F1 Score"),
    ("Figure 12 caption", "Figure 12: Efficiency trade"),
]

def find_paragraph(doc, kw1, kw2=None):
    for p in doc.paragraphs:
        t = p.text.strip()
        if kw1.lower() in t.lower():
            return t
        if kw2 and kw2.lower() in t.lower():
            return t
    return "[NOT FOUND]"

print("=== EXACT BEFORE VS AFTER AUDIT ===")
for label, kw in items:
    # Look up in before and after
    t_before = ""
    for p in doc_before.paragraphs:
        t = p.text.strip()
        if any(w in t.lower() for w in kw.lower().split()[:4]):
            t_before = t
            break
            
    t_after = ""
    for p in doc_after.paragraphs:
        t = p.text.strip()
        if any(w in t.lower() for w in kw.lower().split()[:4]):
            t_after = t
            break
            
    print(f"\n--- {label} ---")
    print(f"BEFORE:\n{t_before}")
    print(f"AFTER:\n{t_after}")
