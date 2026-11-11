"""
Step 1 of the evaluation pipeline: extract REAL sensor features + hidden states from an LLM on the real benchmarks
and cache them to `results/cache/<model_tag>/<dataset>.npz`.  Running evaluation / ablations / plots afterwards
needs no GPU and takes seconds.

Usage:
  python experiments/extract_features.py --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 --n 400
  python experiments/extract_features.py --model gpt2 --datasets halueval_qa truthful_qa --n 120
"""
import argparse, os, sys, time
os.environ.setdefault("USE_TF", "0")
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
from src.tg_pipeline import load_model, build_prompt, score_answer
from src.tg_data import load_pairs, PAIR_DATASETS


def model_tag(name):
    return name.replace("/", "__")


def extract_dataset(model, tok, device, ds_name, n, out_dir, seed=42):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{ds_name}.npz")
    pairs = load_pairs(ds_name, n, seed=seed)
    Fs, Hs, ys, gs = [], [], [], []
    t0 = time.perf_counter()
    for i, it in enumerate(pairs):
        prompt, prefix = build_prompt(tok, it["user_text"])
        r = score_answer(model, tok, device, prompt, prefix + it["answer"])
        if r is None:
            continue
        F, H = r
        Fs.append(F); Hs.append(H); ys.append(it["label"]); gs.append(it["group"])
        if (i + 1) % 100 == 0:
            print(f"  [{ds_name}] {i+1}/{len(pairs)}  ({time.perf_counter()-t0:.1f}s)", flush=True)
    np.savez_compressed(path, F=np.array(Fs, np.float32), H=np.array(Hs, np.float16),
                        y=np.array(ys, np.int64), groups=np.array(gs, np.int64))
    print(f"saved {path}  rows={len(ys)}  ({time.perf_counter()-t0:.1f}s)", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    ap.add_argument("--datasets", nargs="+", default=PAIR_DATASETS)
    ap.add_argument("--n", type=int, default=400, help="questions per dataset (2x rows)")
    ap.add_argument("--4bit", dest="fourbit", action="store_true")
    args = ap.parse_args()
    model, tok, device = load_model(args.model, load_in_4bit=args.fourbit)
    out = os.path.join(ROOT, "results", "cache", model_tag(args.model))
    for d in args.datasets:
        extract_dataset(model, tok, device, d, args.n, out)


if __name__ == "__main__":
    main()

