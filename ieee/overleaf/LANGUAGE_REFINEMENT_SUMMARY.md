# Language Refinement Summary

**Original Draft Preserved:** [TRUEGUARD_Manuscript_Draft.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/manuscript/TRUEGUARD_Manuscript_Draft.md)  
**Refined Manuscript:** [TRUEGUARD_Manuscript_Refined.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/manuscript/TRUEGUARD_Manuscript_Refined.md) *(also copied to `E:\trueguard\ieee\overleaf\TRUEGUARD_Manuscript_Refined.md`)*

---

## 1. Improvements Made Across the Manuscript

1. **Connected Paragraph Prose Throughout:**
   - Converted all ordinary prose bullet lists and numbered lists (Section I-D Research Questions, Section I-E Main Research Contributions, and Section IV-I External Baseline Descriptions) into smooth, connected academic paragraphs.
   - Removed all em dashes (`—`) and decorative arrows (`→`) from prose paragraphs, replacing them with natural punctuation (commas, parentheses, semicolons, and clear shorter sentences).
2. **Simple, Direct Academic English & Narrative Flow:**
   - Rewrote stiff or overly dense phrasing into clear, direct sentences while preserving every technical detail, hyperparameter, and mathematical definition (`Equations (1)–(10)`).
   - Structured every Results subsection (`Section V-A` through `V-J`) in consistent evidence-driven order: experiment conducted, relevant table/figure, key numerical findings, observed pattern, and cautious interpretation.
   - Removed repetitive AI-style transition formulas (`"Crucially,"`, `"Taken together,"`, etc.) and avoided inflated adjectives (`"novel"`, `"comprehensive"`, `"robust"`, `"groundbreaking"`, `"state-of-the-art"`).
3. **Strict Preservation of All Scientific Facts, Citations, Tables, and Figures:**
   - Retained every verified number across `TABLE I` through `TABLE VIII` and `FIGURE 1` through `FIGURE 9` without altering any experimental evidence.
   - Preserved all `32` verified BibTeX keys (`[@review01]`–`[@review39]`) from untouched `E:\trueguard\ieee\overleaf\references.bib` and all `11` `[PENDING_APPROVAL: key]` markers from `ADDITIONAL_REFERENCES_FOR_APPROVAL.md`.
   - Kept all negative findings and mandatory disclosures prominent: HaluEval length/TF-IDF artifacts (and the caveat that other subtler artifacts may remain), ISP dominance (`>96%` weight) with no consistent 4-sensor AUROC gain over ISP alone, zero-shot collapse (`0.4597–0.5205`, TriviaQA `0.5504`), `Target-Domain Few-Shot Refitting (Target-Only Probe Training)` with zero source weight transfer and simple-baseline wins at `K=50` / XSum `K=250`, TriviaQA supervision asymmetry (`250` calibration labels vs. label-free `SelfCheckGPT-NLI` and `Semantic Entropy`), verified genuine NLL (`0.4678`), selective abstention (`55.65%`) vs. full 3-tier controller (`54.78%`, `4` fixed / `3` broken, no measurable net benefit), latency protocol non-equivalence, and single frozen `1.1B` model scope.

---

## 2. Scientifically Ambiguous or Unresolved Items Flagged (Not Silently Altered)

- **Author Metadata & Biographies:** Confirmed author names, affiliations, emails, and biographies remain clearly marked as placeholders until supplied by the authors.
- **Pending Additional References (`11` keys):** Still marked `[PENDING_APPROVAL: key]` pending explicit approval before LaTeX/BibTeX conversion; original `references.bib` (`40` entries, including flagged incomplete `review06` and `review20`) was not modified.
- **Figure 1 Architecture Schematic:** Remains marked as a vector TikZ/SVG placeholder for the LaTeX preparation stage (no data plot invented or altered).
