"""
Fractional-Order Particle Swarm Optimization (FO-PSO).
"""

import time
from typing import Tuple, List, Optional, Callable, Any
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from ..base import BasePSO
from ...models.fitness import LOW, HIGH, DIM, decode_position, fitness_single


class FOPSO(BasePSO):
    """
    PSO sử dụng đạo hàm bậc phân số (Fractional-Order) lưu giữ bộ nhớ vận tốc các thế hệ trước.
    """
    def __init__(
        self,
        fitness_func: Callable[[np.ndarray], float],
        lower_bounds: np.ndarray = LOW,
        upper_bounds: np.ndarray = HIGH,
        n_particles: int = 12,
        max_iter: int = 20,
        alpha: float = 0.6,
        r: int = 4,
        c1: float = 1.5,
        c2: float = 1.5,
        v_max_ratio: float = 0.2,
        random_seed: int = 42
    ):
        super().__init__(fitness_func, lower_bounds, upper_bounds, n_particles, max_iter, random_seed)
        self.alpha = alpha
        self.r = r
        self.c1 = c1
        self.c2 = c2
        self.v_max_ratio = v_max_ratio

        # Tính các hệ số trọng lượng phân số (Fractional Coefficients)
        self.c_w = np.zeros(self.r)
        self.c_w[0] = self.alpha
        for k in range(1, self.r):
            self.c_w[k] = self.c_w[k - 1] * (k - self.alpha) / (k + 1)

    def optimize(self, verbose: bool = True) -> Tuple[np.ndarray, float, List[float], pd.DataFrame]:
        self.initialize_swarm()
        v_max = self.v_max_ratio * (self.ub - self.lb)
        detailed_history = []
        t_start = time.time()

        # Bộ nhớ vận tốc quá khứ
        v_memory = np.zeros((self.r, self.n_particles, self.dim))
        v_memory[0] = self.V

        if verbose:
            print(f'🟣 FO-PSO | alpha: {self.alpha} | r: {self.r} | c_w: {np.round(self.c_w, 4)}')
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

            r1 = self.rng.random(size=(self.n_particles, self.dim))
            r2 = self.rng.random(size=(self.n_particles, self.dim))

            inertial_velocity = np.zeros((self.n_particles, self.dim))
            for k in range(self.r):
                inertial_velocity += self.c_w[k] * v_memory[k]

            self.V = (
                inertial_velocity
                + self.c1 * r1 * (self.pbest_pos - self.X)
                + self.c2 * r2 * (self.gbest_pos - self.X)
            )
            self.V = np.clip(self.V, -v_max, v_max)

            # Cập nhật bộ nhớ vận tốc
            for k in range(self.r - 1, 0, -1):
                v_memory[k] = v_memory[k - 1]
            v_memory[0] = self.V

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


def run_fopso(
    X_tr: Optional[np.ndarray] = None,
    y_tr: Optional[np.ndarray] = None,
    n_particles: int = 12,
    n_iter: int = 20,
    alpha: float = 0.6,
    r: int = 4,
    n1: float = 1.5,
    n2: float = 1.5,
    v_max_ratio: float = 0.2,
    seed: int = 42,
    fitness_func: Optional[Callable[[np.ndarray], float]] = None,
    verbose: bool = True
) -> Tuple[np.ndarray, float, List[float], pd.DataFrame]:
    """
    Fractional-Order PSO (FO-PSO).
    """
    if fitness_func is None:
        if X_tr is None or y_tr is None:
            raise ValueError("Cần cung cấp (X_tr, y_tr) hoặc fitness_func")
        cv_obj = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
        fitness_func = lambda x: fitness_single(x, X_tr, y_tr, cv_obj, seed)

    optimizer = FOPSO(
        fitness_func=fitness_func,
        lower_bounds=LOW,
        upper_bounds=HIGH,
        n_particles=n_particles,
        max_iter=n_iter,
        alpha=alpha,
        r=r,
        c1=n1,
        c2=n2,
        v_max_ratio=v_max_ratio,
        random_seed=seed
    )
    return optimizer.optimize(verbose=verbose)
