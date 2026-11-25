"""
Mean-based / Top-K Attraction Particle Swarm Optimization (MB-PSO).
"""

import time
from typing import Tuple, List, Optional, Callable, Any
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from ..base import BasePSO
from ...models.fitness import LOW, HIGH, DIM, decode_position, fitness_single


class MBPSO(BasePSO):
    """
    PSO kết hợp khoảng cách và trọng tâm các hạt tốt nhất (Mean-based / Top-K attraction).
    """
    def __init__(
        self,
        fitness_func: Callable[[np.ndarray], float],
        lower_bounds: np.ndarray = LOW,
        upper_bounds: np.ndarray = HIGH,
        n_particles: int = 12,
        max_iter: int = 20,
        w: float = 0.729,
        c1: float = 1.0,
        c2: float = 1.0,
        c3: float = 1.0,
        top_k: int = 4,
        v_max_ratio: float = 0.2,
        random_seed: int = 42
    ):
        super().__init__(fitness_func, lower_bounds, upper_bounds, n_particles, max_iter, random_seed)
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.top_k = min(top_k, n_particles)
        self.v_max_ratio = v_max_ratio

    def optimize(self, verbose: bool = True) -> Tuple[np.ndarray, float, List[float], pd.DataFrame]:
        self.initialize_swarm()
        v_max = self.v_max_ratio * (self.ub - self.lb)
        detailed_history = []
        t_start = time.time()

        if verbose:
            print(f'🟣 MB-PSO | Mean-based (Top-{self.top_k}) Attraction | w={self.w}, c1={self.c1}, c2={self.c2}, c3={self.c3}')
            print(f'   {self.n_particles} particles × {self.max_iter} iterations')
            print('─' * 60)

        for it in range(self.max_iter):
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

            top_indices = np.argsort(self.pbest_val)[-self.top_k:]
            mbest = np.mean(self.pbest_pos[top_indices], axis=0)

            r1 = self.rng.random(size=(self.n_particles, self.dim))
            r2 = self.rng.random(size=(self.n_particles, self.dim))
            r3 = self.rng.random(size=(self.n_particles, self.dim))

            self.V = (
                self.w * self.V
                + self.c1 * r1 * (self.pbest_pos - self.X)
                + self.c2 * r2 * (self.gbest_pos - self.X)
                + self.c3 * r3 * (mbest - self.X)
            )
            self.V = np.clip(self.V, -v_max, v_max)
            self.X = self.clip_bounds(self.X + self.V)

            self.history.append(self.gbest_val)
            if verbose and self.gbest_pos is not None:
                n_neur, lr, al = decode_position(self.gbest_pos)
                print(f'  Iter {it+1:2d}/{self.max_iter} | gbest={self.gbest_val:.4f} | '
                      f'neurons={n_neur:3d}, lr={lr:.5f} | [{time.time()-t_start:.0f}s]')

        if verbose:
            print('─' * 60)
            print(f'✅ Hoàn thành! Thời gian: {time.time()-t_start:.1f}s')

        return self.gbest_pos, self.gbest_val, self.history, pd.DataFrame(detailed_history)


def run_mb_pso(
    X_tr: Optional[np.ndarray] = None,
    y_tr: Optional[np.ndarray] = None,
    n_particles: int = 12,
    n_iter: int = 20,
    w: float = 0.729,
    c1: float = 1.0,
    c2: float = 1.0,
    c3: float = 1.0,
    top_k: int = 4,
    v_max_ratio: float = 0.2,
    seed: int = 42,
    fitness_func: Optional[Callable[[np.ndarray], float]] = None,
    verbose: bool = True
) -> Tuple[np.ndarray, float, List[float], pd.DataFrame]:
    """
    PSO kết hợp khoảng cách và trọng tâm các hạt tốt nhất (Mean-based attraction).
    """
    if fitness_func is None:
        if X_tr is None or y_tr is None:
            raise ValueError("Cần cung cấp (X_tr, y_tr) hoặc fitness_func")
        cv_obj = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
        fitness_func = lambda x: fitness_single(x, X_tr, y_tr, cv_obj, seed)

    optimizer = MBPSO(
        fitness_func=fitness_func,
        lower_bounds=LOW,
        upper_bounds=HIGH,
        n_particles=n_particles,
        max_iter=n_iter,
        w=w,
        c1=c1,
        c2=c2,
        c3=c3,
        top_k=top_k,
        v_max_ratio=v_max_ratio,
        random_seed=seed
    )
    return optimizer.optimize(verbose=verbose)
