"""
Evaluation utilities for TRUEGUARD v2: leakage-free grouped CV, cross-dataset transfer, bootstrap CIs,
thresholds, selective-prediction (risk-coverage) analysis, calibration, plots.
All functions operate on features cached by experiments/extract_features.py.
"""
import numpy as np
from sklearn.metrics import (roc_auc_score, roc_curve, confusion_matrix, accuracy_score, precision_score,
                             recall_score, f1_score, average_precision_score)
from sklearn.model_selection import GroupKFold

from .tg_pipeline import TrueGuardDetector, SENSORS, FEATURE_NAMES


# ------------------------------------------------------------------ basic helpers
def auc_safe(y, s):
    y = np.asarray(y)
    return float(roc_auc_score(y, s)) if len(np.unique(y)) == 2 else float("nan")


def bootstrap_auc(y, s, groups, n_boot=500, seed=0):
    """Group-level bootstrap (resamples whole questions) -> (lo, hi) 95% CI."""
    y, s, groups = np.asarray(y), np.asarray(s), np.asarray(groups)
    rng = np.random.RandomState(seed)
    ug = np.unique(groups)
    idx = {g: np.where(groups == g)[0] for g in ug}
    vals = []
    for _ in range(n_boot):
        pick = np.concatenate([idx[g] for g in rng.choice(ug, len(ug))])
        a = auc_safe(y[pick], s[pick])
        if not np.isnan(a):
            vals.append(a)
    return (float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))) if vals else (np.nan, np.nan)


def bootstrap_delta(y, s_a, s_b, groups, n_boot=500, seed=0):
    """Paired group bootstrap of AUROC(a) - AUROC(b).  Returns (mean_delta, lo, hi, p_a_not_better)."""
    y, s_a, s_b, groups = map(np.asarray, (y, s_a, s_b, groups))
    rng = np.random.RandomState(seed)
    ug = np.unique(groups)
    idx = {g: np.where(groups == g)[0] for g in ug}
    d = []
    for _ in range(n_boot):
        pick = np.concatenate([idx[g] for g in rng.choice(ug, len(ug))])
        if len(np.unique(y[pick])) < 2:
            continue
        d.append(roc_auc_score(y[pick], s_a[pick]) - roc_auc_score(y[pick], s_b[pick]))
    d = np.array(d)
    return float(d.mean()), float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5)), float((d <= 0).mean())


def youden_threshold(y, s):
    fpr, tpr, thr = roc_curve(y, s)
    return float(thr[np.argmax(tpr - fpr)])


def fpr_threshold(y, s, max_fpr=0.10):
    """Smallest threshold whose false-positive rate on `y` is <= max_fpr (high-confidence 'fault' operating point)."""
    fpr, tpr, thr = roc_curve(y, s)
    ok = np.where(fpr <= max_fpr)[0]
    return float(thr[ok[-1]]) if len(ok) else float(thr[1])


def calibrate_thresholds(y, risk, fault_max_fpr=0.10):
    """Warning threshold = Youden-optimal point; Fault threshold = high-precision point (FPR <= fault_max_fpr).
    Guaranteed tau_fault >= tau_warning."""
    tw = youden_threshold(y, risk)
    tf = max(fpr_threshold(y, risk, fault_max_fpr), tw)
    return tw, tf


def class_metrics(y, risk, thr):
    y = np.asarray(y).astype(int)
    p = (np.asarray(risk) >= thr).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, p, labels=[0, 1]).ravel()
    return dict(threshold=float(thr), auroc=auc_safe(y, risk), auprc=float(average_precision_score(y, risk)),
                accuracy=float(accuracy_score(y, p)), precision=float(precision_score(y, p, zero_division=0)),
                recall=float(recall_score(y, p, zero_division=0)), f1=float(f1_score(y, p, zero_division=0)),
                tp=int(tp), fp=int(fp), tn=int(tn), fn=int(fn))


def ece(y, p, bins=10):
    y, p = np.asarray(y), np.asarray(p)
    edges = np.linspace(0, 1, bins + 1)
    e = 0.0
    for i in range(bins):
        m = (p >= edges[i]) & (p < edges[i + 1] if i < bins - 1 else p <= edges[i + 1])
        if m.any():
            e += m.mean() * abs(y[m].mean() - p[m].mean())
    return float(e)


# ------------------------------------------------------------------ raw baselines (no training)
def raw_baselines(F, y):
    """AUROC of untrained single signals / classic baselines.  Higher raw value assumed = riskier; the reversed
    AUROC (1-auc) is reported too so an inverted sensor is visible instead of hidden."""
    idx = {n: i for i, n in enumerate(FEATURE_NAMES)}
    out = {}
    for name in ["AAS_mean", "AAS_max", "EEM_mean", "EEM_max", "DST_mean", "DST_max", "ENT_mean", "ENT_max",
                 "NLL_mean", "LEN"]:
        a = auc_safe(y, F[:, idx[name]])
        out[name] = dict(auroc=a, auroc_if_inverted=1 - a)
    return out


# ------------------------------------------------------------------ grouped CV of the full detector
def grouped_cv(F, H, y, groups, use=SENSORS, k=5, seed=42, **det_kw):
    """Leakage-free grouped K-fold.  ISP probes, probe-C selection, fusion and thresholds are all fit on the
    training fold only.  Returns pooled out-of-fold risk, per-fold AUROC and per-fold Youden thresholds."""
    oof = np.zeros(len(y))
    fold_auc, fold_thr, sensor_oof = [], [], {s: np.zeros(len(y)) for s in use}
    gkf = GroupKFold(n_splits=min(k, len(np.unique(groups))))
    for tr, te in gkf.split(F, y, groups):
        det = TrueGuardDetector(use=use, seed=seed, **det_kw).fit(F[tr], H[tr], y[tr], groups[tr])
        oof[te] = det.predict_proba(F[te], H[te])
        fold_auc.append(auc_safe(y[te], oof[te]))
        fold_thr.append(youden_threshold(y[tr], det.train_risk_))
        for s, v in det.sensor_scores(F[te], H[te]).items():
            if s in sensor_oof:
                sensor_oof[s][te] = v
    return dict(oof=oof, fold_auc=fold_auc, fold_thr=fold_thr, sensor_oof=sensor_oof)


def pooled_metrics(y, oof, fold_thr):
    return class_metrics(y, oof, float(np.mean(fold_thr)))


# ------------------------------------------------------------------ complementarity
def complementarity(y, sensor_scores, fpr=0.10):
    """For each sensor: fraction of hallucinated samples it flags at a threshold giving `fpr` on the grounded
    samples.  Reports how many positives are caught by exactly one sensor (unique) and by the union."""
    y = np.asarray(y)
    flags = {}
    for s, v in sensor_scores.items():
        thr = np.percentile(v[y == 0], 100 * (1 - fpr))
        flags[s] = (v > thr)
    pos = y == 1
    M = np.stack([flags[s][pos] for s in flags])
    res = {s: dict(recall_at_fpr=float(flags[s][pos].mean())) for s in flags}
    for i, s in enumerate(flags):
        others = np.delete(M, i, axis=0).any(0) if len(flags) > 1 else np.zeros(M.shape[1], bool)
        res[s]["unique_catches"] = float((M[i] & ~others).mean())
    res["union_recall"] = float(M.any(0).mean())
    res["fpr_level"] = fpr
    return res


# ------------------------------------------------------------------ selective prediction (risk-coverage)
def risk_coverage(correct, score, coverages=(1.0, 0.9, 0.8, 0.7, 0.6, 0.5)):
    """correct: 1 if the answer is right.  score: higher = more likely wrong.  Keep the (coverage) fraction of
    answers with the lowest score; return accuracy on the kept answers."""
    correct, score = np.asarray(correct), np.asarray(score)
    order = np.argsort(score, kind="stable")
    res = {}
    for c in coverages:
        k = max(1, int(round(c * len(order))))
        res[f"{int(c*100)}%"] = float(correct[order[:k]].mean())
    # area under risk-coverage (lower is better)
    cum_err = np.cumsum(1 - correct[order]) / np.arange(1, len(order) + 1)
    res["AURC"] = float(cum_err.mean())
    return res


# ------------------------------------------------------------------ plotting
def plot_roc(y, curves, path, title):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.figure(figsize=(5.5, 5))
    for name, s in curves.items():
        fpr, tpr, _ = roc_curve(y, s)
        plt.plot(fpr, tpr, label=f"{name} ({auc_safe(y, s):.3f})", lw=2 if name.startswith("TRUEGUARD") else 1.2)
    plt.plot([0, 1], [0, 1], "k--", lw=.8)
    plt.xlabel("False positive rate"); plt.ylabel("True positive rate"); plt.title(title)
    plt.legend(fontsize=7, loc="lower right"); plt.tight_layout(); plt.savefig(path, dpi=200); plt.close()


def plot_bars(labels, vals, errs, path, title, ylabel="AUROC", hline=0.5):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.figure(figsize=(7, 4))
    plt.bar(range(len(vals)), vals, yerr=errs, capsize=3, color="#4c78a8")
    plt.axhline(hline, color="k", ls="--", lw=.8)
    plt.xticks(range(len(vals)), labels, rotation=35, ha="right", fontsize=8)
    plt.ylabel(ylabel); plt.title(title); plt.ylim(0.3, 1.0); plt.tight_layout(); plt.savefig(path, dpi=200); plt.close()


def plot_heatmap(mat, rows, cols, path, title):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.figure(figsize=(5.5, 4.5))
    plt.imshow(mat, vmin=0.4, vmax=1.0, cmap="viridis")
    for i in range(len(rows)):
        for j in range(len(cols)):
            if not np.isnan(mat[i, j]):
                plt.text(j, i, f"{mat[i,j]:.2f}", ha="center", va="center", color="w", fontsize=9)
    plt.xticks(range(len(cols)), cols, rotation=30, ha="right"); plt.yticks(range(len(rows)), rows)
    plt.xlabel("test set"); plt.ylabel("train set"); plt.title(title); plt.colorbar(label="AUROC")
    plt.tight_layout(); plt.savefig(path, dpi=200); plt.close()


def plot_confusion(cm, path, title):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.figure(figsize=(3.8, 3.4))
    plt.imshow(cm, cmap="Blues")
    for i in range(2):
        for j in range(2):
            plt.text(j, i, cm[i, j], ha="center", va="center", fontsize=12)
    plt.xticks([0, 1], ["pred grounded", "pred halluc."], fontsize=8); plt.yticks([0, 1], ["grounded", "halluc."], fontsize=8)
    plt.title(title, fontsize=9); plt.tight_layout(); plt.savefig(path, dpi=200); plt.close()


def plot_risk_hist(y, risk, tw, tf, path, title):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.figure(figsize=(5.5, 3.5))
    plt.hist(risk[y == 0], bins=25, alpha=.6, label="grounded", color="#59a14f")
    plt.hist(risk[y == 1], bins=25, alpha=.6, label="hallucinated", color="#e15759")
    if tw is not None:
        plt.axvline(tw, color="orange", ls="--", label=f"warning {tw:.2f}")
        plt.axvline(tf, color="red", ls="--", label=f"fault {tf:.2f}")
    plt.xlabel("TRUEGUARD risk"); plt.legend(fontsize=8); plt.title(title); plt.tight_layout()
    plt.savefig(path, dpi=200); plt.close()

