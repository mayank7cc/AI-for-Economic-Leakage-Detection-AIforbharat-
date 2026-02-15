"""Data loading and validation utilities."""
import pandas as pd
from pathlib import Path
from typing import Optional, List
from utils.logger import setup_logger

logger = setup_logger(__name__)

def load_csv(
    file_path: Path,
    required_columns: Optional[List[str]] = None
) -> Optional[pd.DataFrame]:
    """
    Load CSV file with error handling and validation.
    
    Args:
        file_path: Path to CSV file
        required_columns: List of required column names
        
    Returns:
        DataFrame if successful, None otherwise
    """
    try:
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return None
        
        df = pd.read_csv(file_path)
        logger.info(f"Loaded {len(df)} records from {file_path}")
        
        if required_columns:
            missing_cols = set(required_columns) - set(df.columns)
            if missing_cols:
                logger.error(f"Missing required columns: {missing_cols}")
                return None
        
        return df
    
    except Exception as e:
        logger.error(f"Error loading {file_path}: {str(e)}")
        return None

def save_csv(df: pd.DataFrame, file_path: Path) -> bool:
    """
    Save DataFrame to CSV with error handling.
    
    Args:
        df: DataFrame to save
        file_path: Destination path
        
    Returns:
        True if successful, False otherwise
    """
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(file_path, index=False)
        logger.info(f"Saved {len(df)} records to {file_path}")
        return True
    
    except Exception as e:
        logger.error(f"Error saving to {file_path}: {str(e)}")
        return False
