# TRUEGUARD — Complete Session State & Chat Restore Handover

**Previous Conversation ID:** `fde343c8-893c-42cf-b120-bc6081bcf61f`  
**Transcript Path:** `C:\Users\INDIA\.gemini\antigravity\brain\fde343c8-893c-42cf-b120-bc6081bcf61f\.system_generated\logs\transcript.jsonl`  
**Date Saved:** November 11, 2026

> **Instruction for Agent when user says "restore chat":** Read this file (`E:\trueguard\CHAT_RESTORE_STATE.md`) immediately to restore the complete context of our two-paper TRUEGUARD project, all verified Tesla T4 GPU experimental results, and all generated deliverables.

---

## 1. Two-Paper Project Structure
1. **Paper 1 (Systematic Review & Conceptual Proposal — Ready to Submit):**
   - Clean Manuscript: `E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models_standard.docx`
   - Marked Manuscript: `E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models_coloured.docx`
   - Response to Reviewers: `E:\trueguard\CAPSTONE\Response_to_Reviewers_269790004.docx`
   - Standalone 40-Paper Literature Review by 6 Pillars (Navy Table Format):
     - `E:\trueguard\TRUEGUARD_40_Papers_Literature_Review_By_Pillars.docx`
     - `E:\trueguard\CAPSTONE\FInal\paper\TRUEGUARD_40_Papers_Literature_Review_By_Pillars.docx`
     - `E:\trueguard\TRUEGUARD_40_Papers_Literature_Review_By_Pillars.md`

2. **Paper 2 (Empirical Implementation & Evaluation of TRUEGUARD v2 — Executed & Verified on Colab Tesla T4 GPU):**
   - Word Manuscript (`.docx` with tables & 6 T4 GPU plots): `E:\trueguard\CAPSTONE\FInal\paper\TRUEGUARD_Paper2_Implementation.docx`
   - Markdown Manuscript: `E:\trueguard\CAPSTONE\FInal\paper\TRUEGUARD_Paper2_Implementation.md`
   - IEEE Two-Column LaTeX Manuscript: `E:\trueguard\CAPSTONE\FInal\paper\TRUEGUARD_Paper2_IEEE.tex`
   - Faculty Presentation Slides (`.pptx`): `E:\trueguard\CAPSTONE\FInal\TRUEGUARD_Faculty_Presentation_Verified.pptx`
   - Architecture Verification Report: `E:\trueguard\CAPSTONE\FInal\ARCHITECTURE_VERIFICATION_REPORT.md`

---

## 2. Refactored Codebase (`E:\trueguard\CAPSTONE\FInal\`)
- `src/tg_pipeline.py` — 4 single-pass sensors (`ISP` supervised 4-layer probes with inner OOF stacking, `AAS` final-quartile attention entropy, `EEM` $0.6\,\text{Shannon}+0.4\,\text{Rényi-2}$ logit monitor, `DST` layer-averaged cosine drift), `score_answer` (teacher-forced) & `OnlineSignalMonitor` (KV-cached step-by-step), `TrueGuardDetector` (leakage-free logistic fusion + `explain` log-odds attribution).
- `src/tg_controller.py` — Two calibrated thresholds ($\tau_{\text{warning}}, \tau_{\text{fault}}$) & three-tier closed-loop controller (`SAFE`, `TIER1_RESAMPLE`, `TIER2_RETRIEVAL` with `WikipediaRetriever`, `TIER3_ABSTAIN`).
- `src/tg_eval.py` — Grouped 5-fold CV (`GroupKFold`), group bootstrap CIs, threshold calibration, complementarity, risk–coverage (`AURC`), and figure plotters.
- `src/tg_data.py` & `datasets/` — 5 real downloaded benchmarks (`TruthfulQA`, `HaluEval-QA`, `HaluEval-Dialogue`, `HaluEval-Summarization`, `TriviaQA`) + `datasets/DATASET_SOURCES.md` & `datasets/manifest.json`.
- `experiments/extract_features.py`, `experiments/evaluate_detection.py`, `experiments/evaluate_mitigation.py`, `experiments/profile_real_latency.py`.
- `tests/test_equivalence.py` — All 3 unit & leakage tests passed.
- `notebooks/TRUEGUARD_Colab_REAL.ipynb` & `notebooks/TRUEGUARD_Colab.ipynb` + `E:\trueguard\CAPSTONE\trueguard_final.zip`.

---

## 3. Verified Tesla T4 GPU Experimental Results (`TinyLlama/TinyLlama-1.1B-Chat-v1.0`)
Stored in `E:\trueguard\CAPSTONE\FInal\results\v2\TinyLlama__TinyLlama-1.1B-Chat-v1.0\` (unpacked from `E:\trueguard\CAPSTONE\FInal\trueguard_v2_results.zip`):

1. **In-Distribution 5-Fold Grouped CV ($3{,}196$ Real Answers):**
   - `halueval_summarization` ($N=400$ pairs): **0.986 AUROC** [0.980, 0.991], F1 = 0.935, ECE = 0.025 (ISP = 0.987, $-\text{ISP}$ = 0.745)
   - `halueval_qa` ($N=400$ pairs): **0.975 AUROC** [0.964, 0.987], F1 = 0.955, ECE = 0.024 (ISP = 0.977, $-\text{ISP}$ = 0.918)
   - `halueval_dialogue` ($N=400$ pairs): **0.903 AUROC** [0.883, 0.922], F1 = 0.820, ECE = 0.034 (ISP = 0.904, $-\text{ISP}$ = 0.714)
   - `truthful_qa` ($N=398$ pairs): **0.876 AUROC** [0.853, 0.900], F1 = 0.817, ECE = 0.042 (ISP = 0.877, $-\text{ISP}$ = 0.626)
   - **4-Benchmark Macro Mean:** **0.935 AUROC**, F1 = 0.882, ECE = 0.031.
2. **Live `TriviaQA` 3-Tier Mitigation (`n_cal=150`, `n_test=150`):**
   - $\tau_{\text{warning}} = 0.611$, $\tau_{\text{fault}} = 0.898$; Detection AUROC on own generations = **0.795**.
   - Unmitigated hallucination rate: **62.0%** (accuracy 38.0%).
   - Post-mitigation hallucination rate among answered queries: **40.0%** (**35.5% relative reduction**; accuracy rises $38.0\% \to 60.0\%$ at 43.3% coverage).
   - System-wide emitted hallucination rate: **17.3%** (**72.0% relative reduction**).
   - Risk–Coverage AURC: **TRUEGUARD = 0.412** vs. Entropy = 0.526 and NLL = 0.603.
3. **Real Tesla T4 GPU Per-Token Latency:**
   - Vanilla KV-cached decode: `33.49 ms/tok`
   - TRUEGUARD Post-pass decode: **`36.41 ms/tok`** (`+2.92 ms/tok`, $+8.7\%$ overhead, **4.65x faster** than 5-sample consistency at `169.31 ms/tok`)
   - TRUEGUARD Online decode: **`39.30 ms/tok`** (`+5.81 ms/tok`, **4.31x faster** than 5-sample consistency).

