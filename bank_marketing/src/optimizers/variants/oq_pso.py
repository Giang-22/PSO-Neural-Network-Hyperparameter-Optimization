"""
Opposition-based Quantum Particle Swarm Optimization (OQ-PSO).
"""

import time
from typing import Tuple, List, Optional, Callable, Any
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from ..base import BasePSO
from ...models.fitness import LOW, HIGH, DIM, decode_position, fitness_single


class OQPSO(BasePSO):
    """
    OQ-PSO: Kết hợp Học đối kháng (Opposition-Based Learning - OBL) vào Quantum PSO.
    - Khởi tạo đối kháng: Đánh giá 2*N hạt (quần thể gốc + đối kháng) và chọn N hạt tốt nhất.
    - Nhảy đối kháng (OBL Jumping): Định kỳ tạo quần thể đối kháng trong không gian thu hẹp để thoát cực trị.
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
        jump_rate: int = 5,
        random_seed: int = 42
    ):
        super().__init__(fitness_func, lower_bounds, upper_bounds, n_particles, max_iter, random_seed)
        self.beta_start = beta_start
        self.beta_end = beta_end
        self.jump_rate = jump_rate

    def optimize(self, verbose: bool = True) -> Tuple[np.ndarray, float, List[float], pd.DataFrame]:
        # 1. Khởi tạo quần thể ban đầu & Đối kháng (OBL Initialization)
        pos_init = self.rng.uniform(self.lb, self.ub, size=(self.n_particles, self.dim))
        pos_op = self.lb + self.ub - pos_init
        combined_pos = np.vstack((pos_init, pos_op))
        combined_scores = np.zeros(2 * self.n_particles)

        if verbose:
            print(f'⚛️ OQ-PSO (Opposition-Based QPSO) | beta: {self.beta_start} -> {self.beta_end}')
            print(f'   Khởi tạo: Đánh giá {2 * self.n_particles} hạt (OBL)')
            print(f'   {self.n_particles} particles × {self.max_iter} iterations | jump_rate={self.jump_rate}')
            print('─' * 60)

        for i in range(2 * self.n_particles):
            combined_scores[i] = self.fitness_func(combined_pos[i])

        best_indices = np.argsort(combined_scores)[-self.n_particles:]
        self.X = combined_pos[best_indices].copy()
        self.pbest_pos = self.X.copy()
        self.pbest_val = combined_scores[best_indices].copy()
        self.gbest_val = float(np.max(self.pbest_val))
        self.gbest_pos = self.pbest_pos[np.argmax(self.pbest_val)].copy()

        detailed_history = []
        self.history = []
        t_start = time.time()

        for it in range(self.max_iter):
            beta = self.beta_start - (self.beta_start - self.beta_end) * (it / max(self.max_iter - 1, 1))

            # Quantum Position Update
            mbest = np.mean(self.pbest_pos, axis=0)

            for i in range(self.n_particles):
                phi = self.rng.random(size=self.dim)
                p = phi * self.pbest_pos[i] + (1.0 - phi) * self.gbest_pos
                u = np.clip(self.rng.random(size=self.dim), 1e-10, 1.0)
                distance = np.abs(mbest - self.X[i])
                sign = np.where(self.rng.random(size=self.dim) < 0.5, 1.0, -1.0)
                self.X[i] = p + sign * beta * distance * np.log(1.0 / u)

            self.X = self.clip_bounds(self.X)

            # Đánh giá fitness
            for i in range(self.n_particles):
                score = self.fitness_func(self.X[i])
                n_neur, lr, al = decode_position(self.X[i])
                detailed_history.append({
                    'iter': it, 'particle': i, 'score': score,
                    'n_neurons': n_neur, 'lr': lr, 'alpha': al, 'beta': beta,
                    'type': 'normal'
                })

                if score > self.pbest_val[i]:
                    self.pbest_val[i] = score
                    self.pbest_pos[i] = self.X[i].copy()

                if score > self.gbest_val:
                    self.gbest_val = score
                    self.gbest_pos = self.X[i].copy()

            # OBL Jumping định kỳ
            if (it + 1) % self.jump_rate == 0:
                curr_min = np.min(self.X, axis=0)
                curr_max = np.max(self.X, axis=0)
                pos_op_jump = self.clip_bounds(curr_min + curr_max - self.X)

                scores_op_jump = np.zeros(self.n_particles)
                for i in range(self.n_particles):
                    scores_op_jump[i] = self.fitness_func(pos_op_jump[i])
                    n_neur_op, lr_op, al_op = decode_position(pos_op_jump[i])
                    detailed_history.append({
                        'iter': it, 'particle': self.n_particles + i, 'score': scores_op_jump[i],
                        'n_neurons': n_neur_op, 'lr': lr_op, 'alpha': al_op, 'beta': beta,
                        'type': 'opposition'
                    })

                combined_pos_jump = np.vstack((self.X, pos_op_jump))
                combined_pbest = np.vstack((self.pbest_pos, pos_op_jump))
                combined_scores_jump = np.concatenate((self.pbest_val, scores_op_jump))

                best_jump_indices = np.argsort(combined_scores_jump)[-self.n_particles:]
                self.X = combined_pos_jump[best_jump_indices].copy()
                self.pbest_pos = combined_pbest[best_jump_indices].copy()
                self.pbest_val = combined_scores_jump[best_jump_indices].copy()

                if np.max(self.pbest_val) > self.gbest_val:
                    self.gbest_val = float(np.max(self.pbest_val))
                    self.gbest_pos = self.pbest_pos[np.argmax(self.pbest_val)].copy()

            self.history.append(self.gbest_val)

            if verbose and self.gbest_pos is not None:
                n_neur, lr, al = decode_position(self.gbest_pos)
                print(f'  Iter {it+1:2d}/{self.max_iter} | beta={beta:.3f} | gbest={self.gbest_val:.4f} | '
                      f'neurons={n_neur:3d}, lr={lr:.5f}, alpha={al:.6f} | [{time.time()-t_start:.0f}s]')

        if verbose:
            print('─' * 60)
            print(f'✅ Hoàn thành OQ-PSO! Thời gian: {time.time()-t_start:.1f}s')

        return self.gbest_pos, self.gbest_val, self.history, pd.DataFrame(detailed_history)


def run_oq_pso(
    X_tr: Optional[np.ndarray] = None,
    y_tr: Optional[np.ndarray] = None,
    n_particles: int = 12,
    n_iter: int = 20,
    beta_start: float = 1.0,
    beta_end: float = 0.5,
    jump_rate: int = 5,
    seed: int = 42,
    fitness_func: Optional[Callable[[np.ndarray], float]] = None,
    verbose: bool = True
) -> Tuple[np.ndarray, float, List[float], pd.DataFrame]:
    """
    Opposition-based Quantum PSO (OQ-PSO).
    """
    if fitness_func is None:
        if X_tr is None or y_tr is None:
            raise ValueError("Cần cung cấp (X_tr, y_tr) hoặc fitness_func")
        cv_obj = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
        fitness_func = lambda x: fitness_single(x, X_tr, y_tr, cv_obj, seed)

    optimizer = OQPSO(
        fitness_func=fitness_func,
        lower_bounds=LOW,
        upper_bounds=HIGH,
        n_particles=n_particles,
        max_iter=n_iter,
        beta_start=beta_start,
        beta_end=beta_end,
        jump_rate=jump_rate,
        random_seed=seed
    )
    return optimizer.optimize(verbose=verbose)
