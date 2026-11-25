"""
General helper functions for seeding, logging, and checkpointing.
"""

import os
import random
import numpy as np
import joblib


def set_seed(seed: int = 42) -> None:
    """Thiết lập seed cho môi trường tái lập kết quả."""
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


def save_checkpoint(data: dict, filepath: str) -> None:
    """Lưu dữ liệu checkpoint sang file .pkl."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(data, filepath)
    print(f"Checkpoint saved: {filepath}")


def load_checkpoint(filepath: str) -> dict:
    """Tải dữ liệu checkpoint từ file .pkl."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Checkpoint not found: {filepath}")
    return joblib.load(filepath)
