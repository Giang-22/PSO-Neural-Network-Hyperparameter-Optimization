"""
Optimizers module containing Base PSO, Standard PSO and all its variants.
"""

from .base import BasePSO
from .standard_pso import StandardPSO, run_standard_pso
from .variants.linear_decay import LinearDecayPSO, run_pso_linear_decay
from .variants.constriction import ConstrictionPSO, run_cpso, compute_constriction_factor
from .variants.fitness_avg import FitnessAvgPSO, run_pso_fitness_avg
from .variants.fopso import FOPSO, run_fopso
from .variants.apso import APSO, run_apso
from .variants.nl_pso import NLPSO, run_nl_pso
from .variants.mb_pso import MBPSO, run_mb_pso
from .variants.clpso import CLPSO, run_clpso
from .variants.lfpso import LFPSO, run_lfpso
from .variants.qpso import QPSO, run_qpso, run_q_spso
from .variants.q_ldpso import QLDPSO, run_q_ldpso
from .variants.q_mbpso import QMBPSO, run_q_mbpso
from .variants.pso_5d import PSO5D, run_pso_5d
from .variants.qpso_nonlinear import QPSONonlinear, run_qpso_nonlinear
from .variants.qpso_adaptive import QPSOAdaptive, run_qpso_adaptive
from .variants.qpso_per_particle import QPSOPerParticle, run_qpso_per_particle
from .variants.oq_pso import OQPSO, run_oq_pso

__all__ = [
    # Classes
    "BasePSO",
    "StandardPSO",
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
    "run_standard_pso",
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
