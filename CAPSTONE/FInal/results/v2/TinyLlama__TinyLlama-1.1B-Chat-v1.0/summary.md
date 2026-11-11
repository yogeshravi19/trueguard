# TRUEGUARD v2 – Experimental Detection Report (real model activations)

## 1. In-distribution 5-fold grouped CV

| Dataset | N (pairs) | Fusion AUROC [95% CI] | ISP | AAS | EEM | DST | Best raw baseline | Gain vs best single (p) | F1 | ECE |
|---|---:|---|---|---|---|---|---|---|---|---|
| halueval_dialogue | 400 | **0.903** [0.883,0.922] | 0.904 | 0.618 | 0.668 | 0.634 | LEN=0.687 | -0.001 (p=0.78) | 0.820 | 0.034 |
| halueval_qa | 400 | **0.975** [0.964,0.987] | 0.977 | 0.512 | 0.850 | 0.859 | LEN=0.953 | -0.002 (p=1.00) | 0.955 | 0.024 |
| halueval_summarization | 400 | **0.986** [0.980,0.991] | 0.987 | 0.627 | 0.580 | 0.672 | EEM_mean=0.581 | -0.000 (p=0.70) | 0.935 | 0.025 |
| truthful_qa | 398 | **0.876** [0.853,0.900] | 0.877 | 0.607 | 0.522 | 0.533 | EEM_max=0.523 | -0.001 (p=0.77) | 0.817 | 0.042 |

## 2. Cross-dataset generalisation (train row → test column)

- **halueval_dialogue → halueval_qa**: fusion AUROC = **0.946** (ISP-only=0.948, AAS+EEM+DST=0.737, F1@τ_warn=0.863)
- **halueval_dialogue → halueval_summarization**: fusion AUROC = **0.767** (ISP-only=0.776, AAS+EEM+DST=0.497, F1@τ_warn=0.680)
- **halueval_dialogue → truthful_qa**: fusion AUROC = **0.533** (ISP-only=0.540, AAS+EEM+DST=0.544, F1@τ_warn=0.586)
- **halueval_qa → halueval_dialogue**: fusion AUROC = **0.709** (ISP-only=0.723, AAS+EEM+DST=0.613, F1@τ_warn=0.681)
- **halueval_qa → halueval_summarization**: fusion AUROC = **0.684** (ISP-only=0.678, AAS+EEM+DST=0.490, F1@τ_warn=0.667)
- **halueval_qa → truthful_qa**: fusion AUROC = **0.422** (ISP-only=0.427, AAS+EEM+DST=0.456, F1@τ_warn=0.629)
- **halueval_summarization → halueval_dialogue**: fusion AUROC = **0.779** (ISP-only=0.768, AAS+EEM+DST=0.561, F1@τ_warn=0.572)
- **halueval_summarization → halueval_qa**: fusion AUROC = **0.777** (ISP-only=0.845, AAS+EEM+DST=0.647, F1@τ_warn=0.392)
- **halueval_summarization → truthful_qa**: fusion AUROC = **0.567** (ISP-only=0.551, AAS+EEM+DST=0.509, F1@τ_warn=0.532)
- **truthful_qa → halueval_dialogue**: fusion AUROC = **0.615** (ISP-only=0.605, AAS+EEM+DST=0.610, F1@τ_warn=0.103)
- **truthful_qa → halueval_qa**: fusion AUROC = **0.382** (ISP-only=0.340, AAS+EEM+DST=0.322, F1@τ_warn=0.363)
- **truthful_qa → halueval_summarization**: fusion AUROC = **0.530** (ISP-only=0.530, AAS+EEM+DST=0.536, F1@τ_warn=0.246)

## 3. Automatic diagnostics

- **halueval_dialogue**: AAS_mean: raw AUROC=0.378 (<0.5) -> signal points the OPPOSITE way on halueval_dialogue (inverted AUROC=0.622); logistic fusion flips its sign automatically.
- **halueval_dialogue**: EEM_mean: raw AUROC=0.372 (<0.5) -> signal points the OPPOSITE way on halueval_dialogue (inverted AUROC=0.628); logistic fusion flips its sign automatically.
- **halueval_dialogue**: DST_mean: raw AUROC=0.407 (<0.5) -> signal points the OPPOSITE way on halueval_dialogue (inverted AUROC=0.593); logistic fusion flips its sign automatically.
- **halueval_dialogue**: ENT_mean: raw AUROC=0.370 (<0.5) -> signal points the OPPOSITE way on halueval_dialogue (inverted AUROC=0.630); logistic fusion flips its sign automatically.
- **halueval_dialogue**: NLL_mean: raw AUROC=0.240 (<0.5) -> signal points the OPPOSITE way on halueval_dialogue (inverted AUROC=0.760); logistic fusion flips its sign automatically.
- **halueval_dialogue**: Fusion did NOT beat best single sensor (ISP=0.904 vs fusion=0.903); non-ISP sensors add noise on this dataset.
- **halueval_qa**: EEM_mean: raw AUROC=0.358 (<0.5) -> signal points the OPPOSITE way on halueval_qa (inverted AUROC=0.642); logistic fusion flips its sign automatically.
- **halueval_qa**: DST_mean: raw AUROC=0.306 (<0.5) -> signal points the OPPOSITE way on halueval_qa (inverted AUROC=0.694); logistic fusion flips its sign automatically.
- **halueval_qa**: ENT_mean: raw AUROC=0.349 (<0.5) -> signal points the OPPOSITE way on halueval_qa (inverted AUROC=0.651); logistic fusion flips its sign automatically.
- **halueval_qa**: NLL_mean: raw AUROC=0.089 (<0.5) -> signal points the OPPOSITE way on halueval_qa (inverted AUROC=0.911); logistic fusion flips its sign automatically.
- **halueval_qa**: Fusion did NOT beat best single sensor (ISP=0.977 vs fusion=0.975); non-ISP sensors add noise on this dataset.
- **halueval_summarization**: AAS_mean: raw AUROC=0.477 (<0.5) -> signal points the OPPOSITE way on halueval_summarization (inverted AUROC=0.523); logistic fusion flips its sign automatically.
- **halueval_summarization**: AAS_max: raw AUROC=0.388 (<0.5) -> signal points the OPPOSITE way on halueval_summarization (inverted AUROC=0.612); logistic fusion flips its sign automatically.
- **halueval_summarization**: DST_mean: raw AUROC=0.326 (<0.5) -> signal points the OPPOSITE way on halueval_summarization (inverted AUROC=0.674); logistic fusion flips its sign automatically.
- **halueval_summarization**: DST_max: raw AUROC=0.423 (<0.5) -> signal points the OPPOSITE way on halueval_summarization (inverted AUROC=0.577); logistic fusion flips its sign automatically.
- **halueval_summarization**: NLL_mean: raw AUROC=0.301 (<0.5) -> signal points the OPPOSITE way on halueval_summarization (inverted AUROC=0.699); logistic fusion flips its sign automatically.
- **halueval_summarization**: Fusion did NOT beat best single sensor (ISP=0.987 vs fusion=0.986); non-ISP sensors add noise on this dataset.
- **truthful_qa**: AAS_mean: raw AUROC=0.392 (<0.5) -> signal points the OPPOSITE way on truthful_qa (inverted AUROC=0.608); logistic fusion flips its sign automatically.
- **truthful_qa**: DST_max: raw AUROC=0.469 (<0.5) -> signal points the OPPOSITE way on truthful_qa (inverted AUROC=0.531); logistic fusion flips its sign automatically.
- **truthful_qa**: LEN: raw AUROC=0.456 (<0.5) -> signal points the OPPOSITE way on truthful_qa (inverted AUROC=0.544); logistic fusion flips its sign automatically.
- **truthful_qa**: Fusion did NOT beat best single sensor (ISP=0.877 vs fusion=0.876); non-ISP sensors add noise on this dataset.
