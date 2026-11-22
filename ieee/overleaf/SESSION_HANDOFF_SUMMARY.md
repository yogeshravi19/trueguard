# TRUEGUARD Manuscript Session Handoff Summary

**Saved:** 2026-11-22  
**Workspace:** `E:\trueguard\ieee\overleaf\`  
**GitHub:** `https://github.com/yogeshravi19/trueguard.git` (last pushed commit `937d98a` on `main`)

---

## 1. Confirmed Author Metadata
- **First Author:** Yogesh Ravi M — School of Computer Science and Engineering, Vellore Institute of Technology, Chennai, Tamil Nadu, India (`yogeshravi4343@gmail.com` / `yogeshravim@gmail.com` — confirm preferred email in Overleaf)
- **Second Author (Corresponding):** T. S. Pradeep Kumar, Senior Member, IEEE — Professor, School of Computer Science and Engineering, Vellore Institute of Technology, Chennai, Tamil Nadu, India (`tspradeepkumar@vit.ac.in`; IEEE Senior Member & ACM Senior Member)

---

## 2. Final Verified Deliverables
- **Overleaf Upload Folder (Clean Review 10-Page Version):** `E:\trueguard\ieee\overleaf\uploadtooverleaf\` (ZIP: `uploadtooverleaf.zip`)
  - Includes updated vector diagrams:
    - `figures/Fig1_TRUEGUARD_Architecture.pdf`
    - `figures/Fig2_OOF_Training_Pipeline.pdf` (leak-free nested CV & OOF fusion training)
    - `figures/Fig_Section4_Experimental_Protocol.pdf` (3-track protocol — updated so Track 1 & Track 2 boxes reference **`Table II`**)
    - Experimental plots: `Fig2_TargetDomain_FewShot_Refitting_vs_Baselines.png`, `Fig8_CrossDomain_Diagnostics_Cosine_and_LengthControlled_EEM.png`, `Fig7_External_Baselines_RiskCurve.png`, `Fig3_TriviaQA_Matched_Coverage_RiskCurve.png`
- **Local Compiled 10-Page Review PDF & Source:** `E:\trueguard\ieee\overleaf\TRUEGUARD_REVIEW_MANUSCRIPT_10P_CORRECTED.pdf` & `review_main_corrected.tex`
- **Official IEEE Access Template PDF & Overleaf ZIP (15 pages, all 9 figs / 8 tables):** `TRUEGUARD_IEEE_ACCESS_FINAL_UPDATED.pdf`, `main.tex`, `TRUEGUARD_IEEE_ACCESS_OVERLEAF.zip`
- **Layout Verification Report:** `E:\trueguard\ieee\overleaf\FINAL_MANUSCRIPT_LAYOUT_VERIFICATION.md`
- **Original 40-Entry Bibliography Backup (untouched):** `references_original_40_verbatim_backup.bib`

---

## 3. Independent Authenticity Audit Result (100% Passed)
- **Zero fabricated or invented values** across all **7 tables**, **7 figures**, **9 equations**, and **43 references**.
- **All 10 datasets (32,590 total sequences)** verified from public Hugging Face repos (`results/dataset_manifest.json`, `checkpoints/*.npz`).
- **XSum accounting verified:** 5,597 annotator rows → 1,869 unique summaries → 1 exact tie excluded → 1,868 usable summaries (`498` groups).
- **Table V `Random 2048-d Null` row:** Theoretical reference values ($1/\sqrt{2048} = 0.0221$, chance AUROC `0.5000`, zero corr `0.0000`).
- **Table VI & VII TriviaQA AURC CI:** Both now consistently report **`[0.360, 0.524]`** (half-up rounding of `[0.3596, 0.5235]`).
- **Controller counts verified (`triviaqa_test_predictions.npz`):** Greedy `85/250 (34.00%)`; Pure Abstain `64/115 (55.65%, 20.40% sys. halluc.)`; Full 3-Tier Controller `63/115 (54.78%, 20.80% sys. halluc.)` on its own 115 answered subset (`62 + 4 fixed - 3 broken = 63`, sharing `96/115` questions with Pure Abstention).
- **All 9 equations** verified 100% against `tg_pipeline.py` and `tg_controller.py`.

---

## 4. Tiny Final Polish Items Remaining in Your Overleaf Copy (Next Session)
1. **Pull Table VII off Page 9 (inside References) onto Page 8 top:** Move `\begin{table*}[!t] ... \label{tab:mitigation}` slightly earlier (or set `\renewcommand{\dbltopfraction}{0.92}` in the preamble).
2. **Fix 2 tiny Abstract typos (Page 1):** `effect the performance` → `affect the performance`, and `others..The` → `others. The`.
3. **Optional 1-line clarity notes:** XSum annotator-row aggregation note in Table II caption; `(Theor. Ref.)` on Table V's bottom null row; quick spacing check after periods/commas in humanized prose.
4. **Push final Overleaf `.tex` + final PDF to GitHub** once those quick touches are done.
