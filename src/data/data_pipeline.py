import pandas as pd
import numpy as np
from typing import Optional, List
from src.utils.utils import save_dataframe


# =========================================================
# DATA LOADING
# =========================================================
def load_dataset(path: str) -> pd.DataFrame:
    """
    Loads the raw cybersecurity incident dataset from a CSV file.

    Args:
        path (str): File path to the raw dataset

    Returns:
        pd.DataFrame: Loaded dataset or empty DataFrame if file not found
    """
    try:
        # Attempt to read CSV and automatically parse date columns (if present)
        return pd.read_csv(path, parse_dates=True)
    
    # Handle missing file gracefully
    except FileNotFoundError:
        print(f"Error: File not found at {path}")
        return pd.DataFrame()


# =========================================================
# DATA CLEANING
# =========================================================
def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and standardizes dataset:
        - Normalizes column names
        - Cleans string values
        - Converts invalid string representations of missing values to NaN

    Args:
        df (pd.DataFrame): Raw dataset

    Returns:
        pd.DataFrame: Cleaned dataset
    """
    # Early exit if dataset is empty
    if df.empty: return df
    
    # Work on a copy to avoid mutating original DataFrame
    df = df.copy()

    # Standardize column names:
    # Example: "Attack Type" -> "attack_type"
    df.columns = [
        c.strip().lower().replace(" ", "_").replace("-", "_")
        for c in df.columns
    ]
    
    # Clean string/object columns
    for col in df.select_dtypes(include=["object"]).columns:
        # Ensure all values are strings and remove leading/trailing whitespace
        df[col] = df[col].astype(str).str.strip()

        # Replace common string representations of missing values with actual NaN
        df[col] = df[col].replace(['nan', 'None', 'NULL', ''], np.nan)
        
    return df


# =========================================================
# MISSING VALUE HANDLING
# =========================================================
def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handles missing values using type-aware strategies:
        - Numeric columns → filled with median
        - Categorical columns → filled with mode (most frequent value)
        - Fallback → "Unknown" if mode cannot be determined

    Args:
        df (pd.DataFrame): Input dataset

    Returns:
        pd.DataFrame: Dataset with missing values handled
    """
    # Early exit if dataset is empty
    if df.empty: return df

    # Work on a copy to preserve original data
    df = df.copy()
    
    # Iterate through each column
    for col in df.columns:
        # Process only columns with missing values
        if df[col].isna().any():

            # --- NUMERIC COLUMNS ---
            # Fill missing values with median (robust to outliers)
            if df[col].dtype.kind in "biufc":
                df[col] = df[col].fillna(df[col].median())

            # --- CATEGORICAL / OBJECT COLUMNS ---
            else:
                # Compute mode (most frequent value)
                mode_val = df[col].mode()

                # If mode exists, use it
                if not mode_val.empty:
                    df[col] = df[col].fillna(mode_val.iloc[0])

                # Fallback if no mode found (edge case)
                else:
                    df[col] = df[col].fillna("Unknown")

    return df


# =========================================================
# DUPLICATE REMOVAL
# =========================================================
def remove_duplicates(df: pd.DataFrame, subset: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Removes duplicate rows from the dataset.

    Args:
        df (pd.DataFrame): Input dataset
        subset (Optional[List[str]]): Columns to consider for identifying duplicates

    Returns:
        pd.DataFrame: Deduplicated dataset
    """
    # Early exit if dataset is empty
    if df.empty: return df

    # Track original size for logging
    initial_count = len(df)

    # Remove duplicates (optionally based on subset of columns)
    df = df.drop_duplicates(subset=subset).copy()
    
    # Calculate how many records were removed
    removed = initial_count - len(df)

    # Log only if duplicates were found
    if removed > 0:
        print(f"Removed {removed} duplicate records.")
        
    return df


# =========================================================
# DATA PIPELINE ORCHESTRATOR
# =========================================================
def run_data_pipeline(raw_path: str, processed_path: str) -> pd.DataFrame:
    """
    Executes the full data processing pipeline in sequence.

    Steps:
        1. Load raw dataset
        2. Clean data (column names, strings)
        3. Handle missing values
        4. Remove duplicates
        5. Save processed dataset

    Args:
        raw_path (str): Path to raw dataset
        processed_path (str): Output path for cleaned dataset

    Returns:
        pd.DataFrame: Final processed dataset
    """
    print("Starting Data Pipeline...")

    # Step 1: Load raw data
    df = load_dataset(raw_path)

    # Step 2: Clean dataset
    df = clean_dataset(df)

    # Step 3: Handle missing values
    df = handle_missing_values(df)

    # Step 4: Remove duplicate records
    df = remove_duplicates(df)
    
    # Step 5: Save processed dataset
    save_dataframe(df, processed_path)

    print("Data Pipeline complete.")
    
    return df