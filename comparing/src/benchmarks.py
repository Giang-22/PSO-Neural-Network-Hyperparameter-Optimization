"""
Benchmark Objective Functions for PSO Evaluation and Comparison
"""

import numpy as np
from typing import Callable, Tuple, Dict, Any


def sphere(x: np.ndarray) -> np.ndarray:
    """
    Sphere Function (Unimodal).
    f(x) = sum(x_i^2)
    Global minimum: f(0, ..., 0) = 0
    Bounds: [-5.12, 5.12]
    """
    x = np.atleast_2d(x)
    return np.sum(x**2, axis=-1)


def rastrigin(x: np.ndarray) -> np.ndarray:
    """
    Rastrigin Function (Highly Multimodal with numerous local minima).
    f(x) = 10 * d + sum(x_i^2 - 10 * cos(2 * pi * x_i))
    Global minimum: f(0, ..., 0) = 0
    Bounds: [-5.12, 5.12]
    """
    x = np.atleast_2d(x)
    d = x.shape[-1]
    return 10.0 * d + np.sum(x**2 - 10.0 * np.cos(2.0 * np.pi * x), axis=-1)


def rosenbrock(x: np.ndarray) -> np.ndarray:
    """
    Rosenbrock Function (Narrow, curved banana valley).
    f(x) = sum(100 * (x_{i+1} - x_i^2)^2 + (x_i - 1)^2)
    Global minimum: f(1, ..., 1) = 0
    Bounds: [-5.0, 10.0]
    """
    x = np.atleast_2d(x)
    return np.sum(100.0 * (x[:, 1:] - x[:, :-1]**2)**2 + (x[:, :-1] - 1.0)**2, axis=-1)


BENCHMARK_SUITE: Dict[str, Dict[str, Any]] = {
    'Sphere': {
        'func': sphere,
        'bounds': (-5.12, 5.12),
        'optimum': 0.0,
        'type': 'Unimodal (Kiểm tra tốc độ khai thác - Exploitation)',
        'description': 'Mặt nón lồi hoàn hảo, đánh giá khả năng hội tụ nhanh về cực tiểu toàn cục.'
    },
    'Rastrigin': {
        'func': rastrigin,
        'bounds': (-5.12, 5.12),
        'optimum': 0.0,
        'type': 'Multimodal (Kiểm tra khả năng thoát cực tiểu địa phương - Exploration)',
        'description': 'Bề mặt lồi lõm với vô số bẫy cực tiểu địa phương, kiểm tra nguy cơ premature convergence.'
    },
    'Rosenbrock': {
        'func': rosenbrock,
        'bounds': (-5.0, 10.0),
        'optimum': 0.0,
        'type': 'Valley (Kiểm tra điều hướng trong thung lũng dốc cong)',
        'description': 'Đáy thung lũng cong hẹp, kiểm tra khả năng bám theo độ cong phức tạp.'
    }
}
