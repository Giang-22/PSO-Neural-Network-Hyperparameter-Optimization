"""
Standard Particle Swarm Optimization (Standard PSO)
With comprehensive tracking for criteria comparison and visualization
"""

import time
from typing import Callable, Tuple, List, Dict, Any, Optional
import numpy as np


class StandardPSO:
    """
    Standard PSO Optimizer with full trajectory and diagnostic telemetry.
    Minimization formulation: min f(x).
    """

    def __init__(
        self,
        fitness_func: Callable[[np.ndarray], np.ndarray],
        dim: int = 2,
        bounds: Tuple[float, float] = (-5.12, 5.12),
        n_particles: int = 30,
        max_iter: int = 50,
        w: float = 0.7,
        c1: float = 1.5,
        c2: float = 1.5,
        v_max_ratio: float = 0.2,
        random_seed: Optional[int] = 42
    ):
        self.fitness_func = fitness_func
        self.dim = dim
        self.lb = np.full(dim, bounds[0], dtype=float)
        self.ub = np.full(dim, bounds[1], dtype=float)
        self.n_particles = n_particles
        self.max_iter = max_iter
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.v_max_ratio = v_max_ratio
        self.random_seed = random_seed
        self.rng = np.random.default_rng(random_seed)

        # State variables
        self.X: np.ndarray = np.empty((0, 0))
        self.V: np.ndarray = np.empty((0, 0))
        self.pbest_pos: np.ndarray = np.empty((0, 0))
        self.pbest_val: np.ndarray = np.empty(0)
        self.gbest_pos: Optional[np.ndarray] = None
        self.gbest_val: float = float('inf')

        # Diagnostic History (Criteria Metrics)
        self.history_gbest_val: List[float] = []
        self.history_mean_val: List[float] = []
        self.history_diversity: List[float] = []
        self.history_avg_velocity: List[float] = []
        self.history_positions: List[np.ndarray] = []  # shape: (max_iter, n_particles, dim)
        self.history_velocities: List[np.ndarray] = []

    def _initialize_swarm(self):
        """Khởi tạo ngẫu nhiên vị trí và vận tốc các hạt."""
        self.X = self.rng.uniform(self.lb, self.ub, size=(self.n_particles, self.dim))
        v_max = self.v_max_ratio * (self.ub - self.lb)
        self.V = self.rng.uniform(-v_max, v_max, size=(self.n_particles, self.dim))

        self.pbest_pos = self.X.copy()
        fitness_values = self.fitness_func(self.X)
        self.pbest_val = fitness_values.copy()

        best_idx = np.argmin(self.pbest_val)
        self.gbest_val = float(self.pbest_val[best_idx])
        self.gbest_pos = self.pbest_pos[best_idx].copy()

        self.history_gbest_val = [self.gbest_val]
        self.history_mean_val = [float(np.mean(fitness_values))]
        
        # Initial Diversity & Velocity
        centroid = np.mean(self.X, axis=0)
        diversity = float(np.mean(np.linalg.norm(self.X - centroid, axis=1)))
        self.history_diversity = [diversity]
        
        avg_v = float(np.mean(np.linalg.norm(self.V, axis=1)))
        self.history_avg_velocity = [avg_v]
        
        self.history_positions = [self.X.copy()]
        self.history_velocities = [self.V.copy()]

    def optimize(self, verbose: bool = False) -> Dict[str, Any]:
        """
        Thực hiện tối ưu hóa và ghi nhận toàn bộ chỉ số đánh giá.
        """
        t0 = time.time()
        self._initialize_swarm()
        v_max = self.v_max_ratio * (self.ub - self.lb)

        for it in range(1, self.max_iter + 1):
            # 1. Sinh các số ngẫu nhiên r1, r2 ~ U(0, 1)
            r1 = self.rng.random(size=(self.n_particles, self.dim))
            r2 = self.rng.random(size=(self.n_particles, self.dim))

            # 2. Cập nhật vận tốc
            cognitive = self.c1 * r1 * (self.pbest_pos - self.X)
            social = self.c2 * r2 * (self.gbest_pos - self.X)
            self.V = self.w * self.V + cognitive + social

            # 3. Kẹp vận tốc (Velocity Clamping)
            self.V = np.clip(self.V, -v_max, v_max)

            # 4. Cập nhật vị trí và giới hạn biên
            self.X = np.clip(self.X + self.V, self.lb, self.ub)

            # 5. Đánh giá độ thích nghi (Fitness)
            fitness_values = self.fitness_func(self.X)

            # 6. Cập nhật Pbest và Gbest
            improved = fitness_values < self.pbest_val
            self.pbest_val[improved] = fitness_values[improved]
            self.pbest_pos[improved] = self.X[improved].copy()

            current_best_idx = np.argmin(self.pbest_val)
            if self.pbest_val[current_best_idx] < self.gbest_val:
                self.gbest_val = float(self.pbest_val[current_best_idx])
                self.gbest_pos = self.pbest_pos[current_best_idx].copy()

            # 7. Ghi nhận các tiêu chí động học (Kinetic & Diversity Criteria)
            centroid = np.mean(self.X, axis=0)
            diversity = float(np.mean(np.linalg.norm(self.X - centroid, axis=1)))
            avg_vel = float(np.mean(np.linalg.norm(self.V, axis=1)))

            self.history_gbest_val.append(self.gbest_val)
            self.history_mean_val.append(float(np.mean(fitness_values)))
            self.history_diversity.append(diversity)
            self.history_avg_velocity.append(avg_vel)
            self.history_positions.append(self.X.copy())
            self.history_velocities.append(self.V.copy())

            if verbose and (it % 10 == 0 or it == self.max_iter):
                print(f"Iter {it:3d}/{self.max_iter} | Gbest: {self.gbest_val:.6e} | "
                      f"Diversity: {diversity:.4f} | Avg Vel: {avg_vel:.4f}")

        elapsed_time = time.time() - t0

        return {
            'gbest_pos': self.gbest_pos,
            'gbest_val': self.gbest_val,
            'elapsed_time': elapsed_time,
            'history_gbest': np.array(self.history_gbest_val),
            'history_mean': np.array(self.history_mean_val),
            'history_diversity': np.array(self.history_diversity),
            'history_avg_velocity': np.array(self.history_avg_velocity),
            'positions': np.array(self.history_positions),
            'velocities': np.array(self.history_velocities),
            'params': {
                'w': self.w,
                'c1': self.c1,
                'c2': self.c2,
                'n_particles': self.n_particles,
                'max_iter': self.max_iter,
                'seed': self.random_seed
            }
        }
