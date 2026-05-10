"""
File loading utilities for DataChat.

Supports CSV and Excel files. Returns a cleaned pandas DataFrame
along with a plain-English summary of what the data looks like.
"""

import pandas as pd
from pathlib import Path
from typing import Tuple


SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls"}


def load_file(file_path_or_buffer) -> pd.DataFrame:
    """
    Load a CSV or Excel file into a pandas DataFrame.

    Handles both file paths (str/Path) and Streamlit UploadedFile objects.

    Args:
        file_path_or_buffer: Path to file, or a file-like object from st.file_uploader.

    Returns:
        Cleaned pandas DataFrame.

    Raises:
        ValueError: If the file type is not supported.
    """
    # Determine file extension
    if hasattr(file_path_or_buffer, "name"):
        # Streamlit UploadedFile
        name = file_path_or_buffer.name
    else:
        name = str(file_path_or_buffer)

    ext = Path(name).suffix.lower()

    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type '{ext}'. Please upload a CSV or Excel file."
        )

    if ext == ".csv":
        df = pd.read_csv(file_path_or_buffer)
    else:
        df = pd.read_excel(file_path_or_buffer)

    df = _clean_dataframe(df)
    return df


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply basic cleaning to make the DataFrame easier to query.

    - Strip whitespace from column names
    - Replace spaces in column names with underscores
    - Drop completely empty rows
    """
    df.columns = [col.strip().replace(" ", "_") for col in df.columns]
    df = df.dropna(how="all")
    return df


def summarise_dataframe(df: pd.DataFrame) -> str:
    """
    Generate a plain-English summary of the DataFrame for the LLM context.

    Tells the agent:
        - How many rows and columns
        - Column names and data types
        - Numeric column ranges
        - Sample values for text columns

    Args:
        df: The loaded DataFrame.

    Returns:
        A descriptive string the LLM uses to understand the data structure.
    """
    lines = [
        f"The dataset has {len(df):,} rows and {len(df.columns)} columns.",
        f"Columns: {', '.join(df.columns.tolist())}",
        "",
        "Column details:",
    ]

    for col in df.columns:
        dtype = df[col].dtype
        nulls = df[col].isna().sum()
        null_str = f" ({nulls} missing)" if nulls > 0 else ""

        if pd.api.types.is_numeric_dtype(dtype):
            lines.append(
                f"  - {col} [numeric{null_str}]: "
                f"min={df[col].min():,.2f}, max={df[col].max():,.2f}, "
                f"mean={df[col].mean():,.2f}"
            )
        else:
            unique_vals = df[col].dropna().unique()
            sample = ", ".join(str(v) for v in unique_vals[:5])
            more = f" ... ({len(unique_vals)} unique)" if len(unique_vals) > 5 else ""
            lines.append(
                f"  - {col} [text{null_str}]: e.g. {sample}{more}"
            )

    return "\n".join(lines)
