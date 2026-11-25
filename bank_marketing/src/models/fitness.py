"""
Fitness functions and search space position decoding.
"""

from typing import Tuple
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.neural_network import MLPClassifier

# Default 3D search space bounds: [n_neurons, log10(lr), log10(alpha)]
LOW = np.array([16, -4.0, -5.0], dtype=float)
HIGH = np.array([256, -1.0, -1.0], dtype=float)
DIM = 3

# Default 5D search space bounds: [n_neurons, log10(lr), log10(alpha), n_layers, batch_size]
LOW_5D = np.array([16, -4.0, -5.0, 1, 16], dtype=float)
HIGH_5D = np.array([256, -1.0, -1.0, 4, 128], dtype=float)
DIM_5D = 5


def decode_position(x: np.ndarray) -> Tuple[int, float, float]:
    """
    Giải mã vector vị trí hạt x = [n_neurons, log10_lr, log10_alpha]
    thành các siêu tham số thực tế: (n_neurons, lr, alpha).
    """
    n_neurons = int(np.clip(round(x[0]), 16, 256))
    lr = float(10 ** np.clip(x[1], -4.0, -1.0))
    alpha = float(10 ** np.clip(x[2], -5.0, -1.0))
    return n_neurons, lr, alpha


def decode_position_5d(x: np.ndarray) -> Tuple[int, float, float, int, int]:
    """
    Giải mã vector vị trí 5D x = [n_neurons, log10_lr, log10_alpha, n_layers, batch_size]
    thành các siêu tham số thực tế: (n_neurons, lr, alpha, n_layers, batch_size).
    """
    n_neurons = int(np.clip(round(x[0]), 16, 256))
    lr = float(10 ** np.clip(x[1], -4.0, -1.0))
    alpha = float(10 ** np.clip(x[2], -5.0, -1.0))
    n_layers = int(np.clip(round(x[3]), 1, 4))
    batch_size = int(np.clip(round(x[4]), 16, 128))
    return n_neurons, lr, alpha, n_layers, batch_size


def fitness_single(
    x: np.ndarray, 
    X_tr: np.ndarray, 
    y_tr: np.ndarray, 
    cv_obj: StratifiedKFold, 
    seed: int = 42
) -> float:
    """
    Đánh giá fitness (K-Fold CV accuracy) cho 1 vị trí hạt (không gian 3D).
    """
    n_neurons, lr, alpha = decode_position(x)
    model = MLPClassifier(
        hidden_layer_sizes=(n_neurons, n_neurons),
        activation='relu',
        learning_rate_init=lr,
        alpha=alpha,
        max_iter=500,
        random_state=seed,
        early_stopping=True,
        n_iter_no_change=15
    )
    scores = cross_val_score(model, X_tr, y_tr, cv=cv_obj, scoring='accuracy', n_jobs=-1)
    return float(scores.mean())


def fitness_averaged(
    x: np.ndarray, 
    X_tr: np.ndarray, 
    y_tr: np.ndarray, 
    cv_obj: StratifiedKFold, 
    seed: int = 42, 
    k: int = 3
) -> float:
    """
    Đánh giá fitness lấy trung bình qua k lần chạy với các seed khác nhau (Fitness Averaging).
    """
    scores_all = []
    for run in range(k):
        n_neurons, lr, alpha = decode_position(x)
        model = MLPClassifier(
            hidden_layer_sizes=(n_neurons, n_neurons),
            activation='relu',
            learning_rate_init=lr,
            alpha=alpha,
            max_iter=500,
            random_state=seed + run,
            early_stopping=True,
            n_iter_no_change=15
        )
        s = cross_val_score(model, X_tr, y_tr, cv=cv_obj, scoring='accuracy', n_jobs=-1)
        scores_all.append(s.mean())
    return float(np.mean(scores_all))


def fitness_single_5d(
    x: np.ndarray, 
    X_tr: np.ndarray, 
    y_tr: np.ndarray, 
    cv_obj: StratifiedKFold, 
    seed: int = 42
) -> float:
    """
    Đánh giá fitness (K-Fold CV accuracy) cho 1 vị trí hạt (không gian 5D).
    """
    n_neurons, lr, alpha, n_layers, batch_size = decode_position_5d(x)
    hidden_layer_sizes = tuple([n_neurons] * n_layers)
    model = MLPClassifier(
        hidden_layer_sizes=hidden_layer_sizes,
        activation='relu',
        learning_rate_init=lr,
        alpha=alpha,
        batch_size=batch_size,
        max_iter=500,
        random_state=seed,
        early_stopping=True,
        n_iter_no_change=15
    )
    scores = cross_val_score(model, X_tr, y_tr, cv=cv_obj, scoring='accuracy', n_jobs=-1)
    return float(scores.mean())
