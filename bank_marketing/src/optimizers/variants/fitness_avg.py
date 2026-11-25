"""
PSO with Fitness Averaging to reduce stochastic evaluation noise.
"""

import time
from typing import Tuple, List, Optional, Callable, Any
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from ..base import BasePSO
from ...models.fitness import LOW, HIGH, DIM, decode_position, fitness_averaged


class FitnessAvgPSO(BasePSO):
    """
    PSO sử dụng hàm fitness lấy trung bình qua k lần chạy (seeds khác nhau) để giảm thiểu nhiễu.
    """
    def __init__(
        self,
        fitness_func: Callable[[np.ndarray], float],
        lower_bounds: np.ndarray = LOW,
        upper_bounds: np.ndarray = HIGH,
        n_particles: int = 12,
        max_iter: int = 20,
        w_start: float = 0.9,
        w_end: float = 0.4,
        c1: float = 1.5,
        c2: float = 1.5,
        v_max_ratio: float = 0.2,
        k_avg: int = 3,
        random_seed: int = 42
    ):
        super().__init__(fitness_func, lower_bounds, upper_bounds, n_particles, max_iter, random_seed)
        self.w_start = w_start
        self.w_end = w_end
        self.c1 = c1
        self.c2 = c2
        self.v_max_ratio = v_max_ratio
        self.k_avg = k_avg

    def optimize(self, verbose: bool = True) -> Tuple[np.ndarray, float, List[float], pd.DataFrame]:
        self.initialize_swarm()
        v_max = self.v_max_ratio * (self.ub - self.lb)
        detailed_history = []
        t_start = time.time()

        if verbose:
            print(f'🟡 PSO + Fitness Averaging (k={self.k_avg}) | w_start={self.w_start} → w_end={self.w_end}')
            print(f'   {self.n_particles} particles × {self.max_iter} iterations')
            print('─' * 60)

        for it in range(self.max_iter):
            w_current = self.w_start - (self.w_start - self.w_end) / self.max_iter * it

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
            self.V = (
                w_current * self.V
                + self.c1 * r1 * (self.pbest_pos - self.X)
                + self.c2 * r2 * (self.gbest_pos - self.X)
            )
            self.V = np.clip(self.V, -v_max, v_max)
            self.X = self.clip_bounds(self.X + self.V)

            self.history.append(self.gbest_val)
            if verbose and self.gbest_pos is not None:
                n, lr, al = decode_position(self.gbest_pos)
                print(f'  Iter {it+1:2d}/{self.max_iter} | w={w_current:.3f} | gbest={self.gbest_val:.4f} | '
                      f'neurons={n:3d}, lr={lr:.5f} | [{time.time()-t_start:.0f}s]')

        if verbose:
            print('─' * 60)
            print(f'✅ Hoàn thành! Thời gian: {time.time()-t_start:.1f}s')

        return self.gbest_pos, self.gbest_val, self.history, pd.DataFrame(detailed_history)


def run_pso_fitness_avg(
    X_tr: Optional[np.ndarray] = None,
    y_tr: Optional[np.ndarray] = None,
    n_particles: int = 12,
    n_iter: int = 20,
    w_start: float = 0.9,
    w_end: float = 0.4,
    n1: float = 1.5,
    n2: float = 1.5,
    v_max_ratio: float = 0.2,
    k_avg: int = 3,
    seed: int = 42,
    fitness_func: Optional[Callable[[np.ndarray], float]] = None,
    verbose: bool = True
) -> Tuple[np.ndarray, float, List[float], pd.DataFrame]:
    """
    PSO sử dụng hàm fitness lấy trung bình nhiều seed để giảm nhiễu.
    """
    if fitness_func is None:
        if X_tr is None or y_tr is None:
            raise ValueError("Cần cung cấp (X_tr, y_tr) hoặc fitness_func")
        cv_obj = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
        fitness_func = lambda x: fitness_averaged(x, X_tr, y_tr, cv_obj, seed, k=k_avg)

    optimizer = FitnessAvgPSO(
        fitness_func=fitness_func,
        lower_bounds=LOW,
        upper_bounds=HIGH,
        n_particles=n_particles,
        max_iter=n_iter,
        w_start=w_start,
        w_end=w_end,
        c1=n1,
        c2=n2,
        v_max_ratio=v_max_ratio,
        k_avg=k_avg,
        random_seed=seed
    )
    return optimizer.optimize(verbose=verbose)
