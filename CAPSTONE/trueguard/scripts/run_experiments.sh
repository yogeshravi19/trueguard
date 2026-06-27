#!/bin/bash

# TRUEGUARD Real-Time Detection Pipeline Runner

echo "============================================================"
echo "TRUEGUARD: Real-Time Hallucination Detection Pipeline"
echo "============================================================"

# Step 1: Ensure dependencies are installed
echo "[1/4] Checking dependencies..."
pip install -r requirements.txt -q

# Step 2: Download datasets (TruthfulQA, HaluEval)
echo "[2/4] Preparing Benchmark Datasets..."
python data/download_benchmarks.py

# Step 3: Run the Evaluation Pipeline
echo "[3/4] Running 5-Fold Cross Validation and Latency Benchmarks..."
python src/evaluation/evaluate.py

echo "[4/4] Pipeline Complete!"
echo "Check output logs to update main.tex AUROC and Latency values."
