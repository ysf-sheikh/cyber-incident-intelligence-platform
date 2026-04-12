import numpy as np
import pandas as pd
from typing import Optional  # (Currently unused, retained as-is per instructions)


# =========================================================
# BREACH SEVERITY FEATURE
# =========================================================
def create_breach_severity_feature(
    df: pd.DataFrame, 
    records_col: str = "records_lost", 
    threshold: int = 100000
) -> pd.DataFrame:
    """
    Creates a binary target feature indicating breach severity.

    Logic:
        - 0 → Low severity breach
        - 1 → High severity breach (records >= threshold)

    Args:
        df (pd.DataFrame): Input dataset
        records_col (str): Column representing number of records lost
        threshold (int): Threshold to classify high severity breaches

    Returns:
        pd.DataFrame: Dataset with 'breach_severity' feature added
    """
    # Work on a copy to avoid mutating original dataset
    df = df.copy()

    # Fallback: if records column is missing, assign default low severity
    if records_col not in df.columns:
        df["breach_severity"] = 0
        return df
    
    # Create binary feature using threshold comparison
    # .astype(int) converts boolean values to 0/1
    df["breach_severity"] = (df[records_col] >= threshold).astype(int)
    
    return df


# =========================================================
# TEMPORAL FEATURE EXTRACTION
# =========================================================
def extract_temporal_features(df: pd.DataFrame, date_col: str = "incident_date") -> pd.DataFrame:
    """
    Extracts time-based features from a date column.

    Features created:
        - incident_year
        - incident_month

    Args:
        df (pd.DataFrame): Input dataset
        date_col (str): Column containing date information

    Returns:
        pd.DataFrame: Dataset with temporal features added
    """
    # Work on a copy to preserve original dataset
    df = df.copy()

    # Exit early if date column does not exist
    if date_col not in df.columns:
        return df
    
    # Convert column to datetime format (invalid parsing → NaT)
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    
    # Extract year component
    df["incident_year"] = df[date_col].dt.year

    # Handle missing years to prevent downstream errors (e.g., in models/plots)
    if df["incident_year"].isna().any():
        # Fill with most common year (mode), fallback to 2023 if mode unavailable
        df["incident_year"] = df["incident_year"].fillna(
            df["incident_year"].mode().get(0, 2023)
        )
    
    # Extract month component (missing values filled with 0)
    df["incident_month"] = df[date_col].dt.month.fillna(0)
    
    return df


# =========================================================
# LOG TRANSFORMATION (SKEW REDUCTION)
# =========================================================
def log_transform_records_lost(df: pd.DataFrame, records_col: str = "records_lost") -> pd.DataFrame:
    """
    Applies log transformation to reduce skewness in 'records_lost'.

    This is useful because breach sizes often follow a heavy-tailed distribution.

    Args:
        df (pd.DataFrame): Input dataset
        records_col (str): Column representing records lost

    Returns:
        pd.DataFrame: Dataset with 'records_lost_log' feature added
    """
    # Work on a copy
    df = df.copy()

    if records_col in df.columns:
        # np.log1p(x) computes log(1 + x), safely handling zero values
        # clip(lower=0) ensures no negative values are passed to log
        df["records_lost_log"] = np.log1p(
            df[records_col].fillna(0).clip(lower=0)
        )

    return df


# =========================================================
# INDUSTRY RISK SCORE
# =========================================================
def create_industry_risk_score(df: pd.DataFrame, sector_col: str = "sector") -> pd.DataFrame:
    """
    Computes a sector-level risk score based on median records lost.

    Why median?
        - More robust to extreme outliers (common in cyber incidents)
        - Prevents single large breaches from skewing results

    Args:
        df (pd.DataFrame): Input dataset
        sector_col (str): Column representing industry/sector

    Returns:
        pd.DataFrame: Dataset with 'industry_risk_score' feature added
    """
    # Work on a copy
    df = df.copy()

    # Exit early if sector column is missing
    if sector_col not in df.columns:
        return df
    
    # Compute median records lost per sector
    sector_risk = df.groupby(sector_col)['records_lost'] \
                    .median() \
                    .rename("industry_risk_score")
    
    # Map sector-level risk scores back to original dataset
    # Using .map is efficient for single-column joins
    df["industry_risk_score"] = df[sector_col].map(sector_risk)
    
    return df


# =========================================================
# FEATURE ENGINEERING PIPELINE
# =========================================================
def run_feature_engineering(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Orchestrates all feature engineering steps in sequence.

    Steps:
        1. Create breach severity target variable
        2. Extract temporal features
        3. Apply log transformation to numeric skewed data
        4. Compute industry-level risk score

    Args:
        df (pd.DataFrame): Input dataset
        config (dict): Configuration dictionary

    Returns:
        pd.DataFrame: Dataset with engineered features
    """
    print("Engineering features...")
    
    # Retrieve threshold from config (fallback to default if missing)
    threshold = config.get('analysis_params', {}).get(
        'high_severity_threshold', 100000
    )
    
    # Apply feature engineering steps sequentially
    df = create_breach_severity_feature(df, threshold=threshold)
    df = extract_temporal_features(df)
    df = log_transform_records_lost(df)
    df = create_industry_risk_score(df)
    
    return df