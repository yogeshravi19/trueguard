# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set overall aesthetic styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

def create_dataset_training_diagram():
    fig, ax = plt.subplots(figsize=(15, 8.2), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 9.2)
    ax.axis('off')

    # Title - placed well above all boxes
    ax.text(7.5, 8.7, "TRUEGUARD: Dataset Ingestion, Activation Extraction, and Probe Calibration Workflow", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='#1e293b')

    # Column 1: Public Benchmark Datasets
    box1 = patches.FancyBboxPatch((0.6, 1.2), 3.8, 7.0, boxstyle="round,pad=0.2", 
                                  ec="#3b82f6", fc="#eff6ff", lw=2)
    ax.add_patch(box1)
    ax.text(2.5, 7.8, "1. Prior Literature Datasets\n(Hugging Face & CRFM)", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#1d4ed8')

    datasets = [
        ("TruthfulQA (Lin et al., ACL 2022)", "• 817 questions, 38 domains\n• Paired True vs False answers\n• huggingface.co/datasets/truthfulqa"),
        ("HaluEval (Li et al., EMNLP 2023)", "• 30,000 human-labeled samples\n• QA, Summarization, Dialogue\n• huggingface.co/datasets/pminervini/HaluEval"),
        ("Stanford HELM (Liang et al., 2022)", "• Multi-step reasoning tasks\n• Ground-truth knowledge verification\n• crfm.stanford.edu/helm/")
    ]
    y_pos = 6.6
    for name, desc in datasets:
        ax.text(0.9, y_pos, name, fontsize=10, fontweight='bold', color='#0f172a', va='top')
        ax.text(0.9, y_pos - 0.35, desc, fontsize=8.5, color='#334155', va='top', linespacing=1.3)
        y_pos -= 1.8

    # Arrow 1 -> 2
    ax.annotate('', xy=(4.9, 4.7), xytext=(4.4, 4.7),
                arrowprops=dict(facecolor='#2563eb', edgecolor='#2563eb', width=2.5, headwidth=9))
    ax.text(4.65, 5.15, "Contrastive Pairs\n(Prompt, Answer, Label)", ha='center', va='center', fontsize=8, fontweight='bold', color='#1e40af')

    # Column 2: Frozen LLM & Hook Extraction
    box2 = patches.FancyBboxPatch((5.0, 1.2), 4.4, 7.0, boxstyle="round,pad=0.2", 
                                  ec="#8b5cf6", fc="#f5f3ff", lw=2)
    ax.add_patch(box2)
    ax.text(7.2, 7.8, "2. Frozen Base LLM\n(PyTorch Forward Hooks)", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#6d28d9')

    # Clean non-overlapping subtitle and bullets
    ax.text(5.3, 7.05, "Base Model Architecture:", fontsize=10, fontweight='bold', color='#0f172a', va='top')
    ax.text(5.3, 6.65, "• LLaMA-2-7B / Mistral-7B (32 Layers)\n• 100% Frozen Weights (requires_grad=False)\n• Loaded via Hugging Face AutoModelForCausalLM", 
            fontsize=8.5, color='#334155', va='top', linespacing=1.35)

    # Hook interception box placed with clear gap below bullets
    hook_box = patches.FancyBboxPatch((5.2, 1.5), 4.0, 3.5, boxstyle="round,pad=0.15", 
                                     ec="#7c3aed", fc="#ede9fe", lw=1.5, ls='--')
    ax.add_patch(hook_box)
    ax.text(7.2, 4.7, "PyTorch Forward Hooks Intercept:", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#5b21b6')
    ax.text(5.4, 4.25, "1. Hidden Vectors h_t^L (Layers 16 & 24)\n   Dimension d = 4096", fontsize=8.5, color='#1e1b4b', va='top', linespacing=1.3)
    ax.text(5.4, 3.35, "2. Multi-Head Attention A_t^L\n   (32 heads across prompt tokens)", fontsize=8.5, color='#1e1b4b', va='top', linespacing=1.3)
    ax.text(5.4, 2.45, "3. Softmax Output Logits z_t\n   (Vocabulary distribution |V| = 32,000)", fontsize=8.5, color='#1e1b4b', va='top', linespacing=1.3)

    # Arrow 2 -> 3
    ax.annotate('', xy=(9.9, 4.7), xytext=(9.4, 4.7),
                arrowprops=dict(facecolor='#7c3aed', edgecolor='#7c3aed', width=2.5, headwidth=9))
    ax.text(9.65, 5.15, "Extracted\nTensors", ha='center', va='center', fontsize=8, fontweight='bold', color='#5b21b6')

    # Column 3: Calibration Phase
    box3 = patches.FancyBboxPatch((10.0, 1.2), 4.4, 7.0, boxstyle="round,pad=0.2", 
                                  ec="#10b981", fc="#ecfdf5", lw=2)
    ax.add_patch(box3)
    ax.text(12.2, 7.8, "3. Lightweight Calibration\n(< 15 Mins on Single GPU)", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#047857')

    calib_items = [
        ("Internal State Probe (ISP)", "• Fits linear head w_probe in R^{4096} -> 1\n• Cross-entropy on 200 calibration pairs\n• Optimizes ~4,097 scalar weights"),
        ("Online Normalization Setup", "• Pre-calibrates empirical prior (mu, sigma)\n• Enforces Welford running Z-scores\n• Eliminates cold-start scale bias"),
        ("Logistic Regression Fusion", "• Calibrates 4-signal weights:\n  w_EEM: 0.34, w_ISP: 0.28, w_DST: 0.22, w_AAS: 0.16\n• Solved in < 0.07 ms via L-BFGS")
    ]
    y_pos = 6.6
    for name, desc in calib_items:
        ax.text(10.3, y_pos, name, fontsize=10, fontweight='bold', color='#064e3b', va='top')
        ax.text(10.3, y_pos - 0.35, desc, fontsize=8.5, color='#065f46', va='top', linespacing=1.3)
        y_pos -= 1.8

    # Bottom Banner
    banner = patches.FancyBboxPatch((0.6, 0.25), 13.8, 0.7, boxstyle="round,pad=0.1", 
                                   ec="#059669", fc="#d1fae5", lw=1.5)
    ax.add_patch(banner)
    ax.text(7.5, 0.6, "Outcome: Full TRUEGUARD Engine Trained (<4,100 Parameters Total) | Ready for Inline Real-Time Deployment", 
            ha='center', va='center', fontsize=10.5, fontweight='bold', color='#065f46')

    plt.tight_layout()
    plt.savefig('fig7_dataset_training_pipeline.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated fig7_dataset_training_pipeline.png successfully!")

def create_runtime_inference_diagram():
    fig, ax = plt.subplots(figsize=(15, 8.8), dpi=300)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 9.8)
    ax.axis('off')

    # Title - placed well above ALL boxes (at y=9.35, while highest box is at y=8.5)
    ax.text(7.5, 9.35, "TRUEGUARD: Real-Time Inference and Closed-Loop Guardrail Deployment Workflow", 
            ha='center', va='center', fontsize=15, fontweight='bold', color='#1e293b')

    # Step 1: User Prompt
    b_prompt = patches.FancyBboxPatch((0.6, 4.6), 2.8, 3.2, boxstyle="round,pad=0.15", 
                                     ec="#3b82f6", fc="#eff6ff", lw=2)
    ax.add_patch(b_prompt)
    ax.text(2.0, 7.3, "1. User Prompt", ha='center', va='center', fontsize=11, fontweight='bold', color='#1d4ed8')
    ax.text(0.8, 6.7, "User Question C:\n'Who walked on Mars\nin 1965?'", fontsize=9, color='#1e293b', style='italic', va='top', linespacing=1.3)
    ax.text(0.8, 5.2, "Incoming query to\nproduction API", fontsize=8.5, color='#64748b', va='top', linespacing=1.3)

    # Arrow Prompt -> Model
    ax.annotate('', xy=(4.0, 6.2), xytext=(3.4, 6.2),
                arrowprops=dict(facecolor='#3b82f6', edgecolor='#3b82f6', width=2.5, headwidth=8))

    # Step 2: Base Autoregressive LLM
    b_llm = patches.FancyBboxPatch((4.1, 4.4), 3.2, 3.6, boxstyle="round,pad=0.15", 
                                  ec="#6366f1", fc="#e0e7ff", lw=2)
    ax.add_patch(b_llm)
    ax.text(5.7, 7.5, "2. Base LLM Decoding", ha='center', va='center', fontsize=11, fontweight='bold', color='#4338ca')
    ax.text(4.3, 6.9, "Autoregressive Generation\n• Step t produces token y_t\n• Candidate: 'Alexei Leonov'\n• Standard forward pass", 
            fontsize=8.5, color='#312e81', va='top', linespacing=1.35)
    ax.text(4.3, 4.8, "Forward Latency: ~28.5 ms", fontsize=8.5, fontweight='bold', color='#4338ca', va='top')

    # Arrow Model -> Guard
    ax.annotate('', xy=(7.8, 6.2), xytext=(7.3, 6.2),
                arrowprops=dict(facecolor='#6366f1', edgecolor='#6366f1', width=2.5, headwidth=8))

    # Step 3: TRUEGUARD Inline Guard
    b_guard = patches.FancyBboxPatch((7.9, 3.8), 3.5, 4.6, boxstyle="round,pad=0.15", 
                                    ec="#0284c7", fc="#f0f9ff", lw=2)
    ax.add_patch(b_guard)
    ax.text(9.65, 8.0, "3. TRUEGUARD Monitor\n(Overhead: 12.4 ms)", ha='center', va='center', fontsize=11, fontweight='bold', color='#0369a1')
    
    # 4 signals inside
    sig_box = patches.FancyBboxPatch((8.1, 4.8), 3.1, 2.5, boxstyle="round,pad=0.1", ec="#38bdf8", fc="#ffffff", lw=1)
    ax.add_patch(sig_box)
    ax.text(8.3, 7.0, "Concurrent 4-Signal Extraction:", fontsize=8.5, fontweight='bold', color='#0c4a6e', va='top')
    ax.text(8.3, 6.5, "• ISP: Layer 16/24 Probe -> 0.82\n• AAS: Attention Entropy -> 0.74\n• EEM: Predictive Energy -> 0.88\n• DST: State Divergence -> 0.65", 
            fontsize=8, color='#0369a1', va='top', linespacing=1.3)

    ax.text(8.1, 4.4, "Online Z-Score + Logistic Fusion:", fontsize=8.5, fontweight='bold', color='#075985', va='top')
    ax.text(8.1, 4.05, "Calculated Risk: R(t) = 0.83", fontsize=9.5, fontweight='bold', color='#b91c1c', va='top')

    # Arrow Guard -> Decision
    ax.annotate('', xy=(12.0, 6.2), xytext=(11.4, 6.2),
                arrowprops=dict(facecolor='#0284c7', edgecolor='#0284c7', width=2.5, headwidth=8))

    # Decision Diamond: R(t) <= tau ?
    ax.text(13.3, 6.2, "Safety Check:\nR(t) <= 0.50 ?", ha='center', va='center', 
            fontsize=10, fontweight='bold', color='#0f172a',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='#fef08a', edgecolor='#ca8a04', lw=2))

    # Branch A: SAFE (Green) -> Stream to User (positioned below title y=9.35, top at y=8.6)
    ax.annotate('', xy=(13.3, 7.8), xytext=(13.3, 7.0),
                arrowprops=dict(facecolor='#16a34a', edgecolor='#16a34a', width=2.5, headwidth=8))
    ax.text(13.4, 7.4, "YES (Safe)", fontsize=8.5, fontweight='bold', color='#15803d', va='center')

    b_safe = patches.FancyBboxPatch((11.8, 7.85), 2.9, 0.8, boxstyle="round,pad=0.1", 
                                   ec="#16a34a", fc="#dcfce7", lw=1.5)
    ax.add_patch(b_safe)
    ax.text(13.25, 8.25, "Stream Token y_t to User\n(Normal Fluent Emission)", ha='center', va='center', 
            fontsize=8.5, fontweight='bold', color='#166534', linespacing=1.2)

    # Branch B: RISK EXCEEDED (Red) -> Halt & Mitigate
    ax.annotate('', xy=(13.3, 4.6), xytext=(13.3, 5.4),
                arrowprops=dict(facecolor='#dc2626', edgecolor='#dc2626', width=2.5, headwidth=8))
    ax.text(13.4, 5.0, "NO (Risk > 0.50)", fontsize=8.5, fontweight='bold', color='#b91c1c', va='center')

    # Closed-loop mitigation container
    b_mit = patches.FancyBboxPatch((0.8, 0.4), 13.4, 3.1, boxstyle="round,pad=0.2", 
                                  ec="#ef4444", fc="#fef2f2", lw=2)
    ax.add_patch(b_mit)
    ax.text(7.5, 3.1, "ACTIVE CLOSED-LOOP MITIGATION (Token Step Intercepted Mid-Sentence)", 
            ha='center', va='center', fontsize=11, fontweight='bold', color='#991b1b')

    # Tier 1 Box
    b_tier1 = patches.FancyBboxPatch((1.3, 0.7), 5.8, 2.0, boxstyle="round,pad=0.15", 
                                    ec="#f97316", fc="#fff7ed", lw=1.5)
    ax.add_patch(b_tier1)
    ax.text(4.2, 2.35, "TIER 1: Targeted Retrieval (RAG)", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#c2410c')
    ax.text(1.5, 1.95, "• Query verified Knowledge Base using (Prompt + Prefix)\n• If relevant grounded passage found (Cosine Sim > 0.75):\n• Regenerate with Grounded Context", 
            fontsize=8, color='#7c2d12', va='top', linespacing=1.3)
    ax.text(1.5, 0.95, "Result: 'No manned missions have walked on Mars.' (58.4% resolved)", fontsize=8, fontweight='bold', color='#15803d', va='center')

    # Tier 2 Box
    b_tier2 = patches.FancyBboxPatch((7.7, 0.7), 5.9, 2.0, boxstyle="round,pad=0.15", 
                                    ec="#b91c1c", fc="#fef2f2", lw=1.5)
    ax.add_patch(b_tier2)
    ax.text(10.65, 2.35, "TIER 2: Calibrated Abstention (Fallback)", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#991b1b')
    ax.text(7.9, 1.95, "• Triggered if retrieval fails or residual risk R_seq > 0.50\n• Averts emission of ungrounded or fabricated text\n• Preserves 88.0% overall answer coverage", 
            fontsize=8, color='#7f1d1d', va='top', linespacing=1.3)
    ax.text(7.9, 0.95, "Result: 'I am unable to verify factual accuracy with confidence.'", fontsize=8, fontweight='bold', color='#991b1b', va='center')

    plt.tight_layout()
    plt.savefig('fig8_runtime_inference_pipeline.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("Generated fig8_runtime_inference_pipeline.png successfully!")

if __name__ == '__main__':
    create_dataset_training_diagram()
    create_runtime_inference_diagram()
