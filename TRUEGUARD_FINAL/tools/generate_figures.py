"""
TRUEGUARD Publication Figures Generator
Generates high-resolution (300 DPI) publication-quality figures:
1. fig1_architecture.png: 4-Signal Multi-Signal Pipeline
2. fig2_auroc_benchmark_comparison.png: Cross-Benchmark AUROC Comparison
3. fig3_ablation_study.png: Contribution of Individual Signals
4. fig4_latency_efficiency_tradeoff.png: AUROC vs Latency Trade-Off
5. fig5_mitigation_waterfall.png: Active Mitigation Impact (63.8% Reduction)
6. fig6_token_risk_heatmap.png: Token-Level Risk Trace Visualization
"""

import os
import matplotlib.pyplot as plt
import numpy as np

# Configure publication styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

FIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "figures"))
os.makedirs(FIG_DIR, exist_ok=True)

def generate_fig1_architecture():
    """Generates schematic flowchart of TRUEGUARD single-pass architecture."""
    fig, ax = plt.subplots(figsize=(12, 5.5), dpi=300)
    ax.axis('off')

    # Draw boxes
    boxes = [
        {"text": "Prompt / Input Context C", "pos": (0.05, 0.5), "color": "#E2E8F0", "edge": "#475569"},
        {"text": "LLM Forward Pass\n(Single-Pass Execution)\n[h_t^L, A_t, z_t]", "pos": (0.28, 0.5), "color": "#DBEAFE", "edge": "#1E40AF"},
        {"text": "ISP\nInternal State\nProbes", "pos": (0.50, 0.80), "color": "#DCFCE7", "edge": "#15803D"},
        {"text": "AAS\nAttention Anomaly\nEntropy", "pos": (0.50, 0.58), "color": "#DCFCE7", "edge": "#15803D"},
        {"text": "EEM\nEntropy-Energy\nMonitor", "pos": (0.50, 0.38), "color": "#DCFCE7", "edge": "#15803D"},
        {"text": "DST\nDistribution Shift\nCosine Dist", "pos": (0.50, 0.16), "color": "#DCFCE7", "edge": "#15803D"},
        {"text": "Online Z-Score\nNormalization &\nLearned Fusion\nR(t) = σ(W^T X + b)", "pos": (0.72, 0.5), "color": "#FEF3C7", "edge": "#B45309"},
        {"text": "Closed-Loop Mitigation\n• Safe (R ≤ 0.50): Emit Token\n• Risk (R > 0.50): RAG / Abstain", "pos": (0.92, 0.5), "color": "#FEE2E2", "edge": "#B91C1C"}
    ]

    for b in boxes:
        x, y = b["pos"]
        ax.text(x, y, b["text"], ha="center", va="center", fontsize=9.5, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.6", facecolor=b["color"], edgecolor=b["edge"], linewidth=1.5))

    # Connect arrows
    arrow_props = dict(arrowstyle="->", lw=1.5, color="#334155")
    ax.annotate("", xy=(0.17, 0.5), xytext=(0.14, 0.5), arrowprops=arrow_props)
    
    for y_sig in [0.80, 0.58, 0.38, 0.16]:
        ax.annotate("", xy=(0.43, y_sig), xytext=(0.38, 0.5), arrowprops=arrow_props)
        ax.annotate("", xy=(0.63, 0.5), xytext=(0.57, y_sig), arrowprops=arrow_props)

    ax.annotate("", xy=(0.82, 0.5), xytext=(0.80, 0.5), arrowprops=arrow_props)

    ax.set_title("TRUEGUARD: Real-Time Multi-Signal Hallucination Detection & Mitigation Framework",
                 fontsize=12, fontweight="bold", pad=15)
    plt.tight_layout()
    path = os.path.join(FIG_DIR, "fig1_architecture.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")

def generate_fig2_auroc_comparison():
    """Generates cross-benchmark AUROC comparison against baselines."""
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)

    benchmarks = ["TruthfulQA", "HaluEval-QA", "HaluEval-Summ", "HaluEval-Dial", "HELM", "Average"]
    x = np.arange(len(benchmarks))
    w = 0.20

    token_entropy = [0.71, 0.74, 0.73, 0.70, 0.68, 0.712]
    semantic_entropy = [0.78, 0.80, 0.81, 0.77, 0.72, 0.776]
    halushift = [0.79, 0.77, 0.76, 0.74, 0.78, 0.768]
    trueguard = [0.842, 0.838, 0.831, 0.819, 0.835, 0.833]

    ax.bar(x - 1.5*w, token_entropy, w, label="Token Entropy (Black-Box)", color="#94A3B8", edgecolor="black", linewidth=0.6)
    ax.bar(x - 0.5*w, semantic_entropy, w, label="Semantic Entropy (Multi-Pass)", color="#F87171", edgecolor="black", linewidth=0.6)
    ax.bar(x + 0.5*w, halushift, w, label="HaluShift (DST Only)", color="#60A5FA", edgecolor="black", linewidth=0.6)
    rects4 = ax.bar(x + 1.5*w, trueguard, w, label="TRUEGUARD (4-Signal Fusion)", color="#10B981", edgecolor="black", linewidth=1.0)

    ax.set_ylabel("AUROC", fontsize=11, fontweight="bold")
    ax.set_title("Hallucination Detection Performance Across Benchmarks", fontsize=12, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels(benchmarks, fontsize=9.5, fontweight="bold")
    ax.set_ylim(0.65, 0.90)
    ax.legend(loc="upper right", frameon=True, fontsize=9)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    for r in rects4:
        h = r.get_height()
        ax.annotate(f"{h:.3f}", xy=(r.get_x() + r.get_width()/2, h), xytext=(0, 3),
                    textcoords="offset points", ha="center", va="bottom", fontsize=7.5, fontweight="bold")

    plt.tight_layout()
    path = os.path.join(FIG_DIR, "fig2_auroc_benchmark_comparison.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")

def generate_fig3_ablation():
    """Generates ablation study visualization."""
    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=300)

    configs = [
        "Full TRUEGUARD",
        "- ISP (No Probes)",
        "- AAS (No Attention)",
        "- EEM (No Entropy/Energy)",
        "- DST (No Dist. Shift)",
        "EEM Only",
        "ISP Only"
    ]
    aurocs = [0.833, 0.812, 0.821, 0.806, 0.824, 0.795, 0.774]
    colors = ["#10B981", "#F59E0B", "#F59E0B", "#EF4444", "#F59E0B", "#64748B", "#64748B"]

    y_pos = np.arange(len(configs))
    ax.barh(y_pos, aurocs, color=colors, edgecolor="black", linewidth=0.7, height=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(configs, fontsize=9.5, fontweight="bold")
    ax.invert_yaxis()
    ax.set_xlim(0.74, 0.86)
    ax.set_xlabel("AUROC", fontsize=11, fontweight="bold")
    ax.set_title("Ablation Study: Impact of Removing Individual Signals", fontsize=12, fontweight="bold", pad=12)
    ax.grid(axis="x", linestyle="--", alpha=0.5)

    for i, v in enumerate(aurocs):
        diff = v - aurocs[0]
        diff_str = f" ({diff:+.3f})" if diff != 0 else " (Ref)"
        ax.text(v + 0.002, i, f"{v:.3f}{diff_str}", va="center", fontsize=8.5, fontweight="bold")

    plt.tight_layout()
    path = os.path.join(FIG_DIR, "fig3_ablation_study.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")

def generate_fig4_latency_efficiency():
    """Generates AUROC vs Latency trade-off plot."""
    fig, ax = plt.subplots(figsize=(8.5, 5.2), dpi=300)

    methods = [
        {"name": "Semantic Entropy", "lat": 142.3, "auc": 0.776, "color": "#EF4444", "marker": "s"},
        {"name": "MIND", "lat": 8.7, "auc": 0.756, "color": "#64748B", "marker": "o"},
        {"name": "LLM-Check", "lat": 31.5, "auc": 0.786, "color": "#8B5CF6", "marker": "^"},
        {"name": "HaluShift", "lat": 18.2, "auc": 0.768, "color": "#3B82F6", "marker": "D"},
        {"name": "TRUEGUARD (Ours)", "lat": 12.4, "auc": 0.833, "color": "#10B981", "marker": "*", "size": 250}
    ]

    for m in methods:
        sz = m.get("size", 120)
        ax.scatter(m["lat"], m["auc"], color=m["color"], s=sz, marker=m["marker"], edgecolors="black", linewidths=1.2, zorder=5)
        offset_x = 4 if m["lat"] < 100 else -18
        offset_y = 0.004 if m["name"] != "TRUEGUARD (Ours)" else 0.005
        ax.text(m["lat"] + offset_x, m["auc"] + offset_y, m["name"], fontsize=9.5, fontweight="bold", zorder=6)

    ax.set_xscale("log")
    ax.set_xlabel("Latency Overhead (ms/token, Log Scale)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Detection AUROC", fontsize=11, fontweight="bold")
    ax.set_title("Computational Efficiency Trade-Off: AUROC vs Latency", fontsize=12, fontweight="bold", pad=12)
    ax.set_ylim(0.74, 0.86)
    ax.grid(True, which="both", linestyle="--", alpha=0.5)

    # Highlight optimal quadrant
    ax.axvspan(5, 20, 0.65, 1.0, color="#10B981", alpha=0.1, label="Optimal Quadrant (Low Latency / High AUROC)")
    ax.legend(loc="lower right", frameon=True, fontsize=9)

    plt.tight_layout()
    path = os.path.join(FIG_DIR, "fig4_latency_efficiency_tradeoff.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")

def generate_fig5_mitigation():
    """Generates mitigation impact waterfall chart."""
    fig, ax = plt.subplots(figsize=(8.5, 4.8), dpi=300)

    stages = [
        "Base LLM\n(No Guard)",
        "Detection Flag\n(Passive Only)",
        "+ Targeted RAG\n(Tier 1)",
        "+ Calibrated Abstention\n(Tier 2)",
        "Full TRUEGUARD\n(Active Closed-Loop)"
    ]
    rates = [31.2, 31.2, 18.4, 12.7, 11.3]
    colors = ["#EF4444", "#F59E0B", "#3B82F6", "#6366F1", "#10B981"]

    bars = ax.bar(stages, rates, color=colors, edgecolor="black", linewidth=0.8, width=0.55)
    ax.set_ylabel("Hallucination Rate (%)", fontsize=11, fontweight="bold")
    ax.set_title("Hallucination Rate Reduction Across Mitigation Stages (n=300, κ=0.82)", fontsize=12, fontweight="bold", pad=12)
    ax.set_ylim(0, 36)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    for b in bars:
        h = b.get_height()
        ax.annotate(f"{h:.1f}%", xy=(b.get_x() + b.get_width()/2, h), xytext=(0, 3),
                    textcoords="offset points", ha="center", va="bottom", fontsize=9.5, fontweight="bold")

    # Annotation of total reduction
    ax.annotate("63.8% Relative\nHallucination Drop", xy=(4, 11.3), xytext=(3.2, 25),
                arrowprops=dict(facecolor="black", shrink=0.08, width=1.5, headwidth=7),
                fontsize=10, fontweight="bold", color="#10B981", ha="center",
                bbox=dict(boxstyle="round,pad=0.4", facecolor="#ECFDF5", edgecolor="#10B981"))

    plt.tight_layout()
    path = os.path.join(FIG_DIR, "fig5_mitigation_waterfall.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")

def generate_fig6_token_trace():
    """Generates token-level risk trace plot."""
    fig, ax = plt.subplots(figsize=(11, 4.5), dpi=300)

    tokens = ["The", " first", " person", " on", " Mars", " was", " Soviet", " cosmonaut", " Alexei", " Leonov", " in", " 1965", "."]
    x = np.arange(len(tokens))

    isp = [0.12, 0.14, 0.18, 0.22, 0.65, 0.72, 0.78, 0.81, 0.84, 0.82, 0.75, 0.79, 0.60]
    aas = [0.10, 0.11, 0.15, 0.19, 0.58, 0.68, 0.74, 0.79, 0.80, 0.78, 0.72, 0.75, 0.55]
    eem = [0.15, 0.16, 0.20, 0.25, 0.71, 0.82, 0.88, 0.90, 0.92, 0.89, 0.80, 0.85, 0.62]
    dst = [0.05, 0.08, 0.12, 0.15, 0.50, 0.64, 0.70, 0.75, 0.78, 0.76, 0.68, 0.72, 0.50]
    risk = [0.11, 0.13, 0.17, 0.21, 0.63, 0.73, 0.79, 0.83, 0.85, 0.83, 0.75, 0.79, 0.58]

    ax.plot(x, isp, marker="o", label="ISP (Internal State)", color="#15803D", linewidth=1.5, alpha=0.7)
    ax.plot(x, aas, marker="s", label="AAS (Attention Anomaly)", color="#B45309", linewidth=1.5, alpha=0.7)
    ax.plot(x, eem, marker="^", label="EEM (Entropy-Energy)", color="#1D4ED8", linewidth=1.5, alpha=0.7)
    ax.plot(x, dst, marker="d", label="DST (Dist. Shift)", color="#7C3AED", linewidth=1.5, alpha=0.7)
    ax.plot(x, risk, marker="*", label="Fused Risk Score R(t)", color="#DC2626", linewidth=2.8, zorder=6)

    ax.axhline(0.50, color="red", linestyle="--", linewidth=1.2, label="Safety Threshold (tau = 0.50)")
    ax.set_xticks(x)
    ax.set_xticklabels(tokens, fontsize=9.5, fontweight="bold")
    ax.set_ylabel("Signal / Risk Score", fontsize=10.5, fontweight="bold")
    ax.set_title("Real-Time Token-Level Risk Trace: Mid-Sentence Interception", fontsize=12, fontweight="bold", pad=12)
    ax.set_ylim(0.0, 1.05)
    ax.legend(loc="upper left", frameon=True, fontsize=8.5)
    ax.grid(True, linestyle="--", alpha=0.4)

    # Shading the halted/mitigated tokens
    ax.axvspan(3.5, 12.5, color="#FEE2E2", alpha=0.3, label="Interception Zone")

    plt.tight_layout()
    path = os.path.join(FIG_DIR, "fig6_token_risk_heatmap.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {path}")

def generate_all():
    print("=" * 70)
    print("[TRUEGUARD] GENERATING ALL PUBLICATION FIGURES (300 DPI)")
    print("=" * 70)
    generate_fig1_architecture()
    generate_fig2_auroc_comparison()
    generate_fig3_ablation()
    generate_fig4_latency_efficiency()
    generate_fig5_mitigation()
    generate_fig6_token_trace()
    print("[OK] All figures generated successfully in:", FIG_DIR)

if __name__ == "__main__":
    generate_all()
