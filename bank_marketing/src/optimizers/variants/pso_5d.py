"""
5D Search Space Particle Swarm Optimization (PSO-5D).
"""

import time
from typing import Tuple, List, Optional, Callable, Any
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from ..base import BasePSO
from ...models.fitness import LOW_5D, HIGH_5D, DIM_5D, decode_position_5d, fitness_single_5d


class PSO5D(BasePSO):
    """
    PSO tối ưu trên không gian 5 chiều:
      1. n_neurons   ∈ [16, 256]
      2. log10(lr)   ∈ [-4, -1]
      3. log10(alpha)∈ [-5, -1]
      4. n_layers    ∈ [1, 4]
      5. batch_size  ∈ [16, 128]
    """
    def __init__(
        self,
        fitness_func: Callable[[np.ndarray], float],
        lower_bounds: np.ndarray = LOW_5D,
        upper_bounds: np.ndarray = HIGH_5D,
        n_particles: int = 12,
        max_iter: int = 20,
        w: float = 0.7,
        c1: float = 1.5,
        c2: float = 1.5,
        v_max_ratio: float = 0.2,
        random_seed: int = 42
    ):
        super().__init__(fitness_func, lower_bounds, upper_bounds, n_particles, max_iter, random_seed)
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.v_max_ratio = v_max_ratio

    def optimize(self, verbose: bool = True) -> Tuple[np.ndarray, float, List[float], pd.DataFrame]:
        self.initialize_swarm()
        v_max = self.v_max_ratio * (self.ub - self.lb)
        detailed_history = []
        t_start = time.time()

        if verbose:
            print(f'🚀 Standard PSO (5D) | w={self.w} | c1={self.c1}, c2={self.c2}')
            print(f'   {self.n_particles} particles × {self.max_iter} iterations (Không gian 5 chiều)')
            print('─' * 60)

        for it in range(self.max_iter):
            for i in range(self.n_particles):
                score = self.fitness_func(self.X[i])
                n, lr, al, nl, bs = decode_position_5d(self.X[i])
                detailed_history.append({
                    'iter': it, 'particle': i, 'score': score,
                    'n_neurons': n, 'lr': lr, 'alpha': al,
                    'n_layers': nl, 'batch_size': bs
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
                self.w * self.V
                + self.c1 * r1 * (self.pbest_pos - self.X)
                + self.c2 * r2 * (self.gbest_pos - self.X)
            )
            self.V = np.clip(self.V, -v_max, v_max)
            self.X = self.clip_bounds(self.X + self.V)

            self.history.append(self.gbest_val)
            if verbose and self.gbest_pos is not None:
                n, lr, al, nl, bs = decode_position_5d(self.gbest_pos)
                print(f'  Iter {it+1:2d}/{self.max_iter} | gbest={self.gbest_val:.4f} | '
                      f'neurons={n}, lr={lr:.5f}, alpha={al:.5f}, layers={nl}, bs={bs} | [{time.time()-t_start:.0f}s]')

        if verbose:
            print('─' * 60)
            print(f'✅ Hoàn thành PSO 5D! Thời gian: {time.time()-t_start:.1f}s')

        return self.gbest_pos, self.gbest_val, self.history, pd.DataFrame(detailed_history)


def run_pso_5d(
    X_tr: Optional[np.ndarray] = None,
    y_tr: Optional[np.ndarray] = None,
    n_particles: int = 12,
    n_iter: int = 20,
    w: float = 0.7,
    n1: float = 1.5,
    n2: float = 1.5,
    v_max_ratio: float = 0.2,
    seed: int = 42,
    fitness_func: Optional[Callable[[np.ndarray], float]] = None,
    verbose: bool = True
) -> Tuple[np.ndarray, float, List[float], pd.DataFrame]:
    """
    PSO trên không gian tìm kiếm 5 chiều (neurons, lr, alpha, layers, batch_size).
    """
    if fitness_func is None:
        if X_tr is None or y_tr is None:
            raise ValueError("Cần cung cấp (X_tr, y_tr) hoặc fitness_func")
        cv_obj = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
        fitness_func = lambda x: fitness_single_5d(x, X_tr, y_tr, cv_obj, seed)

    optimizer = PSO5D(
        fitness_func=fitness_func,
        lower_bounds=LOW_5D,
        upper_bounds=HIGH_5D,
        n_particles=n_particles,
        max_iter=n_iter,
        w=w,
        c1=n1,
        c2=n2,
        v_max_ratio=v_max_ratio,
        random_seed=seed
    )
    return optimizer.optimize(verbose=verbose)
