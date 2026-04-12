# =========================================================
# PACKAGE CONFIGURATION (SETUP.PY)
# =========================================================

# setuptools is used to package and distribute the project
from setuptools import setup, find_packages


# =========================================================
# PACKAGE METADATA & DEPENDENCIES
# =========================================================
setup(
    # Package name (used when installing via pip)
    name="cyber-incident-intelligence",

    # Versioning (semantic versioning recommended)
    version="0.1.0",

    # Short project description (appears on PyPI or package listings)
    description="Cyber Incident Intelligence Platform: E2E exploratory analysis and risk prediction",

    # Author name (replace with your actual name before publishing)
    author="Your Name",

    # Automatically discover all packages in the project
    packages=find_packages(),

    # Minimum Python version requirement
    # Ensures compatibility with modern features like type hints
    python_requires=">=3.9",

    # =========================================================
    # PROJECT DEPENDENCIES
    # =========================================================
    # These packages will be installed automatically with your project
    install_requires=[
        "pandas>=2.0.0",        # Data manipulation and analysis
        "numpy>=1.24.0",        # Numerical computing
        "matplotlib>=3.7.0",    # Core plotting library
        "seaborn>=0.12.0",      # Statistical data visualization
        "scikit-learn>=1.2.0",  # Machine learning models and utilities
        "scipy>=1.10.0",        # Scientific computing (stats, tests)
        "streamlit>=1.22.0",    # Interactive dashboard framework
        "pyyaml>=6.0",          # Configuration file parsing (YAML)
        "plotly>=5.14.0",       # Advanced interactive visualizations
    ],

    # =========================================================
    # CLI ENTRY POINT
    # =========================================================
    # Allows running the dashboard directly from terminal:
    #   $ cyber-intel-dashboard
    entry_points={
        'console_scripts': [
            'cyber-intel-dashboard=app.dashboard:main',
        ],
    },
)