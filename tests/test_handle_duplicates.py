#from data.data_transformation import handle_duplicates
import sys
import os
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.data_transformation import handle_duplicates


def test_remove_duplicates():
    """Test removing duplicate rows."""
    data = {"A": [1, 1, 2, 3], "B": [4, 4, 5, 6]}
    df = pd.DataFrame(data)
    df_cleaned = handle_duplicates(df, handle_dupes="Remove")
    assert df_cleaned.shape[0] == 3  # One duplicate should be removed (1,4)


def test_no_duplicates():
    """Test when no duplicates are present."""
    data = {"A": [1, 2, 3], "B": [4, 5, 6]}
    df = pd.DataFrame(data)
    df_cleaned = handle_duplicates(df, handle_dupes="Remove")
    assert df_cleaned.equals(df)  # No changes expected