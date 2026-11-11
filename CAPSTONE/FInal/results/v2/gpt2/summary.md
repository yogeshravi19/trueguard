# TRUEGUARD v2 – Experimental Detection Report (real model activations)

## 1. In-distribution 5-fold grouped CV

| Dataset | N (pairs) | Fusion AUROC [95% CI] | ISP | AAS | EEM | DST | Best raw baseline | Gain vs best single (p) | F1 | ECE |
|---|---:|---|---|---|---|---|---|---|---|---|
| halueval_qa | 80 | **0.960** [0.916,0.992] | 0.957 | 0.486 | 0.857 | 0.894 | LEN=0.951 | +0.002 (p=0.36) | 0.948 | 0.102 |
| truthful_qa | 80 | **0.744** [0.669,0.820] | 0.766 | 0.485 | 0.383 | 0.489 | ENT_max=0.517 | -0.021 (p=0.98) | 0.729 | 0.080 |

## 2. Cross-dataset generalisation (train row → test column)

- **halueval_qa → truthful_qa**: fusion AUROC = **0.440** (ISP-only=0.442, AAS+EEM+DST=0.475, F1@τ_warn=0.635)
- **truthful_qa → halueval_qa**: fusion AUROC = **0.385** (ISP-only=0.265, AAS+EEM+DST=0.506, F1@τ_warn=0.451)

## 3. Automatic diagnostics

- **halueval_qa**: EEM_mean: raw AUROC=0.181 (<0.5) -> signal points the OPPOSITE way on halueval_qa (inverted AUROC=0.819); logistic fusion flips its sign automatically.
- **halueval_qa**: DST_mean: raw AUROC=0.411 (<0.5) -> signal points the OPPOSITE way on halueval_qa (inverted AUROC=0.589); logistic fusion flips its sign automatically.
- **halueval_qa**: ENT_mean: raw AUROC=0.182 (<0.5) -> signal points the OPPOSITE way on halueval_qa (inverted AUROC=0.818); logistic fusion flips its sign automatically.
- **halueval_qa**: NLL_mean: raw AUROC=0.148 (<0.5) -> signal points the OPPOSITE way on halueval_qa (inverted AUROC=0.852); logistic fusion flips its sign automatically.
- **halueval_qa**: Fusion gain over ISP is +0.002 but 95% CI [-0.010, 0.017] crosses 0 (p=0.36).
- **truthful_qa**: AAS_mean: raw AUROC=0.465 (<0.5) -> signal points the OPPOSITE way on truthful_qa (inverted AUROC=0.535); logistic fusion flips its sign automatically.
- **truthful_qa**: DST_mean: raw AUROC=0.436 (<0.5) -> signal points the OPPOSITE way on truthful_qa (inverted AUROC=0.564); logistic fusion flips its sign automatically.
- **truthful_qa**: LEN: raw AUROC=0.464 (<0.5) -> signal points the OPPOSITE way on truthful_qa (inverted AUROC=0.536); logistic fusion flips its sign automatically.
- **truthful_qa**: Fusion did NOT beat best single sensor (ISP=0.766 vs fusion=0.744); non-ISP sensors add noise on this dataset.
