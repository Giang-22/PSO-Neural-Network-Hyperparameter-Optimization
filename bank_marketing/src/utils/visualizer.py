"""
Visualization utilities: convergence plots, variant comparisons, metric charts.
"""

import os
from typing import Dict, Any
import matplotlib.pyplot as plt
import numpy as np


def plot_convergence_comparison(
    results: Dict[str, Dict[str, Any]], 
    save_path: str = "results/figures/convergence_comparison.png"
):
    """
    Vẽ biểu đồ so sánh đường cong hội tụ (Fitness qua các thế hệ) giữa các biến thể PSO.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.figure(figsize=(12, 6))
    for name, res in results.items():
        if not isinstance(res, dict):
            continue
        curve = None
        if "convergence" in res:
            curve = res["convergence"]
        elif "convergence_curve" in res:
            curve = res["convergence_curve"]
        elif "history_gbest" in res:
            curve = res["history_gbest"]
        elif "history" in res and not hasattr(res["history"], "columns"):
            curve = res["history"]
            
        if curve is not None:
            plt.plot(curve, label=name)
    plt.xlabel("Iteration")
    plt.ylabel("Best Fitness (CV Accuracy)")
    plt.title("PSO Variants Convergence Comparison")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.close()
    print(f"Saved convergence plot to {save_path}")


def plot_confusion_matrices(*args, **kwargs):
    """Vẽ grid ma trận nhầm lẫn cho tất cả các mô hình."""
    pass
