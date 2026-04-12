import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Optional  # (Currently unused, retained as-is)

# =========================================================
# GLOBAL VISUAL STYLE
# =========================================================
# Set a consistent, professional theme for all plots
sns.set_theme(style="whitegrid", palette="viridis")


# =========================================================
# ATTACK TYPE DISTRIBUTION
# =========================================================
def plot_attack_type_distribution(df: pd.DataFrame, attack_col: str = "attack_type") -> plt.Figure:
    """
    Visualizes the distribution of attack types.

    Features:
        - Sorted by frequency (most common attacks first)
        - Clean bar chart for quick threat landscape overview

    Args:
        df (pd.DataFrame): Input dataset
        attack_col (str): Column containing attack types

    Returns:
        plt.Figure: Matplotlib figure object
    """
    # Handle edge cases: missing column or empty dataset
    if attack_col not in df.columns or df.empty:
        return plt.figure()
        
    # Initialize figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Order categories by frequency for better readability
    order = df[attack_col].value_counts().index

    # Create count plot
    sns.countplot(data=df, x=attack_col, order=order, ax=ax)
    
    # Set titles and labels
    ax.set_title("Threat Landscape: Incident Count by Attack Type", fontsize=14, fontweight='bold')
    ax.set_xlabel("Attack Vector")
    ax.set_ylabel("Number of Incidents")

    # Rotate x-axis labels for readability
    plt.xticks(rotation=45, ha='right')

    return fig


# =========================================================
# INCIDENTS OVER TIME (TREND ANALYSIS)
# =========================================================
def plot_incidents_over_time(df: pd.DataFrame, year_col: str = "incident_year") -> plt.Figure:
    """
    Plots yearly incident trends.

    Features:
        - Line chart with markers
        - Area shading for visual emphasis
        - Sorted chronological order

    Args:
        df (pd.DataFrame): Input dataset
        year_col (str): Column representing year

    Returns:
        plt.Figure: Matplotlib figure object
    """
    # Handle missing column or empty dataset
    if year_col not in df.columns or df.empty:
        return plt.figure()
        
    # Clean and sort yearly data
    yearly_counts = df[year_col].dropna().value_counts().sort_index()
    
    # Initialize figure
    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot line with markers
    ax.plot(
        yearly_counts.index,
        yearly_counts.values,
        marker="s",
        linewidth=2,
        color='#2c3e50'
    )

    # Add shaded area under the curve for better visual effect
    ax.fill_between(
        yearly_counts.index,
        yearly_counts.values,
        alpha=0.1
    )
    
    # Titles and labels
    ax.set_title("Temporal Trend: Annual Cybersecurity Incidents", fontsize=14, fontweight='bold')
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Incidents")

    # Ensure x-axis shows integer values (years)
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))

    return fig


# =========================================================
# SECTOR RISK COMPARISON
# =========================================================
def plot_sector_risk_comparison(df: pd.DataFrame, sector_col: str = "sector") -> plt.Figure:
    """
    Compares industry sectors based on median records lost.

    Why median?
        - More robust to extreme outliers
        - Aligns with feature engineering logic

    Args:
        df (pd.DataFrame): Input dataset
        sector_col (str): Column representing industry sector

    Returns:
        plt.Figure: Matplotlib figure object
    """
    # Validate required columns exist
    if sector_col not in df.columns or 'records_lost' not in df.columns:
        return plt.figure()
        
    # Compute median records lost per sector
    sector_stats = (
        df.groupby(sector_col)['records_lost']
        .median()
        .sort_values(ascending=False)
        .reset_index()
    )
    
    # Initialize figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create bar plot
    sns.barplot(
        data=sector_stats,
        x=sector_col,
        y='records_lost',
        palette="rocket",
        ax=ax
    )
    
    # Titles and labels
    ax.set_title("Industry Exposure: Median Records Lost per Incident", fontsize=14, fontweight='bold')
    ax.set_xlabel("Economic Sector")
    ax.set_ylabel("Median Records Lost")

    # Rotate labels for readability
    plt.xticks(rotation=45, ha='right')

    return fig


# =========================================================
# CORRELATION HEATMAP
# =========================================================
def plot_correlation_heatmap(df: pd.DataFrame) -> plt.Figure:
    """
    Generates a correlation heatmap for numeric features.

    Features:
        - Displays only lower triangle (removes redundancy)
        - Annotated correlation values
        - Centered colormap for positive/negative relationships

    Args:
        df (pd.DataFrame): Input dataset

    Returns:
        plt.Figure: Matplotlib figure object
    """
    import numpy as np  # Local import to limit global dependencies
    
    # Compute correlation matrix for numeric features
    corr = df.select_dtypes(include="number").corr()

    # Handle edge case: no numeric data
    if corr.empty: return plt.figure()
    
    # Initialize figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create mask to hide upper triangle (for cleaner visualization)
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    # Plot heatmap
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="RdBu_r",
        center=0,
        ax=ax
    )

    # Title
    ax.set_title("Feature Correlation Matrix", fontsize=14, fontweight='bold')

    return fig