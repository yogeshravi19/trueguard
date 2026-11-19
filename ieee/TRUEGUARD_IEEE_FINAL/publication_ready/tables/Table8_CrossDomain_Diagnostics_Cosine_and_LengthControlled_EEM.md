# Table VIII — Empirical Domain-Shift Diagnostics: Within-Domain vs. Cross-Domain Probe Cosine and Length-Controlled EEM Audit

| Dataset | Role | Within-Domain Split-Half Cosine (Mean +/- SD) | Cross-Domain Cosine (vs. Pooled Source) | Raw EEM_mean AUROC | Spearman rho(EEM, LEN) | Within-Length-Quartile Mean EEM AUROC | Length-Matched (|dL|<=2) EEM AUROC |
| --- | --- | --- | --- | --- | --- | --- | --- |
| halueval_summarization | In-Domain | +0.6888 +/- 0.0132 | — (source) | 0.5787 | -0.0658 | 0.5331 | 0.5770 |
| halueval_qa | In-Domain | +0.4358 +/- 0.0246 | — (source) | 0.3627 | -0.2909 | 0.4465 | 0.5184 |
| halueval_dialogue | In-Domain | +0.3929 +/- 0.0379 | — (source) | 0.3740 | -0.1038 | 0.3795 | 0.4525 |
| truthful_qa | In-Domain | +0.3440 +/- 0.0269 | — (source) | 0.4912 | -0.3678 | 0.4720 | 0.5030 |
| halueval_general | In-Domain | +0.0506 +/- 0.0252 | — (source) | 0.4829 | -0.1637 | 0.4545 | N/A (unpaired) |
| fever | Claim-Verif. | +0.3680 +/- 0.0212 | +0.0510 | 0.5417 | -0.4285 | 0.5547 | N/A (unpaired) |
| faithdial | Unseen Target | +0.2300 +/- 0.0206 | -0.0306 | 0.7456 | +0.0058 | 0.7662 | N/A (unpaired) |
| wikibio_gpt3 | Unseen Target | +0.1290 +/- 0.0224 | -0.0045 | 0.5207 | -0.2348 | 0.5278 | N/A (unpaired) |
| xsum_factuality | Unseen Target | +0.1073 +/- 0.0272 | +0.0280 | 0.6648 | -0.0321 | 0.6648 | N/A (unpaired) |
| Random 2048-d Gaussian Baseline | Theoretical Null | 0.0000 +/- 0.0221 | 0.0000 +/- 0.0221 | 0.5000 | 0.0000 | 0.5000 | 0.5000 |

*Sources: `research_improvements/phase2_cross_domain_diagnostics.json` and `reviewer_response/cosine_and_eem_controls.json`. Methodological Caveat: In high-dimensional correlated hidden spaces (d=2048), L2-regularized linear probe coefficients are not uniquely identifiable causal axes; however, the sharp empirical contrast between within-domain split-half alignment (+0.230 to +0.689 on homogeneous benchmarks, 10–31x random std) and cross-domain alignment (-0.031 to +0.051, within random noise) provides clear diagnostic evidence of domain-dependent linear decision boundaries. Length-controlled EEM separates genuine length-free uncertainty signal on FaithDial (0.7662) and XSum (0.6648) from length-confounded inversion on HaluEval-QA (0.3627 -> 0.5184 under length matching) and persistent inverse association on HaluEval-Dialogue (0.3795 quartile-mean).*
