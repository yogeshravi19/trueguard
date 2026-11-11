import docx
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_COLOR_INDEX
import re

def process_manuscript(input_path, output_path, is_highlighted=True):
    doc = docx.Document(input_path)
    
    def set_run_style(run, text, highlight=is_highlighted, bold=False, italic=False):
        run.text = text
        run.font.name = "Times New Roman"
        run.bold = bold
        run.italic = italic
        if highlight:
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW
        else:
            run.font.highlight_color = None

    # 1. Figure 1 reference in P[15]
    for p in doc.paragraphs:
        if "phenomenon commonly termed hallucination" in p.text:
            # Check if it ends with (Figure 1) or needs clean wording
            t = p.text
            t_clean = re.sub(r'\(Figure\s+1\)', '', t).strip()
            # Replace with clear reference
            p.text = ""
            r1 = p.add_run(t_clean + " ")
            r1.font.name = "Times New Roman"
            r2 = p.add_run("As illustrated in Figure 1, hallucination manifestations span both intrinsic self-contradictions and extrinsic factual fabrications, which require distinct sensing strategies.")
            set_run_style(r2, r2.text, highlight=is_highlighted)
            break

    # Figure 1 caption
    for p in doc.paragraphs:
        if "Semantic Entropy excels at detecting extrinsic hallucinations" in p.text and p.text.strip().startswith("Figure 1"):
            p.text = "Figure 1: Semantic Entropy excels at detecting extrinsic hallucinations, while attention-based methods better capture intrinsic contradictions."
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(10)
            p.runs[0].italic = True
            break

    # 2. Figure 2 and Table 1 reference in Included paragraph
    for p in doc.paragraphs:
        if "Included: A final corpus of 40 representative studies met all eligibility" in p.text:
            base_text = "Included: A final corpus of 40 representative studies met all eligibility and quality criteria and was selected for synthesis."
            p.text = ""
            r1 = p.add_run(base_text + " ")
            r1.font.name = "Times New Roman"
            r2 = p.add_run("The sequential screening yield and quantitative filtering stages are illustrated in the PRISMA flow diagram (Figure 2), while the comprehensive database search strings, inclusion and exclusion criteria, and screening results are systematically summarized in Table 1.")
            set_run_style(r2, r2.text, highlight=is_highlighted)
            break

    # Figure 2 caption clean up
    for p in doc.paragraphs:
        if "PRISMA flow diagram showing the literature selection process from 688" in p.text:
            p.text = "Figure 2: PRISMA flow diagram showing the literature selection process from 688 initial records across five databases to the final synthesized corpus of 40 studies."
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(10)
            p.runs[0].italic = True
            break
            
    # Clear orphan "to the final corpus of 40 studies."
    for p in doc.paragraphs:
        if p.text.strip() == "to the final corpus of 40 studies.":
            p.text = ""
            break

    # 3. Figure 3 caption clean up
    for p in doc.paragraphs:
        if "SEP matches or exceeds Semantic Entropy accuracy across four LLMs" in p.text:
            p.text = "Figure 3: SEP matches or exceeds Semantic Entropy accuracy across four LLMs at roughly one-eighth the computational cost."
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(10)
            p.runs[0].italic = True
            break

    # 4. Figure 4 reference in Pillar 3
    for p in doc.paragraphs:
        if "At their fundamental level, transformers are attention machineries" in p.text:
            t = p.text
            # replace "Figure 3 shows the performance of the different LLM Check variants."
            t = re.sub(r'Figure\s+3\s+shows\s+the\s+performance\s+of\s+the\s+different\s+LLM\s+Check\s+variants\.?', '', t).strip()
            p.text = ""
            r1 = p.add_run(t + " ")
            r1.font.name = "Times New Roman"
            r2 = p.add_run("As illustrated in Figure 4, LLM-Check's black-box variant achieves an operational speedup factor of up to 450x with only a modest drop in AUROC compared to the full white-box configuration.")
            set_run_style(r2, r2.text, highlight=is_highlighted)
            break

    # Figure 4 caption
    for p in doc.paragraphs:
        if "LLM Check's black box variant achieves a 450" in p.text and "Figure 4" in p.text:
            p.text = "Figure 4: LLM-Check's black-box variant achieves a 450x speedup with only a modest drop in AUROC compared to the full white-box setting."
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(10)
            p.runs[0].italic = True
            break

    # 5. Figure 5 and Figure 6 reference in Pillar 4
    for p in doc.paragraphs:
        if "The thesaurus of any body of research is good benchmarks" in p.text:
            p.text = ""
            r1 = p.add_run("Rigorous benchmarking is essential to distinguish genuine algorithmic advances from artifacts of constrained test environments. ")
            r1.font.name = "Times New Roman"
            r2 = p.add_run("The comparative performance of proprietary and open-source models across the eight TrustLLM dimensions is presented in Figure 5. Furthermore, the relative percentage performance improvements achieved by calibration and explainability methods over their respective baselines are summarized in Figure 6.")
            set_run_style(r2, r2.text, highlight=is_highlighted)
            break

    # Figure 5 caption
    for p in doc.paragraphs:
        if "Proprietary models outscore open source counterparts on all eight TrustLLM dimensions" in p.text:
            p.text = "Figure 5: Proprietary models outscore open-source counterparts on all eight TrustLLM dimensions, though the gap narrows for safety and ethics."
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(10)
            p.runs[0].italic = True
            break

    # Figure 6 caption merge
    for i, p in enumerate(doc.paragraphs):
        if p.text.strip() == "Figure 6:":
            p.text = "Figure 6: Percentage performance gains achieved by calibration and explainability methods (BehCal RL, Human Trust) over their respective baseline configurations."
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(10)
            p.runs[0].italic = True
            # Check next paragraph
            if i + 1 < len(doc.paragraphs) and "Calibration and explainability methods" in doc.paragraphs[i+1].text:
                doc.paragraphs[i+1].text = ""
            break

    # 6. Table 2 caption and reference
    # Check if Table 2 caption already exists before Table index 1
    tbl1 = doc.tables[1]
    prev_elem = tbl1._tbl.getprevious()
    prev_text = ""
    for p in doc.paragraphs:
        if p._p is prev_elem:
            prev_text = p.text.strip()
            break
    if not prev_text.startswith("Table 2:"):
        cap_p = doc.add_paragraph()
        cap_p.paragraph_format.space_before = Pt(8)
        cap_p.paragraph_format.space_after = Pt(4)
        r = cap_p.add_run("Table 2: Key benchmarks, evaluation frameworks, and diagnostic dimensions for LLM hallucination assessment.")
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        tbl1._tbl.addprevious(cap_p._p)

    # 7. Figure 7 and Figure 8 references in Pillar 5
    for p in doc.paragraphs:
        if p.text.startswith("Behaviorally Calibrated Reinforcement Learning: Wu."):
            t = p.text
            # Insert Figure 8 reference after discussion of BehCal RL
            # and Figure 7 reference under ExpandR
            parts = t.split("ExpandR: Yao et al.")
            if len(parts) == 2:
                beh_text = parts[0].strip()
                exp_text = parts[1].strip()
                p.text = ""
                r1 = p.add_run(beh_text + " ")
                r1.font.name = "Times New Roman"
                r2 = p.add_run("Figure 8 illustrates that BehCal RL achieves the lowest expected calibration error across three benchmarks without sacrificing task accuracy. ")
                set_run_style(r2, r2.text, highlight=is_highlighted)
                r3 = p.add_run("ExpandR: Yao et al. " + exp_text + " ")
                r3.font.name = "Times New Roman"
                r4 = p.add_run("As illustrated in Figure 7, ExpandR's joint LLM-retriever optimization consistently outperforms standalone retrieval baselines across four benchmark datasets.")
                set_run_style(r4, r4.text, highlight=is_highlighted)
                break

    # Figure 7 caption
    for p in doc.paragraphs:
        if "ExpandR's joint LLM" in p.text and "Figure 7" in p.text:
            p.text = "Figure 7: ExpandR's joint LLM-retriever optimization consistently outperforms standalone baselines on four retrieval benchmarks."
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(10)
            p.runs[0].italic = True
            break

    # Figure 8 caption merge
    for i, p in enumerate(doc.paragraphs):
        if "Figure 8:" in p.text:
            p.text = "Figure 8: Expected calibration error across three benchmarks, demonstrating that BehCal RL achieves the lowest calibration error without sacrificing task accuracy."
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(10)
            p.runs[0].italic = True
            # Clear following split lines
            for offset in [1, 2]:
                if i + offset < len(doc.paragraphs):
                    if "BehCal RL achieves" in doc.paragraphs[i+offset].text or doc.paragraphs[i+offset].text.strip() == "accuracy.":
                        doc.paragraphs[i+offset].text = ""
            break

    # 8. Table 3 reference and caption
    for p in doc.paragraphs:
        if p.text.startswith("What this pillar tells us. Mitigating hallucinations is not just about catching mistakes after text is written"):
            if "Table 3" not in p.text:
                r_add = p.add_run(" The core mitigation frameworks, correction mechanisms, trigger conditions, and model-access requirements are comparatively summarized in Table 3.")
                set_run_style(r_add, r_add.text, highlight=is_highlighted)
            break

    # Table 3 caption before Table index 2
    tbl2 = doc.tables[2]
    prev_elem = tbl2._tbl.getprevious()
    prev_text = ""
    for p in doc.paragraphs:
        if p._p is prev_elem:
            prev_text = p.text.strip()
            break
    if not prev_text.startswith("Table 3:"):
        cap_p = doc.add_paragraph()
        cap_p.paragraph_format.space_before = Pt(8)
        cap_p.paragraph_format.space_after = Pt(4)
        r = cap_p.add_run("Table 3: Comparative summary of hallucination mitigation frameworks, correction mechanisms, and operational access paradigms.")
        r.bold = True
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        tbl2._tbl.addprevious(cap_p._p)

    # 9. Figure 9 reference and caption in Pillar 6
    for p in doc.paragraphs:
        if "All the above is geared towards the end result that people should be able to trust the results of LLM" in p.text:
            t = p.text
            t = re.sub(r'The relationship between explanations and user trust is shown in Figure\s+6\.?', '', t).strip()
            p.text = ""
            r1 = p.add_run(t + " ")
            r1.font.name = "Times New Roman"
            r2 = p.add_run("The empirical relationship between explanation framing, presentation modality, and human user trust is shown in Figure 9.")
            set_run_style(r2, r2.text, highlight=is_highlighted)
            break

    # Figure 9 caption merge
    for i, p in enumerate(doc.paragraphs):
        if "Figure 9:" in p.text:
            p.text = "Figure 9: Impact of explanation framing on human user trust across isolated and comparative presentation modalities."
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(10)
            p.runs[0].italic = True
            if i + 1 < len(doc.paragraphs) and "Explanation framing boosts user trust" in doc.paragraphs[i+1].text:
                doc.paragraphs[i+1].text = ""
            break

    # 10. Figure 10, Figure 11, Figure 12, Table 4 in Section 4
    for p in doc.paragraphs:
        if p.text.startswith("Where Are the Explanations? The most notable weakness, perhaps:"):
            # Replace the old ending sentences
            t = p.text
            t = re.sub(r'A comparison of AUROC and F1 scores is presented in Figure\s+7\.?', '', t)
            t = re.sub(r'Figure\s+8\s+shows\s+the\s+trade\s+off\s+between\s+detection\s+performance\s+and\s+efficiency\.?', '', t)
            t = re.sub(r'Table\s+I\s+presents\s+a\s+summary\s+of\s+this\s+comparison\s+of\s+the\s+detection\s+methods\s+on\s+some\s+of\s+the\s+practical\s+dimensions\.?', '', t).strip()
            p.text = ""
            r1 = p.add_run(t + " ")
            r1.font.name = "Times New Roman"
            r2 = p.add_run("The empirical balance between sensitivity and precision is visualized in the AUROC versus F1 scatter distribution (Figure 10). Furthermore, a comprehensive multi-dimensional comparison across all reviewed detection methods, annotated by signal type and speedup factor, is presented in Figure 11. Figure 12 illustrates the operational trade-off between detection accuracy (AUROC) and computational speedup factor on a logarithmic scale. Table 4 presents a systematic comparative analysis of hallucination detection methods across operational access paradigms, computational overhead, and empirical efficacy.")
            set_run_style(r2, r2.text, highlight=is_highlighted)
            break

    # Figure 10 caption merge
    for i, p in enumerate(doc.paragraphs):
        if "Figure 10:" in p.text:
            p.text = "Figure 10: AUROC versus F1 score scatter distribution for representative hallucination detection methods, showing SEP and LLM-Check achieving balanced multi-metric performance."
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(10)
            p.runs[0].italic = True
            if i + 1 < len(doc.paragraphs) and "AUROC versus F1 scatter showing SEP" in doc.paragraphs[i+1].text:
                doc.paragraphs[i+1].text = ""
            break

    # Table 4 caption clean up
    for p in doc.paragraphs:
        if "Table 4: Comparative analysis of hallucination detection methods" in p.text:
            p.text = "Table 4: Comparative analysis of hallucination detection methods across model access, computational overhead, and detection efficacy."
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(10)
            p.runs[0].bold = True
            break

    # Figure 11 caption
    for p in doc.paragraphs:
        if "Figure 11: AUROC vs. F1 Score for all detection methods" in p.text:
            p.text = "Figure 11: AUROC vs. F1 Score for all detection methods. Marker shape indicates signal type and marker size indicates log(speedup). SEP and LLM Check achieve the best overall performance."
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(10)
            p.runs[0].italic = True
            break

    # Figure 12 caption and remove blank spacing
    for i, p in enumerate(doc.paragraphs):
        if "Figure 12: Efficiency trade off" in p.text:
            p.text = "Figure 12: Efficiency trade-off: Speedup factor (log scale) vs. AUROC, demonstrating that LLM-Check achieves up to a 450x speedup."
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(10)
            p.runs[0].italic = True
            break

    doc.save(output_path)
    print(f"Successfully processed and saved: {output_path}")

if __name__ == "__main__":
    process_manuscript(
        r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx.bak_tech_check",
        r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx",
        is_highlighted=True
    )
    process_manuscript(
        r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models_nocolour.docx.bak_tech_check",
        r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models_nocolour.docx",
        is_highlighted=False
    )
