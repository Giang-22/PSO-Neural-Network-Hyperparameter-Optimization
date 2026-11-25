"""
Data loading module for reading raw dataset files.
"""

import os
import pandas as pd


def load_raw_data(filepath: str = "data/raw/bank.csv") -> pd.DataFrame:
    """
    Load raw bank dataset from CSV file.
    
    Args:
        filepath: Đường dẫn tới file CSV.
        
    Returns:
        pd.DataFrame: DataFrame chứa dữ liệu thô.
    """
    if not os.path.exists(filepath):
        # Fallback if run from different working dir
        if os.path.exists(os.path.join("..", filepath)):
            filepath = os.path.join("..", filepath)
        elif os.path.exists("bank.csv"):
            filepath = "bank.csv"
            
    df = pd.read_csv(filepath)
    return df
