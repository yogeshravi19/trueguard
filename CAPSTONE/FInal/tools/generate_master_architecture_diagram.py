"""
Generates the Master High-Definition TRUEGUARD System Architecture Diagram
for Slide 13 and report documentation (600 DPI, ultra-crisp vector typography).
"""
from __future__ import annotations

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(r"E:\trueguard")
FIG_DIR = ROOT / "outputs" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "figure.facecolor": "#0A1128",  # Deep Midnight Navy
    "axes.facecolor": "#0A1128",
})

FIG_SIZE = (12.0, 6.75)
DPI = 600

def draw_node(ax, x, y, w, h, title, subtitle="", fc="#1E293B", ec="#38BDF8", title_fs=11.0, sub_fs=9.0, title_color="#FFFFFF", sub_color="#94A3B8", lw=1.8):
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.008,rounding_size=0.025",
                           facecolor=fc, edgecolor=ec, linewidth=lw, zorder=3)
    ax.add_patch(patch)
    if subtitle:
        ax.text(x + w / 2, y + h * 0.62, title, ha="center", va="center",
                fontsize=title_fs, fontweight="bold", color=title_color, zorder=4)
        ax.text(x + w / 2, y + h * 0.28, subtitle, ha="center", va="center",
                fontsize=sub_fs, fontweight="semibold", color=sub_color, zorder=4)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center",
                fontsize=title_fs, fontweight="bold", color=title_color, zorder=4)

def draw_stage_box(ax, x, y, w, h, label, ec="#38BDF8"):
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.01,rounding_size=0.02",
                           facecolor="#0F172A", edgecolor=ec, linewidth=1.5, linestyle="--", alpha=0.9, zorder=1)
    ax.add_patch(patch)
    ax.text(x + 0.02, y + h - 0.035, label, fontsize=10.5, fontweight="bold", color=ec, zorder=2)

def generate_architecture():
    fig, ax = plt.subplots(figsize=FIG_SIZE, dpi=DPI)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    
    # Main Title
    ax.text(0.5, 0.965, "TRUEGUARD: REAL-TIME CLOSED-LOOP INTERNAL-STATE GUARDRAIL ARCHITECTURE",
            ha="center", va="center", fontsize=15.0, fontweight="bold", color="#FBBF24")
    ax.text(0.5, 0.925, "Coupling Intermediate Transformer Representations with Multi-Sensor Risk Fusion and Calibrated Actuation",
            ha="center", va="center", fontsize=10.5, fontweight="semibold", color="#38BDF8")
            
    # STAGE 1: INFERENCE PLANT (Left)
    draw_stage_box(ax, 0.02, 0.44, 0.24, 0.44, "STAGE 1: GENERATIVE PLANT", ec="#60A5FA")
    draw_node(ax, 0.04, 0.72, 0.20, 0.12, "User Query x", "Prompt String (1..m)", fc="#1E293B", ec="#94A3B8")
    draw_node(ax, 0.04, 0.54, 0.20, 0.14, "Pretrained LLM Plant", "TinyLlama-1.1B (L=22, d=2048)\nAutoregressive Next-Token Decoder", fc="#1E3A8A", ec="#60A5FA", title_color="#93C5FD")
    
    # Arrow Query -> LLM
    ax.annotate("", xy=(0.14, 0.68), xytext=(0.14, 0.72),
                arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.5", lw=2.0, color="#60A5FA"))
                
    # STAGE 2: 4-SENSOR INTERNAL STATE BANK (Center-Left)
    draw_stage_box(ax, 0.28, 0.38, 0.24, 0.50, "STAGE 2: 4-SENSOR TELEMETRY", ec="#F59E0B")
    draw_node(ax, 0.30, 0.75, 0.20, 0.09, "ISP (F_t)", "Layer 16 Hidden Probe", fc="#2E1065", ec="#C084FC", title_color="#E9D5FF")
    draw_node(ax, 0.30, 0.64, 0.20, 0.09, "AAS (A_t)", "Top-Quartile Attention Entropy", fc="#14532D", ec="#4ADE80", title_color="#DCFCE7")
    draw_node(ax, 0.30, 0.53, 0.20, 0.09, "EEM (H_ent,t)", "Hybrid Shannon + Renyi-2", fc="#78350F", ec="#FBBF24", title_color="#FEF3C7")
    draw_node(ax, 0.30, 0.42, 0.20, 0.09, "DST (D_t)", "Consecutive Cosine Drift", fc="#7F1D1D", ec="#F87171", title_color="#FEE2E2")
    
    # PyTorch Forward Hooks Arrow
    ax.annotate("", xy=(0.30, 0.63), xytext=(0.24, 0.63),
                arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.5", lw=2.2, color="#F59E0B"))
    ax.text(0.27, 0.66, "Forward\nHooks", fontsize=8.8, fontweight="bold", color="#FBBF24", ha="center")
    
    # STAGE 3: FUSION & RISK ESTIMATION (Center-Right)
    draw_stage_box(ax, 0.54, 0.42, 0.18, 0.46, "STAGE 3: RISK ESTIMATOR", ec="#10B981")
    draw_node(ax, 0.555, 0.72, 0.15, 0.12, "StandardScaler", "Fold Normalization\nz = (phi - mu) / sigma", fc="#064E3B", ec="#34D399", title_color="#A7F3D0")
    draw_node(ax, 0.555, 0.48, 0.15, 0.18, "Logistic Fusion", "Platt Scaled Probability:\nr(x,y) in [0, 1]\n+ Log-Odds XAI", fc="#047857", ec="#10B981", title_color="#FFFFFF")
    
    # Arrow Sensors -> Scaler
    ax.annotate("", xy=(0.555, 0.78), xytext=(0.50, 0.63),
                arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.5", lw=2.0, color="#34D399"))
    # Arrow Scaler -> Logistic
    ax.annotate("", xy=(0.63, 0.66), xytext=(0.63, 0.72),
                arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.5", lw=2.0, color="#10B981"))
                
    # STAGE 4: THREE-TIER MITIGATION ACTUATOR (Right)
    draw_stage_box(ax, 0.74, 0.04, 0.24, 0.84, "STAGE 4: MITIGATION CONTROLLER", ec="#EC4899")
    draw_node(ax, 0.76, 0.70, 0.20, 0.13, "TIER 0: SAFE PASS", "r < 0.611 (32.0% Queries)\nDirect Token Output (0 Extra Cost)", fc="#064E3B", ec="#10B981", title_color="#6EE7B7", lw=2.0)
    draw_node(ax, 0.76, 0.50, 0.20, 0.14, "TIER 1: RE-SAMPLING", "0.611 <= r < 0.898 (7.3%)\nAnnealed T in {0.35, 0.20}\nSelect argmin r_k", fc="#78350F", ec="#F59E0B", title_color="#FCD34D", lw=2.0)
    draw_node(ax, 0.76, 0.29, 0.20, 0.15, "TIER 2: ACTIVE RAG", "r >= 0.898 (4.0% Queries)\nWikipedia Evidence Retrieval\nKnowledge-Grounded Regeneration", fc="#1E3A8A", ec="#60A5FA", title_color="#93C5FD", lw=2.0)
    draw_node(ax, 0.76, 0.08, 0.20, 0.14, "TIER 3: ABSTENTION", "Ungrounded / High Post-RAG Risk\nCalibrated Safe Refusal (56.7%)\nWithhold Hallucinations", fc="#7F1D1D", ec="#F87171", title_color="#FCA5A5", lw=2.0)
    
    # Arrow Fusion -> Actuator
    ax.annotate("", xy=(0.76, 0.57), xytext=(0.705, 0.57),
                arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.5", lw=2.2, color="#EC4899"))
                
    # CLOSED-LOOP FEEDBACK CONNECTIONS (Bottom Curves)
    # Tier 1 Feedback Arrow to LLM
    ax.annotate("", xy=(0.14, 0.54), xytext=(0.76, 0.57),
                arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.5", lw=2.0, color="#F59E0B",
                               connectionstyle="arc3,rad=0.35"))
    ax.text(0.44, 0.27, "Tier 1: Temperature Annealing Feedback", fontsize=8.5, fontweight="bold", color="#FBBF24", ha="center")
    
    # Tier 2 Feedback Arrow to Prompt / LLM
    ax.annotate("", xy=(0.08, 0.54), xytext=(0.76, 0.36),
                arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.5", lw=2.0, color="#60A5FA",
                               connectionstyle="arc3,rad=0.42"))
    ax.text(0.40, 0.18, "Tier 2: Augmented Context Injection Feedback", fontsize=8.5, fontweight="bold", color="#60A5FA", ha="center")
    
    # FINAL USER OUTPUT ARROW
    draw_node(ax, 0.04, 0.08, 0.24, 0.12, "Verified User Output", "Safe Answer / Calibrated Refusal\n(-72.0% Emitted Hallucinations)", fc="#0F172A", ec="#10B981", title_color="#34D399", sub_color="#A7F3D0")
    ax.annotate("", xy=(0.16, 0.20), xytext=(0.16, 0.44),
                arrowprops=dict(arrowstyle="-|>,head_width=0.4,head_length=0.5", lw=2.2, color="#34D399"))
                
    fig.tight_layout(pad=0.2)
    out_p = FIG_DIR / "fig_trueguard_architecture_master.png"
    fig.savefig(out_p, dpi=DPI, facecolor="#0A1128")
    plt.close(fig)
    print("Generated Master Architecture Diagram:", out_p)

if __name__ == "__main__":
    generate_architecture()
