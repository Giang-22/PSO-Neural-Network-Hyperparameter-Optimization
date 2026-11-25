"""
Neural Network model constructor and evaluation utilities.
"""

from typing import Dict, Any
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, classification_report


def build_mlp_classifier(
    n_neurons: int, 
    learning_rate: float, 
    alpha: float, 
    random_seed: int = 42,
    max_iter: int = 200
) -> MLPClassifier:
    """
    Khởi tạo mô hình MLPClassifier từ các siêu tham số đã giải mã.
    """
    return MLPClassifier(
        hidden_layer_sizes=(int(n_neurons),),
        learning_rate_init=float(learning_rate),
        alpha=float(alpha),
        max_iter=max_iter,
        random_state=random_seed,
        early_stopping=True,
        n_iter_no_change=10
    )


def train_and_evaluate_mlp(
    n_neurons: int,
    lr: float,
    alpha: float,
    X_tr: np.ndarray,
    y_tr: np.ndarray,
    X_te: np.ndarray,
    y_te: np.ndarray,
    seed: int = 42,
    label: str = "Model"
) -> Dict[str, Any]:
    """
    Huấn luyện và đánh giá MLPClassifier trên tập Test.
    """
    pass
