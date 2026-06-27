# TRUEGUARD: Trustworthy, Unified, Real-time, Explainable Guard

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Paper](https://img.shields.io/badge/Paper-IEEE-blue)

**A Unified Multi-Signal Framework for Real-Time Hallucination Detection, Explainability, and Mitigation in Large Language Models (LLMs).**

---

## 📖 Overview

Large Language Models (LLMs) are powerful, but their deployment in critical domains is often hindered by **hallucinations**—fluent but factually incorrect outputs. While many methods exist to detect or mitigate these, they operate in isolation, lack human-interpretable explanations, or fail to correct the model in real-time.

**TRUEGUARD** is the first unified framework that bridges the gap between hallucination detection, human-centered explainability, and active mitigation in a single coherent pipeline. It evaluates the model's internal computational state to identify uncertainty, explains its reasoning to the user, and dynamically corrects hallucinations before they propagate.

---

## ✨ Key Features & Architecture

TRUEGUARD operates through four interconnected modules designed to solve the complete hallucination problem with near-zero error tolerance:

### 1. Multi-Signal Hallucination Detector
Extracts four complementary signals within a **single forward pass** (11.5x faster than typical multi-sampling models):
*   **Internal State Probes (ISP):** Identifies hallucination-aware components in hidden layers.
*   **Attention Anomaly Score (AAS):** Monitors uncertainty-aware attention heads that lose focus on context.
*   **Entropy-Energy Monitor (EEM):** Detects abrupt entropy spikes indicating low model confidence.
*   **Distribution Shift Tracker (DST):** Tracks statistical divergence in the model's generation trajectory.

### 2. Learned Multi-Signal Fusion
Combines the four token-level signals through a learned weighting mechanism to produce a highly accurate, unified hallucination risk score.

### 3. Real-Time Explainability Engine
Translates opaque risk scores into human-interpretable trust indicators:
*   **Token-Level Annotations:** Visual color-coded trust indicators for generated claims.
*   **Contrastive Explanations:** Explains *why* a claim is flagged based on internal state data.
*   **Adaptive Context:** Adjusts explanation depth based on user context.

### 4. Closed-Loop Mitigation Pipeline
An active controller that halts generation upon detecting high risk:
*   **Retrieval-Augmented Grounding (RAG):** Re-queries specific flagged claims against factual knowledge bases.
*   **Calibrated Abstention:** If uncertainty persists, the model gracefully abstains or flags its own uncertainty.

---

## 📊 Experimental Results

Evaluated across TruthfulQA, HaluEval, and HELM using LLaMA-2 (7B/13B), Mistral-7B, and Qwen-2.5-7B, TRUEGUARD demonstrates state-of-the-art performance:

*   **Detection Accuracy:** Achieves **0.844 AUROC**, a 5.2% improvement over the best individual baseline.
*   **Efficiency:** Operates in a single forward pass with only **12.4 ms/token** overhead.
*   **Mitigation:** Reduces overall hallucination rates by **63.8%** compared to unguarded baselines, raising factual accuracy from 68.8% to 85.6%.
*   **Robustness:** Excels at detecting both intrinsic (contradicting input) and extrinsic (fabricated) hallucinations.

---

## 🚀 Getting Started (Coming Soon)

*(Instructions for cloning the repository, installing dependencies, and running inference with TRUEGUARD will be provided upon public code release.)*

```bash
# Example Placeholder
git clone https://github.com/username/trueguard.git
cd trueguard
pip install -r requirements.txt
python run_trueguard.py --model mistral-7b
```

---

## 📄 Paper & Citation

This project is the culmination of a Capstone research initiative documented in an IEEE-format journal paper. It synthesizes insights from 20 foundational works on LLM uncertainty, internal state analysis, and human-computer trust.

If you find this work useful, please consider citing:

```bibtex
@article{trueguard2026,
  title={TRUEGUARD: A Unified Multi-Signal Framework for Real-Time Hallucination Detection, Explainability, and Mitigation in Large Language Models},
  author={Yogesh Ravi (and Collaborators)},
  journal={IEEE/Under Review},
  year={2026}
}
```

---

## 🤝 Contributing

Contributions are welcome! If you are interested in extending TRUEGUARD to Multimodal LLMs (MLLMs), improving probe efficiency for 70B+ models, or developing personalized trust profiles, please open an issue or submit a pull request.

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
