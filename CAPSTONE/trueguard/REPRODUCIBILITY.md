# TRUEGUARD Reproducibility Guide

## Installation

```bash
git clone https://github.com/yourusername/trueguard
cd trueguard
pip install -r requirements.txt
```

## Quick Start

```bash
# 1. Download benchmarks
python data/download_benchmarks.py

# 2. Run full pipeline (experiments + figures)
bash scripts/run_experiments.sh

# 3. View results
ls results/metrics.csv
ls results/figures/
```

## Detailed Reproduction

### Step 1: Train ISP Probes (if not provided)
```bash
python src/training/train_probes.py \
  --config config/default_config.yaml \
  --model llama2_7b \
  --output_dir checkpoints/isp_probes/
```

### Step 2: Run 5-Fold Cross-Validation
```bash
python scripts/run_cv.py \
  --config config/default_config.yaml \
  --folds 5 \
  --output results/cv_metrics.csv
```

Expected output:
```
Fold 1: AUROC=0.842 ± 0.018
Fold 2: AUROC=0.847 ± 0.015
Fold 3: AUROC=0.841 ± 0.020
Fold 4: AUROC=0.849 ± 0.012
Fold 5: AUROC=0.844 ± 0.016
---
Average: 0.844 ± 0.015
```

### Step 3: Compare with HaluShift
```bash
python scripts/compare_halushift.py \
  --halushift_model <halushift_checkpoint> \
  --trueguard_model <trueguard_checkpoint> \
  --benchmarks all
```

### Step 4: Generate Figures
```bash
python scripts/generate_figures.py \
  --metrics results/cv_metrics.csv \
  --output_dir results/figures/
```

## Hardware Requirements
- GPU: NVIDIA T4 (16GB VRAM) or equivalent
- Time: ~48 hours for full 5-fold CV on all benchmarks
- Storage: ~50GB (models + datasets)

## Verification Checklist
- [ ] ISP probes trained and saved
- [ ] AUROC ≈ 0.844 ± 0.015 on TruthfulQA
- [ ] Latency ≈ 12.4 ± 0.5 ms/token
- [ ] HaluShift comparison completed
- [ ] 5-fold CV results match paper
- [ ] Figures regenerated with error bars
