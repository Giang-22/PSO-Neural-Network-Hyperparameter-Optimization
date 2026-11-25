"""
Main entry point for running OPSO Neural Network hyperparameter optimization pipeline.
"""

import os
import sys

# Ensure UTF-8 output encoding for Windows terminal
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.utils.helpers import set_seed
from src.data.loader import load_raw_data
from src.evaluation.benchmark import load_all_results
from src.utils.visualizer import plot_convergence_comparison


def load_config(config_path: str = "configs/default_config.yaml") -> dict:
    """Tải cấu hình từ yaml hoặc trả về cấu hình mặc định."""
    try:
        import yaml
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception:
        # Fallback default configuration dictionary
        return {
            "project": {"name": "OPSO_NeuralNetwork", "seed": 42},
            "data": {"raw_path": "data/raw/bank.csv", "target_column": "y", "test_size": 0.2, "cv_folds": 3},
            "search_space": {"lower_bounds": [16, -4.0, -5.0], "upper_bounds": [256, -1.0, -1.0]},
            "pso": {"n_particles": 20, "max_iter": 30, "w": 0.7298, "c1": 1.49618, "c2": 1.49618, "w_max": 0.9, "w_min": 0.4},
            "results": {"checkpoints_dir": "results/checkpoints", "figures_dir": "results/figures"}
        }


def main():
    print("=" * 60)
    print("[INFO] OPSO Neural Network Hyperparameter Optimization Pipeline")
    print("=" * 60)
    
    # 1. Load config
    config = load_config()
    set_seed(config["project"]["seed"])
    print(f"[CONFIG] Project name: {config['project']['name']}")
    
    # 2. Check existing results
    results = load_all_results(config["results"]["checkpoints_dir"])
    print(f"[RESULTS] Loaded {len(results)} existing checkpoint(s): {list(results.keys())}")
    
    # 3. Generate summary visualization if results exist
    if results:
        fig_path = os.path.join(config["results"]["figures_dir"], "convergence_comparison.png")
        plot_convergence_comparison(results, fig_path)
    
    print("\n[SUCCESS] Pipeline skeleton executed successfully.")
    print("Ready to run and migrate individual optimizer modules!")


if __name__ == "__main__":
    main()
