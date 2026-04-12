# =========================================================
# MAIN PIPELINE ENTRY SCRIPT
# =========================================================

# Import core pipeline components
from src.data.data_pipeline import run_data_pipeline
from src.features.feature_engineering import run_feature_engineering
from src.utils.utils import load_config


def main():
    """
    Main orchestration function for the entire data workflow.

    Steps:
        1. Load configuration settings
        2. Run data ingestion and cleaning pipeline
        3. Perform feature engineering
        4. Save final processed dataset

    This script serves as the central entry point for preparing data
    before launching the dashboard or training models.
    """

    # Load configuration from YAML file
    config = load_config()
    
    # =========================================================
    # STEP 1: DATA PIPELINE
    # =========================================================
    # Load, clean, and preprocess raw data
    df = run_data_pipeline(
        config['paths']['raw_data'],
        config['paths']['processed_data']
    )
    
    # =========================================================
    # STEP 2: FEATURE ENGINEERING
    # =========================================================
    # Generate additional features for analysis and modeling
    df_engineered = run_feature_engineering(df, config)
    
    # =========================================================
    # STEP 3: SAVE FINAL DATASET
    # =========================================================
    # Overwrite processed dataset with engineered features included
    df_engineered.to_csv(
        config['paths']['processed_data'],
        index=False
    )

    # Inform user that pipeline execution is complete
    print("Project Ready. Run 'streamlit run app/dashboard.py' to view.")


# =========================================================
# SCRIPT ENTRY POINT
# =========================================================
if __name__ == "__main__":
    # Execute pipeline when script is run directly
    main()