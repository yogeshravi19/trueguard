import docx
from docx.shared import Pt
from docx.enum.text import WD_COLOR_INDEX
import re

def humanize_manuscript(docx_path, is_highlighted=True):
    doc = docx.Document(docx_path)

    def set_run_style(run, text, highlight=is_highlighted, bold=False, italic=False):
        run.text = text
        run.font.name = "Times New Roman"
        run.bold = bold
        run.italic = italic
        if highlight:
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW
        else:
            run.font.highlight_color = None

    # 1. Figure 1 in Introduction
    for p in doc.paragraphs:
        if "The technical word is hallucination, and it can simply be defined" in p.text or "phenomenon commonly termed hallucination" in p.text:
            t = p.text
            # Find base text before the Figure 1 reference
            # Cut at the start of the hallucination definition
            marker = "The technical word is hallucination"
            if marker in t:
                base = t.split(marker)[0].strip()
            else:
                base = t.split("As illustrated in Figure 1")[0].strip()
                base = re.sub(r'\(Figure\s+1\)', '', base).strip()
            
            p.text = ""
            r1 = p.add_run(base + " The technical word is hallucination, which simply means that the model produces text that sounds fluent and confident, but is factually false [7], [18]. ")
            r1.font.name = "Times New Roman"
            r2 = p.add_run("As illustrated in Figure 1, these errors generally show up in two distinct ways: intrinsic self-contradictions (where the model disagrees with itself) and extrinsic fabrications (where it invents false facts). Because these two errors look completely different internally, each requires its own detection strategy.")
            set_run_style(r2, r2.text, highlight=is_highlighted)
            break

    # 2. Figure 2 & Table 1 in Methodology (Included paragraph)
    for p in doc.paragraphs:
        if "Included: A final corpus of 40 representative studies" in p.text:
            base = "Included: A final corpus of 40 representative studies met all eligibility and quality criteria and was selected for synthesis."
            p.text = ""
            r1 = p.add_run(base + " ")
            r1.font.name = "Times New Roman"
            r2 = p.add_run("Figure 2 presents the full PRISMA flow diagram with our exact screening numbers at each stage, while Table 1 summarizes the database search strings, date window, and inclusion criteria used during selection.")
            set_run_style(r2, r2.text, highlight=is_highlighted)
            break

    # 3. Figure 4 in Pillar 3 (Attention)
    for p in doc.paragraphs:
        if "At their fundamental level, transformers are attention machineries" in p.text:
            base = (
                "At their core, transformers rely on attention mechanisms: every token produced is a weighted blend of earlier tokens. "
                "When a model starts to hallucinate, these attention weights shift in noticeable ways, allowing researchers to spot errors in real time. "
            )
            p.text = ""
            r1 = p.add_run(base)
            r1.font.name = "Times New Roman"
            r2 = p.add_run("Figure 4 highlights this with LLM-Check, showing that its black-box version runs up to 450 times faster than the full white-box version while losing very little detection accuracy.")
            set_run_style(r2, r2.text, highlight=is_highlighted)
            break

    # 4. Figure 5 & 6 in Pillar 4 (Benchmarks)
    for p in doc.paragraphs:
        if "Rigorous benchmarking is essential" in p.text or "The thesaurus of any body of research is good benchmarks" in p.text:
            p.text = ""
            r1 = p.add_run("Reliable benchmarks are essential to see if a detection method genuinely works or only looks good under easy test conditions. ")
            r1.font.name = "Times New Roman"
            r2 = p.add_run("Figure 5 compares how proprietary and open-source models perform across the eight trustworthiness dimensions in TrustLLM. Building on this, Figure 6 highlights the percentage gains achieved by calibration and explainability methods over their baseline setups.")
            set_run_style(r2, r2.text, highlight=is_highlighted)
            break

    # 5. Figure 7 & Figure 8 in Pillar 5 (Mitigation)
    for p in doc.paragraphs:
        if p.text.startswith("Behaviorally Calibrated Reinforcement Learning: Wu."):
            t = p.text
            # split into BehCal RL and ExpandR
            parts = t.split("ExpandR: Yao et al.")
            if len(parts) == 2:
                beh = parts[0].strip()
                # Clean out existing Fig 8 reference if already appended
                beh = re.sub(r'Figure\s+8\s+illustrates\s+that\s+BehCal\s+RL\s+achieves[^\.]*\.', '', beh).strip()
                
                exp = parts[1].strip()
                exp = re.sub(r'As\s+illustrated\s+in\s+Figure\s+7,\s+ExpandR[^\.]*\.', '', exp).strip()
                
                p.text = ""
                r1 = p.add_run(beh + " ")
                r1.font.name = "Times New Roman"
                r2 = p.add_run("As shown in Figure 8, BehCal RL achieves the lowest calibration error across three benchmarks while keeping overall task accuracy high. ")
                set_run_style(r2, r2.text, highlight=is_highlighted)
                
                r3 = p.add_run("ExpandR: Yao et al. " + exp + " ")
                r3.font.name = "Times New Roman"
                r4 = p.add_run("Figure 7 shows that ExpandR's joint optimization consistently beats standard standalone retrieval baselines across four separate benchmarks.")
                set_run_style(r4, r4.text, highlight=is_highlighted)
                break

    # 6. Table 3 in Pillar 5
    for p in doc.paragraphs:
        if p.text.startswith("What this pillar tells us. Mitigating hallucinations is not just about catching"):
            t = p.text
            t_clean = re.sub(r'The core mitigation frameworks, correction mechanisms[^\.]*\.', '', t).strip()
            t_clean = re.sub(r'Table 3 compares these mitigation frameworks[^\.]*\.', '', t_clean).strip()
            p.text = ""
            r1 = p.add_run(t_clean + " ")
            r1.font.name = "Times New Roman"
            r2 = p.add_run("Table 3 compares these mitigation frameworks side by side, outlining how each method corrects mistakes, when it triggers, and what level of model access it requires.")
            set_run_style(r2, r2.text, highlight=is_highlighted)
            break

    # 7. Figure 9 in Pillar 6 (Explainability)
    for p in doc.paragraphs:
        if "All the above is geared towards the end result that people should be able to trust" in p.text:
            base = (
                "Ultimately, users need to trust model outputs, which requires both technical accuracy and clear explanations. "
                "People need to know when and why an answer can be trusted. "
            )
            p.text = ""
            r1 = p.add_run(base)
            r1.font.name = "Times New Roman"
            r2 = p.add_run("Figure 9 shows how explanations affect user trust, demonstrating that clear explanations help users judge answers much better when comparing outputs side by side.")
            set_run_style(r2, r2.text, highlight=is_highlighted)
            break

    # 8. Figures 10, 11, 12 & Table 4 in Section 4 (Comparative Analysis)
    for p in doc.paragraphs:
        if p.text.startswith("Where Are the Explanations? The most notable weakness, perhaps:"):
            base = (
                "Where Are the Explanations? The biggest practical weakness in current tools is that most detection systems only produce a risk number or a yes/no flag, without explaining why an error was flagged. "
                "This is a missed opportunity because the underlying signals—such as attention shifts, entropy spikes, and distribution drift—are naturally interpretable. "
                "Herrera [8] outlined what makes explanations effective, while Sharma et al. [19] showed how they directly shape user trust. "
                "The signals and design principles already exist; they simply need to be connected. "
            )
            p.text = ""
            r1 = p.add_run(base)
            r1.font.name = "Times New Roman"
            r2 = p.add_run(
                "To compare overall performance, Figure 10 plots AUROC against F1 score to show how well each method balances accuracy and error coverage. "
                "Figure 11 broadens this comparison across all detection methods, marking each technique by its signal type and speed. "
                "Figure 12 plots the trade-off between detection accuracy and speedup, showing that optimized methods like LLM-Check can deliver massive speed gains. "
                "Finally, Table 4 brings all these practical trade-offs together, comparing each method by model access, extra generation passes, and performance on intrinsic versus extrinsic hallucinations."
            )
            set_run_style(r2, r2.text, highlight=is_highlighted)
            break

    doc.save(docx_path)
    print(f"Humanized and saved: {docx_path}")

if __name__ == "__main__":
    humanize_manuscript(r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx", is_highlighted=True)
    humanize_manuscript(r"E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models_nocolour.docx", is_highlighted=False)
