"""
Data loading module for reading Covertype dataset files.
"""

import os
from typing import List, Optional
import pandas as pd

CONTINUOUS_COLS = [
    'Elevation', 'Aspect', 'Slope',
    'Horizontal_Distance_To_Hydrology', 'Vertical_Distance_To_Hydrology',
    'Horizontal_Distance_To_Roadways',
    'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm',
    'Horizontal_Distance_To_Fire_Points'
]
WILDERNESS_COLS = [f'Wilderness_Area_{i}' for i in range(1, 5)]
SOIL_COLS = [f'Soil_Type_{i}' for i in range(1, 41)]
ALL_FEATURE_COLS = CONTINUOUS_COLS + WILDERNESS_COLS + SOIL_COLS
TARGET_COL = 'Cover_Type'
COLUMN_NAMES = ALL_FEATURE_COLS + [TARGET_COL]

COVER_TYPE_NAMES = {
    1: 'Spruce/Fir',
    2: 'Lodgepole Pine',
    3: 'Ponderosa Pine',
    4: 'Cottonwood/Willow',
    5: 'Aspen',
    6: 'Douglas-fir',
    7: 'Krummholz'
}


def load_raw_data(filepath: str = "data/raw/covertype/covtype.data") -> pd.DataFrame:
    """
    Load raw Covertype dataset from CSV/data file and assign column names.
    
    Args:
        filepath: Đường dẫn tới file covtype.data.
        
    Returns:
        pd.DataFrame: DataFrame chứa 581,012 mẫu và 55 cột.
    """
    if not os.path.exists(filepath):
        # Fallback if run from notebooks/ or another directory
        if os.path.exists(os.path.join("..", filepath)):
            filepath = os.path.join("..", filepath)
        elif os.path.exists("covtype.data"):
            filepath = "covtype.data"
        elif os.path.exists("data/raw/covertype/covtype.data"):
            filepath = "data/raw/covertype/covtype.data"

    df = pd.read_csv(filepath, header=None, names=COLUMN_NAMES)
    return df
