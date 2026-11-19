# TRUEGUARD Final Manuscript Layout, Author Metadata & Hyperlink Verification Report

**Date:** 2026-11-20  
**Workspace:** `E:\trueguard\ieee\overleaf\`  
**Compiler:** TinyTeX `pdflatex` + `bibtex` (4-pass build: `pdflatex -> bibtex -> pdflatex -> pdflatex`)

---

## 1. Deliverables Summary

| Deliverable | File Path | Pages | Size | Hyperlinks | Broken Links | Undefined Citations / Refs |
|---|---|---:|---:|---:|---:|---:|
| **Corrected Clean 10-Page Review PDF** | `E:\trueguard\ieee\overleaf\TRUEGUARD_REVIEW_MANUSCRIPT_10P_CORRECTED.pdf` | **10** | 1,298,423 B | 89 | **0** | **0 / 0** |
| **Editable Review LaTeX Source** | `E:\trueguard\ieee\overleaf\review_main_corrected.tex` | — | 51,554 B | — | — | — |
| **Updated Official IEEE Access PDF** | `E:\trueguard\ieee\overleaf\TRUEGUARD_IEEE_ACCESS_FINAL_UPDATED.pdf` *(saved alongside locked `TRUEGUARD_IEEE_ACCESS_FINAL.pdf`)* | **15** | 2,039,377 B | 102 | **0** | **0 / 0** |
| **Updated Official IEEE Access LaTeX Source** | `E:\trueguard\ieee\overleaf\main.tex` | — | — | — | — | — |
| **Updated Overleaf-Ready Official ZIP** | `E:\trueguard\ieee\overleaf\TRUEGUARD_IEEE_ACCESS_OVERLEAF.zip` | — | 2,801,157 B | — | — | — |
| **Updated Refined Markdown Manuscript** | `E:\trueguard\ieee\overleaf\TRUEGUARD_Manuscript_Refined.md` *(also synced to `TRUEGUARD_IEEE_FINAL/manuscript/`)* | — | — | — | — | — |

> **Preserved Unmodified:** Earlier files (`TRUEGUARD_REVIEW_MANUSCRIPT_10P.pdf`, `TRUEGUARD_REVIEW_MANUSCRIPT_10P_v3.pdf`, `references_original_40_verbatim_backup.bib`) were not overwritten.

---

## 2. Exact Figure, Table, and References Placement (`TRUEGUARD_REVIEW_MANUSCRIPT_10P_CORRECTED.pdf`)

Every figure and table appears in or directly beside its discussing section, and **zero** figures or tables appear inside or after `REFERENCES`.

| Visual / Section | Exact Page | Discussing Section | Alignment Check |
|---|---:|---|---|
| **Title, Authors, Abstract, Keywords** | Page 1 | Header / Abstract | Left-aligned bold IEEE Access blue (`#00629B`) sans-serif title + uppercase authors; **no** IEEE Access logo, publisher headers, or journal footers |
| **Figure 1** (TRUEGUARD System Architecture) | **Page 3** | Section III (Proposed TRUEGUARD Framework) | Directly accompanies Section III system & four-sensor workflow description |
| **Table I** (10 Evaluation Datasets) | **Page 4** | Section IV (Experimental Setup) | Directly inside Section IV dataset specification |
| **Table II** (In-Domain Detection & Artifact Controls) | **Page 5** | Section V-A (In-Domain & Artifact Controls) | Directly inside Section V-A results |
| **Table III** (Zero-Shot & Target-Only Few-Shot Refitting) | **Page 6** | Section V-B (Domain Shift & Few-Shot Refitting) | Paired directly with Figure 2 in Section V-B |
| **Figure 2** (Target-Domain Few-Shot Refitting) | **Page 6** | Section V-B (Domain Shift & Few-Shot Refitting) | Directly beside Section V-B discussion |
| **Table IV** (Equal-Sample Probe Alignment & EEM Controls) | **Page 6** | Section V-C (Cross-Domain Diagnostics) | Paired directly with Figure 3 in Section V-C |
| **Figure 3** (Cross-Domain Diagnostics) | **Page 6** | Section V-C (Cross-Domain Diagnostics) | Directly beside Section V-C discussion |
| **Figure 4** (TriviaQA External Baselines & Risk–Coverage) | **Page 7** | Section V-D (External Baselines on TriviaQA) | Directly beside Section V-D comparison |
| **Figure 5** (Pure Selective Abstention vs. 3-Tier Controller) | **Page 7** | Section V-E (Mitigation Audit) | Directly beside Section V-E audit |
| **Table V** (TriviaQA External Baselines Summary) | **Page 8** (top) | Section V-D / VI | Cleanly positioned at top of Page 8 prior to Section VII |
| **Table VI** (Forensic Mitigation Audit at 46.0% Coverage) | **Page 8** (top) | Section V-E / VI | Cleanly positioned at top of Page 8 prior to Section VII |
| **Section VII (Conclusion and Future Work)** | **Page 8** | Section VII | Completes cleanly before `REFERENCES` |
| **REFERENCES (`[1]`–`[43]`)** | **Page 8 (bottom-left) – Page 10** | Bibliography | Starts **strictly after** Section VII Conclusion and **all** figures & tables; **0** floats inside/after References |
| **Author Biographies** | **Page 10** | Biographies | Concise verified biographies for Yogesh Ravi M and T. S. Pradeep Kumar |

---

## 3. Comparison Against Earlier 10-Page Review PDF

| Issue in Earlier `TRUEGUARD_REVIEW_MANUSCRIPT_10P.pdf` | Status in `TRUEGUARD_REVIEW_MANUSCRIPT_10P_CORRECTED.pdf` |
|---|---|
| Figures 3, 4, and 5 drifted into the `REFERENCES` section | **Fixed:** All 5 figures and 6 tables finish on or before Page 8 top; `REFERENCES` starts at Page 8 bottom-left with zero trailing floats |
| Equation (8) overflowed into the right column on Page 4 | **Fixed:** Compact `\small` display using $\tau_w, \tau_f$ fits cleanly inside the left column |
| Placeholder author names & placeholder 3rd author | **Fixed:** Replaced with confirmed 2 authors (`Yogesh Ravi M` and `T. S. Pradeep Kumar, Senior Member, IEEE`), VIT Chennai affiliation, confirmed emails, and corresponding author |
| Abstract supervision clarity on TriviaQA | **Fixed:** ~185-word Abstract explicitly states that TRUEGUARD used 250 target calibration labels on TriviaQA while external baselines were label-free |
| Scientific data, equations, and citations | **Unchanged:** All numerical results, statistical controls, equations, and 43 verified references remain 100% intact |

---

## 4. Confirmed Author Information Verification (Both Manuscripts)

Applied identically across `TRUEGUARD_REVIEW_MANUSCRIPT_10P_CORRECTED.pdf`, `TRUEGUARD_IEEE_ACCESS_FINAL_UPDATED.pdf`, `main.tex`, `TRUEGUARD_IEEE_ACCESS_OVERLEAF.zip`, and `TRUEGUARD_Manuscript_Refined.md`:

- **First Author:** `YOGESH RAVI M` — School of Computer Science and Engineering, Vellore Institute of Technology, Chennai, Tamil Nadu, India (`yogeshravi4343@gmail.com`)
- **Second Author:** `T. S. PRADEEP KUMAR, Senior Member, IEEE` — Professor, School of Computer Science and Engineering, Vellore Institute of Technology, Chennai, Tamil Nadu, India (`tspradeepkumar@vit.ac.in`; IEEE Senior Member and ACM Senior Member)
- **Corresponding Author:** `T. S. Pradeep Kumar (e-mail: tspradeepkumar@vit.ac.in)`
- **Compliance Checks:** No "Dr." or "Professor" titles in formal author-name lines; no phone numbers; no third placeholder author; no unverified degrees, awards, or publication counts in biographies.
