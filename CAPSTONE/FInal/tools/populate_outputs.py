"""
Step 3 Verification & Outputs Population Script for TRUEGUARD Final Project Report.
Runs real equivalence tests, compiles all verified TinyLlama-1.1B (Tesla T4 GPU) and
GPT-2 (CPU) metrics into CSV/JSON logs, copies all existing evaluation plots, and
renders high-resolution architectural, PRISMA, data-flow, mitigation, and latency figures
into E:/trueguard/outputs/ and E:/trueguard/CAPSTONE/outputs/.
"""
from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

ROOT = Path(r"E:\trueguard")
CAPSTONE = ROOT / "CAPSTONE"
FINAL_DIR = CAPSTONE / "FInal"
TINY_DIR = FINAL_DIR / "results" / "v2" / "TinyLlama__TinyLlama-1.1B-Chat-v1.0"
GPT2_DIR = FINAL_DIR / "results" / "v2" / "gpt2"

OUT_DIRS = [ROOT / "outputs", CAPSTONE / "outputs"]
for d in OUT_DIRS:
    (d / "figures").mkdir(parents=True, exist_ok=True)
    (d / "tables").mkdir(parents=True, exist_ok=True)
    (d / "logs").mkdir(parents=True, exist_ok=True)

PRIMARY_OUT = OUT_DIRS[0]
FIG_DIR = PRIMARY_OUT / "figures"
TAB_DIR = PRIMARY_OUT / "tables"
LOG_DIR = PRIMARY_OUT / "logs"

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "figure.dpi": 220,
})


def run_equivalence_suite() -> str:
    python_exe = FINAL_DIR / ".venv" / "Scripts" / "python.exe"
    if not python_exe.exists():
        python_exe = Path(sys.executable)
    proc = subprocess.run(
        [str(python_exe), str(FINAL_DIR / "tests" / "test_equivalence.py")],
        cwd=str(FINAL_DIR),
        capture_output=True,
        text=True,
        check=True,
    )
    log_text = proc.stdout + ("\n" + proc.stderr if proc.stderr else "")
    (LOG_DIR / "test_equivalence_run.log").write_text(log_text, encoding="utf-8")
    return log_text


def copy_existing_artifacts() -> None:
    shutil.copy2(TINY_DIR / "detection_report.json", LOG_DIR / "tinyllama_detection_report.json")
    shutil.copy2(TINY_DIR / "mitigation" / "mitigation_report.json", LOG_DIR / "tinyllama_mitigation_report.json")
    shutil.copy2(TINY_DIR / "real_latency.json", LOG_DIR / "tinyllama_real_latency.json")
    shutil.copy2(GPT2_DIR / "detection_report.json", LOG_DIR / "gpt2_detection_report.json")
    shutil.copy2(GPT2_DIR / "real_latency.json", LOG_DIR / "gpt2_real_latency.json")
    shutil.copy2(FINAL_DIR / "datasets" / "manifest.json", LOG_DIR / "dataset_manifest.json")

    for png in (TINY_DIR / "figures").glob("*.png"):
        shutil.copy2(png, FIG_DIR / png.name)
    for png in (GPT2_DIR / "figures").glob("*.png"):
        shutil.copy2(png, FIG_DIR / f"gpt2_{png.name}")


def extract_method_auroc(ds_dict: dict, method_name: str) -> float:
    if method_name == "TRUEGUARD (Full)":
        return float(ds_dict["fusion"]["auroc"])
    if method_name in ("ISP", "AAS", "EEM", "DST"):
        return float(ds_dict["single_sensor_trained"][method_name]["auroc"])
    if method_name.startswith("without_"):
        return float(ds_dict["ablation_leave_one_out"][method_name]["auroc"])
    raw = ds_dict["raw_untrained_baselines"][method_name]
    return float(max(raw["auroc"], raw["auroc_if_inverted"]))


def export_csv_tables() -> None:
    det_tiny = json.loads((TINY_DIR / "detection_report.json").read_text(encoding="utf-8"))
    mit_tiny = json.loads((TINY_DIR / "mitigation" / "mitigation_report.json").read_text(encoding="utf-8"))
    lat_tiny = json.loads((TINY_DIR / "real_latency.json").read_text(encoding="utf-8"))
    det_gpt2 = json.loads((GPT2_DIR / "detection_report.json").read_text(encoding="utf-8"))
    lat_gpt2 = json.loads((GPT2_DIR / "real_latency.json").read_text(encoding="utf-8"))

    datasets = ["truthful_qa", "halueval_qa", "halueval_dialogue", "halueval_summarization"]
    methods = [
        "TRUEGUARD (Full)",
        "ISP", "EEM", "AAS", "DST",
        "without_ISP", "without_AAS", "without_EEM", "without_DST",
        "ENT_mean", "NLL_mean", "LEN"
    ]

    with (TAB_DIR / "tinyllama_detection_metrics.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Method", "TruthfulQA_AUROC", "HaluEval_QA_AUROC", "HaluEval_Dialogue_AUROC", "HaluEval_Summ_AUROC", "Macro_AUROC"])
        for m in methods:
            aurocs = [extract_method_auroc(det_tiny["datasets"][ds], m) for ds in datasets]
            w.writerow([m, *[f"{x:.4f}" for x in aurocs], f"{np.mean(aurocs):.4f}"])

    gpt2_datasets = list(det_gpt2["datasets"].keys())
    with (TAB_DIR / "gpt2_detection_metrics.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Method", *[f"{ds}_AUROC" for ds in gpt2_datasets], "Macro_AUROC"])
        for m in methods:
            aurocs = [extract_method_auroc(det_gpt2["datasets"][ds], m) for ds in gpt2_datasets]
            w.writerow([m, *[f"{x:.4f}" for x in aurocs], f"{np.mean(aurocs):.4f}"])

    with (TAB_DIR / "triviaqa_mitigation_metrics.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Metric", "Value"])
        rows = [
            ("n_cal", mit_tiny["n_cal"]),
            ("n_test", mit_tiny["n_test"]),
            ("tau_warning", f"{mit_tiny['tau_warning']:.4f}"),
            ("tau_fault", f"{mit_tiny['tau_fault']:.4f}"),
            ("test_detection_auroc_on_own_generations", f"{mit_tiny['test_detection_auroc_on_own_generations']:.4f}"),
            ("baseline_accuracy", f"{mit_tiny['before']['accuracy']:.4f}"),
            ("baseline_hallucination_rate", f"{mit_tiny['before']['hallucination_rate']:.4f}"),
            ("coverage", f"{mit_tiny['after']['coverage']:.4f}"),
            ("accuracy_among_answered", f"{mit_tiny['after']['accuracy_among_answered']:.4f}"),
            ("hallucination_rate_among_answered", f"{mit_tiny['after']['hallucination_rate_among_answered']:.4f}"),
            ("hallucination_rate_system_wide", f"{mit_tiny['after']['hallucination_rate_system_wide']:.4f}"),
            ("relative_hallucination_reduction_among_answered", f"{mit_tiny['after']['relative_hallucination_reduction_among_answered']*100:.2f}%"),
            ("relative_hallucination_reduction_system_wide", f"{mit_tiny['after']['relative_hallucination_reduction_system_wide']*100:.2f}%"),
            ("AURC_TRUEGUARD", f"{mit_tiny['selective_prediction_accuracy_at_coverage']['TRUEGUARD']['AURC']:.4f}"),
            ("AURC_Entropy", f"{mit_tiny['selective_prediction_accuracy_at_coverage']['Entropy_baseline']['AURC']:.4f}"),
            ("AURC_NLL", f"{mit_tiny['selective_prediction_accuracy_at_coverage']['NLL_baseline']['AURC']:.4f}"),
        ]
        for k, v in rows:
            w.writerow([k, v])

    with (TAB_DIR / "hardware_latency_metrics.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Hardware_Model", "Mode", "Ms_Per_Token", "Overhead_Ms_Per_Token", "Overhead_Pct", "Speedup_vs_5Sample"])
        for label, lat in [("TinyLlama-1.1B (Tesla T4 GPU)", lat_tiny), ("GPT-2 124M (Local CPU)", lat_gpt2)]:
            van = lat["vanilla_ms_per_token"]
            sc5 = lat["multi_sample_5x_ms_per_token"]
            modes = [
                ("Vanilla Decode", van),
                ("TRUEGUARD Post-Pass", lat["trueguard_postpass_ms_per_token"]),
                ("TRUEGUARD Online (KV)", lat["trueguard_online_ms_per_token"]),
                ("5-Sample Consistency", sc5),
            ]
            for m_name, ms in modes:
                ov_ms = ms - van
                ov_pct = (ov_ms / van) * 100.0
                spd = sc5 / ms
                w.writerow([label, m_name, f"{ms:.2f}", f"{ov_ms:+.2f}", f"{ov_pct:+.1f}%", f"{spd:.2f}x"])


def draw_box(ax, x, y, w, h, title, subtitle="", fc="#EBF3FA", ec="#1B365D", title_fs=9.5, sub_fs=8.2):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.012,rounding_size=0.02",
        facecolor=fc, edgecolor=ec, linewidth=1.4
    )
    ax.add_patch(patch)
    if subtitle:
        ax.text(x + w / 2, y + h * 0.67, title, ha="center", va="center", fontsize=title_fs, fontweight="bold", color="#0F2537")
        ax.text(x + w / 2, y + h * 0.30, subtitle, ha="center", va="center", fontsize=sub_fs, color="#223344")
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center", fontsize=title_fs, fontweight="bold", color="#0F2537")


def generate_diagram_closed_loop_architecture() -> None:
    fig, ax = plt.subplots(figsize=(11.0, 6.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.965, "TRUEGUARD CLOSED-LOOP HALLUCINATION DETECTION & MITIGATION ARCHITECTURE",
            ha="center", va="center", fontsize=12, fontweight="bold", color="#0F2537")

    draw_box(ax, 0.03, 0.72, 0.16, 0.16, "1. Input Prompt x", "User Query / Context\nToken Sequence (1..m)", fc="#F3F6F9", ec="#34495E")
    draw_box(ax, 0.23, 0.68, 0.22, 0.22, "2. Plant: Frozen LLM",
             "Autoregressive Decoder\nTinyLlama-1.1B (L=22, d=2048)\nGPT-2 124M (L=12, d=768)", fc="#D6EAF8", ec="#1B4F72")

    ax.add_patch(FancyBboxPatch((0.49, 0.44), 0.24, 0.47, boxstyle="round,pad=0.01,rounding_size=0.02",
                                facecolor="#FCF3CF", edgecolor="#B7950B", linewidth=1.5, linestyle="--"))
    ax.text(0.61, 0.885, "3. Single-Pass 4-Sensor Bank", ha="center", va="center", fontsize=9.8, fontweight="bold", color="#7D6608")

    draw_box(ax, 0.505, 0.765, 0.21, 0.095, "Sensor 1: ISP (F_t)", "4-Layer Logistic Probes\n{0.45, 0.60, 0.75, 0.90}L", fc="#FEF9E7", ec="#B7950B", title_fs=8.8, sub_fs=7.6)
    draw_box(ax, 0.505, 0.66, 0.21, 0.095, "Sensor 2: AAS (A_t)", "Top-Quartile Attention\nNormalized Shannon Entropy", fc="#FEF9E7", ec="#B7950B", title_fs=8.8, sub_fs=7.6)
    draw_box(ax, 0.505, 0.555, 0.21, 0.095, "Sensor 3: EEM (H_ent,t)", "0.6 H_Shannon + 0.4 H_Renyi2\nScale-Invariant [0,1]", fc="#FEF9E7", ec="#B7950B", title_fs=8.8, sub_fs=7.6)
    draw_box(ax, 0.505, 0.45, 0.21, 0.095, "Sensor 4: DST (D_t)", "Consecutive-Token Cosine\nDrift 1 - cos(h_t, h_{t-1})", fc="#FEF9E7", ec="#B7950B", title_fs=8.8, sub_fs=7.6)

    draw_box(ax, 0.77, 0.58, 0.20, 0.30, "4. State Estimator",
             "Sequence Pooling phi(x,y)\n+ Inner OOF Stacking\n+ Logistic Fusion:\nr = sigma(w^T z + b)\n+ Log-Odds Attribution", fc="#D1F2EB", ec="#117864")

    ax.add_patch(FancyBboxPatch((0.04, 0.06), 0.93, 0.31, boxstyle="round,pad=0.01,rounding_size=0.02",
                                facecolor="#F9EBEA", edgecolor="#922B21", linewidth=1.5))
    ax.text(0.50, 0.34, "5. Closed-Loop 3-Tier Graded Actuator (Two Calibrated Thresholds: tau_warning = 0.611, tau_fault = 0.898)",
            ha="center", va="center", fontsize=9.8, fontweight="bold", color="#78281F")

    draw_box(ax, 0.06, 0.10, 0.20, 0.20, "SAFE (r < tau_warn)", "Emit Initial Answer y^(0)\nZero Extra Decode Passes\n(32.0% of Queries)", fc="#D4EFDF", ec="#1E8449", title_fs=8.8, sub_fs=7.8)
    draw_box(ax, 0.29, 0.10, 0.21, 0.20, "TIER 1: Re-Sampling", "tau_warn <= r < tau_fault\nAnnealed T in {0.35, 0.20}\nSelect argmin r_k (7.3%)", fc="#FCF3CF", ec="#B7950B", title_fs=8.8, sub_fs=7.8)
    draw_box(ax, 0.53, 0.10, 0.21, 0.20, "TIER 2: RAG Grounding", "r >= tau_fault or Tier 1 Fail\nWikipedia Evidence Retrieval\nRe-Score & Verify (4.0%)", fc="#FADBD8", ec="#C0392B", title_fs=8.8, sub_fs=7.8)
    draw_box(ax, 0.77, 0.10, 0.18, 0.20, "TIER 3: Abstention", "r_RAG >= tau_fault\nCalibrated Refusal + Sensor\nAttribution (56.7%)", fc="#E8DAEF", ec="#6C3483", title_fs=8.8, sub_fs=7.8)

    arrow_kw = dict(arrowstyle="-|>,head_width=0.35,head_length=0.5", lw=1.5, color="#1B365D")
    ax.annotate("", xy=(0.23, 0.80), xytext=(0.19, 0.80), arrowprops=arrow_kw)
    ax.annotate("", xy=(0.49, 0.78), xytext=(0.45, 0.78), arrowprops=arrow_kw)
    ax.annotate("", xy=(0.77, 0.73), xytext=(0.73, 0.73), arrowprops=arrow_kw)
    ax.annotate("", xy=(0.87, 0.37), xytext=(0.87, 0.58), arrowprops=arrow_kw)
    ax.annotate("", xy=(0.34, 0.68), xytext=(0.39, 0.30),
                arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.5", lw=1.5, color="#922B21", connectionstyle="arc3,rad=-0.22"))
    ax.text(0.28, 0.51, "Closed-Loop Feedback\n(Re-decode / RAG Prompt\n+ Risk Re-Verification)", fontsize=8.2, fontweight="bold", color="#922B21", ha="center")

    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_system_architecture.png", dpi=220)
    plt.close(fig)


def generate_diagram_prisma_flow() -> None:
    fig, ax = plt.subplots(figsize=(9.5, 5.8))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.96, "PRISMA 2020 SYSTEMATIC LITERATURE REVIEW SELECTION FLOW (2020–2026)",
            ha="center", va="center", fontsize=11.5, fontweight="bold", color="#0F2537")

    draw_box(ax, 0.08, 0.78, 0.46, 0.13, "Stage 1: Identification (n = 688 Records)",
             "5 Databases: arXiv (214), Scopus (186), IEEE Xplore (112),\nWeb of Science (92), ACM Digital Library (84)", fc="#D6EAF8", ec="#1B4F72")
    draw_box(ax, 0.62, 0.78, 0.32, 0.13, "Duplicates Removed (n = 196)",
             "Cross-database deduplication\n-> 492 unique records", fc="#FDEDEC", ec="#922B21")

    draw_box(ax, 0.08, 0.56, 0.46, 0.13, "Stage 2: Title & Abstract Screening (n = 492)",
             "Screened against Inclusion (IC1–IC6) and\nExclusion Criteria (EC1–EC4) by both authors", fc="#E8F8F5", ec="#117864")
    draw_box(ax, 0.62, 0.56, 0.32, 0.13, "Records Excluded (n = 324)",
             "General NLP/off-topic (218),\nnon-technical notes/demos (106)", fc="#FDEDEC", ec="#922B21")

    draw_box(ax, 0.08, 0.34, 0.46, 0.13, "Stage 3: Full-Text Eligibility Assessment (n = 168)",
             "4 Quality Criteria: Methodological Rigor, Benchmark\nValidity, Metric Reliability, Deployment Transparency", fc="#FEF9E7", ec="#B7950B")
    draw_box(ax, 0.62, 0.34, 0.32, 0.13, "Full-Text Excluded (n = 128)",
             "Prompt heuristics only (54), no standard\nbaselines (42), redundant methods (32)", fc="#FDEDEC", ec="#922B21")

    draw_box(ax, 0.08, 0.07, 0.86, 0.19, "Stage 4: Final Synthesized Corpus (n = 40 Studies: 20 Core Architectural + 20 Foundational)",
             "Pillar 1: Internal-State Detection (8)  |  Pillar 2: Uncertainty & Entropy (6)  |  Pillar 3: Attention & Multi-Signal (4)\n"
             "Pillar 4: Benchmarks & Taxonomies (9)  |  Pillar 5: Mitigation & RAG (11)  |  Pillar 6: Explainability & Trust (2)",
             fc="#D4EFDF", ec="#1E8449", title_fs=10.0, sub_fs=8.8)

    arrow_kw = dict(arrowstyle="-|>,head_width=0.35,head_length=0.5", lw=1.5, color="#1B365D")
    ax.annotate("", xy=(0.62, 0.845), xytext=(0.54, 0.845), arrowprops=arrow_kw)
    ax.annotate("", xy=(0.31, 0.69), xytext=(0.31, 0.78), arrowprops=arrow_kw)
    ax.annotate("", xy=(0.62, 0.625), xytext=(0.54, 0.625), arrowprops=arrow_kw)
    ax.annotate("", xy=(0.31, 0.47), xytext=(0.31, 0.56), arrowprops=arrow_kw)
    ax.annotate("", xy=(0.62, 0.405), xytext=(0.54, 0.405), arrowprops=arrow_kw)
    ax.annotate("", xy=(0.31, 0.26), xytext=(0.31, 0.34), arrowprops=arrow_kw)

    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_prisma_flow.png", dpi=220)
    plt.close(fig)


def generate_diagram_oof_dataflow() -> None:
    fig, ax = plt.subplots(figsize=(10.5, 5.2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    ax.text(0.5, 0.95, "LEAKAGE-FREE GROUPED K-FOLD & INNER OUT-OF-FOLD (OOF) STACKING PIPELINE",
            ha="center", va="center", fontsize=11.2, fontweight="bold", color="#0F2537")

    draw_box(ax, 0.03, 0.62, 0.20, 0.22, "1. Benchmark Corpus",
             "TruthfulQA (796)\nHaluEval-QA (800)\nHaluEval-Dial (800)\nHaluEval-Summ (800)\nTotal N = 3,196 Answers", fc="#EBF5FB", ec="#1B4F72")
    draw_box(ax, 0.27, 0.62, 0.21, 0.22, "2. Outer GroupKFold (K=5)",
             "Grouped by group_id\n(Prompt Question ID)\nBoth +/- answers for Q_i\nstay in same fold", fc="#E8F8F5", ec="#117864")
    draw_box(ax, 0.52, 0.62, 0.22, 0.22, "3. Inner GroupKFold (K=3)",
             "On Outer Train Split Only:\nFit 4-Layer Logistic Probes\n{L_0.45, L_0.60, L_0.75, L_0.90}\nCompute Inner OOF F_i", fc="#FEF9E7", ec="#B7950B")
    draw_box(ax, 0.78, 0.62, 0.19, 0.22, "4. Fusion Calibration",
             "StandardScaler + L2\nLogisticRegression on\n[F_OOF, A, H_ent, D]\nw = [+5.79,+0.87,+1.83,+0.74]", fc="#F5EEF8", ec="#6C3483")

    draw_box(ax, 0.12, 0.14, 0.34, 0.28, "5. Dual-Mode Single-Pass Inference",
             "Mode A: Teacher-Forced Post-Pass (score_answer)\nMode B: KV-Cached Step-by-Step (OnlineSignalMonitor)\nVerified Equivalence: max |dF| = 3.49e-6, max |dH| = 1.53e-5",
             fc="#D4EFDF", ec="#1E8449")
    draw_box(ax, 0.54, 0.14, 0.38, 0.28, "6. Out-of-Fold Evaluation & Bootstrap CI",
             "Predict Held-Out Fold Risk r_i in [0,1]\n500-Resample Group Bootstrap 95% CIs\nMetrics: AUROC, AUPRC, F1, Acc, ECE, AURC",
             fc="#FADBD8", ec="#922B21")

    arrow_kw = dict(arrowstyle="-|>,head_width=0.35,head_length=0.5", lw=1.5, color="#1B365D")
    ax.annotate("", xy=(0.27, 0.73), xytext=(0.23, 0.73), arrowprops=arrow_kw)
    ax.annotate("", xy=(0.52, 0.73), xytext=(0.48, 0.73), arrowprops=arrow_kw)
    ax.annotate("", xy=(0.78, 0.73), xytext=(0.74, 0.73), arrowprops=arrow_kw)
    ax.annotate("", xy=(0.29, 0.42), xytext=(0.37, 0.62), arrowprops=arrow_kw)
    ax.annotate("", xy=(0.73, 0.42), xytext=(0.87, 0.62), arrowprops=arrow_kw)
    ax.annotate("", xy=(0.54, 0.28), xytext=(0.46, 0.28), arrowprops=arrow_kw)

    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_oof_dataflow_pipeline.png", dpi=220)
    plt.close(fig)


def generate_mitigation_and_latency_charts() -> None:
    mit = json.loads((TINY_DIR / "mitigation" / "mitigation_report.json").read_text(encoding="utf-8"))
    lat_tiny = json.loads((TINY_DIR / "real_latency.json").read_text(encoding="utf-8"))
    lat_gpt2 = json.loads((GPT2_DIR / "real_latency.json").read_text(encoding="utf-8"))
    det_tiny = json.loads((TINY_DIR / "detection_report.json").read_text(encoding="utf-8"))
    det_gpt2 = json.loads((GPT2_DIR / "detection_report.json").read_text(encoding="utf-8"))

    # Chart 1: TriviaQA 3-Tier Mitigation Tier Routing & Hallucination Drop
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.3))
    tiers = ["SAFE\n(r < 0.611)", "TIER 1\nRe-Sample", "TIER 2\nWikipedia RAG", "TIER 3\nAbstain"]
    counts = [
        mit["tier_counts"]["SAFE"],
        mit["tier_counts"]["TIER1_RESAMPLE"],
        mit["tier_counts"]["TIER2_RETRIEVAL"],
        mit["tier_counts"]["TIER3_ABSTAIN"],
    ]
    pcts = [c / mit["n_test"] * 100.0 for c in counts]
    colors = ["#27AE60", "#F39C12", "#2980B9", "#8E44AD"]
    bars = ax1.bar(tiers, pcts, color=colors, edgecolor="#1B2631", width=0.58)
    ax1.set_ylabel("Percentage of Test Queries (%)")
    ax1.set_title("(a) 3-Tier Controller Routing on TriviaQA (n = 150)")
    ax1.set_ylim(0, 68)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    for b, c, p in zip(bars, counts, pcts):
        ax1.text(b.get_x() + b.get_width() / 2, b.get_height() + 1.5, f"{p:.1f}%\n({c}/150)",
                 ha="center", va="bottom", fontsize=8.5, fontweight="bold")

    categories = ["Baseline\n(Unmitigated)", "TRUEGUARD\n(Answered Subset)", "TRUEGUARD\n(System-Wide Emitted)"]
    hall_rates = [
        mit["before"]["hallucination_rate"] * 100.0,
        mit["after"]["hallucination_rate_among_answered"] * 100.0,
        mit["after"]["hallucination_rate_system_wide"] * 100.0,
    ]
    acc_rates = [
        mit["before"]["accuracy"] * 100.0,
        mit["after"]["accuracy_among_answered"] * 100.0,
        (1.0 - mit["after"]["hallucination_rate_system_wide"]) * 100.0,
    ]
    x = np.arange(len(categories))
    w = 0.35
    b1 = ax2.bar(x - w / 2, hall_rates, w, label="Hallucination Rate (%)", color="#C0392B", edgecolor="#1B2631")
    b2 = ax2.bar(x + w / 2, acc_rates, w, label="Factual / Safe Rate (%)", color="#1F618D", edgecolor="#1B2631")
    ax2.set_xticks(x)
    ax2.set_xticklabels(categories)
    ax2.set_ylabel("Percentage (%)")
    ax2.set_title("(b) Hallucination Reduction & Accuracy Gain")
    ax2.set_ylim(0, 102)
    ax2.legend(loc="upper left", fontsize=8.5)
    ax2.grid(axis="y", linestyle="--", alpha=0.4)
    for b in list(b1) + list(b2):
        ax2.text(b.get_x() + b.get_width() / 2, b.get_height() + 1.3, f"{b.get_height():.1f}%",
                 ha="center", va="bottom", fontsize=8.3, fontweight="bold")

    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_mitigation_tier_breakdown.png", dpi=220)
    plt.close(fig)

    # Chart 1b: Selective Prediction Accuracy & Risk-Coverage Curve on TriviaQA
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.2, 4.2))
    cov_labels = ["100%", "90%", "80%", "70%", "60%", "50%"]
    cov_x = [100, 90, 80, 70, 60, 50]
    sel = mit["selective_prediction_accuracy_at_coverage"]
    tg_acc = [sel["TRUEGUARD"][k] * 100.0 for k in cov_labels]
    ent_acc = [sel["Entropy_baseline"][k] * 100.0 for k in cov_labels]
    nll_acc = [sel["NLL_baseline"][k] * 100.0 for k in cov_labels]
    tg_risk = [100.0 - a for a in tg_acc]
    ent_risk = [100.0 - a for a in ent_acc]
    nll_risk = [100.0 - a for a in nll_acc]

    ax1.plot(cov_x, tg_acc, marker="o", lw=2.2, color="#1B4F72", label=f"TRUEGUARD (AURC = {sel['TRUEGUARD']['AURC']:.3f})")
    ax1.plot(cov_x, ent_acc, marker="s", lw=1.8, linestyle="--", color="#E67E22", label=f"Normalized Entropy (AURC = {sel['Entropy_baseline']['AURC']:.3f})")
    ax1.plot(cov_x, nll_acc, marker="^", lw=1.8, linestyle=":", color="#C0392B", label=f"Mean Token NLL (AURC = {sel['NLL_baseline']['AURC']:.3f})")
    ax1.set_xlim(103, 47)
    ax1.set_ylim(34, 66)
    ax1.set_xlabel("Coverage (% of Queries Answered)")
    ax1.set_ylabel("Factual Accuracy (%)")
    ax1.set_title("(a) Selective Prediction Accuracy vs. Coverage")
    ax1.grid(True, linestyle="--", alpha=0.4)
    ax1.legend(loc="upper left", fontsize=8.0)

    ax2.plot(cov_x, tg_risk, marker="o", lw=2.2, color="#1B4F72", label="TRUEGUARD Risk Curve")
    ax2.plot(cov_x, ent_risk, marker="s", lw=1.8, linestyle="--", color="#E67E22", label="Normalized Entropy Risk Curve")
    ax2.plot(cov_x, nll_risk, marker="^", lw=1.8, linestyle=":", color="#C0392B", label="Mean Token NLL Risk Curve")
    ax2.set_xlim(103, 47)
    ax2.set_ylim(34, 66)
    ax2.set_xlabel("Coverage (% of Queries Answered)")
    ax2.set_ylabel("Empirical Hallucination Risk (%)")
    ax2.set_title("(b) Risk–Coverage Curve on Live TriviaQA (n = 150)")
    ax2.grid(True, linestyle="--", alpha=0.4)
    ax2.legend(loc="lower left", fontsize=8.0)

    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_risk_coverage_curve.png", dpi=220)
    plt.close(fig)

    # Chart 1c: Clean Cross-Dataset Transfer Heatmap
    fig, ax = plt.subplots(figsize=(7.6, 5.8))
    ds_order = ["halueval_dialogue", "halueval_qa", "halueval_summarization", "truthful_qa"]
    ds_pretty = ["HaluEval-Dialogue", "HaluEval-QA", "HaluEval-Summarization", "TruthfulQA"]
    mat = np.zeros((4, 4), dtype=float)
    for i, src in enumerate(ds_order):
        for j, dst in enumerate(ds_order):
            if i == j:
                mat[i, j] = det_tiny["datasets"][src]["fusion"]["auroc"]
            else:
                mat[i, j] = det_tiny["cross_dataset"][src]["transfers"][dst]["auroc"]
    im = ax.imshow(mat, cmap="viridis", vmin=0.35, vmax=1.0)
    ax.set_xticks(np.arange(4))
    ax.set_yticks(np.arange(4))
    ax.set_xticklabels(ds_pretty, rotation=22, ha="right")
    ax.set_yticklabels(ds_pretty)
    ax.set_xlabel("Evaluation Target Benchmark")
    ax.set_ylabel("Training Source Benchmark")
    ax.set_title("Cross-Benchmark AUROC Transfer Matrix (Diagonal = 5-Fold Grouped CV)", pad=12)
    for i in range(4):
        for j in range(4):
            val = mat[i, j]
            txt_color = "#111111" if val > 0.72 else "#FFFFFF"
            tag = " (CV)" if i == j else ""
            ax.text(j, i, f"{val:.3f}{tag}", ha="center", va="center", color=txt_color, fontsize=9.0, fontweight="bold")
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("AUROC")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_cross_dataset_heatmap_clean.png", dpi=220)
    plt.close(fig)

    # Chart 2: Dual-Hardware Latency & Speedup Comparison (Tesla T4 GPU vs CPU)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.3))
    mode_labels = ["Vanilla\nDecode", "TRUEGUARD\nPost-Pass", "TRUEGUARD\nOnline (KV)", "5-Sample\nConsistency"]
    t4_vals = [
        lat_tiny["vanilla_ms_per_token"],
        lat_tiny["trueguard_postpass_ms_per_token"],
        lat_tiny["trueguard_online_ms_per_token"],
        lat_tiny["multi_sample_5x_ms_per_token"],
    ]
    cpu_vals = [
        lat_gpt2["vanilla_ms_per_token"],
        lat_gpt2["trueguard_postpass_ms_per_token"],
        lat_gpt2["trueguard_online_ms_per_token"],
        lat_gpt2["multi_sample_5x_ms_per_token"],
    ]
    bar_colors = ["#5D6D7E", "#1E8449", "#2874A6", "#C0392B"]

    b_t4 = ax1.bar(mode_labels, t4_vals, color=bar_colors, edgecolor="#1B2631", width=0.56)
    ax1.set_ylabel("Latency (ms / token)")
    ax1.set_title("(a) TinyLlama-1.1B on NVIDIA Tesla T4 GPU")
    ax1.set_ylim(0, 195)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    for b, v in zip(b_t4, t4_vals):
        ax1.text(b.get_x() + b.get_width() / 2, v + 3.0, f"{v:.2f} ms", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

    b_cpu = ax2.bar(mode_labels, cpu_vals, color=bar_colors, edgecolor="#1B2631", width=0.56)
    ax2.set_ylabel("Latency (ms / token)")
    ax2.set_title("(b) GPT-2 (124M) on Local CPU")
    ax2.set_ylim(0, max(cpu_vals) * 1.18)
    ax2.grid(axis="y", linestyle="--", alpha=0.4)
    for b, v in zip(b_cpu, cpu_vals):
        ax2.text(b.get_x() + b.get_width() / 2, v + max(cpu_vals) * 0.02, f"{v:.2f} ms", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_dual_hardware_latency.png", dpi=220)
    plt.close(fig)

    # Chart 3: TinyLlama-1.1B Detection Comparison across all 4 Benchmarks + GPT-2 Reference
    fig, ax = plt.subplots(figsize=(9.8, 4.5))
    ds_keys = ["truthful_qa", "halueval_qa", "halueval_dialogue", "halueval_summarization"]
    ds_names = ["TruthfulQA", "HaluEval-QA", "HaluEval-Dialogue", "HaluEval-Summarization", "Macro Average"]
    t_tg = [extract_method_auroc(det_tiny["datasets"][d], "TRUEGUARD (Full)") for d in ds_keys]
    t_tg.append(float(np.mean(t_tg)))
    t_isp = [extract_method_auroc(det_tiny["datasets"][d], "ISP") for d in ds_keys]
    t_isp.append(float(np.mean(t_isp)))
    t_no_isp = [extract_method_auroc(det_tiny["datasets"][d], "without_ISP") for d in ds_keys]
    t_no_isp.append(float(np.mean(t_no_isp)))
    t_ent = [extract_method_auroc(det_tiny["datasets"][d], "ENT_mean") for d in ds_keys]
    t_ent.append(float(np.mean(t_ent)))

    x = np.arange(len(ds_names))
    w = 0.20
    r1 = ax.bar(x - 1.5 * w, t_tg, w, label="TRUEGUARD (Full 4-Sensor Fusion)", color="#1B4F72", edgecolor="#1B2631")
    r2 = ax.bar(x - 0.5 * w, t_isp, w, label="ISP Only (4-Layer Supervised Probe)", color="#2E86C1", edgecolor="#1B2631")
    r3 = ax.bar(x + 0.5 * w, t_no_isp, w, label="AAS + EEM + DST (Without ISP)", color="#1E8449", edgecolor="#1B2631")
    r4 = ax.bar(x + 1.5 * w, t_ent, w, label="Normalized Entropy Baseline", color="#E67E22", edgecolor="#1B2631")

    ax.set_xticks(x)
    ax.set_xticklabels(ds_names)
    ax.set_ylabel("Out-of-Fold AUROC")
    ax.set_ylim(0.35, 1.09)
    ax.set_title("Multi-Benchmark Hallucination Detection AUROC on TinyLlama-1.1B (5-Fold Grouped CV, N = 3,196)")
    ax.legend(ncol=2, loc="upper left", fontsize=8.3)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    for bars_group in (r1, r2, r3, r4):
        for b in bars_group:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.01, f"{b.get_height():.3f}",
                    ha="center", va="bottom", fontsize=7.2, fontweight="bold")

    fig.tight_layout()
    fig.savefig(FIG_DIR / "fig_cross_backbone_comparison.png", dpi=220)
    plt.close(fig)


def sync_secondary_outputs() -> None:
    sec = OUT_DIRS[1]
    for sub in ("figures", "tables", "logs"):
        for f in (PRIMARY_OUT / sub).glob("*"):
            if f.is_file():
                shutil.copy2(f, sec / sub / f.name)


if __name__ == "__main__":
    print("Running Step 3 verification suite...")
    eq_log = run_equivalence_suite()
    print(eq_log.strip())
    copy_existing_artifacts()
    export_csv_tables()
    generate_diagram_closed_loop_architecture()
    generate_diagram_prisma_flow()
    generate_diagram_oof_dataflow()
    generate_mitigation_and_latency_charts()
    sync_secondary_outputs()
    print(f"Populated {len(list(FIG_DIR.glob('*.png')))} figures, {len(list(TAB_DIR.glob('*.csv')))} CSV tables, and {len(list(LOG_DIR.glob('*')))} logs into {OUT_DIRS[0]} and {OUT_DIRS[1]}.")
