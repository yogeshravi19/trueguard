# TRUEGUARD Interactive Research Demonstration (Offline Portable Demo)

## Quick Start (Presentation Laptop)
1. Simply **double-click** `index.html` on any laptop!
2. Opens immediately in **Google Chrome**, **Microsoft Edge**, **Firefox**, or **Safari**.
3. **100% Offline:** Requires **NO Python, NO PyTorch, NO CUDA, NO Model Weights, and NO Internet connection**.

---

## What the Demonstration Shows to the Examiners

### 1. Two Curated Evaluation Suites
- **Suite 1: Cross-Benchmark Research Scenarios:**
  - Watermelon Seeds Digestion Misconception (TruthfulQA)
  - Fortune Cookie Origin (TruthfulQA)
  - Arthur's Magazine vs First for Women Chronological Inversion (HaluEval-QA)
  - Germanwings Flight 9525 Prosecutor Statement (HaluEval-Summarization)
  - Robert Downey Jr. Zodiac Costar Entity Misattribution (HaluEval-Dialogue)
  - 1965 Soviet Mars Landing Counterfactual Trap (Adversarial)
- **Suite 2: Recorded TinyLlama-1.1B Colab Traces ($N=150$):**
  - Real experimental data loaded directly from `mitigation_report.json` on TriviaQA queries.

### 2. Side-by-Side Comparison
- **WITHOUT TRUEGUARD:** Baseline TinyLlama-1.1B emitting hallucinations with 0% internal detection at 33.49 ms/tok.
- **WITH TRUEGUARD:** Token-by-token risk highlighting (Green = Safe, Amber = Warning, Red = Hallucination), real-time sensor dials, and closed-loop mitigation decisions.

### 3. Four-Tier Closed-Loop Controller
- **SAFE PASS-THROUGH:** $R \le 0.611$ (Original answer approved).
- **TIER 1 (RESAMPLE REGENERATION):** $0.611 < R \le 0.898$ (Resamples candidate completions).
- **TIER 2 (RETRIEVAL REPAIR):** $0.611 < R \le 0.898$ (Retrieves verified knowledge grounding).
- **TIER 3 (CALIBRATED ABSTENTION):** $R > 0.898$ (Suppresses fabrication with calibrated refusal).

### 4. Interactive Token Inspector
Click any individual token in the protected stream to inspect its specific **ISP**, **AAS**, **EEM**, and **DST** values.

---

## Author & Capstone Details
- **Project:** Toward Trustworthy Large Language Models: A Comprehensive Review of Hallucination Detection, Explainability, and Mitigation Strategies
- **Candidate:** Yogesh Ravi M (22MIA1052)
- **Guide:** Dr. Pradeep Kumar T.S.
- **Institution:** School of Computer Science and Engineering, Vellore Institute of Technology, Chennai
