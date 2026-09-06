# ==============================================================================
# TRUEGUARD: Comprehensive Comparison Figures Generator
# File: generate_all_comparisons.py
# 
# Generates all multi-paper comparison figures used in the Paper & Review 2 PPT:
#   1. Side-by-Side Comparison (Slide 19: Result 1 + Result 2)
#   2. 4-Panel Master Comparison Grid (Figure 9 in Paper)
#   3. AUROC vs F1 Score Scatter Comparison (All 11 detection papers)
#   4. Speedup vs AUROC Efficiency Trade-Off Comparison
# ==============================================================================

import os
import matplotlib.pyplot as plt
import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# ------------------------------------------------------------------------------
# 1. SIDE-BY-SIDE COMPARISON (Slide 19 in Review 2 PPT)
# ------------------------------------------------------------------------------
def generate_side_by_side():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6.2), dpi=300)

    # (A) Error Type Inversion
    methods1 = ['Semantic Entropy\n(Uncertainty)', 'Attention Aggregation\n(Map of Misbelief)', 'P-True\n(Baseline)']
    extrinsic = [89.3, 76.2, 72.1]
    intrinsic = [61.4, 84.5, 67.3]
    x1 = np.arange(len(methods1))
    w1 = 0.35

    rects1_a = ax1.bar(x1 - w1/2, extrinsic, w1, label='Extrinsic (Fabricated info)', color='#D6604D', edgecolor='black', linewidth=0.8, zorder=3)
    rects1_b = ax1.bar(x1 + w1/2, intrinsic, w1, label='Intrinsic (Contradiction)', color='#2166AC', edgecolor='black', linewidth=0.8, zorder=3)
    ax1.set_ylabel('AUROC (%)', fontsize=11, fontweight='bold')
    ax1.set_title('(A) Detection Accuracy by Error Type [Hajji et al., 2025]', fontsize=12, fontweight='bold', pad=10)
    ax1.set_xticks(x1)
    ax1.set_xticklabels(methods1, fontsize=9.5, fontweight='bold')
    ax1.set_ylim(50, 100)
    ax1.legend(loc='upper right', frameon=True, edgecolor='black', facecolor='white', fontsize=9)
    ax1.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)

    for rect in list(rects1_a) + list(rects1_b):
        h = rect.get_height()
        ax1.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                     textcoords='offset points', ha='center', va='bottom', fontweight='bold', fontsize=9)

    # (B) Single-Pass Probing Efficiency
    models2 = ['LLaMA-2-7B', 'LLaMA-2-13B', 'Mistral-7B', 'Falcon-7B']
    se = [91.2, 93.4, 90.8, 88.6]
    sep = [94.1, 96.8, 93.7, 91.4]
    base = [84.3, 87.1, 83.9, 81.6]
    x2 = np.arange(len(models2))
    w2 = 0.25

    rects2_a = ax2.bar(x2 - w2, se, w2, label='Semantic Entropy (Multi-pass, ~10× Cost)', color='#D6604D', edgecolor='black', linewidth=0.8, zorder=3)
    rects2_b = ax2.bar(x2, sep, w2, label='SEP Probing (Single-pass, 1× Cost)', color='#1B7837', edgecolor='black', linewidth=0.8, zorder=3)
    rects2_c = ax2.bar(x2 + w2, base, w2, label='Prev. Probe Baseline', color='#999999', edgecolor='black', linewidth=0.8, zorder=3)
    ax2.set_ylabel('AUROC (%)', fontsize=11, fontweight='bold')
    ax2.set_xlabel('Language Model', fontsize=11, fontweight='bold')
    ax2.set_title('(B) SEP vs Semantic Entropy Across Models [Han et al., 2024]', fontsize=12, fontweight='bold', pad=10)
    ax2.set_xticks(x2)
    ax2.set_xticklabels(models2, fontsize=9.5, fontweight='bold')
    ax2.set_ylim(75, 102)
    ax2.legend(loc='upper left', frameon=True, edgecolor='black', facecolor='white', fontsize=8.5)
    ax2.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)

    for rect in list(rects2_a) + list(rects2_b) + list(rects2_c):
        h = rect.get_height()
        ax2.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                     textcoords='offset points', ha='center', va='bottom', fontweight='bold', fontsize=8)

    plt.suptitle('TRUEGUARD Literature Review: Empirical Evidence on Complementarity and Probing Efficiency', 
                 fontsize=13.5, fontweight='bold', y=0.98)
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "review2_side_by_side_comparison.png")
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out}")


# ------------------------------------------------------------------------------
# 2. 4-PANEL MASTER COMPARISON GRID (Figure 9 in Paper / 00_combined_summary)
# ------------------------------------------------------------------------------
def generate_4panel_grid():
    fig, axs = plt.subplots(2, 2, figsize=(18, 14), dpi=300)

    # Panel (A): HaluEval AUROC (9 Papers)
    methods_a = ["MIND\n(P1)", "EPR\n(P17)", "PRISM\n(P2)", "HALLUSHIFT\n(P13)", "MHAD\n(P5)",
                 "Sem.Energy\n(P4)", "RAUQ\n(P11)", "LLM-Check\n(P12)", "SEP\n(P14)"]
    auroc_a = [83.6, 83.9, 86.4, 86.9, 87.1, 89.7, 90.2, 92.8, 94.3]
    colors_a = ["#2166AC", "#D6604D", "#2166AC", "#7570B3", "#2166AC", "#D6604D", "#1B7837", "#2166AC", "#D6604D"]
    y_pos_a = np.arange(len(methods_a))
    
    axs[0, 0].barh(y_pos_a, auroc_a, color=colors_a, edgecolor='black', linewidth=0.7, zorder=3)
    axs[0, 0].set_yticks(y_pos_a)
    axs[0, 0].set_yticklabels(methods_a, fontsize=9, fontweight='bold')
    axs[0, 0].set_xlim(75, 98)
    axs[0, 0].set_xlabel('AUROC (%)', fontsize=10, fontweight='bold')
    axs[0, 0].set_title('(A) AUROC on HaluEval Benchmark (9 Papers Compared)', fontsize=11, fontweight='bold')
    axs[0, 0].grid(axis='x', linestyle='--', alpha=0.5, zorder=0)
    for i, v in enumerate(auroc_a):
        axs[0, 0].text(v + 0.3, i, f"{v}%", va='center', fontweight='bold', fontsize=8.5)

    # Panel (B): SEP vs Semantic Entropy
    models_b = ['LLaMA-2-7B', 'LLaMA-2-13B', 'Mistral-7B', 'Falcon-7B']
    se_b = [91.2, 93.4, 90.8, 88.6]
    sep_b = [94.1, 96.8, 93.7, 91.4]
    base_b = [84.3, 87.1, 83.9, 81.6]
    x_b = np.arange(len(models_b))
    wb = 0.25

    axs[0, 1].bar(x_b - wb, se_b, wb, label='Semantic Entropy (10× cost)', color='#D6604D', edgecolor='black', zorder=3)
    axs[0, 1].bar(x_b, sep_b, wb, label='SEP Probe (1× cost)', color='#1B7837', edgecolor='black', zorder=3)
    axs[0, 1].bar(x_b + wb, base_b, wb, label='Prev. Probe Baseline', color='#999999', edgecolor='black', zorder=3)
    axs[0, 1].set_xticks(x_b)
    axs[0, 1].set_xticklabels(models_b, fontsize=9, fontweight='bold')
    axs[0, 1].set_ylim(75, 102)
    axs[0, 1].set_ylabel('AUROC (%)', fontsize=10, fontweight='bold')
    axs[0, 1].set_title('(B) SEP vs Semantic Entropy Across 4 Models', fontsize=11, fontweight='bold')
    axs[0, 1].legend(loc='upper left', frameon=True, fontsize=8.5)
    axs[0, 1].grid(axis='y', linestyle='--', alpha=0.5, zorder=0)

    # Panel (C): Intrinsic vs Extrinsic Error Type
    methods_c = ['Semantic Entropy', 'Map of Misbelief\n(Attention)', 'P-True\n(Baseline)']
    ext_c = [89.3, 76.2, 72.1]
    int_c = [61.4, 84.5, 67.3]
    x_c = np.arange(len(methods_c))
    wc = 0.35

    axs[1, 0].bar(x_c - wc/2, ext_c, wc, label='Extrinsic (Fabricated info)', color='#D6604D', edgecolor='black', zorder=3)
    axs[1, 0].bar(x_c + wc/2, int_c, wc, label='Intrinsic (Contradiction)', color='#2166AC', edgecolor='black', zorder=3)
    axs[1, 0].set_xticks(x_c)
    axs[1, 0].set_xticklabels(methods_c, fontsize=9, fontweight='bold')
    axs[1, 0].set_ylim(50, 100)
    axs[1, 0].set_ylabel('AUROC (%)', fontsize=10, fontweight='bold')
    axs[1, 0].set_title('(C) Performance by Hallucination Type (Signal Inversion)', fontsize=11, fontweight='bold')
    axs[1, 0].legend(loc='upper right', frameon=True, fontsize=8.5)
    axs[1, 0].grid(axis='y', linestyle='--', alpha=0.5, zorder=0)

    # Panel (D): Improvement Over Baseline (%) Across 13 Papers
    methods_d = ["SEP\n(P14)", "ExpandR\n(P20)", "EPR\n(P17)", "RAUQ\n(P11)", "MHAD\n(P5)",
                 "HShift++\n(P16)", "HShift\n(P13)", "FaithEval\n(P10)", "PRISM\n(P2)",
                 "SEnergy\n(P4)", "LLMCheck\n(P12)", "BehCal\n(P15)", "HTrust\n(P19)"]
    gains_d = [4.1, 5.3, 7.3, 8.9, 9.2, 9.4, 11.3, 11.5, 12.4, 13.0, 15.2, 18.6, 22.0]
    y_pos_d = np.arange(len(methods_d))

    axs[1, 1].barh(y_pos_d, gains_d, color='#1B7837', edgecolor='black', linewidth=0.7, zorder=3)
    axs[1, 1].set_yticks(y_pos_d)
    axs[1, 1].set_yticklabels(methods_d, fontsize=8.5, fontweight='bold')
    axs[1, 1].set_xlim(0, 26)
    axs[1, 1].set_xlabel('Improvement Over Baseline (%)', fontsize=10, fontweight='bold')
    axs[1, 1].set_title('(D) Reported Gain Over Baseline Across 13 Papers', fontsize=11, fontweight='bold')
    axs[1, 1].grid(axis='x', linestyle='--', alpha=0.5, zorder=0)
    for i, v in enumerate(gains_d):
        axs[1, 1].text(v + 0.3, i, f"+{v}%", va='center', fontweight='bold', fontsize=8)

    plt.suptitle('TRUEGUARD Meta-Analysis: 4-Panel Cross-Paper Empirical Comparison', 
                 fontsize=15, fontweight='bold', y=0.98)
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "figure9_4panel_master_comparison.png")
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out}")


# ------------------------------------------------------------------------------
# 3. AUROC VS F1 SCORE SCATTER COMPARISON (Figure 7 in Paper)
# ------------------------------------------------------------------------------
def generate_auroc_vs_f1():
    methods = ["MIND", "PRISM", "Sem.Energy", "MHAD", "Map.Misbelief", "RAUQ",
               "LLM-Check", "HALLUSHIFT", "SEP", "HALLUSHIFT++", "EPR"]
    auroc = [83.6, 86.4, 89.7, 87.1, 84.5, 90.2, 92.8, 86.9, 94.3, 86.3, 83.9]
    f1 = [80.4, 83.2, 87.1, 84.5, 81.2, 87.3, 89.7, 83.8, 91.2, 82.4, 81.6]
    speedups = [1, 1, 1, 1, 3, 1, 45, 1, 8, 1, 1]
    signals = ["Internal", "Internal", "Entropy", "Internal", "Attention", "Attention",
               "Internal", "Distribution", "Entropy", "Distribution", "Entropy"]
    
    color_map = {"Internal": "#2166AC", "Entropy": "#D6604D", "Attention": "#1B7837", "Distribution": "#7570B3"}
    point_colors = [color_map[s] for s in signals]
    point_sizes = [np.log(s + 1) * 120 + 80 for s in speedups]

    fig, ax = plt.subplots(figsize=(10, 6.5), dpi=300)
    scatter = ax.scatter(auroc, f1, s=point_sizes, c=point_colors, edgecolors='black', linewidth=1.2, alpha=0.9, zorder=3)

    for i, txt in enumerate(methods):
        ax.annotate(f"{txt} ({speedups[i]}×)", (auroc[i], f1[i]), xytext=(7, 5), textcoords='offset points',
                    fontweight='bold', fontsize=9)

    ax.set_xlabel('AUROC (%)', fontsize=11, fontweight='bold')
    ax.set_ylabel('F1 Score (%)', fontsize=11, fontweight='bold')
    ax.set_title('AUROC vs. F1 Score for All 11 Detection Methods\n(Bubble size = log(speedup), Color = Signal type)', 
                 fontsize=12, fontweight='bold', pad=12)
    ax.set_xlim(82, 96)
    ax.set_ylim(78, 93)
    ax.grid(True, linestyle='--', alpha=0.5, zorder=0)

    # Custom legend for signals
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Internal States', markerfacecolor='#2166AC', markersize=10, markeredgecolor='k'),
        Line2D([0], [0], marker='o', color='w', label='Entropy/Energy', markerfacecolor='#D6604D', markersize=10, markeredgecolor='k'),
        Line2D([0], [0], marker='o', color='w', label='Attention', markerfacecolor='#1B7837', markersize=10, markeredgecolor='k'),
        Line2D([0], [0], marker='o', color='w', label='Distribution', markerfacecolor='#7570B3', markersize=10, markeredgecolor='k')
    ]
    ax.legend(handles=legend_elements, loc='lower right', frameon=True, edgecolor='black', title='Signal Type')

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, "auroc_vs_f1_scatter_comparison.png")
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out}")

if __name__ == "__main__":
    generate_side_by_side()
    generate_4panel_grid()
    generate_auroc_vs_f1()
    print("\nAll comparison figures generated successfully in figures/!")
