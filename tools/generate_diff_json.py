import docx
import json

doc_before = docx.Document(r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx.bak_tech_check")
doc_after = docx.Document(r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx")

# Let's inspect each specific paragraph we modified:
# 1. Figure 1 reference in Introduction
# 2. Figure 1 caption
# 3. Figure 2 & Table 1 reference in Section 2
# 4. Figure 2 caption
# 5. Figure 3 caption
# 6. Figure 4 reference in Pillar 3
# 7. Figure 4 caption
# 8. Figure 5 & 6 reference in Pillar 4
# 9. Figure 5 caption
# 10. Figure 6 caption
# 11. Table 2 caption (inserted before Table index 1)
# 12. Figure 7 & 8 reference in Pillar 5
# 13. Figure 7 caption
# 14. Figure 8 caption
# 15. Table 3 reference & caption (inserted before Table index 2)
# 16. Figure 9 reference in Pillar 6
# 17. Figure 9 caption
# 18. Figure 10, 11, 12 & Table 4 reference in Section 4
# 19. Figure 10 caption
# 20. Table 4 caption
# 21. Figure 11 caption
# 22. Figure 12 caption

# Let's find each paragraph by unique signature
changes = []

# Figure 1 callout
for p_b in doc_before.paragraphs:
    if "phenomenon commonly termed hallucination" in p_b.text:
        for p_a in doc_after.paragraphs:
            if "phenomenon commonly termed hallucination" in p_a.text:
                changes.append({
                    "item": "Figure 1 In-Text Callout (Section I: Introduction)",
                    "before": p_b.text.strip(),
                    "after": p_a.text.strip()
                })
        break

# Figure 1 caption
for p_b in doc_before.paragraphs:
    if "Semantic Entropy excels at detecting extrinsic hallucinations" in p_b.text:
        for p_a in doc_after.paragraphs:
            if "Semantic Entropy excels at detecting extrinsic hallucinations" in p_a.text:
                changes.append({
                    "item": "Figure 1 Caption",
                    "before": p_b.text.strip(),
                    "after": p_a.text.strip()
                })
        break

# Figure 2 & Table 1 callout
for p_b in doc_before.paragraphs:
    if "Included: A final corpus of 40 representative studies" in p_b.text:
        for p_a in doc_after.paragraphs:
            if "Included: A final corpus of 40 representative studies" in p_a.text:
                changes.append({
                    "item": "Figure 2 & Table 1 In-Text Callout (Section II: Methodology)",
                    "before": p_b.text.strip(),
                    "after": p_a.text.strip()
                })
        break

# Figure 2 caption
for p_b in doc_before.paragraphs:
    if "PRISMA flow diagram showing the literature selection process" in p_b.text:
        for p_a in doc_after.paragraphs:
            if "PRISMA flow diagram showing the literature selection process" in p_a.text:
                changes.append({
                    "item": "Figure 2 Caption",
                    "before": p_b.text.strip(),
                    "after": p_a.text.strip()
                })
        break

# Figure 4 callout
for p_b in doc_before.paragraphs:
    if "At their fundamental level, transformers are attention machineries" in p_b.text:
        for p_a in doc_after.paragraphs:
            if "At their fundamental level, transformers are attention machineries" in p_a.text:
                changes.append({
                    "item": "Figure 4 In-Text Callout (Section III: Pillar 3)",
                    "before": p_b.text.strip(),
                    "after": p_a.text.strip()
                })
        break

# Figure 5 & 6 callout
for p_b in doc_before.paragraphs:
    if "The thesaurus of any body of research is good benchmarks" in p_b.text:
        for p_a in doc_after.paragraphs:
            if "Rigorous benchmarking is essential to distinguish" in p_a.text:
                changes.append({
                    "item": "Figure 5 & 6 In-Text Callout (Section III: Pillar 4)",
                    "before": p_b.text.strip(),
                    "after": p_a.text.strip()
                })
        break

# Figure 6 caption
for p_b in doc_before.paragraphs:
    if p_b.text.strip() == "Figure 6:":
        for p_a in doc_after.paragraphs:
            if p_a.text.strip().startswith("Figure 6: Percentage performance gains"):
                changes.append({
                    "item": "Figure 6 Caption",
                    "before": "Figure 6: [Orphan line] + 'Calibration and explainability methods... yield the largest percentage gains...'",
                    "after": p_a.text.strip()
                })
        break

# Table 2 caption
changes.append({
    "item": "Table 2 Caption & Placement (Section III: Pillar 4)",
    "before": "[MISSING - Table was placed immediately after text without an explicit 'Table 2:' caption header]",
    "after": "Table 2: Key benchmarks, evaluation frameworks, and diagnostic dimensions for LLM hallucination assessment."
})

# Figure 7 & 8 callout
for p_b in doc_before.paragraphs:
    if p_b.text.startswith("Behaviorally Calibrated Reinforcement Learning: Wu."):
        for p_a in doc_after.paragraphs:
            if p_a.text.startswith("Behaviorally Calibrated Reinforcement Learning: Wu."):
                changes.append({
                    "item": "Figure 7 & 8 In-Text Callout (Section III: Pillar 5)",
                    "before": p_b.text.strip(),
                    "after": p_a.text.strip()
                })
        break

# Figure 8 caption
for p_b in doc_before.paragraphs:
    if "Figure 8:" in p_b.text:
        for p_a in doc_after.paragraphs:
            if p_a.text.startswith("Figure 8: Expected calibration error"):
                changes.append({
                    "item": "Figure 8 Caption",
                    "before": "Figure 8: [Orphan line split across 3 paragraphs: 'Figure 8:' + 'BehCal RL achieves...' + 'accuracy.']",
                    "after": p_a.text.strip()
                })
        break

# Table 3 callout & caption
for p_b in doc_before.paragraphs:
    if p_b.text.startswith("What this pillar tells us. Mitigating hallucinations is not just about catching"):
        for p_a in doc_after.paragraphs:
            if p_a.text.startswith("What this pillar tells us. Mitigating hallucinations is not just about catching"):
                changes.append({
                    "item": "Table 3 In-Text Callout & Caption (Section III: Pillar 5)",
                    "before": "In-Text: " + p_b.text.strip() + " | Caption: [MISSING caption header before Table]",
                    "after": "In-Text: " + p_a.text.strip() + " | Caption: 'Table 3: Comparative summary of hallucination mitigation frameworks, correction mechanisms, and operational access paradigms.'"
                })
        break

# Figure 9 callout
for p_b in doc_before.paragraphs:
    if "All the above is geared towards the end result that people should be able to trust" in p_b.text:
        for p_a in doc_after.paragraphs:
            if "All the above is geared towards the end result that people should be able to trust" in p_a.text:
                changes.append({
                    "item": "Figure 9 In-Text Callout (Section III: Pillar 6)",
                    "before": p_b.text.strip(),
                    "after": p_a.text.strip()
                })
        break

# Figure 9 caption
for p_b in doc_before.paragraphs:
    if "Figure 9:" in p_b.text:
        for p_a in doc_after.paragraphs:
            if p_a.text.startswith("Figure 9: Impact of explanation framing"):
                changes.append({
                    "item": "Figure 9 Caption",
                    "before": "Figure 9: [Orphan line split across 2 paragraphs: 'Figure 9:' + 'Explanation framing boosts user trust...']",
                    "after": p_a.text.strip()
                })
        break

# Figure 10, 11, 12 & Table 4 callout
for p_b in doc_before.paragraphs:
    if "Where Are the Explanations? The most notable weakness, perhaps:" in p_b.text:
        for p_a in doc_after.paragraphs:
            if "Where Are the Explanations? The most notable weakness, perhaps:" in p_a.text:
                changes.append({
                    "item": "Figure 10, 11, 12 & Table 4 In-Text Callouts (Section IV: Comparative Analysis)",
                    "before": p_b.text.strip(),
                    "after": p_a.text.strip()
                })
        break

# Figure 10 caption
for p_b in doc_before.paragraphs:
    if "Figure 10:" in p_b.text:
        for p_a in doc_after.paragraphs:
            if p_a.text.startswith("Figure 10: AUROC versus F1"):
                changes.append({
                    "item": "Figure 10 Caption",
                    "before": "Figure 10: [Orphan line split across 2 paragraphs: 'Figure 10:' + 'AUROC versus F1 scatter showing SEP...']",
                    "after": p_a.text.strip()
                })
        break

# Table 4 caption
for p_b in doc_before.paragraphs:
    if "Table 4: Comparative analysis of hallucination detection methods" in p_b.text:
        for p_a in doc_after.paragraphs:
            if "Table 4: Comparative analysis of hallucination detection methods" in p_a.text:
                changes.append({
                    "item": "Table 4 Caption",
                    "before": p_b.text.strip(),
                    "after": p_a.text.strip()
                })
        break

print(f"Extracted {len(changes)} target comparison pairs.")
with open(r"E:\trueguard\tools\diff_results.json", "w", encoding="utf-8") as f:
    json.dump(changes, f, indent=2)

print("Saved to diff_results.json successfully!")
