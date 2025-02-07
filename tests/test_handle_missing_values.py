from data.data_transformation import handle_missing_values


def test_fill_missing_mean(sample_df_with_missing):
    """Test filling missing values with the mean."""
    df_filled = handle_missing_values(sample_df_with_missing, strategy="mean")
    assert df_filled.isnull().sum().sum() == 0  # No missing values


def test_fill_missing_median(sample_df_with_missing):
    """Test filling missing values with the median."""
    df_filled = handle_missing_values(sample_df_with_missing, strategy="median")
    assert df_filled.isnull().sum().sum() == 0


def test_fill_missing_most_frequent(sample_df_with_missing):
    """Test filling missing values with the most frequent value."""
    df_filled = handle_missing_values(sample_df_with_missing, strategy="most frequent value")
    assert df_filled.isnull().sum().sum() == 0


def test_drop_missing(sample_df_with_missing):
    """Test dropping missing values."""
    df_dropped = handle_missing_values(sample_df_with_missing, strategy="drop")
    assert df_dropped.shape[0] < sample_df_with_missing.shape[0]  # Rows should be reduced