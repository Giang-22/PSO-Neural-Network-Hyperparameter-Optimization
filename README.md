# Velocity-Adaptive vs. Quantum-Behaved Particle Swarm Optimization for Neural Network Hyperparameter Tuning

Empirical comparative benchmark evaluating **15 Particle Swarm Optimization (PSO) algorithms**—spanning classical/novel Newtonian velocity-adaptive dynamics and velocity-free Quantum-behaved PSO (QPSO) variants—for **Multilayer Perceptron (MLP)** hyperparameter optimization ($n_{\mathrm{neurons}}$, learning rate $\eta$, L2 penalty $\alpha$) across tabular classification benchmarks.

## Repository Structure

```text
PSO/
├── bank_marketing/                 # Binary classification benchmark (Bank Marketing)
│   ├── configs/                    # YAML configuration
│   ├── data/                       # [Ignored in Git] Place raw bank.csv in data/raw/
│   ├── notebooks/                  # Training, checkpoint evaluation, and plotting notebooks
│   ├── results/
│   │   ├── checkpoints/            # Saved optimization histories (.pkl)
│   │   ├── figures/                # Convergence & search-space plots
│   │   └── test_results/           # Final holdout results (test_accuracy.csv)
│   └── src/                        # Modular data loader, MLP fitness, optimizers & utils
├── covertype/                      # 7-class tabular benchmark (Forest Covertype, 30k subsample)
│   ├── configs/
│   ├── data/                       # [Ignored in Git] Place covtype.data in data/raw/covertype/
│   ├── notebooks/
│   ├── results/
│   │   ├── checkpoints/
│   │   ├── figures/
│   │   └── test_results/           # Final holdout results (test_accuracy.csv)
│   └── src/
├── comparing/                      # Standard PSO benchmark behavior & diagnostic scripts
│   ├── notebooks/
│   ├── results/figures/
│   └── src/
├── latex/
│   ├── figures/, fonts/, tables/   # Shared figure assets & result LaTeX tables
│   └── The Joural of Finance and Data Science/
│       ├── main.tex                # Elsevier / KeAi JFDS formatted submission manuscript
│       ├── main.pdf                # Compiled 22-page JFDS manuscript
│       ├── figures/, fonts/, pictures/
│       └── *.py                    # Reference & font helper utilities
├── references/
│   └── all/                        # Master BibTeX database (references.bib) & build scripts
├── requirements.txt
└── .gitignore
```

## Investigated Algorithms (15 Variants)

- **Baseline & Classical Velocity Improvements:** `Standard PSO` ($w=0.7$), `LD-PSO` (Linear Decay $w$), `FA-PSO` (Multi-Seed Fitness Averaging, $k=3$), `CPSO` (Clerc Constriction $K \approx 0.7298$)
- **Novel Velocity Enhancements:** `FO-PSO` (Grünwald–Letnikov Fractional Memory, $r=4, \alpha_{\mathrm{FO}}=0.6$), `A-PSO` (Directional Cosine Adjustment), `NL-PSO` (Exponential Saturation Attraction), `MB-PSO` (Tri-Attractor Consensus)
- **Quantum-Behaved Formulations (QPSO):** `QPSO` (Canonical Linear Decay $\beta: 1.0 \to 0.5$), `Q-LDPSO` (Linear Attractor Modulation), `Q-MBPSO` (Top-$K=3$ Elite Mean-Best), `NL-QPSO` (Cosine-Annealing $\beta$), `FA-QPSO` (Fitness-Adaptive Stagnation Reboot), `PP-QPSO` (Per-Particle Distance-Adaptive $\beta_i$), `OQ-PSO` (Opposition-Based Initialization & Dynamic Jumping)

## Key Holdout Results (`RANDOM_SEED=42`)

| Algorithm | Bank Marketing Test Acc. | Forest Covertype Test Acc. | Mean Rank |
| :--- | :---: | :---: | :---: |
| **LD-PSO** | **0.8580** | 0.8537 | **1.5** |
| **FO-PSO** | 0.8562 (125 units) | 0.8535 | **2.5** |
| **Q-MBPSO** | 0.8562 | 0.8520 | **3.0** |
| **Q-LDPSO** | 0.8424 | **0.8542** | 7.5 |
| **Standard PSO** | 0.8518 (214 units) | 0.8507 | 9.0 |

## Setup & Local Dataset Placement

Raw datasets are excluded from version control via `.gitignore`. To reproduce notebook runs locally:

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Place datasets in their expected local paths:
   - **Bank Marketing:** `bank_marketing/data/raw/bank.csv` (11,162 records, 16 raw attributes)
   - **Forest Covertype:** `covertype/data/raw/covertype/covtype.data` (UCI Covertype corpus, 54 features)
3. Run notebooks under `bank_marketing/notebooks/` and `covertype/notebooks/` (or compile manuscripts in `latex/` using `xelatex`).
