# Baseline Comparison Matrix (Reproduced vs. Literature Reference)

## A. Experimentally Reproduced Baselines (Identical Model, Data, Splits, and Hardware)
| Baseline | Category | Protocol Fidelity | Key Finding vs. TRUEGUARD |
| :--- | :--- | :--- | :--- |
| **ISP-Only (SAPLMA-style multi-layer probe, Azaria & Mitchell 2023)** | White-box linear probe | Identical hidden states & GroupKFold splits | Matches full fusion in-domain (`+/-0.002`); collapses zero-shot (`0.445-0.516`) and under severe imbalance (`XSum K=100: 0.500 vs 0.606`). |
| **Predictive Entropy (`ENT_mean/max`, Kuhn et al. 2023 baseline)** | Token uncertainty | Identical logits & splits | Inverted on synthetic HaluEval (`0.355-0.372`); strong zero-shot on FaithDial (`0.744`) & XSum (`0.667`); significantly worse than TRUEGUARD on TriviaQA (`AURC 0.531 vs 0.436, p<0.0001`). |
| **Length-Normalized NLL (`NLL_mean`)** | Token likelihood | Identical logits & splits | Strongly inverted on HaluEval (`0.095-0.296`); weak on TriviaQA (`AURC 0.684 vs 0.436, p<0.0001`). |
| **Raw EEM (Shannon + Renyi-2)** | Unsupervised white-box | Identical logits & splits | Best zero-shot method on FaithDial (`0.747`) and XSum (`0.635`); surpassed by `K=250` adapted TRUEGUARD on FaithDial (`0.823`), WikiBio (`0.670`), and FEVER (`0.733`). |
| **AAS / DST / Scalars-Only (`AAS+EEM+DST`)** | Attention / trajectory | Identical activations & splits | Individually weaker in-domain (`0.52-0.86`); stabilize fusion on imbalanced `XSum K=50/100` and provide low-FPR complementarity. |
| **Answer-Length Heuristic (`LEN`)** | Confound audit baseline | Identical splits | Exposes severe length confound in HaluEval-QA (`0.957` raw AUROC); neutral/weak on TruthfulQA (`0.450`) and HaluEval-General (`0.475`). |
| **5x Multi-Sample Decoding Cost** | Latency proxy (SelfCheckGPT / Semantic Entropy) | Identical CUDA T4, 25x24 tokens | `158.77 ms/tok` vs. TRUEGUARD `34.52 ms` post-pass (`4.60x` faster) / `37.84 ms` online (`4.20x` faster). |

## B. Published Literature Methods (Contextual Reference Only — NOT Direct Numerical Superiority Claims)
- **SelfCheckGPT** (Manakul et al., EMNLP 2023): Black-box multi-sampling (5–20 samples + NLI/BERTScore); evaluated on GPT-3 WikiBio.
- **Semantic Entropy** (Kuhn et al., Nature 2023; Farquhar et al., Nature 2024): 5–10 sampled generations + bidirectional DeBERTa-MNLI semantic clustering.
- **ITI** (Li et al., NeurIPS 2023), **EigenScore/INSIDE** (Chen et al., ICLR 2024), **Lookback Lens** (Chuang et al., ACL 2024): Different base models (LLaMA-7B/13B) or multi-sample activation covariance.
- **Explicit Gap Note:** Full black-box accuracy reproduction of Semantic Entropy (10 samples + DeBERTa-MNLI) on the 250 TriviaQA test questions was not run (would require ~15 min on a Colab T4 GPU). Our comparison against Semantic Entropy/SelfCheckGPT is strictly on **measured computational cost (4.2–4.6x speedup)** and **architectural trade-offs**, never on mismatched accuracy tables.
