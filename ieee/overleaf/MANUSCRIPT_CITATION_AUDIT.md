# Manuscript Citation Audit

**Manuscript:** `E:\trueguard\ieee\TRUEGUARD_IEEE_FINAL\manuscript\TRUEGUARD_Manuscript_Draft.md`  
**Original Bibliography (Preserved Unchanged):** `E:\trueguard\ieee\overleaf\references.bib` (`40` entries: `review01`–`review40`)

---

## 1. Original Bibliography Entries Cited (`32` of `40` Used; `0` Modified)

| BibTeX Key | Original `references.bib` Entry Summary | Claim Supported in Manuscript | Status |
| :--- | :--- | :--- | :---: |
| `[@review01]` | Su et al. (ACL 2024 Findings) — MIND | Unsupervised real-time hidden-state hallucination monitoring | Verified |
| `[@review02]` | Zhang et al. (2024, arXiv:2403.05838) — PRISM | Prompt-guided internal-state probing | Verified |
| `[@review03]` | Huang et al. (2024, arXiv:2401.05561) — TrustLLM | Trustworthiness & calibration in LLMs | Verified |
| `[@review04]` | Ma et al. (2025, arXiv:2508.14496) — Semantic energy | Energy-based scores beyond Shannon entropy | Verified |
| `[@review05]` | Zhang et al. (IJCAI 2025) | Deep internal representation analysis for hallucination detection | Verified |
| `[@review07]` | Kang et al. (2025, arXiv:2510.12040) | Uncertainty quantification survey for LLM hallucinations | Verified |
| `[@review09]` | Hajji et al. (AAAI Symp. 2025) — Map of Misbelief | Tracing intrinsic/extrinsic hallucinations via attention patterns | Verified |
| `[@review11]` | Vazhentsev et al. (2025, arXiv:2505.20045) | Uncertainty-aware attention heads | Verified |
| `[@review12]` | Sriramanan et al. (NeurIPS 2024) — LLM-Check | White-box hidden-state/attention/perplexity detection | Verified |
| `[@review13]` | Dasgupta et al. (IJCNN 2025) — HalluShift | Representation distribution shifts for hallucination detection | Verified |
| `[@review14]` | Han et al. (ICML 2024 Workshop) | Linear probes predicting semantic entropy from hidden states | Verified |
| `[@review15]` | Wu et al. (2025, arXiv:2512.19920) | Behaviorally calibrated RL for hallucination mitigation | Verified |
| `[@review17]` | Moslonka et al. (2025, arXiv:2509.04492) | Token-level entropy production rate for detection | Verified |
| `[@review18]` | Alansari & Luqman (2024, arXiv:2407.01234) | Comprehensive hallucination survey | Verified |
| `[@review19]` | Sharma et al. (2024, arXiv:2406.02018) | Human trust in LLM responses | Verified |
| `[@review21]` | Manakul, Liusie, & Gales (EMNLP 2023) — SelfCheckGPT | Multi-sample black-box detection baseline & WikiBio-GPT3 benchmark | Verified |
| `[@review22]` | Lin, Hilton, & Evans (ACL 2022) — TruthfulQA | TruthfulQA benchmark | Verified |
| `[@review23]` | Min et al. (EMNLP 2023) — FActScore | Fine-grained factual precision in long-form generation | Verified |
| `[@review24]` | Dhuliawala et al. (ACL 2024 Findings) — CoVe | Chain-of-Verification mitigation | Verified |
| `[@review25]` | Lewis et al. (NeurIPS 2020) — RAG | Retrieval-Augmented Generation | Verified |
| `[@review26]` | Asai et al. (ICLR 2023) — Self-RAG | Self-reflective retrieval and critique | Verified |
| `[@review27]` | Azaria & Mitchell (EMNLP 2023 Findings) — SAPLMA | Linear probing over intermediate hidden layers (`ISP` foundation) | Verified |
| `[@review28]` | Li et al. (NeurIPS 2023) — ITI | Inference-time intervention along truthful activation directions | Verified |
| `[@review29]` | Li et al. (EMNLP 2023) — HaluEval | HaluEval dialogue/QA/summarization/general benchmarks | Verified |
| `[@review31]` | Du et al. (ICML 2024) | Multi-agent debate for factuality | Verified |
| `[@review33]` | Gao et al. (ACL 2023) — RARR | Research-and-revise hallucination correction | Verified |
| `[@review34]` | Chern et al. (2023, arXiv:2307.13528) — FacTool | Tool-augmented factuality detection | Verified |
| `[@review35]` | Ji et al. (ACM Computing Surveys 2023) | Foundational NLG hallucination taxonomy (intrinsic/extrinsic) | Verified |
| `[@review36]` | Mündler et al. (2023, arXiv:2305.15852) | Self-contradictory hallucinations | Verified |
| `[@review37]` | Bang et al. (IJCNLP-AACL 2023) | Empirical evaluation of LLM hallucination rates | Verified |
| `[@review38]` | Chen et al. (AAAI 2024) — Truth Forest | Multi-scale truthfulness intervention without tuning | Verified |
| `[@review39]` | Gou et al. (2023, arXiv:2305.11738) — CRITIC | Tool-interactive self-correction | Verified |

*(Unused original entries intentionally omitted as off-topic or redundant for this empirical study: `review08` XAI survey, `review10` 1–5 faithfulness scale, `review16` MLLM HalluShift++, `review30` CoT prompting, `review32` Woodpecker MLLM, `review40` knowledge graphs survey, plus the two incomplete entries flagged below.)*

---

## 2. Incomplete Original Entries Flagged (NOT Cited, NOT Silently Modified)

- **`review06`:** `Anonymous. (2025). Entropy spike detection and self-confidence calibration for hallucination mitigation. Extended Abstract.` — Flagged as anonymous/incomplete venue; omitted from manuscript.
- **`review20`:** `Yao, S., Huang, P., Liu, Z., Gu, Y., Yan, Y., Yu, S., and Yu, G. (2025). ExpandR: Learning to teach high density retrievers outside query guided` — **Flagged as incomplete** (truncated title, missing venue/year details); preserved verbatim in `references.bib` and omitted from manuscript.

---

## 3. Proposed Additional References Marked `[PENDING_APPROVAL: key]`

Ten essential primary references (datasets, foundation model, external baseline Semantic Entropy, and statistical/selective-prediction foundations) are not in the original 40-entry `references.bib`. They are marked as `[PENDING_APPROVAL: key]` in the draft and documented with full metadata in [ADDITIONAL_REFERENCES_FOR_APPROVAL.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/manuscript/ADDITIONAL_REFERENCES_FOR_APPROVAL.md):
- `kuhn2023semantic`, `farquhar2024detecting` (Semantic Entropy — directly reproduced baseline)
- `zhang2024tinyllama` (TinyLlama-1.1B — our foundation model)
- `dziri2022faithdial`, `maynez2020faithfulness`, `thorne2018fever`, `joshi2017triviaqa` (4 of our 10 evaluated benchmarks)
- `geifman2017selective` (selective prediction / risk–coverage AURC)
- `nadeau2003inference` (repeated-seed / shared-test-set variance flag)
- `burns2023discovering`, `chen2024inside` (unsupervised white-box baselines noted in Limitations)
