import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

# Theme Colors
BG_DARK = "#080F25"
BG_CARD = "#0F1A36"
CYAN = "#00D7F2"
TEAL = "#2EE3BE"
VIOLET = "#9779FF"
CRIMSON = "#FF5F72"
WHITE = "#F4F7FF"
MUTED = "#94A3B8"
BORDER = "#1E2D56"

OUT_DIR = Path("outputs/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = BORDER
plt.rcParams['axes.linewidth'] = 1.2

def draw_white_vs_black_box():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7.5), facecolor=BG_DARK)
    
    # --- Ax1: Black-Box ---
    ax1.set_facecolor(BG_DARK)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    
    ax1.text(5, 9.3, "BLACK-BOX LLM PARADIGM", ha='center', va='center', color=WHITE, fontsize=16, fontweight='bold')
    ax1.text(5, 8.7, "(Commercial APIs: ChatGPT, Claude, Gemini)", ha='center', va='center', color=MUTED, fontsize=12)
    
    # User Input
    box_in = patches.FancyBboxPatch((1.5, 6.8), 7.0, 1.2, boxstyle="round,pad=0.2", fc=BG_CARD, ec=CYAN, lw=2)
    ax1.add_patch(box_in)
    ax1.text(5, 7.4, "USER PROMPT / API REQUEST", ha='center', va='center', color=WHITE, fontsize=13, fontweight='bold')
    
    # Down arrow
    ax1.annotate('', xy=(5, 5.5), xytext=(5, 6.6), arrowprops=dict(arrowstyle="->", color=CYAN, lw=2.5))
    
    # Black Box
    box_bb = patches.FancyBboxPatch((1.5, 3.2), 7.0, 2.3, boxstyle="round,pad=0.2", fc="#050814", ec=CRIMSON, lw=2.5, ls="--")
    ax1.add_patch(box_bb)
    ax1.text(5, 4.8, "OPAQUE BLACK-BOX API", ha='center', va='center', color=CRIMSON, fontsize=14, fontweight='bold')
    ax1.text(5, 4.1, "Hidden States: INACCESSIBLE (403 Forbidden)", ha='center', va='center', color=MUTED, fontsize=11)
    ax1.text(5, 3.6, "Attention Weights: INACCESSIBLE | Logits: Hidden", ha='center', va='center', color=MUTED, fontsize=11)
    
    # Down arrow
    ax1.annotate('', xy=(5, 2.0), xytext=(5, 3.1), arrowprops=dict(arrowstyle="->", color=CRIMSON, lw=2.5))
    
    # Output box
    box_out = patches.FancyBboxPatch((1.5, 0.7), 7.0, 1.2, boxstyle="round,pad=0.2", fc=BG_CARD, ec=MUTED, lw=1.5)
    ax1.add_patch(box_out)
    ax1.text(5, 1.5, "FINAL GENERATED TEXT", ha='center', va='center', color=WHITE, fontsize=13, fontweight='bold')
    ax1.text(5, 1.0, "Detection relies solely on expensive external LLM verifiers", ha='center', va='center', color=CRIMSON, fontsize=10)

    # --- Ax2: White-Box (TRUEGUARD) ---
    ax2.set_facecolor(BG_DARK)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    
    ax2.text(5, 9.3, "WHITE-BOX LLM PARADIGM: TRUEGUARD", ha='center', va='center', color=CYAN, fontsize=16, fontweight='bold')
    ax2.text(5, 8.7, "(Self-Hosted Models: TinyLlama-1.1B, Llama-3, Mistral)", ha='center', va='center', color=TEAL, fontsize=12)
    
    # User Input
    box_in2 = patches.FancyBboxPatch((1.5, 7.6), 7.0, 0.9, boxstyle="round,pad=0.2", fc=BG_CARD, ec=CYAN, lw=2)
    ax2.add_patch(box_in2)
    ax2.text(5, 8.05, "USER PROMPT -> TOKENIZER", ha='center', va='center', color=WHITE, fontsize=12, fontweight='bold')
    
    ax2.annotate('', xy=(5, 6.7), xytext=(5, 7.5), arrowprops=dict(arrowstyle="->", color=CYAN, lw=2))
    
    # Model Layers
    box_model = patches.FancyBboxPatch((1.5, 5.0), 7.0, 1.7, boxstyle="round,pad=0.2", fc=BG_CARD, ec=VIOLET, lw=2)
    ax2.add_patch(box_model)
    ax2.text(5, 6.2, "FROZEN TINYLLAMA-1.1B BACKBONE", ha='center', va='center', color=WHITE, fontsize=13, fontweight='bold')
    ax2.text(5, 5.5, "22 Transformer Layers | 2048-dim Hidden States", ha='center', va='center', color=VIOLET, fontsize=11)
    
    # Lateral arrows to telemetry
    ax2.annotate('', xy=(5, 4.0), xytext=(5, 4.9), arrowprops=dict(arrowstyle="->", color=TEAL, lw=2.5))
    
    # TRUEGUARD Sensors
    box_sensors = patches.FancyBboxPatch((1.0, 2.3), 8.0, 1.7, boxstyle="round,pad=0.2", fc="#0B1C3D", ec=TEAL, lw=2.5)
    ax2.add_patch(box_sensors)
    ax2.text(5, 3.55, "TRUEGUARD INTERNAL TELEMETRY BANK", ha='center', va='center', color=TEAL, fontsize=13, fontweight='bold')
    ax2.text(2.6, 2.85, "ISP (Layers 9,13,16,19)", ha='center', va='center', color=WHITE, fontsize=10)
    ax2.text(7.4, 2.85, "AAS (Layers 16-21)", ha='center', va='center', color=WHITE, fontsize=10)
    ax2.text(2.6, 2.5, "EEM (Shannon + Renyi)", ha='center', va='center', color=WHITE, fontsize=10)
    ax2.text(7.4, 2.5, "DST (Cosine Shift)", ha='center', va='center', color=WHITE, fontsize=10)
    
    ax2.annotate('', xy=(5, 1.5), xytext=(5, 2.2), arrowprops=dict(arrowstyle="->", color=CYAN, lw=2.5))
    
    # Fusion & Controller
    box_ctrl = patches.FancyBboxPatch((1.0, 0.4), 8.0, 1.1, boxstyle="round,pad=0.2", fc=BG_CARD, ec=CYAN, lw=2)
    ax2.add_patch(box_ctrl)
    ax2.text(5, 1.1, "CALIBRATED FUSION & 3-TIER MITIGATION CONTROLLER", ha='center', va='center', color=CYAN, fontsize=12, fontweight='bold')
    ax2.text(5, 0.65, "Safe Pass (32%) | Resampling (7.3%) | RAG (4%) | Abstention (56.7%)", ha='center', va='center', color=WHITE, fontsize=10)
    
    plt.tight_layout()
    plt.savefig(OUT_DIR / "fig_sentinel_white_vs_black_box.png", dpi=300, facecolor=BG_DARK)
    plt.close()
    print("Saved fig_sentinel_white_vs_black_box.png")

def draw_entropy_concept():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5), facecolor=BG_DARK)
    
    # Distribution 1: High Confidence / Low Entropy
    ax1.set_facecolor(BG_CARD)
    x = np.arange(10)
    probs_safe = np.array([0.01, 0.02, 0.85, 0.03, 0.02, 0.01, 0.01, 0.02, 0.01, 0.02])
    tokens = ["the", "a", "Paris", "London", "city", "capital", "is", "of", "France", "in"]
    
    bars1 = ax1.bar(x, probs_safe, color=TEAL, edgecolor=WHITE, linewidth=1.2, width=0.6)
    bars1[2].set_color(CYAN)
    bars1[2].set_edgecolor(WHITE)
    bars1[2].set_linewidth(2.0)
    
    ax1.set_title("CONFIDENT / GROUNDED TOKEN\nLow Entropy ($H_{norm} \\approx 0.12$) -> Low Risk", color=TEAL, fontsize=14, fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(tokens, rotation=45, color=WHITE, fontsize=11)
    ax1.set_ylabel("Softmax Probability $P(w_i | x)$", color=WHITE, fontsize=12)
    ax1.set_ylim(0, 1.0)
    ax1.tick_params(colors=WHITE)
    ax1.grid(True, linestyle="--", alpha=0.15, color=WHITE)
    ax1.annotate("Dominant Peak:\nModel is certain\nof factual token", xy=(2, 0.86), xytext=(4, 0.75),
                 arrowprops=dict(arrowstyle="->", color=CYAN, lw=2), color=CYAN, fontsize=11, fontweight='bold')

    # Distribution 2: Hallucination / High Entropy
    ax2.set_facecolor(BG_CARD)
    probs_halluc = np.array([0.14, 0.12, 0.11, 0.13, 0.15, 0.09, 0.08, 0.07, 0.06, 0.05])
    bars2 = ax2.bar(x, probs_halluc, color=CRIMSON, edgecolor=WHITE, linewidth=1.2, width=0.6)
    
    ax2.set_title("HALLUCINATING / UNCERTAIN TOKEN\nHigh Entropy ($H_{norm} \\approx 0.88$) -> High Risk", color=CRIMSON, fontsize=14, fontweight='bold', pad=15)
    ax2.set_xticks(x)
    ax2.set_xticklabels(tokens, rotation=45, color=WHITE, fontsize=11)
    ax2.set_ylabel("Softmax Probability $P(w_i | x)$", color=WHITE, fontsize=12)
    ax2.set_ylim(0, 1.0)
    ax2.tick_params(colors=WHITE)
    ax2.grid(True, linestyle="--", alpha=0.15, color=WHITE)
    ax2.annotate("Flat Distribution:\nProbability spread\nacross competing facts", xy=(4, 0.16), xytext=(4.5, 0.55),
                 arrowprops=dict(arrowstyle="->", color=CRIMSON, lw=2), color=CRIMSON, fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(OUT_DIR / "fig_sentinel_entropy_concept.png", dpi=300, facecolor=BG_DARK)
    plt.close()
    print("Saved fig_sentinel_entropy_concept.png")

def draw_mitigation_flowchart():
    fig, ax = plt.subplots(figsize=(16, 7.5), facecolor=BG_DARK)
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')
    
    ax.text(8, 8.5, "TRUEGUARD THREE-TIER CLOSED-LOOP MITIGATION CONTROLLER", ha='center', va='center', color=WHITE, fontsize=16, fontweight='bold')
    
    # Start: Generation & Risk Scoring
    b_start = patches.FancyBboxPatch((0.5, 5.0), 3.2, 2.0, boxstyle="round,pad=0.2", fc=BG_CARD, ec=CYAN, lw=2)
    ax.add_patch(b_start)
    ax.text(2.1, 6.4, "GENERATION & AUDIT", ha='center', va='center', color=CYAN, fontsize=12, fontweight='bold')
    ax.text(2.1, 5.8, "TinyLlama generates\nAnswer $y = [y_1, ... y_T]$", ha='center', va='center', color=WHITE, fontsize=10)
    ax.text(2.1, 5.3, "TRUEGUARD Risk $R(y)$", ha='center', va='center', color=TEAL, fontsize=11, fontweight='bold')
    
    # Decision Fork
    ax.annotate('', xy=(4.6, 6.0), xytext=(3.8, 6.0), arrowprops=dict(arrowstyle="->", color=WHITE, lw=2.5))
    
    # Safe Pass (Tier 0)
    b_safe = patches.FancyBboxPatch((4.7, 6.7), 3.2, 1.6, boxstyle="round,pad=0.2", fc=BG_CARD, ec=TEAL, lw=2.5)
    ax.add_patch(b_safe)
    ax.text(6.3, 7.9, "SAFE PASS (32.0%)", ha='center', va='center', color=TEAL, fontsize=12, fontweight='bold')
    ax.text(6.3, 7.4, "Condition: $R(y) < \\tau_w$ (0.50)", ha='center', va='center', color=WHITE, fontsize=10)
    ax.text(6.3, 7.0, "Action: Emit answer as-is", ha='center', va='center', color=MUTED, fontsize=10)
    
    # Branch to Tier 1
    b_t1 = patches.FancyBboxPatch((4.7, 4.3), 3.2, 1.8, boxstyle="round,pad=0.2", fc=BG_CARD, ec=CYAN, lw=2)
    ax.add_patch(b_t1)
    ax.text(6.3, 5.6, "TIER 1: RESAMPLE (7.3%)", ha='center', va='center', color=CYAN, fontsize=12, fontweight='bold')
    ax.text(6.3, 5.1, "Condition: $\\tau_w \\leqq R(y) < \\tau_f$", ha='center', va='center', color=WHITE, fontsize=10)
    ax.text(6.3, 4.6, "Sample $K=4$, $T=0.7$, $p=0.9$\nSelect $\\min R(y_k)$", ha='center', va='center', color=MUTED, fontsize=9)

    # Branch to Tier 2
    b_t2 = patches.FancyBboxPatch((8.8, 4.3), 3.2, 1.8, boxstyle="round,pad=0.2", fc=BG_CARD, ec=VIOLET, lw=2)
    ax.add_patch(b_t2)
    ax.text(10.4, 5.6, "TIER 2: RAG SEARCH (4.0%)", ha='center', va='center', color=VIOLET, fontsize=12, fontweight='bold')
    ax.text(10.4, 5.1, "Condition: Initial $R \\geq \\tau_f$ or T1 fails", ha='center', va='center', color=WHITE, fontsize=10)
    ax.text(10.4, 4.6, "Retrieve Wikipedia context\nConditioned generation", ha='center', va='center', color=MUTED, fontsize=9)
    
    # Branch to Tier 3
    b_t3 = patches.FancyBboxPatch((12.5, 2.0), 3.0, 2.0, boxstyle="round,pad=0.2", fc=BG_CARD, ec=CRIMSON, lw=2.5)
    ax.add_patch(b_t3)
    ax.text(14.0, 3.4, "TIER 3: ABSTAIN (56.7%)", ha='center', va='center', color=CRIMSON, fontsize=12, fontweight='bold')
    ax.text(14.0, 2.9, "Condition: Unfixable risk", ha='center', va='center', color=WHITE, fontsize=10)
    ax.text(14.0, 2.4, "\"I do not have sufficient\nconfidence to answer.\"", ha='center', va='center', color=CRIMSON, fontsize=9, style='italic')

    # Connecting arrows
    ax.annotate('', xy=(4.6, 7.4), xytext=(3.8, 6.4), arrowprops=dict(arrowstyle="->", color=TEAL, lw=2))
    ax.annotate('', xy=(4.6, 5.2), xytext=(3.8, 5.8), arrowprops=dict(arrowstyle="->", color=CYAN, lw=2))
    ax.annotate('Escalate if\nstill $\\geq \\tau_w$', xy=(8.7, 5.2), xytext=(8.0, 5.2),
                arrowprops=dict(arrowstyle="->", color=VIOLET, lw=2), color=MUTED, fontsize=9)
    ax.annotate('Escalate if\nstill $\\geq \\tau_f$', xy=(12.4, 3.0), xytext=(11.5, 4.2),
                arrowprops=dict(arrowstyle="->", color=CRIMSON, lw=2), color=CRIMSON, fontsize=9)

    # Final Output Deliverable Box
    b_final = patches.FancyBboxPatch((8.8, 0.6), 6.7, 1.0, boxstyle="round,pad=0.2", fc="#050E24", ec=TEAL, lw=2)
    ax.add_patch(b_final)
    ax.text(12.15, 1.25, "OUTCOME: 72.0% RELATIVE REDUCTION IN EMITTED HALLUCINATIONS", ha='center', va='center', color=TEAL, fontsize=11, fontweight='bold')
    ax.text(12.15, 0.85, "Answer Coverage = 43.3% | Accuracy Among Answered = 60.0% (vs 38.0% baseline)", ha='center', va='center', color=WHITE, fontsize=10)
    
    # Arrows to final
    ax.annotate('', xy=(10.0, 1.7), xytext=(10.4, 4.2), arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.5, ls="--"))
    ax.annotate('', xy=(6.3, 1.7), xytext=(6.3, 4.2), arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.5, ls="--"))
    ax.annotate('', xy=(6.3, 1.7), xytext=(6.3, 6.6), arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.5, ls="--"))

    plt.tight_layout()
    plt.savefig(OUT_DIR / "fig_sentinel_mitigation_controller.png", dpi=300, facecolor=BG_DARK)
    plt.close()
    print("Saved fig_sentinel_mitigation_controller.png")

if __name__ == '__main__':
    draw_white_vs_black_box()
    draw_entropy_concept()
    draw_mitigation_flowchart()
