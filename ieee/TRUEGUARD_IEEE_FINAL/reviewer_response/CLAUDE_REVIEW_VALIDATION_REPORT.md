# Independent Scientific Review Validation Report (Claude Peer Review vs. Actual Project Evidence)

**Project:** TRUEGUARD (`E:\trueguard\ieee\TRUEGUARD_IEEE_FINAL`)  
**Date:** 2026-11-19  
**Audit Scope:** Cross-examination of every major criticism in Claude's independent scientific review against actual source code, Colab notebooks, saved `.npz` checkpoints/predictions, JSON reports, and newly executed CPU-only control experiments (`reviewer_controls_results.json`, `cosine_and_eem_controls.json`).  
**Constraints Respected:** Zero TinyLlama reruns, zero new foundation model downloads, zero overwrites of original experimental evidence, zero manuscript drafting.

---

## 1. Point-by-Point Classification of Claude's Criticisms

| # | Claude Review Section & Criticism | Classification | Evidence & Resolution Summary |
| :---: | :--- | :---: | :--- |
| **1** | **§2A — HaluEval / Teacher-Forced Dataset Artifacts** (high `0.988–0.994` AUROCs may reflect answer length, GPT-3.5 style, or benchmark construction rather than factual hallucination) | **VALID CONCERN** *(Now Quantified via Control A)* | **Confirmed as a real confound, yet signal survives:** Answer-text TF-IDF alone (zero LLM) gets `0.9661` on HaluEval-QA and `0.9539` on HaluEval-Summ, and 1D `LEN` gets `0.9572` on HaluEval-QA. However, TRUEGUARD beats TF-IDF on all 5 benchmarks (`+0.022` to `+0.071`) and retains `0.790–0.811` AUROC on strictly length-matched pairs (`\|ΔL\| ≤ 2` tok, where `LEN ≈ 0.50`). Headline `0.988–0.994` must **not** be claimed as pure factuality detection. |
| **2** | **§2B — Few-Shot "Adaptation" Is Missing Target-Only & Simple Baselines** (no proof source weights help; could be plain target-only training or beaten by 1D EEM / length / TF-IDF) | **VALID CONCERN** *(Now Quantified via Control B)* | **Confirmed:** Phase 3 (`phase3_fewshot_adaptation_results.json`) actually ran **target-only training from scratch** (zero source weights transferred). Source-risk recalibration (`SrcRecal`) yields `0.496–0.524` (zero transfer). At `K=250`, target-only TG beats EEM-1D, LEN-1D, and TF-IDF on FaithDial (`0.8231`), FEVER (`0.7325`), and WikiBio (`0.6698`), **but on XSum 1D LEN alone gets `0.6445` vs. TG `0.6456` (`+0.0011`)**, and at `K=50` EEM-1D beats TG on FaithDial/XSum and TF-IDF beats TG on FEVER/WikiBio. Must be renamed **target-domain few-shot refitting**. |
| **3** | **§2C — Single Small Frozen Model (`TinyLlama-1.1B`)** (34% TriviaQA accuracy, 66% hallucination rate; unclear if findings generalize to 7B–70B models) | **VALID CONCERN** *(Scope Limitation)* | Real external-validity limitation. Cannot be solved without new GPU runs. Must be framed prominently as a **small-LLM / edge-deployment empirical study** (1.1B parameter regime) rather than universal LLM behavior, with 7B+ scaling explicitly stated as future work. |
| **4** | **§3A — Four-Sensor Architecture vs. ISP-Only** (AAS/EEM/DST add ~0 AUROC in-domain and `+0.017` n.s. on TriviaQA; pooled fusion puts >96% weight on `ISP_logit = +2.935`) | **ALREADY ADDRESSED** *(Needs Stronger Framing)* | Already documented in `phase2_cross_domain_diagnostics.json`, `external_baselines_report.json` (`p_Holm = 0.478`), and `FINAL_IEEE_ACCESS_RESEARCH_READINESS_REPORT.md` §3. However, manuscript framing must stop selling "4-sensor synergy" as an architectural breakthrough and instead report **ISP dominance** as a primary empirical finding (with EEM as a useful 1D zero-shot/low-K fallback on natural dialogue/summarization). |
| **5** | **§3B — Novelty & Differentiation** (ISP = linear probing; AAS/EEM/DST = standard attention/entropy/divergence; 3-tier controller = standard routing) | **VALID CONCERN** *(Requires Paper Reframing)* | The individual sensors are indeed adaptations of established white-box signals. Presenting TRUEGUARD as a "novel architecture" invites desk/major rejection. Reframing as an **empirical & diagnostic study** (artifact controls, cross-domain failure mechanics, sample-efficiency curves, and single-pass vs. multi-sample selective answering) makes the contribution genuinely defensible. |
| **6** | **§4A — Zero-Shot Failure Diagnosed via Teacher-Forced Data** (pooled source trained on HaluEval/TruthfulQA, tested on FaithDial/WikiBio/FEVER/XSum) | **ALREADY ADDRESSED** | `phase2_cross_domain_diagnostics.json` explicitly quantifies target 5-fold ISP AUROC (`0.679–0.893`) vs. pooled zero-shot (`0.460–0.521`), and `FINAL_IEEE_ACCESS_RESEARCH_READINESS_REPORT.md` already separates FEVER as claim-verification transfer. |
| **7** | **§4B — High-Dim Cosine Similarity Needs Within-Domain Baseline** (in `d=2048`, random vectors have `cos ≈ ±0.022`, so `[-0.031, +0.051]` alone is uninformative without a within-domain baseline) | **PARTIALLY ADDRESSED** *(Now Resolved via Control 4B)* | **Valid methodological catch — and running Control 4B vindicates our finding:** Within-domain split-half cosine is `+0.344` to `+0.689` on paired benchmarks, `+0.368` on FEVER, and `+0.230` on FaithDial (10–31× random noise std `0.0221`), whereas cross-domain cosines collapse to `[-0.031, +0.051]`. |
| **8** | **§4C — EEM Sign Reversal May Be Confounded by Answer Length** (longer answers may have lower mean entropy in HaluEval) | **PARTIALLY ADDRESSED** *(Now Resolved via Control 4C)* | **Claude's hunch was half-right and crucial:** On **HaluEval-QA**, `EEM_mean` correlates with length (`ρ = -0.291`), and matching length (`\|ΔL\| ≤ 2`) removes the inversion (`0.3627 → 0.5184`). On **HaluEval-Dialogue**, inversion persists within length quartiles (`0.3795`) and length-matched pairs (`0.4525`). On **FaithDial** (`ρ = +0.006`, quartile-mean `0.7662`) and **XSum** (`ρ = -0.032`, quartile-mean `0.6648`), positive EEM is **completely independent of length**. |
| **9** | **§5 — Three-Tier Mitigation Controller vs. Pure Abstain-Only** (does Tier 1/2 beat pure abstention at matched 46% coverage, or do repairs also break correct answers?) | **PARTIALLY ADDRESSED** *(Now Forensically Audited via Control C)* | `phase5_mitigation_deep_analysis.json` already showed abstain-only `55.65%` vs. controller `54.78%`. Control C completes the forensic audit: at exact 46.0% coverage (`115/250`), **Abstain-Only gets `64/115` (`55.65%`) vs. Full Controller `63/115` (`54.78%`, `-0.87%`)**. Tier 1/2 fixed `4` hallucinations and **broke `3` originally correct answers**. The 3-tier controller does **not** beat pure abstention on TinyLlama-1.1B. |
| **10** | **§6A — TriviaQA Sample Size (`n_test = 250`) & Statistical Power** (wide 95% CIs; underpowered to separate TG `0.7876` from SelfCheckGPT `0.7477`, `p_Holm = 0.478`) | **ALREADY ADDRESSED** *(Scope Limitation)* | `external_baselines_report.json` and `FINAL_IEEE_ACCESS_RESEARCH_READINESS_REPORT.md` already report exact 95% CIs (`[0.720, 0.852]` vs. `[0.681, 0.812]`) and explicitly state non-significance (`p_Holm = 0.478` AUROC, `0.362` AURC). |
| **11** | **§6B — Latency Comparison Non-Equivalence** (`real_latency.json` sequential eager `bs=1` vs. Colab batched `sdpa` `bs=10`) | **ALREADY ADDRESSED** | Already caught, audited, and explicitly marked **non-equivalent** in `FINAL_IEEE_ACCESS_RESEARCH_READINESS_REPORT.md` §1 & §3. Must never claim wall-clock speedup over GPU-batched SelfCheckGPT. |
| **12** | **§6C — Missing White-Box Baselines (SAPLMA, CCS, EigenScore, Inside)** | **VALID CONCERN** *(Literature / Scope Caveat)* | TRUEGUARD ISP is functionally a multi-layer SAPLMA-style linear probe, and `TRUEGUARD_ISP_only` (`0.7706` TriviaQA) serves as an internal SAPLMA proxy. However, unsupervised white-box methods (CCS, EigenScore) were not implemented; this must be stated transparently in Related Work & Limitations. |
| **13** | **§7 — Data Leakage / Group Splitting & `n_cal=250` Reuse** | **ALREADY ADDRESSED** | Group-disjoint 5-fold CV (`0` overlap), 60/40 unseen splits (`0` overlap), shuffled-label sanity checks (`0.489–0.512` in Control A), and zero test-label access in TriviaQA (`n_cal=250` strictly separated from `n_test=250`) are all verified in `phase1_verification_audit.json`, `independent_reproducibility_audit.py`, and `external_baselines_report.json`. |

---

## 2. Existing Results That Already Address Criticisms

Before running new controls, our workspace already contained verified evidence addressing Criticisms #4, #6, #10, #11, and #13:
- **ISP Dominance & Zero-Shot Diagnostics:** [phase2_cross_domain_diagnostics.json](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/research_improvements/phase2_cross_domain_diagnostics.json) documents `ISP_logit = +2.9353` (>96% fusion weight), target 5-fold ISP AUROCs (`0.679–0.893`), and cross-domain cosines (`[-0.0306, +0.0510]`).
- **Statistical Honesty on External Baselines:** [external_baselines_report.json](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/external_validation/external_validation/external_baselines_report.json) and [FINAL_IEEE_ACCESS_RESEARCH_READINESS_REPORT.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/FINAL_IEEE_ACCESS_RESEARCH_READINESS_REPORT.md) explicitly state that TRUEGUARD (`0.7876`) does **not** significantly outperform SelfCheckGPT-NLI (`0.7477`, `p_Holm = 0.478`) or ISP-only (`0.7706`, `p_Holm = 0.478`), while significantly outperforming Semantic Entropy (`0.6859`, `p_Holm = 0.012`), Predictive Entropy (`0.6583`, `p_Holm = 0.006`), and NLL (`0.4678`, `p_Holm = 0.006`).
- **Latency Non-Equivalence Disclosure:** [real_latency.json](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/results/real_latency.json) (`4.20x–4.60x` vs. sequential 5x sampling) is already explicitly decoupled from GPU-batched `M=10` Colab timings (`0.707 s/q` SelfCheckGPT, `1.662 s/q` Semantic Entropy).
- **Zero-Leakage & Independent Audit:** [phase1_verification_audit.json](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/research_improvements/phase1_verification_audit.json) and `independent_reproducibility_audit.py` independently verified all metrics to `1.11e-16` with `0` group overlap.

---

## 3. New CPU-Only Control Experiment Results

All new controls were executed strictly on CPU from saved `.npz` checkpoints, saved OOF predictions, and deterministic `BUILDERS(seed=42)` texts, saved to [reviewer_controls_results.json](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/reviewer_response/reviewer_controls_results.json) and [cosine_and_eem_controls.json](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/reviewer_response/cosine_and_eem_controls.json).

### 3.1 Control A — Dataset-Artifact Controls (5 In-Domain Benchmarks)

| Dataset | `n` | TRUEGUARD 4-Sensor | 1D Length (`LEN`) | Answer-Text TF-IDF *(Zero LLM)* | $\Delta$ (TG − TF-IDF) | Shuffled Label | Length-Matched (`\|ΔL\| ≤ 2` tok): `n` (`%`) | LM: TG AUROC vs. `LEN` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **HaluEval-Dialogue** | 4,000 | **0.9218** | 0.7087 | 0.8618 | `+0.0600` | 0.5072 | 1,352 (33.8%) | **0.7996** vs. 0.5052 |
| **HaluEval-QA** | 4,000 | **0.9880** | **0.9572** | **0.9661** | `+0.0219` | 0.4894 | 256 (6.4%) | **0.7901** vs. 0.5516 |
| **HaluEval-Summ** | 4,000 | **0.9936** | 0.4902 | **0.9539** | `+0.0397` | 0.4971 | 3,546 (88.6%) | **0.9939** vs. 0.5053 |
| **TruthfulQA** | 1,634 | **0.8773** | 0.5510 | 0.8064 | `+0.0709` | 0.4928 | 714 (43.7%) | **0.8106** vs. 0.4909 |
| **HaluEval-General** | 4,507 | **0.7204** | 0.5089 | 0.6944 | `+0.0260` | 0.5123 | N/A (unpaired) | N/A |

**Key Takeaways from Control A:**
1. **HaluEval-QA (`0.9880`) is heavily length-confounded:** 1D answer length alone gets `0.9572` AUROC, and only `6.4%` (`128` pairs) are within `±2` tokens. When length is matched, TRUEGUARD drops by `19.8` points (`0.9880 → 0.7901`), yet still clearly outperforms chance (`0.7901` vs. `LEN 0.5516`).
2. **HaluEval-Summ (`0.9936`) is heavily style/lexical-confounded (not length):** `LEN` is `0.4902`, but Answer-Text TF-IDF alone (zero LLM, zero context) scores `0.9539`, proving GPT-3.5 hallucinated summaries carry strong surface stylistic cues. TRUEGUARD still improves by `+0.0397` (`0.9936`).
3. **TRUEGUARD beats Answer-Text TF-IDF on every benchmark (`+0.0219` to `+0.0709`)** and passes all shuffled-label checks (`0.4894–0.5123`), confirming real above-surface signal — **but** the `0.988–0.994` headline numbers cannot be presented without these artifact controls.

### 3.2 Control B — Few-Shot Target-Only Refitting vs. Source Recalibration vs. Simple Baselines (4 Unseen Datasets, 10 Seeds)

| Dataset (Zero-Shot AUROC) | `K` | Target-Only TG *(Phase 3)* | Source Risk Recalibrated | 1D EEM Calibrated | 1D Length (`LEN`) | Answer-Text TF-IDF *(Zero LLM)* | Verdict at `K` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **FaithDial** (`0.4929`) | 50 | 0.6987 ± 0.088 | 0.4957 | **0.7473** | 0.6721 | 0.5818 | 1D EEM wins at `K=50` |
| | 100 | **0.7899 ± 0.031** | 0.5029 | 0.7473 | 0.6721 | 0.6145 | TG beats all (`+0.043` over EEM) |
| | 250 | **0.8231 ± 0.012** | 0.5043 | 0.7473 | 0.6721 | 0.6615 | **TG wins clearly** (`+0.076` over EEM, `+0.162` over TF-IDF) |
| **WikiBio-GPT3** (`0.4883`) | 50 | 0.5088 ± 0.056 | 0.4977 | 0.5000 | 0.4909 | **0.5321** | High-dim probe overfits; TF-IDF leads |
| | 100 | 0.4939 ± 0.084 | 0.4977 | 0.5045 | 0.4727 | **0.5785** | High-dim probe overfits; TF-IDF leads |
| | 250 | **0.6698 ± 0.038** | 0.5023 | 0.4955 | 0.4909 | 0.6103 | **TG wins** (`+0.060` over TF-IDF, `+0.174` over EEM) |
| **FEVER** (`0.5205`) | 50 | 0.5394 ± 0.048 | 0.5123 | 0.5176 | 0.4977 | **0.5699** | TF-IDF leads at `K=50` |
| | 100 | **0.6195 ± 0.040** | 0.5000 | 0.5264 | 0.4955 | 0.5966 | TG overtakes TF-IDF (`+0.023`) |
| | 250 | **0.7325 ± 0.014** | 0.5000 | 0.5264 | 0.5045 | 0.6315 | **TG wins strongly** (`+0.101` over TF-IDF) |
| **XSum-Factuality** (`0.4597`) | 50 | 0.5401 ± 0.069 | 0.5000 | **0.6082** | 0.5867 | 0.5329 | 1D EEM & LEN beat TG |
| | 100 | 0.6058 ± 0.043 | 0.5242 | 0.6352 | **0.6445** | 0.5331 | 1D LEN & EEM beat TG |
| | 250 | **0.6456 ± 0.041** | 0.5161 | 0.6352 | **0.6445** | 0.5456 | **Tie with 1D LEN (`+0.0011`)** — no neural probe gain |

### 3.3 Control C — TriviaQA Abstain-Only vs. Full Three-Tier Controller (`n_test = 250`)

| System (`Coverage = 46.0%`, `115/250` answered) | Correct Among Answered | Selective Accuracy | System Hallucination Rate | Active Tier 1/2 Repairs | Correct Answers Broken by Tier 1/2 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Baseline Greedy (`100%` coverage)** | 85 / 250 | 34.00% | 66.00% | 0 | 0 |
| **Pure Abstain-Only (`top-115` lowest risk)** | **64 / 115** | **55.65%** | **20.40%** | 0 | 0 |
| **Full 3-Tier Controller** (`81` Safe, `23` T1, `11` T2, `135` T3) | 63 / 115 | 54.78% (`-0.87%`) | 20.80% | **4** (`2` T1 + `2` T2) | **3** |

### 3.4 Control 4B & 4C — Within-Domain Split-Half Cosine Baseline & Length-Controlled EEM Audit

| Dataset | Within-Domain Split-Half Cosine *(Mean ± SD, 4 layers × 5 splits)* | Cross-Domain Cosine *(vs. Pooled Source)* | Raw `EEM_mean` AUROC | Spearman $\rho(\text{EEM}, \text{LEN})$ | Within-Length-Quartile Mean EEM AUROC | Length-Matched (`\|ΔL\| ≤ 2`) EEM AUROC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **HaluEval-Summ** | **`+0.6888 ± 0.0132`** | — | 0.5787 | `-0.0658` | 0.5331 | 0.5770 |
| **HaluEval-QA** | **`+0.4358 ± 0.0246`** | — | **0.3627** | **`-0.2909`** | 0.4465 | **0.5184** *(inversion vanishes)* |
| **HaluEval-Dialogue** | **`+0.3929 ± 0.0379`** | — | **0.3740** | `-0.1038` | **0.3795** | **0.4525** *(partial persistence)* |
| **TruthfulQA** | **`+0.3440 ± 0.0269`** | — | 0.4912 | `-0.3678` | 0.4720 | 0.5030 |
| **HaluEval-General** | `+0.0506 ± 0.0252` | — | 0.4829 | `-0.1637` | 0.4545 | N/A |
| **FEVER** | **`+0.3680 ± 0.0212`** | `+0.0510` | 0.5417 | `-0.4285` | 0.5547 | N/A |
| **FaithDial** | **`+0.2300 ± 0.0206`** | `-0.0306` | **0.7456** | **`+0.0058`** | **0.7662** *(length-free)* | N/A |
| **WikiBio-GPT3** | **`+0.1290 ± 0.0224`** | `-0.0045` | 0.5207 | `-0.2348` | 0.5278 | N/A |
| **XSum-Factuality** | **`+0.1073 ± 0.0272`** | `+0.0280` | **0.6648** | **`-0.0321`** | **0.6648** *(length-free)* | N/A |
| *Random 2048-d baseline* | *`0.0000 ± 0.0221`* | *`0.0000 ± 0.0221`* | *0.5000* | *0.0000* | *0.5000* | *0.5000* |

---

## 4. Assessment: Are Headline In-Domain AUROCs Still Defensible?

**Verdict: NO as unqualified "factual hallucination detection" headlines; YES when paired with artifact controls and closed-book TriviaQA.**
- Reporting `0.9880` (HaluEval-QA) and `0.9936` (HaluEval-Summ) without Control A would be scientifically misleading, because `LEN` alone scores `0.9572` on HaluEval-QA and answer-text TF-IDF alone scores `0.9539–0.9661` on both.
- **What IS defensible:** (1) On strictly length-matched pairs (`|ΔL| ≤ 2`), TRUEGUARD still achieves **`0.7901` (HaluEval-QA)**, **`0.7996` (HaluEval-Dialogue)**, **`0.8106` (TruthfulQA)**, and **`0.9939` (HaluEval-Summ)**; (2) TRUEGUARD outperforms Answer-Text TF-IDF on all 5 benchmarks (`+0.022` to `+0.071`); and (3) on **model-generated closed-book TriviaQA** (where there is no synthetic HaluEval construction artifact), TRUEGUARD achieves **`0.7876` AUROC / `0.4360` AURC**, significantly beating Semantic Entropy (`0.6859`), Predictive Entropy (`0.6583`), and NLL (`0.4678`).
- **Action:** Present Control A in the main paper as a **benchmark-artifact diagnostic contribution** rather than hiding it, and anchor TRUEGUARD's real-world detection credibility on **TriviaQA (`0.7876`)** and **length-matched / TF-IDF-controlled gains**.

---

## 5. Assessment: Does Few-Shot Adaptation Demonstrate Value Beyond Target-Only Training?

**Verdict: NO — Phase 3 IS target-only training, and source weights provide zero transfer (`SrcRecal = 0.496–0.524`).**
- Calling Phase 3 "few-shot adaptation" is a **terminology error** because `fit_all_subsets` fits fresh target-domain probes from scratch without using source weights.
- Furthermore, Control B reveals a sharp, publishable sample-efficiency boundary:
  - At `K=50`, 2,048-dim linear probes overfit: **1D EEM beats TG on FaithDial (`0.747` vs `0.699`) and XSum (`0.608` vs `0.540`)**, while **TF-IDF beats TG on FEVER (`0.570` vs `0.539`) and WikiBio (`0.532` vs `0.509`)**.
  - At `K=250`, **target-only TG refitting genuinely wins** on FaithDial (`0.8231` vs. `0.7473` EEM / `0.6615` TF-IDF), FEVER (`0.7325` vs. `0.6315` TF-IDF), and WikiBio (`0.6698` vs. `0.6103` TF-IDF) — **while on XSum it merely ties 1D length (`0.6456` vs. `0.6445`)**.
- **Action:** Rename Phase 3 to **"Target-Domain Few-Shot Refitting & Sample-Efficiency Analysis"** and report the full Control B comparison table (including `SrcRecal`, `EEM-1D`, `LEN-1D`, and `TF-IDF`) honestly.

---

## 6. Assessment: Does the Three-Tier Mitigation Controller Improve Beyond Abstain-Only?

**Verdict: NO — Pure abstain-only (`55.65%`, `64/115`) slightly outperforms the full 3-tier controller (`54.78%`, `63/115`) at matched 46.0% coverage.**
- Active Tier 1 resampling and Tier 2 TF-IDF retrieval fixed `4` hallucinations (`2` + `2`), **but also broke `3` originally correct greedy answers**, yielding `-0.87%` net selective accuracy compared to simply abstaining on the `135` highest-risk questions.
- **Why this happened (scientifically interesting negative result):** On a 1.1B model with only `34%` closed-book accuracy and no external corpus (local TF-IDF retrieval over limited context), stochastic resampling and weak retrieval cannot inject missing parametric knowledge — they mostly add noise.
- **Action:** Reframe the mitigation contribution strictly as **risk-calibrated selective abstention** (`66.0% → 20.4%` system hallucination / `34.0% → 55.7%` selective accuracy at `46%` coverage, `AURC = 0.4360`), and report the Tier 1/2 active-repair ablation honestly as a **negative result** showing why small frozen LLMs benefit from abstention rather than self-repair without strong external RAG.

---

## 7. Strongest Defensible Research Novelty

Claude's strategic critique (§3B) is right: framing TRUEGUARD as a "novel 4-sensor + 3-tier mitigation architecture" will draw severe reviewer pushback because ISP dominates >96% of fusion weight, individual sensors build on known signals, and Tier 1/2 fails to beat abstain-only.

The **strongest, genuinely defensible IEEE Access framing** is an **Empirical & Diagnostic Study of Single-Pass White-Box Hallucination Detection on a Frozen Small LLM**:
1. **Unmasking Benchmark Artifacts in Teacher-Forced Detection (Control A):** Demonstrating quantitatively that widely used HaluEval benchmarks yield `0.95–0.97` AUROC from surface TF-IDF or length alone, while verifying that white-box probing retains `0.79–0.81` AUROC under strict length matching and beats TF-IDF across all 5 benchmarks.
2. **Mechanistic Diagnosis of Cross-Domain Probe Collapse (Phase 2 + Controls 4B/4C):** Proving via within-domain split-half baselines (`cos = +0.23` to `+0.69`) vs. cross-domain cosines (`[-0.03, +0.05]`) that linear truth probes rotate into orthogonal subspaces across domains, explaining why pooled white-box detectors collapse to chance (`0.46–0.52`), and separating genuine length-free EEM signal on natural data (`FaithDial 0.766`, `XSum 0.665`) from length-confounded EEM inversion on HaluEval-QA (`0.363 → 0.518`).
3. **Sample-Efficiency Boundaries of Target-Domain Refitting (Control B):** Showing that source recalibration fails (`~0.50`), ultra-low-data regimes (`K=50`) favor 1D EEM or TF-IDF over 2,048-dim probes, and `K=250` target-only refitting (`<2s` CPU) unlocks genuine white-box gains on FaithDial, FEVER, and WikiBio (but not length-dominated XSum).
4. **Single-Pass White-Box vs. Multi-Sample Black-Box Selective Answering on Closed-Book TriviaQA (External Baselines + Control C):** Demonstrating on model-generated answers (`n_test=250`) that single-pass TRUEGUARD (`0.7876` AUROC / `0.4360` AURC) significantly outperforms `M=10` Semantic Entropy (`0.6859`, `p_Holm=0.012`), Predictive Entropy (`0.6583`), and NLL (`0.4678`), matches `M=10` SelfCheckGPT-NLI (`0.7477`, n.s.) with `0` external NLI models, and showing forensically that **selective abstention (`55.65%`) outperforms active Tier 1/2 self-repair (`54.78%`)** on a 1.1B model.

---

## 8. Essential Remaining Corrections Before Drafting

### Mandatory Corrections (Zero GPU Required — Update `publication_ready/` Package Only)
1. **Integrate Controls A, B, C, 4B, and 4C into `publication_ready/` tables and summary docs** (`Table1`–`Table7` + a new Artifact & Simple-Baseline Control Table, plus updating `03_contributions_and_limitations.md` and `FINAL_IEEE_ACCESS_RESEARCH_READINESS_REPORT.md`).
2. **Fix Terminology & Claims Across All Docs:**
   - Replace *"few-shot adaptation"* with **"target-domain few-shot refitting"** (explicitly noting zero source-weight transfer and `SrcRecal ≈ 0.50`).
   - Replace *"4-sensor synergy"* with **"ISP-dominant multi-signal diagnostic framework (with EEM as low-K/zero-shot fallback)"**.
   - Replace *"3-tier mitigation reduces hallucinations"* with **"risk-calibrated selective abstention (`55.65%` vs. `34.0%` baseline), with Tier 1/2 active repair reported as a neutral/negative ablation (`54.78%`, 4 fixed / 3 broken)"**.
   - Qualify HaluEval headline AUROCs (`0.988–0.994`) inline with Control A (`LEN`, `TF-IDF`, and length-matched AUROCs).
   - Refine the EEM sign-inversion claim using Control 4C (distinguishing length-confounded HaluEval-QA from length-free FaithDial/XSum and persistent HaluEval-Dialogue).

### Optional GPU Expansions (Recommended Only If Targeting Top-Tier Venues Beyond IEEE Access)
- **Second larger LLM (e.g., Llama-3-8B or Mistral-7B) + larger TriviaQA test set (`n_test = 1,000`):** Would strengthen external validity and statistical power against SelfCheckGPT-NLI, **but is NOT strictly required for IEEE Access** if the paper is honestly scoped as a **small frozen LLM (`1.1B`) empirical & diagnostic study** with all CIs, negative results, and single-model limitations stated transparently.

---

## 9. Final Verdict

# **TARGETED CORRECTIONS STILL REQUIRED** *(Zero-GPU Package & Framing Revisions Only)*

**Why not `READY TO DRAFT` yet:** Our new CPU-only controls uncovered three concrete claims in the current `publication_ready/` package that would fail rigorous peer review if drafted as-is:
1. Unqualified HaluEval `0.988–0.994` headline AUROCs without disclosing `0.957` length / `0.954–0.966` TF-IDF artifacts and length-matched (`0.790–0.811`) controls.
2. Calling Phase 3 "few-shot adaptation" without disclosing it is target-only refitting (`SrcRecal ≈ 0.50`), that 1D LEN matches TG on XSum (`0.6445` vs. `0.6456`), and that EEM-1D/TF-IDF beat TG at `K=50`.
3. Presenting the 3-tier mitigation controller as superior without disclosing that pure abstain-only achieves `55.65%` (`64/115`) vs. `54.78%` (`63/115`) for the full controller (4 fixed, 3 broken).

**Good news:** **Zero additional GPU runs are needed** to resolve all three blockers. Updating the `publication_ready/` tables and reframing docs to incorporate Controls A, B, C, 4B, and 4C will bring the project cleanly to **`READY TO DRAFT`** for IEEE Access.
