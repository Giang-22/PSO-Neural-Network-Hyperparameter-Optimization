"""
Evaluation Criteria and Metrics for PSO Optimization
"""

from typing import Dict, Any, List
import numpy as np
import pandas as pd


def compute_run_metrics(result: Dict[str, Any], optimum: float = 0.0, tol: float = 1e-3) -> Dict[str, Any]:
    """
    Tính toán các chỉ số tiêu chí đánh giá từ một lần chạy PSO:
    1. Error: Sai số so với cực trị lý thuyết.
    2. Convergence Iteration: Vòng lặp đầu tiên sai số nhỏ hơn tol.
    3. Final Diversity: Độ đa dạng quần thể ở vòng lặp cuối.
    4. Diversity Reduction Rate: Tốc độ suy giảm độ đa dạng.
    5. Mean Velocity: Vận tốc trung bình của bầy đàn.
    6. Runtime: Thời gian tính toán (s).
    """
    history_gbest = result['history_gbest']
    history_div = result['history_diversity']
    history_vel = result['history_avg_velocity']
    final_val = result['gbest_val']
    error = abs(final_val - optimum)

    # Vòng lặp hội tụ theo ngưỡng dung sai tol
    hit_indices = np.where(history_gbest - optimum <= tol)[0]
    iter_conv = int(hit_indices[0]) if len(hit_indices) > 0 else len(history_gbest) - 1

    init_div = history_div[0] if history_div[0] > 0 else 1e-9
    final_div = history_div[-1]
    div_reduction = (init_div - final_div) / init_div * 100.0

    return {
        'Final_Value': final_val,
        'Absolute_Error': error,
        'Convergence_Iter': iter_conv,
        'Initial_Diversity': init_div,
        'Final_Diversity': final_div,
        'Diversity_Reduction_Pct': div_reduction,
        'Avg_Velocity_Mean': float(np.mean(history_vel)),
        'Final_Velocity': float(history_vel[-1]),
        'Runtime_Sec': result['elapsed_time']
    }


def aggregate_experiment_metrics(runs_results: List[Dict[str, Any]], optimum: float = 0.0) -> pd.DataFrame:
    """
    Tổng hợp thống kê qua nhiều lần chạy (Mean, Std, Min, Max).
    """
    all_metrics = [compute_run_metrics(r, optimum=optimum) for r in runs_results]
    df = pd.DataFrame(all_metrics)
    
    summary = {
        'Criterion (Tiêu chí)': [
            'Best Fitness (Nghiệm tốt nhất)',
            'Mean Fitness (Trung bình)',
            'Worst Fitness (Kém nhất)',
            'Std Fitness (Độ lệch chuẩn - Tính ổn định)',
            'Mean Convergence Iter (Vòng lặp hội tụ TB)',
            'Final Diversity (Độ đa dạng cuối)',
            'Mean Runtime (Thời gian chạy TB - giây)'
        ],
        'Value (Giá trị)': [
            f"{df['Final_Value'].min():.6e}",
            f"{df['Final_Value'].mean():.6e}",
            f"{df['Final_Value'].max():.6e}",
            f"{df['Final_Value'].std():.6e}",
            f"{df['Convergence_Iter'].mean():.1f}",
            f"{df['Final_Diversity'].mean():.4f}",
            f"{df['Runtime_Sec'].mean():.4f}"
        ]
    }
    return pd.DataFrame(summary)
