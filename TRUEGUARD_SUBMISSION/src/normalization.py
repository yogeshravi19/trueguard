"""
TRUEGUARD Feature Normalization
Provides both Online Welford Z-Score scaler and Offline Scikit-Learn standardizer.
"""

import numpy as np

class OnlineZScoreScaler:
    """
    Online Welford-algorithm Z-score scaler for streaming token-by-token inference.
    Maintains running mean and variance without buffering full sequences.
    """
    def __init__(self, num_features=4, eps=1e-6):
        self.num_features = num_features
        self.eps = eps
        self.count = 0
        self.mean = np.zeros(num_features, dtype=np.float64)
        self.M2 = np.zeros(num_features, dtype=np.float64)
        
        # Pre-calibrated baseline priors (from empirical runs on TruthfulQA/HaluEval)
        self.prior_mean = np.array([0.45, 0.40, 0.38, 0.25], dtype=np.float64)
        self.prior_std = np.array([0.22, 0.20, 0.21, 0.18], dtype=np.float64)

    def update(self, x):
        """Update running statistics with new sample x (shape: (num_features,) or (1, num_features))."""
        x_flat = np.asarray(x).ravel()
        self.count += 1
        delta = x_flat - self.mean
        self.mean += delta / self.count
        delta2 = x_flat - self.mean
        self.M2 += delta * delta2

    def transform(self, x):
        """Normalize sample x using running statistics or prior fallback."""
        x_arr = np.asarray(x, dtype=np.float64)
        if self.count < 5:
            # Use empirical prior if insufficient tokens observed yet
            std = self.prior_std
            mean = self.prior_mean
        else:
            variance = self.M2 / (self.count - 1)
            std = np.sqrt(variance) + self.eps
            mean = self.mean
            
        return (x_arr - mean) / std

    def fit_transform(self, X):
        """Fit on 2D matrix X and return standardized version."""
        for row in X:
            self.update(row)
        return self.transform(X)

    def reset(self):
        """Reset online statistics for a new generation sequence."""
        self.count = 0
        self.mean.fill(0.0)
        self.M2.fill(0.0)
