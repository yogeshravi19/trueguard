"""
Build `notebooks/TRUEGUARD_Colab_REAL.ipynb`: a complete, sequential, end-to-end Google Colab notebook for the
TRUEGUARD v2 implementation paper.  The user runs this on a Colab GPU (T4 or better); nothing in the notebook is
simulated or pre-filled.
"""
import json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(True)}


def code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": text.splitlines(True)}


CELLS = [
    md("""# TRUEGUARD v2 — Complete Experimental Verification (Google Colab GPU)

This notebook runs the **entire real implementation** of the TRUEGUARD architecture proposed in Section 6 of the review paper:
1. **Four real sensors** extracted from the LLM's own hidden states, attention matrices, and output logits (`src/tg_pipeline.py`):
   - **ISP** — per-layer linear probes **trained on labelled hidden states** (no std-dispersion proxy).
   - **AAS** — normalised Shannon entropy of final-quartile attention heads.
   - **EEM** — $0.6\\,H_{\\text{Shannon,norm}} + 0.4\\,H_{\\text{Rényi-2,norm}}$ of output logits.
   - **DST** — temporal cosine distance between consecutive layer-averaged hidden states.
2. **Leakage-free fusion training**: grouped 5-fold CV (both answers of a question stay in the same fold); inner out-of-fold probe scores feed the logistic-regression fusion layer.
3. **Two calibrated thresholds & three mitigation tiers** (`src/tg_controller.py`): Safe $\\to$ Tier 1 risk-guided re-sampling $\\to$ Tier 2 Wikipedia-grounded regeneration $\\to$ Tier 3 calibrated abstention.
4. **Scientific evaluation**: in-distribution CV, single-sensor baselines, leave-one-sensor-out ablation + paired bootstrap significance test, sensor complementarity & correlations, cross-dataset generalisation matrix, real latency profiling, and before/after mitigation on TriviaQA.

**Before running:** `Runtime → Change runtime type → T4 GPU` (or L4 / A100)."""),

    md("## 1. GPU check & dependencies"),
    code("""!nvidia-smi
!pip -q install transformers accelerate datasets bitsandbytes"""),

    md("""## 2. Upload `trueguard_final.zip`
Upload `E:\\trueguard\\CAPSTONE\\trueguard_final.zip` when prompted (or mount Google Drive if you placed it there)."""),
    code("""import os
from google.colab import files
up = files.upload()  # select trueguard_final.zip
zip_name = next(iter(up.keys()))
!rm -rf /content/trueguard && mkdir -p /content/trueguard
!unzip -q -o "{zip_name}" -d /content/trueguard
%cd /content/trueguard
!ls -la"""),

    md("## 3. Unit & leakage verification (must pass before any experiment)"),
    code("""!python -u tests/test_equivalence.py"""),

    md("## 4. Download the real benchmark datasets (TruthfulQA, HaluEval QA/Dial/Summ, TriviaQA)"),
    code("""!python -u tools/download_datasets.py
!cat datasets/manifest.json"""),

    md("""## 5. Configuration
Choose the backbone model and sample budget.
- Default: `TinyLlama/TinyLlama-1.1B-Chat-v1.0` with `N_QUESTIONS = 400` per dataset (800 answers per dataset, ~12–18 min total for feature extraction on a T4).
- Stronger 7B option (fits on a 16 GB T4 in 4-bit): set `MODEL = "mistralai/Mistral-7B-Instruct-v0.2"` and `FOURBIT = "--4bit"`."""),
    code("""MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
TAG = MODEL.replace("/", "__")
N_QUESTIONS = 400          # per dataset (each question gives 1 grounded + 1 hallucinated answer)
FOURBIT = ""               # set to "--4bit" for 7B models on a 16 GB T4"""),

    md("## 6. Step 1 — Extract real sensor features & hidden states on all four benchmarks"),
    code("""!python -u experiments/extract_features.py --model "$MODEL" --n $N_QUESTIONS $FOURBIT"""),

    md("""## 7. Step 2 — Full detection evaluation, ablations, baselines, cross-dataset transfer & figures
Computes AUROC (with 95% group-bootstrap CIs), AUPRC, Accuracy, Precision, Recall, F1, confusion matrices, ECE, single-sensor AUROCs, leave-one-sensor-out ablations, paired bootstrap test for **Fusion vs Best Single Sensor**, complementarity at 10% FPR, cross-dataset transfer matrix, and diagnostics."""),
    code("""!python -u experiments/evaluate_detection.py --cache "results/cache/$TAG" --out "results/v2/$TAG"
from IPython.display import Markdown, Image, display
display(Markdown(open(f"results/v2/{TAG}/summary.md").read()))"""),

    md("## 8. Display ROC curves, ablation bars, risk distributions, confusion matrices & cross-dataset heatmap"),
    code("""import glob
for p in sorted(glob.glob(f"results/v2/{TAG}/figures/*.png")):
    print(p)
    display(Image(filename=p, width=520))"""),

    md("""## 9. Step 3 — End-to-end three-tier mitigation evaluation on TriviaQA (before vs after)
Calibrates $(\\tau_{\\text{warning}},\\tau_{\\text{fault}})$ on 150 calibration questions, then runs the closed-loop controller on 150 disjoint test questions."""),
    code("""!python -u experiments/evaluate_mitigation.py --model "$MODEL" --n_cal 150 --n_test 150 --out "results/v2/$TAG/mitigation" $FOURBIT
import json
mit = json.load(open(f"results/v2/{TAG}/mitigation/mitigation_report.json"))
print(json.dumps({k: v for k, v in mit.items() if k != "examples"}, indent=2))"""),

    md("## 10. Step 4 — Real per-token latency profiling (vanilla vs TRUEGUARD vs 5-sample baseline)"),
    code("""!python -u experiments/profile_real_latency.py --model "$MODEL" --n_prompts 25 --n_tokens 24 --out "results/v2/$TAG/real_latency.json" $FOURBIT"""),

    md("## 11. Interactive single-prompt walkthrough (input → 4 sensors → fusion → tier decision → final answer)"),
    code("""from src.tg_pipeline import load_model, TrueGuardDetector
from src.tg_eval import calibrate_thresholds
from src.tg_controller import ThreeTierController, WikipediaRetriever
import numpy as np, json

d = np.load(f"results/cache/{TAG}/halueval_qa.npz")
det = TrueGuardDetector().fit(d["F"], d["H"], d["y"], d["groups"])
tw, tf = calibrate_thresholds(d["y"], det.train_risk_)
model, tok, dev = load_model(MODEL, load_in_4bit=bool(FOURBIT))
ctrl = ThreeTierController(model, tok, dev, det, tw, tf, retriever=WikipediaRetriever())

for q in [
    "Answer the question briefly in one short sentence.\\nQuestion: What is the capital city of France?",
    "Answer the question briefly in one short sentence.\\nQuestion: Which treaty ended the War of the Triple Alliance in 1870?",
]:
    print("=" * 80)
    print(q)
    print(json.dumps(ctrl.respond(q), indent=2))"""),

    md("## 12. Package and download all experimental outputs"),
    code("""!zip -q -r trueguard_v2_results.zip "results/v2/$TAG"
from google.colab import files
files.download("trueguard_v2_results.zip")"""),
]


def main():
    nb = {
        "cells": CELLS,
        "metadata": {
            "accelerator": "GPU",
            "colab": {"provenance": [], "gpuType": "T4"},
            "kernelspec": {"name": "python3", "display_name": "Python 3"},
        },
        "nbformat": 4,
        "nbformat_minor": 0,
    }
    out = os.path.join(ROOT, "notebooks", "TRUEGUARD_Colab_REAL.ipynb")
    json.dump(nb, open(out, "w", encoding="utf8"), indent=1)
    print("wrote", out)


if __name__ == "__main__":
    main()
