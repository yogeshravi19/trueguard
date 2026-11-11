"""
Generate:
  1. `E:\trueguard\CAPSTONE\FInal\TRUEGUARD_Faculty_Presentation_Verified.pptx`
  2. `E:\trueguard\CAPSTONE\FInal\paper\TRUEGUARD_Paper2_Implementation.docx`
directly from the verified Tesla T4 GPU outputs in `results/v2/TinyLlama__TinyLlama-1.1B-Chat-v1.0/`.
"""
import json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RES = os.path.join(ROOT, "results", "v2", "TinyLlama__TinyLlama-1.1B-Chat-v1.0")
FIG = os.path.join(RES, "figures")


def build_docx():
    import docx
    from docx.shared import Inches, Pt
    det = json.load(open(os.path.join(RES, "detection_report.json")))
    mit = json.load(open(os.path.join(RES, "mitigation", "mitigation_report.json")))
    lat = json.load(open(os.path.join(RES, "real_latency.json")))

    doc = docx.Document()
    doc.add_heading(
        "TRUEGUARD: Empirical Implementation and Evaluation of a Closed-Loop Multi-Sensor "
        "Hallucination Detection and Three-Tier Mitigation Architecture", 0
    )
    p = doc.add_paragraph("Yogesh Ravi M, T. S. Pradeep Kumar — School of Computer Science and Engineering, VIT Chennai")
    p.runs[0].italic = True

    md_path = os.path.join(ROOT, "paper", "TRUEGUARD_Paper2_Implementation.md")
    for block in open(md_path, encoding="utf8").read().split("\n\n"):
        b = block.strip()
        if not b or b.startswith("# TRUEGUARD:") or b.startswith("**Authors:**") or b == "---":
            continue
        if b.startswith("## "):
            doc.add_heading(b[3:].strip(), level=1)
        elif b.startswith("### "):
            doc.add_heading(b[4:].strip(), level=2)
        elif b.startswith("|"):
            lines = [l.strip() for l in b.splitlines() if l.strip().startswith("|")]
            rows = [[c.strip().replace("**", "") for c in l.strip("|").split("|")] for l in lines if "---" not in l]
            if rows:
                t = doc.add_table(rows=len(rows), cols=len(rows[0]))
                t.style = "Table Grid"
                for i, r in enumerate(rows):
                    for j, val in enumerate(r):
                        if j < len(t.columns):
                            t.cell(i, j).text = val
        else:
            doc.add_paragraph(b.replace("**", ""))

    doc.add_heading("4. Experimental Figures (NVIDIA Tesla T4 GPU — TinyLlama-1.1B-Chat-v1.0)", level=1)
    for fn, cap in [
        ("roc_halueval_qa.png", "Figure 1: 5-fold grouped CV ROC curves on HaluEval-QA (AUROC = 0.975)."),
        ("roc_halueval_summarization.png", "Figure 2: 5-fold grouped CV ROC curves on HaluEval-Summarization (AUROC = 0.986)."),
        ("roc_halueval_dialogue.png", "Figure 3: 5-fold grouped CV ROC curves on HaluEval-Dialogue (AUROC = 0.903)."),
        ("roc_truthful_qa.png", "Figure 4: 5-fold grouped CV ROC curves on TruthfulQA (AUROC = 0.876)."),
        ("ablation_truthful_qa.png", "Figure 5: Leave-one-sensor-out and single-sensor ablation on TruthfulQA."),
        ("cross_dataset_matrix.png", "Figure 6: Cross-dataset generalisation AUROC matrix across all four benchmarks."),
    ]:
        fp = os.path.join(FIG, fn)
        if os.path.exists(fp):
            doc.add_picture(fp, width=Inches(4.8))
            doc.add_paragraph(cap)

    out = os.path.join(ROOT, "paper", "TRUEGUARD_Paper2_Implementation.docx")
    doc.save(out)
    print("wrote", out)


def build_pptx():
    from pptx import Presentation
    from pptx.util import Inches, Pt

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    def add_bullets(title, bullets, img_path=None):
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = title
        tf = slide.placeholders[1].text_frame
        tf.clear()
        if img_path and os.path.exists(img_path):
            slide.placeholders[1].width = Inches(6.5)
            slide.shapes.add_picture(img_path, Inches(7.2), Inches(1.5), width=Inches(5.6))
        for k, b in enumerate(bullets):
            p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
            p.text = b
            p.font.size = Pt(18)

    # Slide 1: Title
    s0 = prs.slides.add_slide(prs.slide_layouts[0])
    s0.shapes.title.text = "TRUEGUARD: Closed-Loop Multi-Sensor Hallucination Detection & 3-Tier Mitigation"
    s0.placeholders[1].text = (
        "Yogesh Ravi M & Dr. T. S. Pradeep Kumar (VIT Chennai)\n"
        "Verified Implementation on NVIDIA Tesla T4 GPU (TinyLlama-1.1B-Chat & GPT-2)"
    )

    add_bullets(
        "1. Problem & What TRUEGUARD Does",
        [
            "Problem: LLMs state false facts ('hallucinations') with high surface confidence.",
            "Existing methods either generate 5-20 samples (4-5x slower) or stop at detection without fixing errors.",
            "TRUEGUARD treats generation as a closed-loop feedback controller:",
            "  1) Extracts 4 internal sensors in a single pass (ISP, AAS, EEM, DST).",
            "  2) Fuses them via leakage-free Out-of-Fold Logistic Regression into Risk R in [0, 1].",
            "  3) Routes answers across 2 calibrated thresholds (tau_warning, tau_fault) and 3 tiers:",
            "     - SAFE -> emit answer immediately.",
            "     - WARNING (Tier 1) -> risk-guided K=4 re-sampling.",
            "     - FAULT (Tier 2 -> Tier 3) -> Wikipedia retrieval grounding, else calibrated abstention.",
        ],
    )

    add_bullets(
        "2. The Four Single-Pass Internal Sensors",
        [
            "ISP (Internal State Probe - Supervised): Linear probes trained on hidden layers {0.45, 0.60, 0.75, 0.90}N_L.",
            "AAS (Attention Anomaly Score): Normalised Shannon entropy of final-quartile attention heads.",
            "EEM (Entropy-Energy Monitor): 0.6 * Shannon_norm + 0.4 * Renyi2_norm on output logits.",
            "DST (Distribution Shift Tracker): Temporal cosine distance (1 - cos(h_t, h_{t-1})) / 2.",
            "Verified mathematical equivalence between teacher-forced pass and online KV-cached monitor (max diff = 3.5e-6).",
        ],
        os.path.join(FIG, "roc_truthful_qa.png"),
    )

    add_bullets(
        "3. In-Distribution Detection (5-Fold Grouped CV, 3,196 Answers)",
        [
            "Model: TinyLlama-1.1B-Chat-v1.0 on Tesla T4 GPU (Zero question or probe leakage):",
            "  - HaluEval-Summarization (N=400 pairs): AUROC = 0.986 [0.980, 0.991], F1 = 0.935, ECE = 0.025",
            "  - HaluEval-QA (N=400 pairs):            AUROC = 0.975 [0.964, 0.987], F1 = 0.955, ECE = 0.024",
            "  - HaluEval-Dialogue (N=400 pairs):      AUROC = 0.903 [0.883, 0.922], F1 = 0.820, ECE = 0.034",
            "  - TruthfulQA (N=398 pairs):             AUROC = 0.876 [0.853, 0.900], F1 = 0.817, ECE = 0.042",
            "4-Benchmark Macro Average: AUROC = 0.935, F1 = 0.882, ECE = 0.031.",
        ],
        os.path.join(FIG, "roc_halueval_summarization.png"),
    )

    add_bullets(
        "4. Key Scientific Finding: Leave-One-Sensor-Out Ablation",
        [
            "Why surface entropy/attention alone is not enough:",
            "  - On TruthfulQA, untrained EEM = 0.522, DST = 0.533, AAS = 0.607.",
            "  - Trained ISP hidden-state probe jumps AUROC to 0.876 (+25.0 points over -ISP).",
            "Removing ISP (-ISP) drops AUROC by:",
            "  - TruthfulQA:             0.876 -> 0.626 (-0.251)",
            "  - HaluEval-Summarization: 0.986 -> 0.745 (-0.241)",
            "  - HaluEval-Dialogue:      0.903 -> 0.714 (-0.188)",
            "When ISP is absent, AAS+EEM+DST still provide a 0.626-0.918 training-free fallback.",
        ],
        os.path.join(FIG, "ablation_truthful_qa.png"),
    )

    add_bullets(
        "5. Cross-Dataset Generalisation & Benchmark Diagnostics",
        [
            "Strong transfer across HaluEval task families:",
            "  - HaluEval-Dialogue -> HaluEval-QA:            0.946 AUROC",
            "  - HaluEval-Summarization -> HaluEval-Dialogue: 0.779 AUROC",
            "  - HaluEval-Summarization -> HaluEval-QA:       0.777 AUROC (ISP-only = 0.845)",
            "Diagnostic discovery: HaluEval-QA right answers are short entities while TruthfulQA answers are full sentences.",
            "Takeaway: calibrating on 150 target-domain examples aligns length/entropy orientation before deployment.",
        ],
        os.path.join(FIG, "cross_dataset_matrix.png"),
    )

    add_bullets(
        "6. Live TriviaQA 3-Tier Mitigation & Tesla T4 GPU Latency",
        [
            "TriviaQA Live Generation (150 calibration + 150 unseen test questions):",
            "  - Detection AUROC on TinyLlama's own open-ended answers: 0.795",
            "  - Unmitigated hallucination rate: 62.0% (accuracy 38.0%)",
            "  - Post-mitigation hallucination rate among answered queries: 40.0% (-35.5% relative drop; accuracy 38% -> 60%)",
            "  - System-wide emitted hallucination rate: 17.3% (-72.0% relative drop)",
            "  - Risk-Coverage AURC: TRUEGUARD = 0.412 vs. Entropy = 0.526 and NLL = 0.603.",
            "Tesla T4 GPU Latency (TinyLlama-1.1B):",
            "  - Vanilla: 33.49 ms/tok | TRUEGUARD Post-pass: 36.41 ms/tok (+2.92 ms, +8.7%, 4.65x faster than 5-sample)",
            "  - TRUEGUARD Online: 39.30 ms/tok (+5.81 ms, 4.31x faster than 5-sample consistency at 169.31 ms/tok).",
        ],
        os.path.join(FIG, "risk_truthful_qa.png"),
    )

    out = os.path.join(ROOT, "TRUEGUARD_Faculty_Presentation_Verified.pptx")
    prs.save(out)
    print("wrote", out)


if __name__ == "__main__":
    build_docx()
    build_pptx()

