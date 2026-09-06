"""
TRUEGUARD: A Lightweight Real-Time Framework for Hallucination Detection & Mitigation
Package Initialization
"""

import os
os.environ["USE_TF"] = "0"
os.environ["USE_TORCH"] = "1"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from .signal_extractors import (
    extract_isp,
    extract_aas,
    extract_eem,
    extract_dst,
    extract_all_signals
)
from .normalization import OnlineZScoreScaler
from .fusion import TrueGuardFusion
from .detector import TrueGuardDetector
from .mitigation import TrueGuardMitigationPipeline
from .explainability import TokenTrustVisualizer
from .evaluation import compute_all_metrics, evaluate_cross_validation

__all__ = [
    "extract_isp",
    "extract_aas",
    "extract_eem",
    "extract_dst",
    "extract_all_signals",
    "OnlineZScoreScaler",
    "TrueGuardFusion",
    "TrueGuardDetector",
    "TrueGuardMitigationPipeline",
    "TokenTrustVisualizer",
    "compute_all_metrics",
    "evaluate_cross_validation",
]
