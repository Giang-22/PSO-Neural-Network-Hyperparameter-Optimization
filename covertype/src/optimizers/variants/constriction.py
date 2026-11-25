"""
Constriction-type PSO (CPSO) with constriction factor chi (χ).
"""

def compute_constriction_factor(n1: float = 2.05, n2: float = 2.05) -> float:
    """
    Tính hệ số co thắt chi (χ) theo công thức Clerc & Kennedy.
    """
    phi = n1 + n2
    if phi <= 4.0:
        raise ValueError("phi = n1 + n2 phải > 4")
    import numpy as np
    chi = 2.0 / np.abs(2.0 - phi - np.sqrt(phi**2 - 4*phi))
    return float(chi)


def run_cpso(*args, **kwargs):
    """
    Chạy Constriction PSO (CPSO).
    """
    pass
