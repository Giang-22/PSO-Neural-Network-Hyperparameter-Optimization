"""
Quantum + Top-K Mean-Based Particle Swarm Optimization (Q-MBPSO).
"""

import time
from typing import Tuple, List, Optional, Callable, Any
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from ..base import BasePSO
from ...models.fitness import LOW, HIGH, DIM, decode_position, fitness_single


class QMBPSO(BasePSO):
    """
    Q-MBPSO: Kết hợp Quantum PSO và Top-K Mean-Based Attraction.
    mbest được tính từ trung bình của Top-K cá nhân có pbest cao nhất thay vì toàn bộ bầy đàn.
    """
    def __init__(
        self,
        fitness_func: Callable[[np.ndarray], float],
        lower_bounds: np.ndarray = LOW,
        upper_bounds: np.ndarray = HIGH,
        n_particles: int = 12,
        max_iter: int = 20,
        beta_start: float = 1.0,
        beta_end: float = 0.5,
        top_k: int = 3,
        random_seed: int = 42
    ):
        super().__init__(fitness_func, lower_bounds, upper_bounds, n_particles, max_iter, random_seed)
        self.beta_start = beta_start
        self.beta_end = beta_end
        self.top_k = min(top_k, n_particles)

    def optimize(self, verbose: bool = True) -> Tuple[np.ndarray, float, List[float], pd.DataFrame]:
        self.initialize_swarm()
        detailed_history = []
        t_start = time.time()

        if verbose:
            print(f'🌀 Q-MBPSO (Quantum MB-PSO) | mbest = Top-{self.top_k} pbest | beta: {self.beta_start} → {self.beta_end}')
            print('─' * 60)

        for it in range(self.max_iter):
            beta = self.beta_start - (self.beta_start - self.beta_end) * (it / max(self.max_iter - 1, 1))

            for i in range(self.n_particles):
                score = self.fitness_func(self.X[i])
                n_neur, lr, al = decode_position(self.X[i])
                detailed_history.append({
                    'iter': it, 'particle': i, 'score': score,
                    'n_neurons': n_neur, 'lr': lr, 'alpha': al
                })

                if score > self.pbest_val[i]:
                    self.pbest_val[i] = score
                    self.pbest_pos[i] = self.X[i].copy()
                if score > self.gbest_val:
                    self.gbest_val = score
                    self.gbest_pos = self.X[i].copy()

            top_k_idx = np.argsort(self.pbest_val)[-self.top_k:]
            mbest_topk = np.mean(self.pbest_pos[top_k_idx], axis=0)

            for i in range(self.n_particles):
                phi = self.rng.random(size=self.dim)
                p = phi * self.pbest_pos[i] + (1.0 - phi) * self.gbest_pos
                u = np.clip(self.rng.random(size=self.dim), 1e-10, 1.0)
                distance = np.abs(mbest_topk - self.X[i])
                sign = np.where(self.rng.random(size=self.dim) < 0.5, 1.0, -1.0)
                self.X[i] = p + sign * beta * distance * np.log(1.0 / u)

            self.X = self.clip_bounds(self.X)
            self.history.append(self.gbest_val)

            if verbose and self.gbest_pos is not None:
                n_neur, lr, al = decode_position(self.gbest_pos)
                print(f'  Iter {it+1:2d}/{self.max_iter} | beta={beta:.3f} | gbest={self.gbest_val:.4f} | '
                      f'neurons={n_neur:3d}, lr={lr:.5f} | [{time.time()-t_start:.0f}s]')

        if verbose:
            print('─' * 60)
            print(f'✅ Hoàn thành Q-MBPSO! Thời gian: {time.time()-t_start:.1f}s')

        return self.gbest_pos, self.gbest_val, self.history, pd.DataFrame(detailed_history)


def run_q_mbpso(
    X_tr: Optional[np.ndarray] = None,
    y_tr: Optional[np.ndarray] = None,
    n_particles: int = 12,
    n_iter: int = 20,
    beta_start: float = 1.0,
    beta_end: float = 0.5,
    top_k: int = 3,
    seed: int = 42,
    fitness_func: Optional[Callable[[np.ndarray], float]] = None,
    verbose: bool = True
) -> Tuple[np.ndarray, float, List[float], pd.DataFrame]:
    """
    Quantum + Top-K Mean-Based PSO (Q-MBPSO).
    """
    if fitness_func is None:
        if X_tr is None or y_tr is None:
            raise ValueError("Cần cung cấp (X_tr, y_tr) hoặc fitness_func")
        cv_obj = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
        fitness_func = lambda x: fitness_single(x, X_tr, y_tr, cv_obj, seed)

    optimizer = QMBPSO(
        fitness_func=fitness_func,
        lower_bounds=LOW,
        upper_bounds=HIGH,
        n_particles=n_particles,
        max_iter=n_iter,
        beta_start=beta_start,
        beta_end=beta_end,
        top_k=top_k,
        random_seed=seed
    )
    return optimizer.optimize(verbose=verbose)
