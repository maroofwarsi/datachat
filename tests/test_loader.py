"""Tests for the file loading and cleaning pipeline."""

import pytest
import pandas as pd
import tempfile
from pathlib import Path

from src.loader import load_file, summarise_dataframe, _clean_dataframe


@pytest.fixture
def sample_csv(tmp_path):
    """Create a simple CSV file for testing."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "Month,Region,Revenue,Units\n"
        "Jan,North,10000,50\n"
        "Feb,South,12000,60\n"
        "Mar,East,9500,45\n"
    )
    return csv_file


def test_load_csv(sample_csv):
    df = load_file(sample_csv)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert "Revenue" in df.columns


def test_column_names_cleaned():
    df = pd.DataFrame({"Sales Rep ": [1], " Region": [2], "Total Revenue": [3]})
    cleaned = _clean_dataframe(df)
    assert "Sales_Rep" in cleaned.columns
    assert "Region" in cleaned.columns
    assert "Total_Revenue" in cleaned.columns


def test_unsupported_file_type(tmp_path):
    bad_file = tmp_path / "data.json"
    bad_file.write_text('{"key": "value"}')
    with pytest.raises(ValueError, match="Unsupported file type"):
        load_file(bad_file)


def test_summarise_dataframe(sample_csv):
    df = load_file(sample_csv)
    summary = summarise_dataframe(df)
    assert "rows" in summary
    assert "Revenue" in summary
    assert "Region" in summary


def test_empty_rows_dropped():
    df = pd.DataFrame({
        "A": [1, None, 3],
        "B": [None, None, None],
        "C": [4, None, 6],
    })
    # Row where ALL columns are None should be dropped
    all_null_row = pd.DataFrame({"A": [None], "B": [None], "C": [None]})
    df_with_null = pd.concat([df, all_null_row], ignore_index=True)
    cleaned = _clean_dataframe(df_with_null)
    assert len(cleaned) == len(df)
