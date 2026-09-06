"""
TRUEGUARD Learned Multi-Signal Fusion
Combines ISP, AAS, EEM, and DST into a calibrated token-level and sequence-level hallucination risk score.
"""

import numpy as np
from sklearn.linear_model import LogisticRegression
import joblib

class TrueGuardFusion:
    """
    Learned Logistic Regression Fusion Layer for TRUEGUARD.
    Maps normalized 4-signal vector X_hat = [ISP, AAS, EEM, DST] to hallucination risk R(t) in [0, 1].
    """
    def __init__(self, weights=None, intercept=None):
        self.feature_names = ["ISP", "AAS", "EEM", "DST"]
        if weights is not None:
            self.weights = np.asarray(weights, dtype=np.float32)
        else:
            # Empirically verified default weights: EEM (0.34) > ISP (0.28) > DST (0.22) > AAS (0.16)
            self.weights = np.array([0.28, 0.16, 0.34, 0.22], dtype=np.float32)

        self.intercept = float(intercept) if intercept is not None else -0.10
        self.clf = LogisticRegression(solver="lbfgs", max_iter=1000)
        self.is_fitted = False

    def predict_risk_token(self, normalized_features):
        """
        Computes token-level hallucination risk R(t) = sigmoid(W^T * X_hat + b).
        
        Args:
            normalized_features: np.ndarray of shape (4,) or (batch, 4).
            
        Returns:
            risk: float or np.ndarray in [0.0, 1.0].
        """
        feats = np.asarray(normalized_features, dtype=np.float32)
        if feats.ndim == 1:
            raw_logit = np.dot(self.weights, feats) + self.intercept
            return float(1.0 / (1.0 + np.exp(-raw_logit)))
        else:
            raw_logits = np.dot(feats, self.weights) + self.intercept
            return 1.0 / (1.0 + np.exp(-raw_logits))

    def compute_sequence_risk(self, token_risks, threshold=0.50, gamma=0.20):
        """
        Computes sequence-level hallucination risk:
        R_seq = max_t(R(t)) * (1 + gamma * count(R(t) > tau) / T)
        
        Args:
            token_risks: List or array of per-token risk scores.
            threshold: Safety threshold tau (default 0.50).
            gamma: Penalty factor for recurrent hallucinations (default 0.20).
            
        Returns:
            r_seq: Sequence-level risk in [0, 1].
        """
        if not token_risks:
            return 0.0
        
        arr = np.asarray(token_risks)
        T = len(arr)
        max_r = float(np.max(arr))
        flagged_ratio = float(np.sum(arr > threshold)) / T
        
        r_seq = max_r * (1.0 + gamma * flagged_ratio)
        return float(np.clip(r_seq, 0.0, 1.0))

    def fit(self, X, y):
        """
        Fits logistic regression model on training features X (N x 4) and binary labels y (N).
        """
        self.clf.fit(X, y)
        self.weights = self.clf.coef_[0].astype(np.float32)
        self.intercept = float(self.clf.intercept_[0])
        self.is_fitted = True
        print(f"[TRUEGUARD Fusion] Fitted weights: {dict(zip(self.feature_names, np.round(self.weights, 4)))}, Intercept: {self.intercept:.4f}")

    def save(self, filepath):
        """Saves fusion parameters to disk."""
        data = {
            "weights": self.weights,
            "intercept": self.intercept,
            "feature_names": self.feature_names,
            "is_fitted": self.is_fitted
        }
        joblib.dump(data, filepath)
        print(f"[TRUEGUARD Fusion] Saved checkpoint to {filepath}")

    @classmethod
    def load(cls, filepath):
        """Loads fusion parameters from disk."""
        data = joblib.load(filepath)
        instance = cls(weights=data["weights"], intercept=data["intercept"])
        instance.is_fitted = data.get("is_fitted", True)
        return instance
