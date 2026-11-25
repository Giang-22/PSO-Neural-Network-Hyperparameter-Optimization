"""
Data preprocessing, scaling, sampling, and splitting module for Covertype.
"""

from typing import Tuple, Optional
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from .loader import ALL_FEATURE_COLS, TARGET_COL


def preprocess_data(
    df: pd.DataFrame, 
    target_col: str = TARGET_COL, 
    test_size: float = 0.2, 
    sample_size: Optional[int] = 30000,
    random_seed: int = 42
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, StandardScaler]:
    """
    Tiền xử lý dữ liệu Covertype:
      - Tùy chọn Stratified Sampling (mặc định 30,000 mẫu để tối ưu siêu tham số nhanh chóng).
      - Chuẩn hóa nhãn mục tiêu về 0-indexed (0 đến 6).
      - Chia tập Train/Test theo StratifiedKFold/train_test_split.
      - Chuẩn hóa đặc trưng bằng StandardScaler.
      
    Args:
        df: DataFrame đầu vào.
        target_col: Tên cột mục tiêu ('Cover_Type').
        test_size: Tỉ lệ tập test.
        sample_size: Kích thước mẫu phân tầng (None để dùng toàn bộ 581,012 mẫu).
        random_seed: Seed ngẫu nhiên.
        
    Returns:
        Tuple: (X_train_sc, X_test_sc, y_train, y_test, scaler)
    """
    working_df = df
    if sample_size is not None and sample_size < len(df):
        working_df, _ = train_test_split(
            df, 
            train_size=sample_size, 
            stratify=df[target_col], 
            random_state=random_seed
        )

    feature_cols = [c for c in working_df.columns if c != target_col]
    X = working_df[feature_cols].values
    # Chuyển đổi nhãn về 0-indexed (0 đến 6) cho mạng nơ-ron đa lớp
    y = (working_df[target_col].values - 1).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_seed, stratify=y
    )

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc = scaler.transform(X_test)

    return X_train_sc, X_test_sc, y_train, y_test, scaler


def prepare_kfold(n_splits: int = 3, random_seed: int = 42) -> StratifiedKFold:
    """
    Khởi tạo StratifiedKFold cho đánh giá hàm fitness.
    """
    return StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_seed)
