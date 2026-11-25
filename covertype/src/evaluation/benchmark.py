"""
Benchmark and comparison across all PSO variants.
"""

import os
from typing import Dict, Any
import joblib
import pandas as pd


def load_all_results(checkpoints_dir: str = "results/checkpoints") -> Dict[str, Dict[str, Any]]:
    """
    Load toàn bộ kết quả tối ưu từ các file .pkl trong thư mục checkpoint.
    """
    if not os.path.exists(checkpoints_dir):
        if os.path.exists("pso_results"):
            checkpoints_dir = "pso_results"
            
    results = {}
    if os.path.exists(checkpoints_dir):
        for fname in os.listdir(checkpoints_dir):
            if fname.endswith(".pkl") and fname != "pso_tuning_results.pkl":
                name = fname.replace(".pkl", "")
                fpath = os.path.join(checkpoints_dir, fname)
                try:
                    results[name] = joblib.load(fpath)
                except Exception as e:
                    print(f"Không thể đọc {fpath}: {e}")
    return results


def compare_all_models(results: Dict[str, Dict[str, Any]], X_train, y_train, X_test, y_test) -> pd.DataFrame:
    """
    Huấn luyện lại mô hình với siêu tham số tốt nhất của từng thuật toán và tạo bảng so sánh.
    """
    pass
