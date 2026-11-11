"""
TRUEGUARD REAL benchmark (no simulated signals).

Pipeline per question:
  1. Greedy-generate a short answer with a real causal LM.
  2. At every generated token, extract the 4 real signals (ISP, AAS, EEM, DST)
     from the model's own hidden states / attentions / logits (src.signal_extractors).
  3. Aggregate token signals into a sequence feature vector (mean + max).
  4. Label the answer (1 = hallucinated, 0 = correct) against dataset ground truth.
  5. Train/test the logistic-regression fusion on real features (5-fold CV),
     plus single-signal baselines. Time the guard overhead on real generation.

Datasets (downloaded via HuggingFace `datasets`):
  - trivia_qa (rc.nocontext): label = gold alias appears in generated answer.
  - truthful_qa (generation): label = answer is closer to an incorrect than a correct reference
    (token-F1 heuristic -- documented limitation).

Usage:
  python experiments/real_benchmark.py --model gpt2 --dataset trivia_qa --n 200
  python experiments/real_benchmark.py --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 --n 300
"""
import os
os.environ["USE_TF"] = "0"
import sys, re, json, time, argparse, string
import numpy as np
import torch

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

from src.model_loader import load_trueguard_model
from src.signal_extractors import extract_eem, extract_aas, extract_dst, extract_isp
from src.evaluation import compute_all_metrics
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

SIGNALS = ["ISP", "AAS", "EEM", "DST"]
PROBE_FRACS = [0.45, 0.60, 0.75, 0.90]  # layer depths for the trained ISP probes


def norm(s):
    s = s.lower()
    s = "".join(c for c in s if c not in string.punctuation)
    return " ".join(s.split())


def f1_overlap(a, b):
    a, b = norm(a).split(), norm(b).split()
    if not a or not b:
        return 0.0
    common = {}
    for w in a:
        if w in b:
            common[w] = min(a.count(w), b.count(w))
    n = sum(common.values())
    if n == 0:
        return 0.0
    p, r = n / len(a), n / len(b)
    return 2 * p * r / (p + r)


def load_data(name, n, seed=42):
    from datasets import load_dataset
    rng = np.random.RandomState(seed)
    items = []
    if name == "trivia_qa":
        ds = load_dataset("trivia_qa", "rc.nocontext", split="validation")
        idx = rng.permutation(len(ds))[: n * 2]
        for i in idx:
            r = ds[int(i)]
            items.append({"q": r["question"], "gold": r["answer"]["normalized_aliases"], "kind": "trivia"})
            if len(items) >= n:
                break
    elif name == "truthful_qa":
        ds = load_dataset("truthful_qa", "generation", split="validation")
        idx = rng.permutation(len(ds))[:n]
        for i in idx:
            r = ds[int(i)]
            items.append({"q": r["question"], "correct": r["correct_answers"],
                          "incorrect": r["incorrect_answers"], "kind": "truthful"})
    elif name == "halueval_qa":
        ds = load_dataset("pminervini/HaluEval", "qa", split="data")
        idx = rng.permutation(len(ds))[:n]
        for i in idx:
            r = ds[int(i)]
            items.append({"q": r["question"], "correct": [r["right_answer"]],
                          "incorrect": [r["hallucinated_answer"]], "kind": "truthful"})
    else:
        raise ValueError(name)
    return items


def label_answer(item, ans):
    a = norm(ans)
    if item["kind"] == "trivia":
        ok = any(g and re.search(r"\b" + re.escape(g) + r"\b", a) for g in item["gold"])
        return 0 if ok else 1
    best_c = max(f1_overlap(ans, c) for c in item["correct"])
    best_i = max(f1_overlap(ans, c) for c in item["incorrect"])
    return 0 if best_c >= best_i else 1


def build_prompt(tok, q, chat):
    if chat and getattr(tok, "chat_template", None):
        msgs = [{"role": "user", "content": f"Answer briefly in one short sentence.\nQuestion: {q}"}]
        return tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True)
    return f"Question: {q}\nAnswer:"


@torch.no_grad()
def run_one(model, tok, device, prompt, max_new, timing):
    """Greedy decode with a KV-cache-free loop so every step exposes real hidden/attn/logits."""
    ids = tok(prompt, return_tensors="pt").input_ids.to(device)
    gen_ids, feats, hs = [], [], []
    prev_h = None
    t_guard = 0.0
    t_total0 = time.perf_counter()
    for _ in range(max_new):
        out = model(ids, output_hidden_states=True, output_attentions=True)
        logits = out.logits[:, -1:, :]
        t0 = time.perf_counter()
        f = [
            float(extract_isp(out.hidden_states)[0]),
            float(extract_aas(out.attentions)[0]),
            float(extract_eem(logits)[0]),
        ]
        d, prev_h = extract_dst(out.hidden_states, prev_h_avg=prev_h)
        f.append(float(d[0]))
        nl = len(out.hidden_states)
        pl = [int(nl * fr) for fr in PROBE_FRACS]
        hs.append(np.stack([out.hidden_states[l][0, -1, :].float().cpu().numpy() for l in pl]))
        t_guard += time.perf_counter() - t0
        nxt = torch.argmax(logits[:, -1, :], dim=-1, keepdim=True)
        if nxt.item() == tok.eos_token_id:
            break
        gen_ids.append(nxt.item())
        feats.append(f)
        ids = torch.cat([ids, nxt], dim=1)
    total = time.perf_counter() - t_total0
    text = tok.decode(gen_ids, skip_special_tokens=True).strip().split("\n")[0]
    feats = np.array(feats) if feats else np.zeros((1, 4))
    timing.append((t_guard, total, max(len(gen_ids), 1)))
    H = np.mean(hs, axis=0) if hs else None  # (n_probe_layers, hidden), mean over generated tokens
    return text, feats, H


def aggregate(f):
    # first token excluded for DST (undefined) handled by mean over rest
    return np.concatenate([f.mean(0), f.max(0)])  # 8 dims: mean(4)+max(4)


def cv_auroc(X, y, cols, seed=42):
    skf = StratifiedKFold(5, shuffle=True, random_state=seed)
    aucs, probs = [], np.zeros(len(y))
    for tr, te in skf.split(X, y):
        clf = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
        clf.fit(X[tr][:, cols], y[tr])
        p = clf.predict_proba(X[te][:, cols])[:, 1]
        probs[te] = p
        aucs.append(roc_auc_score(y[te], p))
    return float(np.mean(aucs)), float(np.std(aucs)), probs


def _lr(C=1.0):
    return make_pipeline(StandardScaler(), LogisticRegression(C=C, max_iter=2000))


def cv_fusion(X, H, y, use, seed=42, probe_C=0.01):
    """5-fold CV of the full TRUEGUARD fusion with a REAL trained ISP probe.
    use: subset of {"ISP","AAS","EEM","DST"}. Leakage-free: in each outer fold the ISP probe is fit
    on the training fold only; the fusion's training inputs for ISP are inner out-of-fold probe scores."""
    from sklearn.model_selection import cross_val_predict
    col = {"AAS": [1, 5], "EEM": [2, 6], "DST": [3, 7]}  # cols of X (mean, max); ISP col is the proxy, unused
    other = [c for s in ("AAS", "EEM", "DST") if s in use for c in col[s]]
    Hf = H.reshape(len(H), -1)
    skf = StratifiedKFold(5, shuffle=True, random_state=seed)
    aucs, oof = [], np.zeros(len(y))
    for tr, te in skf.split(X, y):
        parts_tr, parts_te = [], []
        if "ISP" in use:
            probe = _lr(probe_C)
            inner = cross_val_predict(probe, Hf[tr], y[tr], cv=5, method="predict_proba")[:, 1]
            probe.fit(Hf[tr], y[tr])
            parts_tr.append(inner[:, None]); parts_te.append(probe.predict_proba(Hf[te])[:, 1][:, None])
        if other:
            parts_tr.append(X[tr][:, other]); parts_te.append(X[te][:, other])
        Xtr, Xte = np.hstack(parts_tr), np.hstack(parts_te)
        clf = _lr(1.0).fit(Xtr, y[tr])
        p = clf.predict_proba(Xte)[:, 1]
        oof[te] = p
        aucs.append(roc_auc_score(y[te], p))
    return float(np.mean(aucs)), float(np.std(aucs)), oof


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gpt2")
    ap.add_argument("--dataset", default="trivia_qa", choices=["trivia_qa", "truthful_qa", "halueval_qa"])
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--max_new", type=int, default=24)
    ap.add_argument("--chat", action="store_true")
    ap.add_argument("--out", default=os.path.join(ROOT, "results", "real_benchmark_results.json"))
    args = ap.parse_args()

    torch.manual_seed(42)
    model, tok, device = load_trueguard_model(args.model, device="auto", torch_dtype=torch.float32)
    # eager attention needed for output_attentions
    items = load_data(args.dataset, args.n)

    X, Hs, y, rows, timing = [], [], [], [], []
    for i, it in enumerate(items):
        text, f, H = run_one(model, tok, device, build_prompt(tok, it["q"], args.chat), args.max_new, timing)
        if H is None:  # empty generation -> no hidden states, skip sample
            continue
        lab = label_answer(it, text)
        X.append(aggregate(f)); Hs.append(H); y.append(lab)
        rows.append({"q": it["q"], "answer": text, "label_hallucinated": lab})
        if (i + 1) % 10 == 0:
            print(f"[{i+1}/{len(items)}] halluc rate so far {np.mean(y):.2f}", flush=True)
    X, y = np.array(X), np.array(y)
    Hs = np.array(Hs)  # (n, 4 layers, hidden)
    if min(y.sum(), len(y) - y.sum()) < 10:
        print(f"ABORT: only {int(y.sum())}/{len(y)} answers labelled hallucinated -- one class is too rare "
              "for AUROC. Use a stronger model (e.g. TinyLlama --chat) or more samples.")
        sys.exit(2)

    res = {"model": args.model, "dataset": args.dataset, "n": len(y),
           "hallucination_rate": float(y.mean()), "note": "REAL signals from real LLM generation; "
           "no simulated features."}
    names = [("ISPproxy" if s == "ISP" else s) + "_mean" for s in SIGNALS] + \
            [("ISPproxy" if s == "ISP" else s) + "_max" for s in SIGNALS]
    res["single_signal_auroc_untrained"] = {}
    for j, nme in enumerate(names):
        m, s, _ = cv_auroc(X, y, [j])
        res["single_signal_auroc_untrained"][nme] = {"mean": m, "std": s}
    # Trained ISP probe + fusion (the real TRUEGUARD model)
    full = ("ISP", "AAS", "EEM", "DST")
    res["single_signal_auroc_trained_probe"] = {}
    for s in full:
        m, sd, _ = cv_fusion(X, Hs, y, (s,))
        res["single_signal_auroc_trained_probe"][s] = {"mean": m, "std": sd}
    m, s, probs = cv_fusion(X, Hs, y, full)
    res["fusion_auroc_5fold"] = {"mean": m, "std": s}
    res["fusion_metrics_at_0.5_oof"] = compute_all_metrics(y, probs)
    res["ablation"] = {}
    for k in full:
        am, asd, _ = cv_fusion(X, Hs, y, tuple(x for x in full if x != k))
        res["ablation"][f"without_{k}"] = {"mean": am, "std": asd, "delta": am - m}
    best_single = max(v["mean"] for v in res["single_signal_auroc_trained_probe"].values())
    res["fusion_gain_over_best_single"] = m - best_single
    gt = np.array([t[0] for t in timing]); tt = np.array([t[1] for t in timing]); nt = np.array([t[2] for t in timing])
    res["latency"] = {"guard_ms_per_token": float(gt.sum() / nt.sum() * 1000),
                      "total_ms_per_token": float(tt.sum() / nt.sum() * 1000),
                      "guard_share_of_step": float(gt.sum() / tt.sum()),
                      "device": device}
    res["samples"] = rows[:25]
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    json.dump(res, open(args.out, "w"), indent=2)
    print(json.dumps({k: v for k, v in res.items() if k != "samples"}, indent=2))


if __name__ == "__main__":
    main()

