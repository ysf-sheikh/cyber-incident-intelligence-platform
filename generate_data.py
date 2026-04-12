import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os


# =========================================================
# MOCK DATA GENERATION
# =========================================================
def generate_mock_data(n_samples=1000):
    """
    Generates a synthetic cybersecurity incident dataset.

    Purpose:
        - Enables testing of the full pipeline without real data
        - Simulates realistic cyber incident patterns

    Features:
        - Randomized sectors and attack types
        - Time-distributed incidents
        - Heavy-tailed distribution for records lost (realistic breach sizes)
        - Injected patterns to make analysis more meaningful

    Args:
        n_samples (int): Number of synthetic records to generate
    """
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Define possible categorical values
    sectors = ['Finance', 'Healthcare', 'Retail', 'Government', 'Education', 'Technology']
    attacks = ['Ransomware', 'Phishing', 'SQL Injection', 'DDoS', 'Insider Threat', 'Malware']
    
    # Generate synthetic dataset
    data = {
        # Random dates within ~4 years range
        'incident_date': [
            datetime(2020, 1, 1) + timedelta(days=np.random.randint(0, 1500))
            for _ in range(n_samples)
        ],

        # Random sector assignment
        'sector': np.random.choice(sectors, n_samples),

        # Random attack type assignment
        'attack_type': np.random.choice(attacks, n_samples),

        # Records lost follow exponential distribution:
        # - Many small incidents
        # - Few very large breaches (real-world pattern)
        'records_lost': np.random.exponential(
            scale=100000,
            size=n_samples
        ).astype(int)
    }
    
    # Convert dictionary to DataFrame
    df = pd.DataFrame(data)
    
    # =========================================================
    # INJECTED PATTERNS (FOR MORE REALISTIC ANALYSIS)
    # =========================================================
    
    # 1. Finance sector tends to have larger breaches
    df.loc[df['sector'] == 'Finance', 'records_lost'] *= 5

    # 2. Ransomware becomes more common in recent years (trend simulation)
    recent_mask = df['incident_date'].dt.year >= 2023
    df.loc[recent_mask, 'attack_type'] = np.random.choice(
        ['Ransomware', 'Phishing'],
        size=len(df[recent_mask])
    )

    # =========================================================
    # SAVE DATASET
    # =========================================================
    
    # Ensure target directory exists
    os.makedirs('data/raw', exist_ok=True)
    
    # Define output path
    path = 'data/raw/cyber_incidents.csv'

    # Save dataset to CSV
    df.to_csv(path, index=False)

    # Confirmation message
    print(f"✅ Generated {n_samples} mock incidents at: {path}")


# =========================================================
# SCRIPT ENTRY POINT
# =========================================================
if __name__ == "__main__":
    # Run generator when script is executed directly
    generate_mock_data()