# Figure & Table Preparation Report (Pre-LaTeX Compilation)

**Date:** 2026-11-20  
**Scope:** Resolved all 3 items from `MANUSCRIPT_FIGURE_TABLE_FINAL_VERIFICATION.md` while retaining **all 9 figures** and **all 8 tables** completely intact. Zero experimental data or numerical results were modified.

---

## Files Created
1. **`Fig1_TRUEGUARD_Architecture.svg`**, **`Fig1_TRUEGUARD_Architecture.pdf`**, and **`Fig1_TRUEGUARD_Architecture.png`** (300 DPI) — Saved in `overleaf/figures/`, `manuscript/figures/`, and `publication_ready/figures/`. Vector architecture diagram faithfully matching `tg_pipeline.py` and `tg_controller.py` (frozen TinyLlama-1.1B, 4 parallel sensor branches `ISP`/`AAS`/`EEM`/`DST`, 7-dim normalization & L2 logistic fusion, calibrated risk score, and `SAFE` / `TIER 1` / `TIER 2` / `TIER 3` pathways).
2. **`Fig4_InDomain_5x5_Transfer_Matrix_v2.png`** (300 DPI) and **`Fig4_InDomain_5x5_Transfer_Matrix_v2.pdf`** — Saved in `overleaf/figures/`, `manuscript/figures/`, and `publication_ready/figures/`. Re-rendered directly from `results/final_experiment_report.json` with identical matrix values, `viridis` scale (`0.4–1.0`), and an unclipped two-line title. Original `Fig4_InDomain_5x5_Transfer_Matrix.png` preserved untouched as backup.
3. **`overleaf/figures/`** & **`manuscript/figures/`** — Populated with all 15 figure files (all original 300-DPI experimental PNGs + new vector/PNG Fig. 1 and Fig. 4 v2) ready for LaTeX `\includegraphics`.

## Files Modified
1. **`overleaf/TRUEGUARD_Manuscript_Refined.md`** (synced to `manuscript/TRUEGUARD_Manuscript_Refined.md`):
   - Updated **FIGURE 1** caption to point to the newly created `figures/Fig1_TRUEGUARD_Architecture.pdf` / `.svg` / `.png` (conceptual diagram).
   - Fixed **FIGURE 3** caption so it describes only the AUROC ablation bars plotted in `Fig6_Ablation_HaluEval_General.png` (referencing Table III for low-FPR complementarity).
   - Updated **FIGURE 4** caption to point to the unclipped `figures/Fig4_InDomain_5x5_Transfer_Matrix_v2.png` / `.pdf`.
2. **`overleaf/MANUSCRIPT_FIGURE_TABLE_MAP.md`** (synced to `manuscript/MANUSCRIPT_FIGURE_TABLE_MAP.md`):
   - Updated with final filenames, source evidence, and intended IEEE Access LaTeX placements (`figure` vs. `figure*`, `table` vs. `table*`) for all 9 figures and all 8 tables.

## Preserved Unchanged
- All original experimental JSON/NPZ/CSV files in `results/`, `checkpoints/`, `predictions/`, `research_improvements/`, `external_validation/`, `reviewer_response/`.
- Original `Fig4_InDomain_5x5_Transfer_Matrix.png` (backup) and `Fig6_Ablation_HaluEval_General.png`.
- Original `E:\trueguard\ieee\overleaf\references.bib` (`10,790` bytes).
- Previous audit record `MANUSCRIPT_FIGURE_TABLE_FINAL_VERIFICATION.md`.
- All **9 figures** (`FIGURE 1`–`FIGURE 9`) and all **8 tables** (`TABLE I`–`TABLE VIII`).
