# Comprehensive Side-by-Side Formatting & Quality Assurance Audit (`QA_REPORT.md`)

**Audit Date:** November 13, 2026  
**Project Title (Cover, Title, Declaration, Certificate):** *Toward Trustworthy Large Language Models: A Comprehensive Review of Hallucination Detection, Explainability, and Mitigation Strategies*  
**Proposed Framework (Inside Chapters 1–9, Tables, & Figures):** **TRUEGUARD**  
**Primary Deliverables:**
- [FINAL_REPORT.docx](file:///e:/trueguard/FINAL_REPORT.docx) & [FINAL_REPORT.pdf](file:///e:/trueguard/FINAL_REPORT.pdf)
- [CAPSTONE/FINAL_REPORT.docx](file:///e:/trueguard/CAPSTONE/FINAL_REPORT.docx) & [CAPSTONE/FINAL_REPORT.pdf](file:///e:/trueguard/CAPSTONE/FINAL_REPORT.pdf)

---

## 1. Three-Document Side-by-Side Verification Table

The table below reports the **actual measured values** extracted via `python-docx` and `PyMuPDF` (`fitz`) from:
1. **Official MIA Template:** [MIA-Project Template.docx](file:///e:/trueguard/CAPSTONE/sample/MIA-Project%20Template.docx)
2. **Friend's Project Report:** [friend report.pdf](file:///e:/trueguard/CAPSTONE/friend%20report.pdf) (84 pages)
3. **My Final Report:** [FINAL_REPORT.docx](file:///e:/trueguard/FINAL_REPORT.docx) / [FINAL_REPORT.pdf](file:///e:/trueguard/FINAL_REPORT.pdf) (79 pages: 13 Front Matter `i–xiii` + 66 Arabic `1–66`)

| Formatting Element | Official MIA Template (`MIA-Project Template.docx`) | Friend's Report (`friend report.pdf`) | My Final Report (`FINAL_REPORT.docx` / `.pdf`) |
|---|---|---|---|
| **Font style** | `Times New Roman` throughout (`P034` explicit rule; sample styles use `Times New Roman`) | `TimesNewRomanPSMT` in body/headings/tables, **except** footer page numbers which leaked `Aptos 12.0 pt` | **100% `Times New Roman`** across all headings, body text, equations, tables, captions, references, and footers (verified `0` non-TNR spans) |
| **Font size** | Chapter No.: `12 pt Bold` (`P382`)<br>Chapter Title: `16 pt Bold` (`P042, P386`)<br>Section (`1.1`): `14 pt Bold` (`P043`)<br>Subsection (`1.1.1`): `12 pt Bold` (`P044`)<br>Body & Refs: `12 pt` (`P034, P428`)<br>Captions: `10–11 pt Italic` | Chapter No.: `12 pt Bold`<br>Chapter Title: `16 pt Bold`<br>Section: `14 pt Bold`<br>Subsection: `12 pt Bold`<br>Body & Refs: `12 pt`<br>Figure Captions: `12 pt Italic` | Chapter No.: `12 pt Bold CAPS`<br>Chapter Title: `16 pt Bold CAPS`<br>Section (`1.1`): `14 pt Bold CAPS`<br>Subsection (`1.1.1`): `12 pt Bold CAPS`<br>Body & Refs: `12 pt`<br>Captions: `10.5 pt Bold/Italic` |
| **Line spacing** | `1.15` in Body, Abstract & References (`P024, P038, P160, P426`); `1.5` in Declaration & Acknowledgement (`P110, P208`) | `1.15` in Body ($\Delta y = 13.8\text{ pt}$ for `12 pt` font); `1.5` in Declaration/Certificate; `1.15` in References | `1.22` in Body chapters (clean academic readability); `1.5` in Declaration, Certificate & Acknowledgement; `1.15` in Abstract & References |
| **Column spacing** | Single-column body layout (`14.65 cm` printable width); tables must fit within margins without text clipping | Single-column body; multi-column tables (e.g., Page 32) used justified text inside narrow columns, creating wide river gaps (`UAV-focused;  does  not`) | Single-column body (`14.65 cm` exact width); all 37 tables normalized to `14.65 cm` with **left-aligned cells** (`1.12` spacing, `55–95 dxa` padding) eliminating river gaps |
| **Margins & Page Size** | Text rules (`P016–P022`) mandate **A4 (`21.0 × 29.7 cm`)**, **Left = `3.81 cm` (`1.5"`)**, **Right = `2.54 cm` (`1.0"`)**, **Top = `2.54 cm`**, **Bottom = `2.54 cm`** (sample Word file was accidentally left on US Letter) | Used US Letter (`21.59 × 27.94 cm`) with Left = `3.81 cm` (`108 pt`), Right = `2.43 cm`, Top = `2.54 cm`, Bottom = `2.30 cm` | Strictly follows the official MIA rule: **A4 (`21.0 × 29.7 cm` / `595.3 × 841.9 pt`)**, **Left = `3.81 cm`**, **Right = `2.54 cm`**, **Top = `2.54 cm`**, **Bottom = `2.54 cm`** |
| **Headings** | Centered `CHAPTER <N>` (`12 pt Bold`) + `<TITLE>` (`16 pt Bold`); left-aligned numbered sections in **ALL CAPS** (`14 pt` / `12 pt Bold`) with `keep_with_next` | Centered `CHAPTER 1` (`12 pt Bold`) + `INTRODUCTION` (`16 pt Bold`); left-aligned ALL CAPS sections (`14 pt` / `12 pt Bold`) | Centered `CHAPTER 1` (`12 pt Bold`) + `<CHAPTER TITLE>` (`16 pt Bold`); left-aligned ALL CAPS sections (`14 pt` / `12 pt Bold`) with `keep_with_next = True` |
| **Image placement** | Centered figures with numbered captions (`Figure <ch>.<n>`) placed below the figure; listed in `LIST OF FIGURES` | **17 pages with images** (`Pages 1–4` logos + 13 interior pages `42, 46, 48, 50, 57, 59, 62, 63, 65, 71, 72, 74, 75`), stacking 2–3 images per page on `Pages 71, 74, 75` | **Only 6 pages with images total**: `Pages 1–4` (VIT logos) + **only 2 interior pages (`PDF Page 63` & `PDF Page 69`)**, each stacking **3 composite figures per page** (`Figures 7.1–7.3` and `Figures 8.1–8.3`), plus 14 in-text replacement tables (`3.1B–8.3B`) |
| **Reference formatting** | Numbered `[1]..[n]` in **APA style**, `12 pt Times New Roman`, `1.15` spacing, hanging indent (`P426–P434`) | Numbered `[1]..[20]` in APA style, `12 pt Times New Roman`, `1.15` spacing, italicized venue names, hanging indent | All **45 references (`[1]–[45]`)** in APA style, `12 pt Times New Roman`, `1.15` spacing, `0.8 cm` hanging indent, italicized journals/venues, matching all in-text citations |
| **Hyperlink colours** | Standard Word hyperlink styling for DOI/URL entries in APA references | **Clickable blue hyperlinks** (`#0563C1` / `#467885`, underlined) on `https://doi.org/...` URLs across `Pages 83–84` | **Clickable blue hyperlinks (`#0563C1`, underlined)** on all 45 reference URLs (`https://doi.org/...`, `https://arxiv.org/abs/...`, `https://aclanthology.org/...`) — 52 clickable PDF link annotations verified |
| **Overall layout** | Front matter in lowercase Roman (`i, ii, iii...`), main body starting at Chapter 1 in Arabic (`1, 2, 3...`), minimum 60 pages | 84 pages total (`12` Roman front matter + `72` Arabic main pages); occasional mid-page gaps before figures | **79 pages total** (`13` Roman front matter `i–xiii` + `66` Arabic main pages `1–66`); `widow_control = True` and `keep_together = False` eliminate bottom-of-page blank gaps |

---

## 2. Exact Print Guide for Color Pages

If you are printing only the image pages in color and the rest in black-and-white:
- **Front Matter Institutional Logo Pages (4 pages):** **PDF Pages `1, 2, 3, 4`** (Cover Page, Title Page, Declaration, Certificate).
- **Interior Analytical Figure Pages (Only 2 pages):**
  - **PDF Page `63`** (Report Arabic Page `50`): Contains **Figure 7.1**, **Figure 7.2**, and **Figure 7.3** stacked vertically on one page.
  - **PDF Page `69`** (Report Arabic Page `56`): Contains **Figure 8.1**, **Figure 8.2**, and **Figure 8.3** stacked vertically on one page.
- **All other 73 pages** are 100% crisp text, equations, and structured tables (`37` tables total, including the `14` replacement tables `Table 3.1B` through `Table 8.3B`).
