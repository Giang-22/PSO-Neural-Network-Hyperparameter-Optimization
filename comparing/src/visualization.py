"""
Visualization Module for PSO Criteria Comparison
Features clean aesthetics, harmonious pastel palettes, and square aspect ratios for 2D search maps.
"""

from typing import List, Dict, Any, Tuple
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Harmonious, modern color palette
PALETTE = {
    'primary': '#3498db',     # Soft pastel blue
    'secondary': '#2ecc71',   # Soft pastel green
    'accent': '#e74c3c',      # Soft coral / red
    'purple': '#9b59b6',      # Soft purple
    'yellow': '#f1c40f',      # Soft amber
    'dark': '#2c3e50',        # Deep navy/slate
    'gray': '#7f8c8d',        # Muted gray
    'light_gray': '#ecf0f1',  # Light background gray
    'cyan': '#1abc9c'         # Turquoise
}


def setup_plot_style():
    """Thiết lập style chuẩn, thẩm mỹ cao cho Matplotlib."""
    plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
    plt.rcParams['axes.edgecolor'] = '#bdc3c7'
    plt.rcParams['axes.linewidth'] = 0.8
    plt.rcParams['grid.color'] = '#e0e0e0'
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.alpha'] = 0.6


def plot_convergence_and_diversity(result: Dict[str, Any], func_name: str = 'Rastrigin', title_suffix: str = ''):
    """
    Biểu đồ 2 ô:
    1. Đường cong hội tụ Gbest & Mean qua các vòng lặp (Log-scale / Linear)
    2. Sự suy giảm độ đa dạng bầy đàn (Swarm Diversity) & Vận tốc trung bình (Average Velocity)
    """
    setup_plot_style()
    iters = np.arange(len(result['history_gbest']))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f'Tiêu chí Hội tụ & Động học Quần thể — Standard PSO ({func_name} Function){title_suffix}',
                 fontsize=14, fontweight='bold', y=1.02)

    # 1. Convergence Curve
    ax1.plot(iters, result['history_gbest'], color=PALETTE['primary'], lw=2.2, label='Gbest Fitness (Nghiệm tốt nhất)')
    ax1.plot(iters, result['history_mean'], color=PALETTE['gray'], lw=1.5, ls='--', alpha=0.7, label='Swarm Mean Fitness')
    ax1.set_xlabel('Iteration (Vòng lặp)', fontsize=11)
    ax1.set_ylabel('Objective Value (Giá trị hàm mục tiêu)', fontsize=11)
    ax1.set_title('1. Tốc độ & Xu hướng Hội tụ (Convergence Profile)', fontsize=12, fontweight='bold')
    ax1.grid(True)
    if np.min(result['history_gbest']) > 0 and np.max(result['history_gbest']) / (np.min(result['history_gbest']) + 1e-12) > 100:
        ax1.set_yscale('log')
    ax1.legend(frameon=True, facecolor='white', framealpha=0.9)

    # 2. Diversity & Velocity
    color_div = PALETTE['secondary']
    color_vel = PALETTE['accent']

    ax2.plot(iters, result['history_diversity'], color=color_div, lw=2.0, label='Swarm Diversity (Khoảng cách tới tâm)')
    ax2.set_xlabel('Iteration (Vòng lặp)', fontsize=11)
    ax2.set_ylabel('Độ đa dạng bầy đàn', color=color_div, fontsize=11)
    ax2.tick_params(axis='y', labelcolor=color_div)
    ax2.grid(True)

    ax2_twin = ax2.twinx()
    ax2_twin.plot(iters, result['history_avg_velocity'], color=color_vel, lw=1.8, ls=':', label='Vận tốc TB (Avg Velocity)')
    ax2_twin.set_ylabel('Độ lớn vận tốc TB (|V|)', color=color_vel, fontsize=11)
    ax2_twin.tick_params(axis='y', labelcolor=color_vel)

    ax2.set_title('2. Cân bằng Khám phá - Khai thác & Động học Vận tốc', fontsize=12, fontweight='bold')
    
    # Combined legend
    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right', frameon=True, facecolor='white', framealpha=0.9)

    plt.tight_layout()
    return fig


def plot_particle_trajectories_2d(
    result: Dict[str, Any],
    func,
    bounds: Tuple[float, float] = (-5.12, 5.12),
    func_name: str = 'Rastrigin'
):
    """
    Trực quan hóa không gian tìm kiếm 2D với tỉ lệ vuông vắn (square aspect ratio),
    đường đồng mức (contour lines) và quỹ đạo dịch chuyển của các hạt từ t=0 đến kết thúc.
    """
    setup_plot_style()
    positions = result['positions']  # shape: (n_iter+1, n_particles, 2)
    n_iter, n_particles, dim = positions.shape

    # Generate Contour Grid
    grid_res = 120
    x_lin = np.linspace(bounds[0], bounds[1], grid_res)
    y_lin = np.linspace(bounds[0], bounds[1], grid_res)
    X_grid, Y_grid = np.meshgrid(x_lin, y_lin)
    pts = np.column_stack([X_grid.ravel(), Y_grid.ravel()])
    Z_grid = func(pts).reshape((grid_res, grid_res))

    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Contour fill with muted pastel colormap
    cp = ax.contourf(X_grid, Y_grid, Z_grid, levels=30, cmap='YlGnBu', alpha=0.55)
    ax.contour(X_grid, Y_grid, Z_grid, levels=15, colors='#7f8c8d', linewidths=0.5, alpha=0.4)
    plt.colorbar(cp, ax=ax, shrink=0.78, label='Fitness Landscape f(x)')

    # Draw particle trajectories (lines)
    for p in range(n_particles):
        p_traj = positions[:, p, :]
        ax.plot(p_traj[:, 0], p_traj[:, 1], color='#95a5a6', lw=0.8, alpha=0.5, zorder=2)

    # Initial positions (t=0)
    ax.scatter(positions[0, :, 0], positions[0, :, 1], 
               color=PALETTE['primary'], s=45, alpha=0.85, edgecolors='white', lw=0.6,
               label=f'Khởi tạo (t=0, N={n_particles})', zorder=3)

    # Final positions (t=T)
    ax.scatter(positions[-1, :, 0], positions[-1, :, 1], 
               color=PALETTE['accent'], s=55, alpha=0.9, marker='o', edgecolors='black', lw=0.8,
               label=f'Kết thúc (t={n_iter-1})', zorder=4)

    # Global Best Position
    gbest = result['gbest_pos']
    ax.scatter(gbest[0], gbest[1], 
               color=PALETTE['yellow'], s=160, marker='*', edgecolors='black', lw=1.2,
               label=f'Gbest [x1={gbest[0]:.2f}, x2={gbest[1]:.2f}]', zorder=5)

    ax.set_aspect('equal')
    ax.set_xlim(bounds[0], bounds[1])
    ax.set_ylim(bounds[0], bounds[1])
    ax.set_xlabel('Chiều X1', fontsize=11)
    ax.set_ylabel('Chiều X2', fontsize=11)
    ax.set_title(f'Phân bố & Quỹ đạo hạt trên Không gian tìm kiếm — {func_name}\n(Tỉ lệ vuông 1:1, Khám phá vs Khai thác)', 
                 fontsize=12, fontweight='bold', pad=12)
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.legend(loc='upper right', frameon=True, facecolor='white', framealpha=0.9)

    plt.tight_layout()
    return fig


def plot_parameter_sensitivity(
    results_dict: Dict[str, Dict[str, Any]],
    param_name: str,
    criterion: str = 'Convergence & Diversity'
):
    """
    So sánh độ nhạy tham số (Inertia Weight w, Acceleration c1/c2, Swarm Size N).
    """
    setup_plot_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f'Phân tích Độ nhạy Tiêu chí theo Tham số: {param_name}', 
                 fontsize=14, fontweight='bold', y=1.02)

    colors = [PALETTE['primary'], PALETTE['secondary'], PALETTE['accent'], PALETTE['purple']]

    for i, (label, res) in enumerate(results_dict.items()):
        c = colors[i % len(colors)]
        iters = np.arange(len(res['history_gbest']))
        ax1.plot(iters, res['history_gbest'], color=c, lw=2.0, label=label)
        ax2.plot(iters, res['history_diversity'], color=c, lw=2.0, label=label)

    # 1. Convergence
    ax1.set_xlabel('Iteration (Vòng lặp)', fontsize=11)
    ax1.set_ylabel('Gbest Fitness', fontsize=11)
    ax1.set_title(f'1. Ảnh hưởng tới Tốc độ Hội tụ (Convergence)', fontsize=12, fontweight='bold')
    ax1.grid(True)
    ax1.legend(frameon=True, facecolor='white')

    # 2. Diversity
    ax2.set_xlabel('Iteration (Vòng lặp)', fontsize=11)
    ax2.set_ylabel('Swarm Diversity', fontsize=11)
    ax2.set_title(f'2. Ảnh hưởng tới Độ đa dạng Quần thể (Exploration)', fontsize=12, fontweight='bold')
    ax2.grid(True)
    ax2.legend(frameon=True, facecolor='white')

    plt.tight_layout()
    return fig


def plot_robustness_boxplots(benchmark_runs: Dict[str, List[float]]):
    """
    Biểu đồ Boxplot so sánh độ ổn định (Stability / Robustness) qua nhiều lần chạy ngẫu nhiên.
    """
    setup_plot_style()
    fig, ax = plt.subplots(figsize=(9, 5))

    names = list(benchmark_runs.keys())
    data = [benchmark_runs[name] for name in names]

    bp = ax.boxplot(data, patch_artist=True, labels=names,
                    boxprops=dict(facecolor='#a8d8ea', color='#2c3e50', lw=1.2),
                    whiskerprops=dict(color='#2c3e50', lw=1.2),
                    capprops=dict(color='#2c3e50', lw=1.2),
                    medianprops=dict(color='#e74c3c', lw=1.8),
                    flierprops=dict(marker='o', color='#e74c3c', markersize=5))

    colors = [PALETTE['primary'], PALETTE['secondary'], PALETTE['cyan'], PALETTE['purple']]
    for patch, c in zip(bp['boxes'], colors * 3):
        patch.set_facecolor(c)
        patch.set_alpha(0.65)

    ax.set_ylabel('Sai số / Giá trị hàm mục tiêu (Error)', fontsize=11)
    ax.set_title('Đánh giá Tiêu chí Độ ổn định (Robustness & Stability across Runs)', 
                 fontsize=12, fontweight='bold', pad=12)
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    return fig


def plot_real_datasets_scatter(
    bank_ckpt_path: str,
    covertype_ckpt_path: str,
    title: str = 'Biểu đồ Phân tán Hạt Standard PSO trên 2 Bộ Dữ liệu Thực nghiệm (Tỉ lệ vuông 1:1)'
):
    """
    Vẽ 2 biểu đồ phân tán hạt cạnh nhau với tỉ lệ vuông 1:1 cho Bank Marketing và Forest Covertype.
    """
    import joblib
    setup_plot_style()

    b_data = joblib.load(bank_ckpt_path)
    c_data = joblib.load(covertype_ckpt_path)

    hist_b = b_data['history']
    hist_c = c_data['history']

    fig = plt.figure(figsize=(15, 7))
    gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.25)

    def _draw_sub(ax, hist, dataset_name):
        scores = hist['score']
        vmin = max(float(np.percentile(scores, 5)), float(scores.max() - 0.025))
        vmax = float(scores.max())
        
        sc = ax.scatter(
            hist['n_neurons'], np.log10(hist['lr']),
            c=scores, cmap='RdYlGn', vmin=vmin, vmax=vmax,
            alpha=0.65, s=50, edgecolors='grey', lw=0.4
        )
        cbar = plt.colorbar(sc, ax=ax, fraction=0.046, pad=0.04)
        cbar.set_label('CV Accuracy', fontsize=10)

        best_row = hist.loc[hist['score'].idxmax()]
        n_best = int(best_row['n_neurons'])
        lr_best = best_row['lr']
        cv_best = best_row['score']

        ax.scatter(
            n_best, np.log10(lr_best), c='#e74c3c', s=260, marker='*',
            edgecolors='black', lw=1.2, zorder=6,
            label=f"gbest: N={n_best}, lr={lr_best:.5f}\n(CV Acc: {cv_best:.4f})"
        )

        ax.set_box_aspect(1)
        ax.set_xlabel('Số lượng nơ-ron ẩn (n_neurons)', fontsize=11)
        ax.set_ylabel(r'$\log_{10}(\mathrm{learning\_rate})$', fontsize=11)
        ax.set_title(f'Standard PSO — {dataset_name}', fontsize=12, fontweight='bold', pad=10)
        ax.set_xlim(10, 260)
        ax.set_ylim(-4.2, -0.8)
        ax.grid(True, linestyle='--', alpha=0.4)
        ax.legend(loc='lower left', fontsize=9, framealpha=0.9)

    _draw_sub(fig.add_subplot(gs[0, 0]), hist_b, 'Bank Marketing Dataset')
    _draw_sub(fig.add_subplot(gs[0, 1]), hist_c, 'Forest Covertype Dataset')

    fig.suptitle(title, fontsize=14, fontweight='bold', y=0.98)
    return fig

