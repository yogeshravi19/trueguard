"""
Step 2 of the evaluation pipeline: run every detection experiment on the cached features produced by
`extract_features.py`, write `results/v2/<model_tag>/detection_report.json` and `summary.md`, and render all figures.

Covers:
  * In-distribution 5-fold GROUPED CV (no question-level leakage, no probe-to-fusion leakage):
      AUROC + 95% bootstrap CI, AUPRC, Accuracy, Precision, Recall, F1, confusion matrix, ECE.
  * Individual sensor evaluation (trained ISP, AAS, EEM, DST) + raw untrained baselines
    (token entropy mean/max, mean NLL, answer length).
  * Leave-one-sensor-out and single-sensor ablations + paired bootstrap test for
    H1: AUROC(4-sensor fusion) > AUROC(best single sensor).
  * Sensor complementarity (unique hallucinations caught at 10% FPR, union recall) + correlation matrix.
  * Cross-dataset generalisation matrix (train on dataset A, test on dataset B with zero refitting;
    thresholds calibrated on A only).
  * Automatic diagnostics when AUROC is weak or a sensor is inverted / unhelpful.
"""
import argparse, json, os, sys
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
from src.tg_pipeline import TrueGuardDetector, SENSORS, FEATURE_NAMES
from src.tg_eval import (auc_safe, bootstrap_auc, bootstrap_delta, calibrate_thresholds, class_metrics, ece,
                         raw_baselines, grouped_cv, pooled_metrics, complementarity,
                         plot_roc, plot_bars, plot_heatmap, plot_confusion, plot_risk_hist)


def _load(cache_dir, name):
    d = np.load(os.path.join(cache_dir, f"{name}.npz"))
    F, H, y, g = d["F"].astype(np.float64), d["H"].astype(np.float32), d["y"].astype(int), d["groups"].astype(int)
    # keep only complete pairs (both answers present)
    ug, cnt = np.unique(g, return_counts=True)
    keep = np.isin(g, ug[cnt == 2])
    return F[keep], H[keep], y[keep], g[keep]


def evaluate_all(cache_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    fig_dir = os.path.join(out_dir, "figures"); os.makedirs(fig_dir, exist_ok=True)
    names = sorted(f[:-4] for f in os.listdir(cache_dir) if f.endswith(".npz"))
    data = {n: _load(cache_dir, n) for n in names}

    report = dict(datasets={}, cross_dataset={}, notes=[
        "All numbers computed from REAL model activations cached in " + cache_dir,
        "Grouped 5-fold CV keeps both answers of each question in the same fold.",
        "ISP probes and fusion weights are fit inside each fold (inner OOF stacking prevents probe leakage).",
    ])

    for name, (F, H, y, g) in data.items():
        print(f"=== {name}  (rows={len(y)}, questions={len(np.unique(g))}) ===", flush=True)
        full = grouped_cv(F, H, y, g, use=SENSORS)
        oof = full["oof"]
        auc_ci = bootstrap_auc(y, oof, g)
        pm = pooled_metrics(y, oof, full["fold_thr"])
        pm.update(auroc_fold_mean=float(np.mean(full["fold_auc"])), auroc_fold_std=float(np.std(full["fold_auc"])),
                  auroc_ci95=list(auc_ci), ece=ece(y, oof))

        # single sensors (each fitted cleanly inside the same grouped folds)
        single, single_oof = {}, {}
        for s in SENSORS:
            r = grouped_cv(F, H, y, g, use=(s,))
            single_oof[s] = r["oof"]
            single[s] = dict(auroc=auc_safe(y, r["oof"]), auroc_ci95=list(bootstrap_auc(y, r["oof"], g)),
                             fold_mean=float(np.mean(r["fold_auc"])), fold_std=float(np.std(r["fold_auc"])))

        # leave-one-sensor-out ablation
        loso = {}
        for s in SENSORS:
            sub = tuple(x for x in SENSORS if x != s)
            r = grouped_cv(F, H, y, g, use=sub)
            d_mean, d_lo, d_hi, p = bootstrap_delta(y, oof, r["oof"], g)
            loso[f"without_{s}"] = dict(auroc=auc_safe(y, r["oof"]), delta_vs_full= -d_mean,
                                        full_minus_ablated_ci95=[d_lo, d_hi], p_sensor_not_helping=p)

        best_s = max(single, key=lambda k: single[k]["auroc"])
        d_mean, d_lo, d_hi, p_val = bootstrap_delta(y, oof, single_oof[best_s], g)

        # complementarity & correlations on out-of-fold sensor scores
        comp = complementarity(y, full["sensor_oof"])
        S_mat = np.column_stack([full["sensor_oof"][s] for s in SENSORS])
        corr = {SENSORS[i]: {SENSORS[j]: float(np.corrcoef(S_mat[:, i], S_mat[:, j])[0, 1])
                             for j in range(len(SENSORS))} for i in range(len(SENSORS))}

        raw = raw_baselines(F, y)
        # diagnostics
        diag = []
        for k, v in raw.items():
            if v["auroc"] < 0.48:
                diag.append(f"{k}: raw AUROC={v['auroc']:.3f} (<0.5) -> signal points the OPPOSITE way on {name} "
                            f"(inverted AUROC={v['auroc_if_inverted']:.3f}); logistic fusion flips its sign automatically.")
        if d_mean <= 0:
            diag.append(f"Fusion did NOT beat best single sensor ({best_s}={single[best_s]['auroc']:.3f} vs "
                        f"fusion={pm['auroc']:.3f}); non-ISP sensors add noise on this dataset.")
        elif p_val > 0.05:
            diag.append(f"Fusion gain over {best_s} is +{d_mean:.3f} but 95% CI [{d_lo:.3f}, {d_hi:.3f}] crosses 0 (p={p_val:.2f}).")

        report["datasets"][name] = dict(
            n_rows=int(len(y)), n_questions=int(len(np.unique(g))),
            fusion=pm, single_sensor_trained=single, ablation_leave_one_out=loso,
            fusion_vs_best_single=dict(best_single=best_s, gain=d_mean, gain_ci95=[d_lo, d_hi], p_value=p_val),
            raw_untrained_baselines=raw, complementarity_at_10pct_fpr=comp, sensor_correlation=corr,
            diagnostics=diag,
        )

        # plots
        idx = {n: i for i, n in enumerate(FEATURE_NAMES)}
        curves = {"TRUEGUARD (4-sensor)": oof, **{f"{s} only": single_oof[s] for s in SENSORS},
                  "Baseline: NLL": F[:, idx["NLL_mean"]], "Baseline: Entropy": F[:, idx["ENT_mean"]]}
        plot_roc(y, curves, os.path.join(fig_dir, f"roc_{name}.png"), f"ROC – {name}")
        cm = np.array([[pm["tn"], pm["fp"]], [pm["fn"], pm["tp"]]])
        plot_confusion(cm, os.path.join(fig_dir, f"cm_{name}.png"), f"Confusion – {name}")
        tw, tf = calibrate_thresholds(y, oof)
        plot_risk_hist(y, oof, tw, tf, os.path.join(fig_dir, f"risk_{name}.png"), f"Out-of-fold risk – {name}")
        labels = ["Full (4)"] + [f"-{s}" for s in SENSORS] + [f"{s} only" for s in SENSORS]
        vals = [pm["auroc"]] + [loso[f"without_{s}"]["auroc"] for s in SENSORS] + [single[s]["auroc"] for s in SENSORS]
        plot_bars(labels, vals, [0] * len(vals), os.path.join(fig_dir, f"ablation_{name}.png"), f"Ablation – {name}")

    # ---- cross-dataset transfer (train on A, evaluate on B; thresholds calibrated on A only)
    mat = np.full((len(names), len(names)), np.nan)
    for i, tr_name in enumerate(names):
        Ftr, Htr, ytr, gtr = data[tr_name]
        det = TrueGuardDetector().fit(Ftr, Htr, ytr, gtr)
        tw, tf = calibrate_thresholds(ytr, det.train_risk_)
        report["cross_dataset"][tr_name] = dict(tau_warning=tw, tau_fault=tf, transfers={})
        for j, te_name in enumerate(names):
            if i == j:
                mat[i, j] = report["datasets"][tr_name]["fusion"]["auroc"]
                continue
            Fte, Hte, yte, gte = data[te_name]
            r = det.predict_proba(Fte, Hte)
            m = class_metrics(yte, r, tw)
            m["auroc_ci95"] = list(bootstrap_auc(yte, r, gte))
            # compare with ISP-only transfer and best raw baseline on B
            det_isp = TrueGuardDetector(use=("ISP",)).fit(Ftr, Htr, ytr, gtr)
            m["isp_only_transfer_auroc"] = auc_safe(yte, det_isp.predict_proba(Fte, Hte))
            m["unsupervised_sensors_transfer_auroc"] = auc_safe(
                yte, TrueGuardDetector(use=("AAS", "EEM", "DST")).fit(Ftr, Htr, ytr, gtr).predict_proba(Fte, Hte))
            report["cross_dataset"][tr_name]["transfers"][te_name] = m
            mat[i, j] = m["auroc"]
    if len(names) > 1:
        plot_heatmap(mat, names, names, os.path.join(fig_dir, "cross_dataset_matrix.png"),
                     "Cross-dataset AUROC (diagonal = 5-fold CV)")

    json.dump(report, open(os.path.join(out_dir, "detection_report.json"), "w"), indent=2)
    _write_markdown(report, os.path.join(out_dir, "summary.md"))
    print("wrote", os.path.join(out_dir, "detection_report.json"))
    return report


def _write_markdown(rep, path):
    lines = ["# TRUEGUARD v2 – Experimental Detection Report (real model activations)\n"]
    lines.append("## 1. In-distribution 5-fold grouped CV\n")
    lines.append("| Dataset | N (pairs) | Fusion AUROC [95% CI] | ISP | AAS | EEM | DST | Best raw baseline | Gain vs best single (p) | F1 | ECE |")
    lines.append("|---|---:|---|---|---|---|---|---|---|---|---|")
    for d, r in rep["datasets"].items():
        f = r["fusion"]; s = r["single_sensor_trained"]; g = r["fusion_vs_best_single"]
        best_raw = max(r["raw_untrained_baselines"].items(), key=lambda kv: kv[1]["auroc"])
        lines.append(f"| {d} | {r['n_questions']} | **{f['auroc']:.3f}** [{f['auroc_ci95'][0]:.3f},{f['auroc_ci95'][1]:.3f}] "
                     f"| {s['ISP']['auroc']:.3f} | {s['AAS']['auroc']:.3f} | {s['EEM']['auroc']:.3f} | {s['DST']['auroc']:.3f} "
                     f"| {best_raw[0]}={best_raw[1]['auroc']:.3f} | {g['gain']:+.3f} (p={g['p_value']:.2f}) | {f['f1']:.3f} | {f['ece']:.3f} |")
    lines.append("\n## 2. Cross-dataset generalisation (train row → test column)\n")
    for tr, d in rep["cross_dataset"].items():
        for te, m in d["transfers"].items():
            lines.append(f"- **{tr} → {te}**: fusion AUROC = **{m['auroc']:.3f}** "
                         f"(ISP-only={m['isp_only_transfer_auroc']:.3f}, "
                         f"AAS+EEM+DST={m['unsupervised_sensors_transfer_auroc']:.3f}, F1@τ_warn={m['f1']:.3f})")
    lines.append("\n## 3. Automatic diagnostics\n")
    for d, r in rep["datasets"].items():
        for msg in r["diagnostics"] or ["No issues flagged."]:
            lines.append(f"- **{d}**: {msg}")
    open(path, "w", encoding="utf8").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", required=True, help="e.g. results/cache/TinyLlama__TinyLlama-1.1B-Chat-v1.0")
    ap.add_argument("--out", required=True, help="e.g. results/v2/TinyLlama__TinyLlama-1.1B-Chat-v1.0")
    a = ap.parse_args()
    evaluate_all(a.cache, a.out)

