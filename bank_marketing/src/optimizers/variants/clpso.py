"""
Comprehensive Learning Particle Swarm Optimization (CLPSO).
"""

import time
from typing import Tuple, List, Optional, Callable, Any
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from ..base import BasePSO
from ...models.fitness import LOW, HIGH, DIM, decode_position, fitness_single


class CLPSO(BasePSO):
    """
    CLPSO: Các chiều tọa độ của hạt học từ các pbest của các hạt khác nhau để bảo toàn tính đa dạng.
    (Liang et al., 2006: Comprehensive Learning Particle Swarm Optimizer).
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
        c: float = 1.49445,
        refreshing_gap: int = 5,
        v_max_ratio: float = 0.2,
        random_seed: int = 42
    ):
        super().__init__(fitness_func, lower_bounds, upper_bounds, n_particles, max_iter, random_seed)
        self.w_start = w_start
        self.w_end = w_end
        self.c = c
        self.refreshing_gap = refreshing_gap
        self.v_max_ratio = v_max_ratio

        # Tính learning probability Pc cho từng hạt theo công thức Liang et al.
        if self.n_particles > 1:
            self.Pc = 0.05 + 0.45 * (np.exp(10.0 * np.arange(self.n_particles) / (self.n_particles - 1)) - 1.0) / (np.exp(10.0) - 1.0)
        else:
            self.Pc = np.array([0.5])

    def _generate_exemplars(self, i: int) -> np.ndarray:
        """Sinh vector chỉ số exemplar cho từng chiều của hạt i."""
        exemplar = np.zeros(self.dim, dtype=int)
        for d in range(self.dim):
            if self.rng.random() < self.Pc[i]:
                # Chọn 2 hạt ngẫu nhiên khác nhau
                candidates = [p for p in range(self.n_particles) if p != i]
                if not candidates:
                    candidates = [i]
                c1, c2 = self.rng.choice(candidates, size=min(2, len(candidates)), replace=False)
                if self.pbest_val[c1] >= self.pbest_val[c2]:
                    exemplar[d] = c1
                else:
                    exemplar[d] = c2
            else:
                exemplar[d] = i

        # Nếu tất cả các chiều đều học từ chính mình, chọn ngẫu nhiên 1 chiều học từ hạt khác
        if np.all(exemplar == i) and self.n_particles > 1:
            d_rand = self.rng.integers(0, self.dim)
            candidates = [p for p in range(self.n_particles) if p != i]
            exemplar[d_rand] = self.rng.choice(candidates)

        return exemplar

    def optimize(self, verbose: bool = True) -> Tuple[np.ndarray, float, List[float], pd.DataFrame]:
        self.initialize_swarm()
        v_max = self.v_max_ratio * (self.ub - self.lb)
        detailed_history = []
        t_start = time.time()

        # Khởi tạo ma trận exemplar và bộ đếm bế tắc (stay_count)
        exemplars = np.zeros((self.n_particles, self.dim), dtype=int)
        stay_count = np.zeros(self.n_particles, dtype=int)

        for i in range(self.n_particles):
            exemplars[i] = self._generate_exemplars(i)

        if verbose:
            print(f'🟣 CLPSO | Comprehensive Learning | w: {self.w_start} → {self.w_end}, c={self.c}, gap={self.refreshing_gap}')
            print(f'   {self.n_particles} particles × {self.max_iter} iterations')
            print('─' * 60)

        for it in range(self.max_iter):
            w_current = self.w_start - (self.w_start - self.w_end) * (it / max(self.max_iter - 1, 1))

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
                    stay_count[i] = 0
                else:
                    stay_count[i] += 1

                if score > self.gbest_val:
                    self.gbest_val = score
                    self.gbest_pos = self.X[i].copy()

                # Refresh exemplars nếu bế tắc
                if stay_count[i] >= self.refreshing_gap:
                    exemplars[i] = self._generate_exemplars(i)
                    stay_count[i] = 0

            # Cập nhật vận tốc CLPSO
            for i in range(self.n_particles):
                r = self.rng.random(size=self.dim)
                # Lấy vị trí pbest của từng exemplar tương ứng với từng chiều
                pbest_exemplar = np.array([self.pbest_pos[exemplars[i, d], d] for d in range(self.dim)])
                self.V[i] = (
                    w_current * self.V[i]
                    + self.c * r * (pbest_exemplar - self.X[i])
                )

            self.V = np.clip(self.V, -v_max, v_max)
            self.X = self.clip_bounds(self.X + self.V)

            self.history.append(self.gbest_val)
            if verbose and self.gbest_pos is not None:
                n_neur, lr, al = decode_position(self.gbest_pos)
                print(f'  Iter {it+1:2d}/{self.max_iter} | w={w_current:.3f} | gbest={self.gbest_val:.4f} | '
                      f'neurons={n_neur:3d}, lr={lr:.5f} | [{time.time()-t_start:.0f}s]')

        if verbose:
            print('─' * 60)
            print(f'✅ Hoàn thành CLPSO! Thời gian: {time.time()-t_start:.1f}s')

        return self.gbest_pos, self.gbest_val, self.history, pd.DataFrame(detailed_history)


def run_clpso(
    X_tr: Optional[np.ndarray] = None,
    y_tr: Optional[np.ndarray] = None,
    n_particles: int = 12,
    n_iter: int = 20,
    w_start: float = 0.9,
    w_end: float = 0.4,
    c: float = 1.49445,
    refreshing_gap: int = 5,
    v_max_ratio: float = 0.2,
    seed: int = 42,
    fitness_func: Optional[Callable[[np.ndarray], float]] = None,
    verbose: bool = True
) -> Tuple[np.ndarray, float, List[float], pd.DataFrame]:
    """
    CLPSO: Các chiều tọa độ của hạt học từ các pbest của các hạt khác nhau để bảo toàn tính đa dạng.
    """
    if fitness_func is None:
        if X_tr is None or y_tr is None:
            raise ValueError("Cần cung cấp (X_tr, y_tr) hoặc fitness_func")
        cv_obj = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
        fitness_func = lambda x: fitness_single(x, X_tr, y_tr, cv_obj, seed)

    optimizer = CLPSO(
        fitness_func=fitness_func,
        lower_bounds=LOW,
        upper_bounds=HIGH,
        n_particles=n_particles,
        max_iter=n_iter,
        w_start=w_start,
        w_end=w_end,
        c=c,
        refreshing_gap=refreshing_gap,
        v_max_ratio=v_max_ratio,
        random_seed=seed
    )
    return optimizer.optimize(verbose=verbose)
