# =========================================================
# MAIN PIPELINE ENTRY SCRIPT
# =========================================================

from src.data.data_pipeline import run_data_pipeline
from src.features.feature_engineering import run_feature_engineering
from src.utils.utils import load_config


def main():
    """
    Central orchestration pipeline for end-to-end data processing.

    This script coordinates the full workflow:
        1. Load configuration
        2. Run data ingestion and preprocessing
        3. Apply feature engineering
        4. Save final dataset for downstream use (modeling/dashboard)

    It acts as the primary entry point before analytics or model training.
    """

    # Load project configuration (paths, parameters, settings)
    config = load_config()

    # =========================================================
    # STEP 1: DATA PIPELINE
    # =========================================================
    # Load raw dataset and apply cleaning + preprocessing steps
    df = run_data_pipeline(
        config['paths']['raw_data'],
        config['paths']['processed_data']
    )

    # =========================================================
    # STEP 2: FEATURE ENGINEERING
    # =========================================================
    # Transform raw features into model-ready / analysis-ready features
    df_engineered = run_feature_engineering(df, config)

    # =========================================================
    # STEP 3: SAVE FINAL OUTPUT
    # =========================================================
    # Persist engineered dataset for downstream consumption
    df_engineered.to_csv(
        config['paths']['processed_data'],
        index=False
    )

    # Pipeline completion message
    print("Project Ready. Run 'streamlit run app/dashboard.py' to view.")


# =========================================================
# ENTRY POINT
# =========================================================
if __name__ == "__main__":
    main()
