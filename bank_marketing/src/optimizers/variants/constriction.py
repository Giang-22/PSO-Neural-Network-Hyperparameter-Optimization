"""
Constriction-type PSO (CPSO) with constriction factor chi (χ) / K.
"""

import time
from typing import Tuple, List, Optional, Callable, Any
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from ..base import BasePSO
from ...models.fitness import LOW, HIGH, DIM, decode_position, fitness_single


def compute_constriction_factor(n1: float = 2.05, n2: float = 2.05) -> float:
    """
    Tính Constriction Factor K (chi) — Equation (5) từ Clerc & Kennedy / Meissner et al. 2006.
    Yêu cầu: phi = n1 + n2 > 4.
    """
    phi = n1 + n2
    if phi <= 4.0:
        raise ValueError(f"phi = n1 + n2 = {phi} phải > 4 để hệ số co thắt có nghĩa.")
    chi = 2.0 / np.abs(2.0 - phi - np.sqrt(phi**2 - 4.0 * phi))
    return float(chi)


class ConstrictionPSO(BasePSO):
    """
    Constriction-type PSO (CPSO) sử dụng hệ số co thắt K để kiểm soát vận tốc thay vì Vmax.
    """
    def __init__(
        self,
        fitness_func: Callable[[np.ndarray], float],
        lower_bounds: np.ndarray = LOW,
        upper_bounds: np.ndarray = HIGH,
        n_particles: int = 12,
        max_iter: int = 20,
        n1: float = 2.05,
        n2: float = 2.05,
        random_seed: int = 42
    ):
        super().__init__(fitness_func, lower_bounds, upper_bounds, n_particles, max_iter, random_seed)
        self.n1 = n1
        self.n2 = n2
        self.K = compute_constriction_factor(n1, n2)

    def optimize(self, verbose: bool = True) -> Tuple[np.ndarray, float, List[float], pd.DataFrame, float]:
        self.initialize_swarm()
        detailed_history = []
        t_start = time.time()
        phi = self.n1 + self.n2

        if verbose:
            print(f'🟠 CPSO | n1={self.n1}, n2={self.n2} | φ={phi:.2f} | K={self.K:.4f}')
            print(f'   {self.n_particles} particles × {self.max_iter} iterations')
            print('─' * 60)

        for it in range(self.max_iter):
            for i in range(self.n_particles):
                score = self.fitness_func(self.X[i])
                n, lr, al = decode_position(self.X[i])
                detailed_history.append({
                    'iter': it, 'particle': i, 'score': score,
                    'n_neurons': n, 'lr': lr, 'alpha': al
                })
                if score > self.pbest_val[i]:
                    self.pbest_val[i] = score
                    self.pbest_pos[i] = self.X[i].copy()
                if score > self.gbest_val:
                    self.gbest_val = score
                    self.gbest_pos = self.X[i].copy()

            r1 = self.rng.random(size=(self.n_particles, self.dim))
            r2 = self.rng.random(size=(self.n_particles, self.dim))
            self.V = self.K * (
                self.V
                + self.n1 * r1 * (self.pbest_pos - self.X)
                + self.n2 * r2 * (self.gbest_pos - self.X)
            )
            self.X = self.clip_bounds(self.X + self.V)

            self.history.append(self.gbest_val)
            if verbose and self.gbest_pos is not None:
                n, lr, al = decode_position(self.gbest_pos)
                print(f'  Iter {it+1:2d}/{self.max_iter} | K={self.K:.4f} | gbest={self.gbest_val:.4f} | '
                      f'neurons={n:3d}, lr={lr:.5f} | [{time.time()-t_start:.0f}s]')

        if verbose:
            print('─' * 60)
            print(f'✅ Hoàn thành! Thời gian: {time.time()-t_start:.1f}s')

        return self.gbest_pos, self.gbest_val, self.history, pd.DataFrame(detailed_history), self.K


def run_cpso(
    X_tr: Optional[np.ndarray] = None,
    y_tr: Optional[np.ndarray] = None,
    n_particles: int = 12,
    n_iter: int = 20,
    n1: float = 2.05,
    n2: float = 2.05,
    seed: int = 42,
    fitness_func: Optional[Callable[[np.ndarray], float]] = None,
    verbose: bool = True
) -> Tuple[np.ndarray, float, List[float], pd.DataFrame, float]:
    """
    Chạy Constriction PSO (CPSO).
    """
    if fitness_func is None:
        if X_tr is None or y_tr is None:
            raise ValueError("Cần cung cấp (X_tr, y_tr) hoặc fitness_func")
        cv_obj = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
        fitness_func = lambda x: fitness_single(x, X_tr, y_tr, cv_obj, seed)

    optimizer = ConstrictionPSO(
        fitness_func=fitness_func,
        lower_bounds=LOW,
        upper_bounds=HIGH,
        n_particles=n_particles,
        max_iter=n_iter,
        n1=n1,
        n2=n2,
        random_seed=seed
    )
    return optimizer.optimize(verbose=verbose)
