"""
Base PSO Class defining common state, bounds clipping, and interface for all PSO variants.
"""

from typing import Callable, Tuple, List, Optional
import numpy as np


class BasePSO:
    """
    Lớp cơ sở (Base Class) cho các thuật toán PSO.
    Quản lý quần thể (swarm), vận tốc (velocity), giới hạn tìm kiếm (bounds) và lịch sử gbest.
    """
    def __init__(
        self,
        fitness_func: Callable[[np.ndarray], float],
        lower_bounds: np.ndarray,
        upper_bounds: np.ndarray,
        n_particles: int = 20,
        max_iter: int = 30,
        random_seed: int = 42
    ):
        self.fitness_func = fitness_func
        self.lb = np.array(lower_bounds, dtype=float)
        self.ub = np.array(upper_bounds, dtype=float)
        self.dim = len(self.lb)
        self.n_particles = n_particles
        self.max_iter = max_iter
        self.random_seed = random_seed
        
        self.rng = np.random.default_rng(random_seed)
        
        # State placeholders
        self.X: Optional[np.ndarray] = None
        self.V: Optional[np.ndarray] = None
        self.pbest_pos: Optional[np.ndarray] = None
        self.pbest_val: Optional[np.ndarray] = None
        self.gbest_pos: Optional[np.ndarray] = None
        self.gbest_val: float = -np.inf
        self.history: List[float] = []

    def initialize_swarm(self) -> None:
        """Khởi tạo ngẫu nhiên vị trí và vận tốc các hạt trong không gian tìm kiếm."""
        self.X = self.rng.uniform(self.lb, self.ub, size=(self.n_particles, self.dim))
        v_span = self.ub - self.lb
        self.V = self.rng.uniform(-0.1 * v_span, 0.1 * v_span, size=(self.n_particles, self.dim))
        
        self.pbest_pos = self.X.copy()
        self.pbest_val = np.full(self.n_particles, -np.inf)
        self.gbest_pos = None
        self.gbest_val = -np.inf
        self.history = []

    def clip_bounds(self, X: np.ndarray) -> np.ndarray:
        """Cắt giới hạn tọa độ hạt trong [lower_bounds, upper_bounds]."""
        return np.clip(X, self.lb, self.ub)

    def optimize(self) -> Tuple[np.ndarray, float, List[float]]:
        """Phương thức tối ưu chính (sẽ được override ở các lớp con)."""
        raise NotImplementedError("Subclasses must implement optimize()")
