"""
TRUEGUARD: A Lightweight Real-Time Framework for Hallucination Detection & Mitigation
Package Initialization (exposes both legacy v1 classes and the v2 paper-faithful pipeline).
"""

import os
os.environ.setdefault("USE_TF", "0")
os.environ.setdefault("USE_TORCH", "1")
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")

from .signal_extractors import (
    extract_isp,
    extract_aas,
    extract_eem,
    extract_dst,
    extract_all_signals,
)
from .normalization import OnlineZScoreScaler
from .fusion import TrueGuardFusion
from .explainability import TokenTrustVisualizer
from .evaluation import compute_all_metrics, evaluate_cross_validation

# v2 paper-faithful implementation
from .tg_pipeline import (
    SENSORS,
    FEATURE_NAMES,
    load_model,
    build_prompt,
    score_answer,
    OnlineSignalMonitor,
    generate_answer,
    TrueGuardDetector,
)
from .tg_controller import ThreeTierController, WikipediaRetriever, ABSTAIN_TEXT
from .tg_eval import calibrate_thresholds, grouped_cv

__all__ = [
    "extract_isp",
    "extract_aas",
    "extract_eem",
    "extract_dst",
    "extract_all_signals",
    "OnlineZScoreScaler",
    "TrueGuardFusion",
    "TokenTrustVisualizer",
    "compute_all_metrics",
    "evaluate_cross_validation",
    "SENSORS",
    "FEATURE_NAMES",
    "load_model",
    "build_prompt",
    "score_answer",
    "OnlineSignalMonitor",
    "generate_answer",
    "TrueGuardDetector",
    "ThreeTierController",
    "WikipediaRetriever",
    "ABSTAIN_TEXT",
    "calibrate_thresholds",
    "grouped_cv",
]
