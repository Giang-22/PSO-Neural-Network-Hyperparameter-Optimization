"""
Evaluation and benchmarking module.
"""

from .metrics import calculate_metrics, compute_confusion_matrix
from .benchmark import load_all_results, compare_all_models

__all__ = [
    "calculate_metrics",
    "compute_confusion_matrix",
    "load_all_results",
    "compare_all_models",
]
