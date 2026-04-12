import pandas as pd
from typing import Dict  # (Note: currently unused, kept as-is without modification)

# =========================================================
# ATTACK TYPE DISTRIBUTION
# =========================================================
def compute_attack_distribution(df: pd.DataFrame, attack_col: str = "attack_type") -> pd.Series:
    """
    Computes the frequency distribution of different attack types.

    Args:
        df (pd.DataFrame): Input dataset
        attack_col (str): Column containing attack type labels

    Returns:
        pd.Series: Count of each attack type
    """
    # Safety check: ensure column exists before processing
    if attack_col not in df.columns: return pd.Series()
    
    return df[attack_col].value_counts()


# =========================================================
# SECTOR-LEVEL INCIDENT COUNTS
# =========================================================
def sector_incident_counts(df: pd.DataFrame, sector_col: str = "sector") -> pd.Series:
    """
    Computes number of incidents per industry sector.

    Args:
        df (pd.DataFrame): Input dataset
        sector_col (str): Column representing sector/industry

    Returns:
        pd.Series: Incident counts per sector
    """
    # Validate required column exists
    if sector_col not in df.columns: return pd.Series()
    
    return df[sector_col].value_counts()


# =========================================================
# YEARLY INCIDENT TRENDS
# =========================================================
def yearly_incident_trends(df: pd.DataFrame, year_col: str = "incident_year") -> pd.Series:
    """
    Computes yearly trend of incidents.

    Args:
        df (pd.DataFrame): Input dataset
        year_col (str): Column containing incident year

    Returns:
        pd.Series: Sorted incident counts by year
    """
    # Ensure column exists before processing
    if year_col not in df.columns: return pd.Series()
    
    # Drop NaN values to avoid invalid year entries in visualization
    return df[year_col].value_counts(dropna=True).sort_index()


# =========================================================
# IMPACT ANALYSIS BY ATTACK TYPE
# =========================================================
def compute_impact_by_attack(df: pd.DataFrame, 
                            attack_col: str = "attack_type", 
                            metric: str = "records_lost") -> pd.DataFrame:
    """
    Analyzes impact of each attack type using statistical aggregation.

    Provides:
        - Median impact (typical severity)
        - Total impact (overall damage)
        - Count of occurrences

    Useful for distinguishing:
        - High-frequency low-impact attacks
        - Low-frequency high-impact attacks
    """
    # Validate required columns exist
    if attack_col not in df.columns or metric not in df.columns:
        return pd.DataFrame()
        
    # Group by attack type and compute summary statistics
    impact = df.groupby(attack_col)[metric].agg(['median', 'sum', 'count']) \
               .sort_values(by='median', ascending=False)
    
    return impact


# =========================================================
# SECTOR vs ATTACK TYPE ANALYSIS (HEATMAP DATA)
# =========================================================
def cross_tabulate_sector_attack(df: pd.DataFrame, 
                                 sector_col: str = "sector", 
                                 attack_col: str = "attack_type") -> pd.DataFrame:
    """
    Generates a normalized cross-tabulation between sectors and attack types.

    Output is percentage-based and ideal for heatmap visualization.

    Shows:
        - Which industries are most targeted
        - Common attack patterns per sector
    """
    # Validate required columns exist
    if sector_col not in df.columns or attack_col not in df.columns:
        return pd.DataFrame()
        
    # Create normalized contingency table (percentage distribution)
    return pd.crosstab(df[sector_col], df[attack_col], normalize='index') * 100


# =========================================================
# CORRELATION ANALYSIS
# =========================================================
def compute_correlations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes correlation matrix for all numeric features.

    Helps identify:
        - Relationships between variables
        - Potential predictive features
    """
    # Select only numeric columns for correlation analysis
    numeric_df = df.select_dtypes(include="number")
    
    # Handle edge case: no numeric data available
    if numeric_df.empty: return pd.DataFrame()
    
    return numeric_df.corr()