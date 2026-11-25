"""
PSO Variants Package.
Tập hợp tất cả các biến thể PSO từ cơ bản đến nâng cao:
  1. Linear Decay PSO
  2. Constriction PSO (CPSO)
  3. Fitness Averaging PSO
  4. Fractional-Order PSO (FO-PSO)
  5. Angle-based PSO (A-PSO)
  6. Non-linear Attraction PSO (NL-PSO)
  7. Mean-based / Top-K Attraction PSO (MB-PSO)
  8. Comprehensive Learning PSO (CLPSO)
  9. Levy Flight PSO (LFPSO)
  10. Quantum-inspired PSO (QPSO / Q-SPSO)
  11. Quantum + Linear Decay PSO (Q-LDPSO)
  12. Quantum + Top-K Mean-Based PSO (Q-MBPSO)
  13. 5D Search Space PSO (PSO-5D)
  14. Non-linear Cosine Annealing QPSO (QPSO-Nonlinear)
  15. Fitness-adaptive QPSO (QPSO-Adaptive)
  16. Per-particle Adaptive Beta QPSO (QPSO-PerParticle)
  17. Opposition-based Quantum PSO (OQ-PSO)
"""

from .linear_decay import LinearDecayPSO, run_pso_linear_decay
from .constriction import ConstrictionPSO, run_cpso, compute_constriction_factor
from .fitness_avg import FitnessAvgPSO, run_pso_fitness_avg
from .fopso import FOPSO, run_fopso
from .apso import APSO, run_apso
from .nl_pso import NLPSO, run_nl_pso
from .mb_pso import MBPSO, run_mb_pso
from .clpso import CLPSO, run_clpso
from .lfpso import LFPSO, run_lfpso
from .qpso import QPSO, run_qpso, run_q_spso
from .q_ldpso import QLDPSO, run_q_ldpso
from .q_mbpso import QMBPSO, run_q_mbpso
from .pso_5d import PSO5D, run_pso_5d
from .qpso_nonlinear import QPSONonlinear, run_qpso_nonlinear
from .qpso_adaptive import QPSOAdaptive, run_qpso_adaptive
from .qpso_per_particle import QPSOPerParticle, run_qpso_per_particle
from .oq_pso import OQPSO, run_oq_pso

__all__ = [
    # Classes
    "LinearDecayPSO",
    "ConstrictionPSO",
    "FitnessAvgPSO",
    "FOPSO",
    "APSO",
    "NLPSO",
    "MBPSO",
    "CLPSO",
    "LFPSO",
    "QPSO",
    "QLDPSO",
    "QMBPSO",
    "PSO5D",
    "QPSONonlinear",
    "QPSOAdaptive",
    "QPSOPerParticle",
    "OQPSO",
    # Functions
    "run_pso_linear_decay",
    "run_cpso",
    "compute_constriction_factor",
    "run_pso_fitness_avg",
    "run_fopso",
    "run_apso",
    "run_nl_pso",
    "run_mb_pso",
    "run_clpso",
    "run_lfpso",
    "run_qpso",
    "run_q_spso",
    "run_q_ldpso",
    "run_q_mbpso",
    "run_pso_5d",
    "run_qpso_nonlinear",
    "run_qpso_adaptive",
    "run_qpso_per_particle",
    "run_oq_pso",
]
