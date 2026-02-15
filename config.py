"""Configuration management for the beneficiary fraud detection system."""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# File paths
BENEFICIARIES_RAW = RAW_DATA_DIR / "beneficiaries.csv"
PROCESSED_DATA = PROCESSED_DATA_DIR / "processed.csv"
ANOMALY_OUTPUT = PROCESSED_DATA_DIR / "anomaly_output.csv"
RISK_OUTPUT = PROCESSED_DATA_DIR / "risk_output.csv"

# Model parameters
ANOMALY_CONTAMINATION = float(os.getenv("ANOMALY_CONTAMINATION", "0.05"))
DUPLICATE_THRESHOLD = int(os.getenv("DUPLICATE_THRESHOLD", "90"))

# Risk scoring weights
RISK_WEIGHTS = {
    "same_bank_count": 2,
    "same_address_count": 2,
    "anomaly_multiplier": 5
}

# API configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
