import pytest
import pandas as pd
import numpy as np
import io


@pytest.fixture
def sample_csv_file():
    """Creates a mock CSV file."""
    csv_content = "A,B,C\n1,2,3\n4,5,6\n7,8,9"
    return io.StringIO(csv_content)


@pytest.fixture
def sample_df_with_missing():
    """Creates a sample DataFrame with missing values."""
    data = {
        "A": [1, 2, np.nan, 4],
        "B": [np.nan, 2, 3, 4],
        "C": ["X", np.nan, "Z", "Y"]
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_df_with_outliers():
    """Creates a DataFrame with outliers."""
    data = {
        "A": [1, 2, 3, 1000],  # 1000 is an outlier
        "B": [10, 20, 30, 40],
    }
    return pd.DataFrame(data)
