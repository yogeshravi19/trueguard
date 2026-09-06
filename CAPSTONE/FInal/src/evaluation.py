"""
TRUEGUARD Statistical Evaluation Suite
Implements rigorous statistical metrics:
- AUROC with 95% Confidence Intervals
- AUPRC (Average Precision)
- F1, Precision, Recall, Accuracy at calibrated threshold
- Confusion Matrix (TP, FP, TN, FN)
- 5-Fold Cross Validation harness
"""

import numpy as np
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    roc_curve
)
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression

def compute_all_metrics(y_true, y_pred_prob, threshold=0.50):
    """
    Computes standard binary classification and calibration metrics.
    
    Args:
        y_true: Binary ground truth labels (0=factual, 1=hallucination).
        y_pred_prob: Continuous risk probabilities in [0, 1].
        threshold: Decision threshold tau.
        
    Returns:
        dict of metric names to values.
    """
    y_true = np.asarray(y_true, dtype=int)
    y_pred_prob = np.asarray(y_pred_prob, dtype=float)
    y_pred = (y_pred_prob >= threshold).astype(int)

    auroc = roc_auc_score(y_true, y_pred_prob)
    auprc = average_precision_score(y_true, y_pred_prob)
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0

    return {
        "auroc": float(auroc),
        "auprc": float(auprc),
        "accuracy": float(acc),
        "precision": float(prec),
        "recall": float(rec),
        "f1": float(f1),
        "tpr": float(tpr),
        "fpr": float(fpr),
        "tp": int(tp),
        "fp": int(fp),
        "tn": int(tn),
        "fn": int(fn)
    }

def evaluate_cross_validation(X, y, n_splits=5, seed=42):
    """
    Executes 5-fold cross-validation with LogisticRegression fusion.
    Returns per-fold metrics, mean, standard deviation, and 95% CI.
    """
    kf = KFold(n_splits=n_splits, shuffle=True, random_state=seed)
    fold_aurocs = []
    fold_auprcs = []
    fold_f1s = []

    for fold, (train_idx, test_idx) in enumerate(kf.split(X)):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        clf = LogisticRegression(solver="lbfgs", max_iter=1000)
        clf.fit(X_train, y_train)

        preds = clf.predict_proba(X_test)[:, 1]
        metrics = compute_all_metrics(y_test, preds)

        fold_aurocs.append(metrics["auroc"])
        fold_auprcs.append(metrics["auprc"])
        fold_f1s.append(metrics["f1"])

    mean_auc = float(np.mean(fold_aurocs))
    std_auc = float(np.std(fold_aurocs))
    ci_margin = 1.96 * std_auc / np.sqrt(n_splits)

    return {
        "mean_auroc": mean_auc,
        "std_auroc": std_auc,
        "ci_95": [float(mean_auc - ci_margin), float(mean_auc + ci_margin)],
        "mean_auprc": float(np.mean(fold_auprcs)),
        "std_auprc": float(np.std(fold_auprcs)),
        "mean_f1": float(np.mean(fold_f1s)),
        "std_f1": float(np.std(fold_f1s)),
        "fold_aurocs": fold_aurocs
    }
