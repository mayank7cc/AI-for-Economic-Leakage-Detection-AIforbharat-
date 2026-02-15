"""Data preprocessing pipeline."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
from config import BENEFICIARIES_RAW, PROCESSED_DATA
from utils.data_loader import load_csv, save_csv
from utils.validators import validate_beneficiary_data
from utils.logger import setup_logger

logger = setup_logger(__name__)

def preprocess_data() -> bool:
    """
    Preprocess raw beneficiary data with feature engineering.
    
    Returns:
        True if successful, False otherwise
    """
    logger.info("Starting data preprocessing")
    
    # Load raw data
    df = load_csv(BENEFICIARIES_RAW)
    if df is None:
        return False
    
    # Validate data
    if not validate_beneficiary_data(df):
        logger.error("Data validation failed")
        return False
    
    # Feature engineering
    logger.info("Performing feature engineering")
    df["same_bank_count"] = df.groupby("bank_account")["bank_account"].transform("count")
    df["same_address_count"] = df.groupby("address")["address"].transform("count")
    
    # Save processed data
    if save_csv(df, PROCESSED_DATA):
        logger.info("Preprocessing complete")
        return True
    
    return False

if __name__ == "__main__":
    success = preprocess_data()
    exit(0 if success else 1)
