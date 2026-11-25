"""
PSO Criteria Comparison Framework
Main Execution Script
Runs the standard criteria evaluation suite for Standard PSO and exports figures/tables.
"""

import os
import sys

# Ensure UTF-8 output on Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Thêm đường dẫn project
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from src.benchmarks import BENCHMARK_SUITE
from src.standard_pso import StandardPSO
from src.metrics import compute_run_metrics, aggregate_experiment_metrics
from src.visualization import (
    plot_convergence_and_diversity,
    plot_particle_trajectories_2d,
    plot_parameter_sensitivity,
    plot_robustness_boxplots
)
import matplotlib.pyplot as plt


def main():
    print("=" * 70)
    print("    PSO CRITERIA COMPARISON & BENCHMARKING FRAMEWORK")
    print("=" * 70)

    figures_dir = os.path.join(ROOT_DIR, "results", "figures")
    os.makedirs(figures_dir, exist_ok=True)

    # 1. Thử nghiệm trên hàm Rastrigin (kiểm tra Exploration & Premature Convergence)
    print("\n[1/4] Đang chạy Standard PSO trên hàm mục tiêu Rastrigin...")
    bench = BENCHMARK_SUITE['Rastrigin']
    pso = StandardPSO(
        fitness_func=bench['func'],
        dim=2,
        bounds=bench['bounds'],
        n_particles=25,
        max_iter=40,
        w=0.7,
        c1=1.5,
        c2=1.5,
        random_seed=42
    )
    res_rastrigin = pso.optimize(verbose=False)
    metrics = compute_run_metrics(res_rastrigin, optimum=bench['optimum'])
    print(f"  -> Nghiệm tốt nhất Gbest: {metrics['Final_Value']:.6f}")
    print(f"  -> Độ đa dạng ban đầu: {metrics['Initial_Diversity']:.4f} -> Cuối: {metrics['Final_Diversity']:.4f} (Giảm {metrics['Diversity_Reduction_Pct']:.1f}%)")
    print(f"  -> Vận tốc trung bình bầy: {metrics['Avg_Velocity_Mean']:.4f}")

    # Vẽ và lưu biểu đồ hội tụ & đa dạng
    fig1 = plot_convergence_and_diversity(res_rastrigin, func_name='Rastrigin')
    fig1_path = os.path.join(figures_dir, "rastrigin_convergence_diversity.png")
    fig1.savefig(fig1_path, dpi=200, bbox_inches='tight')
    plt.close(fig1)
    print(f"  -> Đã lưu biểu đồ: {fig1_path}")

    # Vẽ và lưu biểu đồ quỹ đạo hạt 2D (tỉ lệ vuông)
    fig2 = plot_particle_trajectories_2d(res_rastrigin, func=bench['func'], bounds=bench['bounds'], func_name='Rastrigin')
    fig2_path = os.path.join(figures_dir, "rastrigin_particles_trajectory_2d.png")
    fig2.savefig(fig2_path, dpi=200, bbox_inches='tight')
    plt.close(fig2)
    print(f"  -> Đã lưu biểu đồ: {fig2_path}")

    # 2. Phân tích độ nhạy của Trọng số quán tính w
    print("\n[2/4] Đang phân tích độ nhạy của Trọng số quán tính (Inertia Weight w)...")
    w_experiments = {}
    for w_val in [0.4, 0.7, 0.9]:
        optimizer = StandardPSO(
            fitness_func=bench['func'],
            dim=2,
            bounds=bench['bounds'],
            n_particles=25,
            max_iter=40,
            w=w_val,
            c1=1.5,
            c2=1.5,
            random_seed=42
        )
        w_experiments[f"w = {w_val}"] = optimizer.optimize()

    fig3 = plot_parameter_sensitivity(w_experiments, param_name="Inertia Weight (w)")
    fig3_path = os.path.join(figures_dir, "sensitivity_inertia_weight_w.png")
    fig3.savefig(fig3_path, dpi=200, bbox_inches='tight')
    plt.close(fig3)
    print(f"  -> Đã lưu biểu đồ: {fig3_path}")

    # 3. Phân tích độ ổn định qua nhiều lần chạy (Robustness across 15 seeds)
    print("\n[3/4] Đánh giá tính ổn định (Robustness) qua 15 seeds ngẫu nhiên...")
    runs = []
    box_data = {"Sphere": [], "Rastrigin": []}
    for b_name in ["Sphere", "Rastrigin"]:
        b_info = BENCHMARK_SUITE[b_name]
        for s in range(15):
            opt = StandardPSO(
                fitness_func=b_info['func'],
                dim=2,
                bounds=b_info['bounds'],
                n_particles=20,
                max_iter=30,
                random_seed=s * 10 + 7
            )
            r = opt.optimize()
            box_data[b_name].append(r['gbest_val'])
            if b_name == "Rastrigin":
                runs.append(r)

    fig4 = plot_robustness_boxplots(box_data)
    fig4_path = os.path.join(figures_dir, "multi_run_robustness_boxplot.png")
    fig4.savefig(fig4_path, dpi=200, bbox_inches='tight')
    plt.close(fig4)
    print(f"  -> Đã lưu biểu đồ: {fig4_path}")

    # 4. Biểu đồ phân tán Standard PSO trên 2 bộ dữ liệu thực nghiệm (Bank Marketing & Covertype)
    print("\n[4/5] Đang vẽ biểu đồ phân tán hạt Standard PSO trên 2 bộ dữ liệu thực nghiệm...")
    bank_ckpt = os.path.join(ROOT_DIR, "..", "bank_marketing", "results", "checkpoints", "standard_pso.pkl")
    covertype_ckpt = os.path.join(ROOT_DIR, "..", "covertype", "results", "checkpoints", "standard_pso.pkl")
    if os.path.exists(bank_ckpt) and os.path.exists(covertype_ckpt):
        from src.visualization import plot_real_datasets_scatter
        fig_real_sc = plot_real_datasets_scatter(bank_ckpt, covertype_ckpt)
        fig_real_path = os.path.join(figures_dir, "standard_pso_datasets_scatter.png")
        fig_real_sc.savefig(fig_real_path, dpi=200, bbox_inches='tight')
        plt.close(fig_real_sc)
        print(f"  -> Đã lưu biểu đồ phân tán 2 bộ dữ liệu: {fig_real_path}")
    else:
        print("  -> Bỏ qua vì chưa tìm thấy file checkpoint.")

    # 5. Xuất bảng tổng hợp tiêu chí
    print("\n[5/5] Bảng tổng hợp các tiêu chí đánh giá Standard PSO (Rastrigin):")
    summary_df = aggregate_experiment_metrics(runs, optimum=0.0)
    print(summary_df.to_string(index=False))

    print("\n" + "=" * 70)
    print(f"✅ Hoàn thành thử nghiệm! Tất cả biểu đồ đã được lưu trong: {figures_dir}")
    print("=" * 70)


if __name__ == "__main__":
    main()
