"""Data validation utilities."""
import pandas as pd
from typing import List
from utils.logger import setup_logger

logger = setup_logger(__name__)

def validate_beneficiary_data(df: pd.DataFrame) -> bool:
    """
    Validate beneficiary data schema and content.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_columns = [
        'beneficiary_id', 'name', 'phone', 'address',
        'bank_account', 'scheme', 'amount', 'district', 'date'
    ]
    
    # Check required columns
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        logger.error(f"Missing columns: {missing_cols}")
        return False
    
    # Check for null values in critical columns
    critical_cols = ['beneficiary_id', 'name', 'bank_account']
    null_counts = df[critical_cols].isnull().sum()
    if null_counts.any():
        logger.warning(f"Null values found: {null_counts[null_counts > 0].to_dict()}")
    
    # Check data types
    if not pd.api.types.is_numeric_dtype(df['beneficiary_id']):
        logger.error("beneficiary_id must be numeric")
        return False
    
    logger.info("Data validation passed")
    return True
