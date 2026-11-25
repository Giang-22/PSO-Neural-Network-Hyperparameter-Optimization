"""
Data preprocessing, encoding, scaling, and splitting module.
"""

from typing import Tuple
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler


def preprocess_data(
    df: pd.DataFrame, 
    target_col: str = "y", 
    test_size: float = 0.2, 
    random_seed: int = 42
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, StandardScaler]:
    """
    Tiền xử lý dữ liệu: Mã hóa nhãn mục tiêu, One-Hot Encoding biến phân loại, 
    chuẩn hóa StandardScaler và chia tập Train/Test.
    
    Args:
        df: DataFrame đầu vào.
        target_col: Tên cột mục tiêu.
        test_size: Tỉ lệ tập test.
        random_seed: Seed ngẫu nhiên.
        
    Returns:
        Tuple: (X_train, X_test, y_train, y_test, scaler)
    """
    # Sẽ được hoàn thiện hoặc tùy chỉnh từ notebook
    pass


def prepare_kfold(n_splits: int = 3, random_seed: int = 42) -> StratifiedKFold:
    """
    Khởi tạo StratifiedKFold cho đánh giá hàm fitness.
    """
    return StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_seed)
