# --- IMPORTS ---
# Core libraries for app functionality
import streamlit as st
import pandas as pd
import yaml
import os
import sys
import os  # (Duplicate import - kept as-is per instructions not to modify code)

# Adds the root directory to the Python path
# This allows importing modules from the 'src' folder when running the app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- CUSTOM MODULE IMPORTS ---
# Visualization functions for plotting insights
from src.visualization.visualization import (
    plot_attack_type_distribution, 
    plot_incidents_over_time, 
    plot_sector_risk_comparison,
    plot_correlation_heatmap
)

# Machine learning functions for risk prediction
from src.models.risk_prediction import train_risk_model, get_feature_importance


# --- STREAMLIT SETUP & THEMING ---
# Configure the main app layout and appearance
st.set_page_config(
    page_title="CyberIntel | Incident Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for a professional dark mode UI
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    h1, h2, h3 { color: #58a6ff !important; }
    </style>
    """, unsafe_allow_html=True)


# --- DATA LOADING FUNCTION ---
@st.cache_data
def load_data():
    """
    Loads processed dataset and configuration file.

    Returns:
        df (pd.DataFrame): Processed incident dataset
        config (dict): Configuration settings loaded from YAML
    """
    # Attempt to load dataset path from configuration file
    try:
        with open("config/config.yaml", "r") as f:
            config = yaml.safe_load(f)

        # Load processed dataset using path defined in config
        df = pd.read_csv(config["paths"]["processed_data"])
        return df, config

    # Handle any errors during loading
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), {}


# --- MAIN APPLICATION FUNCTION ---
def main():
    """
    Main entry point for the Streamlit application.
    Handles UI rendering, filtering, and visualization logic.
    """
    
    # Load dataset and configuration
    df, config = load_data()

    # If dataset is empty, prompt user to run preprocessing pipeline
    if df.empty:
        st.warning("Please run the data pipeline first to generate 'cleaned_incidents.csv'.")
        return

    # --- SIDEBAR FILTERS ---
    # Display logo/icon
    st.sidebar.image("https://img.icons8.com/fluency/96/shield.png", width=80)
    st.sidebar.title("Intelligence Filters")
    
    # Year range filter (slider)
    years = sorted(df["incident_year"].unique().tolist())
    selected_years = st.sidebar.slider(
        "Timeline",
        min(years),
        max(years),
        (min(years), max(years))
    )
    
    # Sector filter (multi-select)
    sectors = sorted(df["sector"].unique().tolist())
    selected_sectors = st.sidebar.multiselect(
        "Target Sectors",
        sectors,
        default=sectors[:5]
    )

    # --- DATA FILTERING ---
    # Apply selected filters to dataset
    mask = (
        df["incident_year"].between(selected_years[0], selected_years[1])
    ) & (
        df["sector"].isin(selected_sectors)
    )
    df_filtered = df[mask]

    # --- HEADER SECTION ---
    # Main dashboard title and subtitle
    st.title("🛡️ Cyber Incident Intelligence Platform")
    st.markdown("### Strategic Analysis & Predictive Risk Modeling")
    
    # --- KPI METRICS ---
    # Display key performance indicators in a row
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        # Total number of filtered incidents
        st.metric("Total Incidents", len(df_filtered))

    with kpi2:
        # Total records exposed across incidents
        total_records = df_filtered["records_lost"].sum()
        st.metric("Records Exposed", f"{total_records:,.0f}")

    with kpi3:
        # Average breach severity (converted to percentage)
        avg_severity = (df_filtered["breach_severity"].mean() * 100)
        st.metric("High Severity Rate", f"{avg_severity:.1f}%")

    with kpi4:
        # Most common attack type
        top_threat = df_filtered["attack_type"].mode()[0]
        st.metric("Primary Threat", top_threat)

    # Visual separator
    st.divider()

    # --- TAB NAVIGATION ---
    # Organize app into 3 sections
    tab1, tab2, tab3 = st.tabs([
        "📊 Threat Landscape",
        "🤖 Risk Prediction",
        "📋 Raw Intelligence"
    ])

    # --- TAB 1: VISUAL ANALYTICS ---
    with tab1:
        col_l, col_r = st.columns(2)

        with col_l:
            # Distribution of attack types
            st.pyplot(plot_attack_type_distribution(df_filtered))

            # Sector-based risk comparison
            st.pyplot(plot_sector_risk_comparison(df_filtered))

        with col_r:
            # Incident trends over time
            st.pyplot(plot_incidents_over_time(df_filtered))

            # Feature correlation heatmap
            st.pyplot(plot_correlation_heatmap(df_filtered))

    # --- TAB 2: MACHINE LEARNING / RISK PREDICTION ---
    with tab2:
        st.header("Predictive Intelligence")

        # Button to trigger model training
        if st.button("Generate Risk Model"):
            with st.spinner("Training model..."):
                
                # Train model and retrieve evaluation metrics
                model, metrics = train_risk_model(df)
                
                # Layout for model results
                m_col1, m_col2 = st.columns([1, 2])

                with m_col1:
                    st.subheader("Model Performance")

                    # Display ROC-AUC score
                    st.write(f"**ROC-AUC Score:** `{metrics['roc_auc']:.3f}`")

                    # Display key classification metrics
                    st.json(metrics['report']['weighted avg'])

                with m_col2:
                    st.subheader("Risk Drivers (Feature Importance)")

                    # Extract and visualize feature importance
                    importance_df = get_feature_importance(model)
                    st.bar_chart(
                        importance_df.set_index('feature').head(10)
                    )

                    # Explanation for interpretation
                    st.info(
                        "Positive values increase the likelihood of a High Severity breach."
                    )

    # --- TAB 3: RAW DATA VIEW ---
    with tab3:
        st.subheader("Incident Logs")

        # Display filtered dataset in an interactive table
        st.dataframe(df_filtered, use_container_width=True)


# --- APPLICATION ENTRY POINT ---
# Ensures the app runs only when executed directly
if __name__ == "__main__":
    main()