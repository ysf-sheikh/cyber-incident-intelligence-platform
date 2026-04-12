import os
import yaml
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, Any


# =========================================================
# CONFIGURATION LOADER
# =========================================================
def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Loads the YAML configuration file.

    Supports fallback path resolution in case the script is executed
    from a different working directory.

    Args:
        config_path (str): Path to the configuration file

    Returns:
        Dict[str, Any]: Parsed configuration dictionary
    """
    try:
        # Primary attempt: load config from provided path
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)

    except FileNotFoundError:
        # Fallback: adjust path relative to current file location
        alt_path = os.path.join(os.path.dirname(__file__), "../../", config_path)
        
        with open(alt_path, 'r') as file:
            return yaml.safe_load(file)


# =========================================================
# DIRECTORY MANAGEMENT
# =========================================================
def ensure_directory(path: str) -> None:
    """
    Ensures that a directory exists; creates it if it does not.

    Useful for preventing file write errors when saving outputs.

    Args:
        path (str): Directory path to validate/create
    """
    # Create directory only if path is valid and does not already exist
    if path and not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


# =========================================================
# FIGURE SAVING UTILITY
# =========================================================
def save_figure(fig: plt.Figure, path: str, dpi: int = 300) -> None:
    """
    Saves a matplotlib figure to disk with high-quality settings.

    Features:
        - Ensures output directory exists
        - Applies tight layout when possible
        - Saves with high resolution (DPI)
        - Frees memory after saving

    Args:
        fig (plt.Figure): Matplotlib figure object
        path (str): Output file path
        dpi (int): Resolution for saved image
    """
    # Extract directory from file path
    directory = os.path.dirname(path)

    # Ensure directory exists before saving
    ensure_directory(directory)
    
    # Attempt to optimize layout
    # Some complex figures may fail, so we handle gracefully
    try:
        fig.tight_layout()
    except ValueError:
        pass
        
    # Save figure with consistent formatting
    fig.savefig(
        path,
        dpi=dpi,
        bbox_inches="tight",
        transparent=False,
        facecolor='white'
    )

    # IMPORTANT: Close figure to release memory (prevents memory leaks in loops)
    plt.close(fig)


# =========================================================
# DATAFRAME SAVING UTILITY
# =========================================================
def save_dataframe(df: pd.DataFrame, path: str, index: bool = False) -> None:
    """
    Saves a pandas DataFrame to a CSV file.

    Features:
        - Ensures output directory exists
        - Provides simple logging upon success

    Args:
        df (pd.DataFrame): DataFrame to save
        path (str): Output file path
        index (bool): Whether to include index in CSV
    """
    # Ensure target directory exists
    directory = os.path.dirname(path)
    ensure_directory(directory)

    # Save DataFrame to CSV
    df.to_csv(path, index=index)

    # Basic confirmation log
    print(f"Successfully saved to: {path}")