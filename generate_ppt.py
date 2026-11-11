from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

def add_title_slide(prs):
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]

    title.text = "TRUEGUARD"
    
    # Format subtitle
    subtitle.text = ("A Lightweight Real-Time Framework for Hallucination Detection and Mitigation in LLMs\n\n"
                     "Presented by: YOGESH RAVI M (22MIA0001)\n"
                     "Guide: Dr. T. S. PRADEEP KUMAR\n"
                     "Review 3 - Final Presentation")
    
    # Speaker notes
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = "Good morning everyone. My project is TRUEGUARD, a real-time framework to detect and mitigate hallucinations in Large Language Models."

def add_bullet_slide(prs, title_text, bullet_points, notes_text=""):
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    body = slide.placeholders[1]
    
    title.text = title_text
    
    tf = body.text_frame
    tf.text = bullet_points[0]
    for point in bullet_points[1:]:
        p = tf.add_paragraph()
        p.text = point
        p.level = 0
        
    # Add notes
    notes_slide = slide.notes_slide
    notes_tf = notes_slide.notes_text_frame
    notes_tf.text = notes_text

def create_presentation():
    prs = Presentation()
    
    # Slide 1: Title
    add_title_slide(prs)
    
    # Slide 2: Problem Statement
    add_bullet_slide(prs, 
        "Problem Statement & Motivation", 
        [
            "LLMs frequently generate fluent yet factually unfounded statements (hallucinations).",
            "This severely limits deployment in safety-critical domains (healthcare, legal).",
            "Existing detection requires multi-sample checks (high latency: ~142ms/token) or relies on single white-box metrics.",
            "There is a persistent disconnect between post-hoc detection and active real-time mitigation."
        ],
        "The core motivation is that current hallucination detection methods are either too slow for streaming, or they only capture one type of hallucination without actively stopping it."
    )
    
    # Slide 3: Literature Review
    add_bullet_slide(prs,
        "Literature Review Summary",
        [
            "Black-Box Multi-Sample: SelfCheckGPT & Semantic Entropy (Reliable but computationally expensive).",
            "Single-Signal Probes: MIND, HaluShift, Attention Entropy (Fast but captures limited uncertainty facets).",
            "Inference-Time Mitigation: Chain-of-Verification, Universal RAG (Adds massive latency to every query).",
            "Research Gap: Lack of a unified, lightweight, multi-signal tracker with an integrated active mitigation controller."
        ],
        "We reviewed several key papers. The main gap identified is that no framework unites multiple intrinsic signals (attention, hidden states, logits) into a fast, closed-loop mitigation engine."
    )
    
    # Slide 4: Proposed Objectives
    add_bullet_slide(prs,
        "Objectives of TRUEGUARD",
        [
            "Develop a multi-signal white-box extraction pipeline directly from the LLM execution graph.",
            "Combine four orthogonal signals: Representation, Attention, Predictive, and Temporal uncertainty.",
            "Maintain ultra-low latency overhead to support real-time token streaming.",
            "Implement a closed-loop active mitigation strategy (Targeted RAG & Calibrated Abstention)."
        ],
        "Our primary objective was to build a system that can track hallucination risk inline, per-token, without running multiple forward passes."
    )
    
    # Slide 5: The TRUEGUARD Framework
    add_bullet_slide(prs,
        "System Architecture",
        [
            "Intercepts activations from a frozen LLM in a single forward pass.",
            "Extracts 4 signals: ISP (Internal State Probes), AAS (Attention Anomaly Score), EEM (Entropy-Energy Monitor), DST (Distribution Shift Tracker).",
            "Signals are dynamically standardized (Z-score) online.",
            "A learned logistic regression layer fuses signals into a token risk score R(t)."
        ],
        "The architecture is lightweight. We hook into the transformer layers to pull hidden states and attention matrices while the model generates text normally."
    )
    
    # Slide 6: Multi-Signal Details
    add_bullet_slide(prs,
        "The Four Intrinsic Signals",
        [
            "ISP: Probes middle-to-late transformer layers for factual confidence.",
            "AAS: Monitors context attention dispersion via normalized Shannon entropy.",
            "EEM: Combines output Shannon entropy and Rényi-2 sharpness.",
            "DST: Measures temporal cosine drift between successive token representations."
        ],
        "Each signal captures a different dimension. EEM captures predictive uncertainty, ISP captures representational truth, AAS catches context loss, and DST catches semantic drift."
    )
    
    # Slide 7: Active Closed-Loop Mitigation
    add_bullet_slide(prs,
        "Active Mitigation Engine",
        [
            "If sequence risk exceeds a calibrated threshold (τ = 0.50), generation halts mid-sentence.",
            "Tier 1 (Targeted RAG): System attempts to retrieve verified entities and restart generation.",
            "Tier 2 (Calibrated Abstention): If RAG fails, the model emits an honest disclaimer declining to answer.",
            "Prevents ungrounded text from reaching the end-user."
        ],
        "Instead of just flagging errors after the fact, TRUEGUARD stops the generation immediately when risk spikes and attempts to ground the response or abstain gracefully."
    )
    
    # Slide 8: Experimental Setup
    add_bullet_slide(prs,
        "Experimental Methodology",
        [
            "Models: LLaMA-2-7B-Chat, Mistral-7B-Instruct, TinyLlama-1.1B.",
            "Datasets: TruthfulQA, HaluEval (QA, Summ, Dial), HELM.",
            "Validation Protocol: Strict 5-fold cross-validation.",
            "Hardware: NVIDIA T4 GPU and local CPU smoke tests."
        ],
        "We strictly evaluated this across five benchmarks, including TruthfulQA and HaluEval, utilizing proper 5-fold CV to ensure robustness."
    )
    
    # Slide 9: Results - Detection Accuracy
    add_bullet_slide(prs,
        "Results: Hallucination Detection",
        [
            "Achieved an average AUROC of 0.8821 ± 0.0170 across all 5 benchmarks.",
            "TruthfulQA AUROC: 0.8533 ± 0.0533.",
            "HaluEval-QA AUROC: 0.8840 ± 0.0185.",
            "Ablation studies proved all 4 signals were necessary (dropping EEM caused the largest penalty)."
        ],
        "TRUEGUARD consistently outperformed single-signal baselines and achieved strong AUROC across all domains."
    )
    
    # Slide 10: Results - Latency
    add_bullet_slide(prs,
        "Results: Efficiency & Latency Speedup",
        [
            "Semantic Entropy (Baseline): 142.3 ms overhead per token.",
            "LLM-Check: 31.5 ms overhead.",
            "TRUEGUARD: 12.4 ± 0.5 ms overhead per token.",
            "Speedup: 11.5x faster than Semantic Entropy.",
            "Total extraction requires < 0.05% of a standard forward pass compute."
        ],
        "Our system introduces only 12.4 milliseconds of latency per token. This is an 11.5x speedup compared to multi-sample methods, making it highly feasible for real-time edge use."
    )
    
    # Slide 11: Results - Mitigation Effectiveness
    add_bullet_slide(prs,
        "Results: Mitigation Performance",
        [
            "Baseline Hallucination Rate: 31.2%.",
            "With Full TRUEGUARD Closed-Loop: 11.3%.",
            "Relative Hallucination Reduction: 63.8%.",
            "Maintained high query answer coverage: 88.0%."
        ],
        "By applying Tier 1 and Tier 2 mitigation, we achieved a verified 63.8% relative reduction in hallucinations without severely crippling the model's usefulness."
    )
    
    # Slide 12: Conclusion
    add_bullet_slide(prs,
        "Conclusion & Future Scope",
        [
            "TRUEGUARD successfully unifies four intrinsic model signals into a real-time guard layer.",
            "Delivers high AUROC (0.8821) with negligible streaming latency (12.4 ms).",
            "Provides a defensible, verified active mitigation strategy.",
            "Future Work: Extend calibration to multilingual settings and multi-agent workflows."
        ],
        "In conclusion, TRUEGUARD is a lightweight, effective, and verifiable framework for trustworthy LLM inference. Thank you."
    )

    prs.save('TRUEGUARD_Final_Review.pptx')
    print("Presentation generated successfully.")

if __name__ == '__main__':
    create_presentation()
