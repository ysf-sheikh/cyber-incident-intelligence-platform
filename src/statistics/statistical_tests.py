import numpy as np
import pandas as pd

# Statistical tests for hypothesis testing
from scipy.stats import chi2_contingency, pearsonr

from typing import Tuple, Dict, Any


# =========================================================
# CHI-SQUARE TEST (CATEGORICAL RELATIONSHIP)
# =========================================================
def perform_chi_square_analysis(
    df: pd.DataFrame, 
    col1: str = "attack_type", 
    col2: str = "sector"
) -> Dict[str, Any]:
    """
    Performs a Chi-Square test of independence between two categorical variables.

    Purpose:
        - Determines whether two categorical variables are statistically related
        - Common use case: attack type vs targeted sector

    Args:
        df (pd.DataFrame): Input dataset
        col1 (str): First categorical variable
        col2 (str): Second categorical variable

    Returns:
        Dict[str, Any]: Test results including statistic, p-value, and interpretation
    """
    # Validate required columns exist
    if col1 not in df.columns or col2 not in df.columns:
        return {"error": "Columns missing"}

    # Create contingency table (frequency table)
    contingency = pd.crosstab(df[col1], df[col2])
    
    # Ensure table contains data before performing test
    if contingency.size == 0:
        return {"error": "Empty contingency table"}

    # Perform Chi-Square test
    chi2, p, dof, expected = chi2_contingency(contingency)
    
    # Return results with basic interpretation
    return {
        "statistic": chi2,
        "p_value": p,
        "dof": dof,
        "significant": p < 0.05,  # Standard significance threshold
        "interpretation": (
            "Significant relationship found"
            if p < 0.05
            else "No significant relationship"
        )
    }


# =========================================================
# PEARSON CORRELATION TEST (NUMERIC RELATIONSHIP)
# =========================================================
def perform_correlation_test(
    df: pd.DataFrame, 
    col_x: str, 
    col_y: str
) -> Dict[str, Any]:
    """
    Performs Pearson correlation test between two numeric variables.

    Purpose:
        - Measures linear relationship strength between two variables
        - Returns both correlation coefficient and statistical significance

    Args:
        df (pd.DataFrame): Input dataset
        col_x (str): First numeric variable
        col_y (str): Second numeric variable

    Returns:
        Dict[str, Any]: Correlation results and interpretation
    """
    # Validate required columns exist
    if col_x not in df.columns or col_y not in df.columns:
        return {"error": "Columns missing"}

    # Clean data:
    # - Replace infinite values with NaN
    # - Drop rows with missing values for this specific test
    temp_df = df[[col_x, col_y]] \
        .replace([np.inf, -np.inf], np.nan) \
        .dropna()
    
    # Ensure sufficient data points for statistical test
    if len(temp_df) < 2:
        return {"error": "Not enough data points after cleaning"}

    # Compute Pearson correlation coefficient and p-value
    r, p = pearsonr(temp_df[col_x], temp_df[col_y])
    
    # Interpret correlation strength based on absolute value
    return {
        "correlation_coefficient": r,
        "p_value": p,
        "strength": (
            "Strong" if abs(r) > 0.7
            else "Moderate" if abs(r) > 0.3
            else "Weak"
        ),
        "significant": p < 0.05  # Statistical significance threshold
    }