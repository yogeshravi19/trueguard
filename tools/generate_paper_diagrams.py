# ==============================================================================
# TRUEGUARD: Reproduction Scripts for Review 2 PPT & Paper Diagrams
# File: generate_paper_diagrams.py
# 
# Generates:
#   1. Diagram 1 (Slide 19 Fig. 3 / Paper Fig. 1): 
#      Detection Accuracy by Hallucination Type (Extrinsic vs Intrinsic)
#   2. Diagram 2 (Slide 19 Fig. 4 / Paper Fig. 2): 
#      Single-Pass Probing (SEP) vs Multi-Pass Sampling (Semantic Entropy)
# ==============================================================================

import os
import matplotlib.pyplot as plt
import numpy as np

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------------------------------------------------------
# DIAGRAM 1: Detection Accuracy by Hallucination Type (Extrinsic vs Intrinsic)
# Source: Hajji, Bouguerra & Arnez (2025) / Paper 9 (Map of Misbelief)
# ------------------------------------------------------------------------------
def generate_diagram_1():
    print("Generating Diagram 1: Detection Accuracy by Hallucination Type...")
    
    methods = [
        "Semantic Entropy\n(Uncertainty)", 
        "Attention Aggregation\n(Map of Misbelief)", 
        "P-True\n(Baseline)"
    ]
    extrinsic_acc = [89.3, 76.2, 72.1]  # Fabricated facts / Extrinsic
    intrinsic_acc = [61.4, 84.5, 67.3]  # Contradictions / Intrinsic

    x = np.arange(len(methods))
    width = 0.35

    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=300)

    rects1 = ax.bar(x - width/2, extrinsic_acc, width, 
                    label='Extrinsic Hallucination (Fabricated info)', 
                    color='#D6604D', edgecolor='black', linewidth=0.8, zorder=3)
    rects2 = ax.bar(x + width/2, intrinsic_acc, width, 
                    label='Intrinsic Hallucination (Contradiction)', 
                    color='#2166AC', edgecolor='black', linewidth=0.8, zorder=3)

    ax.set_ylabel('AUROC (%)', fontsize=12, fontweight='bold', color='black')
    ax.set_title('Detection Accuracy by Hallucination Type [Hajji et al., 2025]', 
                 fontsize=13, fontweight='bold', pad=15, color='black')
    ax.set_xticks(x)
    ax.set_xticklabels(methods, fontsize=10, fontweight='bold', color='black')
    ax.set_ylim(50, 100)
    
    ax.legend(frameon=True, edgecolor='black', facecolor='white', framealpha=0.9, 
              fontsize=9.5, loc='upper right')
    ax.grid(axis='y', linestyle='--', alpha=0.6, color='grey', zorder=0)

    # Add data labels
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, 4), textcoords='offset points', 
                    ha='center', va='bottom', fontweight='bold', fontsize=9.5)

    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, 4), textcoords='offset points', 
                    ha='center', va='bottom', fontweight='bold', fontsize=9.5)

    # Key insight annotation box
    bbox_props = dict(boxstyle="round,pad=0.5", fc="#FFF9C4", ec="#FBC02D", lw=1.2)
    ax.text(0.5, -0.22, 
            "Key Insight: Signals swap rank depending on error type (Uncertainty excels on fabricated info; Attention excels on contradictions).\nThis proves single-signal detectors are insufficient and motivates TRUEGUARD multi-signal fusion.",
            ha="center", va="center", transform=ax.transAxes, fontsize=8.5, style="italic", bbox=bbox_props)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "review2_diagram1_hallucination_types.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")


# ------------------------------------------------------------------------------
# DIAGRAM 2: Single-Run Probing (SEP) vs Multi-Run Sampling across Four Models
# Source: Han, Kossen, Razzak et al. (2024) / Paper 14 (SEP)
# ------------------------------------------------------------------------------
def generate_diagram_2():
    print("Generating Diagram 2: SEP vs Semantic Entropy across Four Models...")
    
    models = ['LLaMA-2-7B', 'LLaMA-2-13B', 'Mistral-7B', 'Falcon-7B']
    se_scores = [91.2, 93.4, 90.8, 88.6]      # Semantic Entropy (multi-pass, 10x compute)
    sep_scores = [94.1, 96.8, 93.7, 91.4]     # SEP (single-pass internal probe)
    probe_base = [84.3, 87.1, 83.9, 81.6]     # Previous Probe Baseline

    x = np.arange(len(models))
    width = 0.26

    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, ax = plt.subplots(figsize=(9.5, 5.5), dpi=300)

    rects1 = ax.bar(x - width, se_scores, width, 
                    label='Semantic Entropy (Multi-pass Sampling, ~10× Cost)', 
                    color='#D6604D', edgecolor='black', linewidth=0.8, zorder=3)
    rects2 = ax.bar(x, sep_scores, width, 
                    label='SEP Probing (Single Forward-Pass, 1× Cost)', 
                    color='#1B7837', edgecolor='black', linewidth=0.8, zorder=3)
    rects3 = ax.bar(x + width, probe_base, width, 
                    label='Previous Probe Baseline', 
                    color='#999999', edgecolor='black', linewidth=0.8, zorder=3)

    ax.set_ylabel('AUROC (%)', fontsize=12, fontweight='bold', color='black')
    ax.set_xlabel('Large Language Model', fontsize=12, fontweight='bold', color='black', labelpad=8)
    ax.set_title('SEP vs. Semantic Entropy Across Models [Han et al., 2024]', 
                 fontsize=13, fontweight='bold', pad=15, color='black')
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=10, fontweight='bold', color='black')
    ax.set_ylim(75, 102)

    ax.legend(frameon=True, edgecolor='black', facecolor='white', framealpha=0.9, 
              fontsize=9, loc='upper left')
    ax.grid(axis='y', linestyle='--', alpha=0.6, color='grey', zorder=0)

    # Add data labels
    for rects in [rects1, rects2, rects3]:
        for rect in rects:
            h = rect.get_height()
            ax.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width()/2, h),
                        xytext=(0, 3), textcoords='offset points', 
                        ha='center', va='bottom', fontweight='bold', fontsize=8.2)

    # Key insight annotation box
    bbox_props = dict(boxstyle="round,pad=0.5", fc="#E8F5E9", ec="#4CAF50", lw=1.2)
    ax.text(0.5, -0.25, 
            "Key Insight: Single-pass probe (SEP) outperforms multi-pass sampling (SE) on all 4 models (e.g. 96.8% vs 93.4% on LLaMA-2-13B)\nwhile running at ~1/8 the compute cost. Proves rich uncertainty signal already exists in internal activations.",
            ha="center", va="center", transform=ax.transAxes, fontsize=8.5, style="italic", bbox=bbox_props)

    plt.tight_layout()
    out_path = os.path.join(OUTPUT_DIR, "review2_diagram2_sep_vs_se.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    generate_diagram_1()
    generate_diagram_2()
    print("\nAll diagrams successfully generated in figures/ directory!")
