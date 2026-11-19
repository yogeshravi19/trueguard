# Table VI — Controlled Sequential Inference Latency Profiling on CUDA T4 (TinyLlama-1.1B, eager, batch_size=1, 25×24 tokens)

| Decoding Mode (TinyLlama-1.1B, CUDA T4, 25x24 tok) | Latency (ms/tok) | Abs. Overhead (ms/tok) | Rel. Overhead (%) | Speedup vs 5x Sampling |
| --- | --- | --- | --- | --- |
| Vanilla KV-Cached Decode | 29.78 | 0.00 | 0.0% | 5.33x |
| TRUEGUARD Post-Pass (1x Forward) | 34.52 | +4.74 | +15.9% | 4.60x |
| TRUEGUARD Online (Per-Token; math=4.93ms) | 37.84 | +8.06 | +27.1% | 4.20x |
| 5x Multi-Sample Baseline (SelfCheck/SE cost) | 158.77 | +129.00 | +433.2% | 1.00x |

*Source: `results/real_latency.json`. Protocol Non-Equivalence Disclosure: The 4.20x–4.60x speedup applies strictly to controlled sequential single-query decoding (`attn_implementation='eager'`, `batch_size=1`, `min_new_tokens=24`). It does NOT establish universal wall-clock speedup over GPU-batched (`batch_size=10`, `sdpa`, early EOS) SelfCheckGPT-NLI (0.7068 s/q in Colab vs. 0.8285 s/q TRUEGUARD eager post-pass). Monitoring-only latency excludes Tier 1/2 mitigation overhead.*
