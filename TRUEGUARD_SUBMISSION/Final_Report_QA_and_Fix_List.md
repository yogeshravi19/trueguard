# QA Report — Final_Project_Report_ARUNPRASAD_22MIA1058.docx
Checked against: MIA-Project_Template.docx | Rendered: 48 pages actual

---

## 🔴 CRITICAL — fix before this goes anywhere near a guide or plagiarism checker

### 1. The entire literature review (Chapter 2, 25 references) is fabricated
Verified by web search: **"Al-Antari et al. (2026), IEEE Trans. Biomed. Eng."**, **"Kovacs et al. (2024), Measurement"**, **"Sharma & Kumar (2026), ACM Trans. Comput. Healthcare"**, and the rest of this 25-paper list do not exist. Signs that confirm this isn't just an unlucky search:
- DOIs don't match their own years (e.g. a "2026" paper with a `10.1109/TBME.2025...` DOI).
- Several "papers" report metrics suspiciously identical to *your own* bench results (Kovacs "validates" HX711 linearity at R²=0.999 — the exact number in your own hardware test).
- Two of the fabricated papers list **"Joe, P. I. R."** — your actual guide's name — as a co-author on external journal papers he did not write. This is the most dangerous part: it's not just fabricated literature, it puts words in your guide's mouth.
- This fabricated list appears in three places: the Chapter 2 narrative (2.2–2.6), the Table 2.1 synthesis, and the References list — so it's not an isolated copy-paste, it's structural.

**Fix:** Replace this entire literature review with the 25 real, verifiable IEEE papers already in your **Review 1** document (Ahmed & Noor, Ali, Bhattacharya & Saha, etc.) — those check out. I can rewrite Chapter 2 and the References section around that real list, restructured into the same thematic clusters (ML staging, imaging/deep learning, XAI, chatbot/LLM) you already have in Chapter 2's headings. This is a straight swap of content, not a structural rewrite.

---

## 🟠 MAJOR — real compliance/quality gaps

### 2. Zero page numbers anywhere
No header/footer exists in the file at all. The template explicitly requires **Arabic numerals, bottom-center, on every page** (front matter conventionally in lowercase roman — iii, iv, v… — then Arabic from Chapter 1). Right now nothing is numbered, and there's only one document section, so front-matter/body can't even use different numbering styles yet.

### 3. Table of Contents is hand-typed, not a real TOC — and the page numbers are fictional
The Contents table lists References at **page 98**, Appendices starting at **92** — but the actual document is **48 pages**. This isn't a rounding issue; it reads as a page count that was aspirational/copy-pasted rather than generated from the real content. Also, since it's a static table (no Word heading styles applied anywhere in the doc — confirmed zero `Heading1/2/3` style usage), it can never auto-update; every edit you make will make it wrong.

**Fix:** Apply real Word heading styles to every chapter/section title, insert a native TOC field, and let it regenerate page numbers automatically once pagination is final.

### 4. Below the required page count
Template minimum is **60 pages**; current draft is **48**, and that's before removing the fabricated-literature bulk. Once Chapter 2 is rebuilt with real content and figures are added (below), this should close most of the gap — but budget for it.

### 5. No images anywhere — despite a List of Figures with 6+ captioned entries
The docx has **no embedded media at all** (confirmed: no `word/media` folder). Figures 1.1, 3.1, 3.2, 4.1–4.6, 5.1… are captioned in the List of Figures but the actual diagrams/charts are missing from the body. I have the real hardware renders, circuit schematic, and ML performance chart already extracted from your patent doc — these should be dropped into Chapter 4/6 rather than left as bare captions.

### 6. Broken raw LaTeX/math syntax in body text
Page 27 (and likely elsewhere) has literal unrendered math markup leaking into the paragraph text, e.g.:
> `$E ... V_s^2$, where $\rho$ is tissue density`
> `$R^2 = 0.999$`

This reads as broken/corrupted to anyone opening the file. Needs to be replaced with plain-English or a properly inserted Word equation — not raw `$...$` LaTeX.

### 7. Missing VIT logo
Template shows the VIT crest on the cover page, title page, and above the Declaration. Current draft has none. I have it extracted directly from your official template file, ready to place.

### 8. Stale placeholder date
Cover/title pages say **"December, 2025"** — that looks like it was left over from the template default rather than updated to your actual submission month (you're in the Sept 2026 Review 3 window).

---

## 🟡 MINOR — polish items

- Appendix 2 ("Core Source Code Repository Index") only lists filenames and one-line descriptions — the template's convention (and most VIT panels' expectation) is an actual numbered source-code listing appendix, not just an index. Worth adding at least the key files (`train_models.py`, `views.py`, `ml_service.py`) as real listings.
- A handful of table/caption runs are set at 8–9.5pt — below the template's explicit 10pt minimum for captions/tables.
- The abstract repeats the same unqualified stats flagged earlier in the Review 2 deck cleanup (84% pain incidence, 18% elastography failure rate, unqualified "64 ms" latency) — same fix as before: soften to defensible language unless you have a citation for each figure now that fabricated sources are gone.

---

## ✅ Already solid — no action needed
- Page margins: exactly correct (3.81 cm left / 2.54 cm top-right-bottom).
- Font: Times New Roman throughout.
- Declaration, Certificate, Acknowledgement content and wording — well-written, matches template tone.
- Chapter/section numbering scheme and overall 7-chapter structure — sensible and matches rubric expectations.
- Table 2.1 synthesis table formatting (once the content inside it is fixed).

---

## Recommended order of fixes
1. Swap in the real 25-paper literature review (Chapter 2 + References) — **do this first**, everything else is safe to build around it.
2. Apply Heading styles + insert real TOC field + add header/footer with page numbers (roman → arabic split).
3. Insert the 4 real figures (hardware render, exploded assembly, circuit schematic, ML performance chart) + add the missing chart/diagram figures referenced elsewhere in the List of Figures.
4. Fix the broken LaTeX fragments.
5. Add VIT logo + correct the submission date.
6. Re-check page count once 1–3 are done; pad Chapter 6/7 discussion if still short of 60 pages.
7. Polish pass: font sizes in tables, Appendix 2 code listing, abstract wording.

Say the word and I'll execute this list directly on your docx (unzip → edit → validate) rather than rebuilding from scratch, so your existing wording and structure are preserved everywhere except the fabricated parts.
