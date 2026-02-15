"""Risk scoring for beneficiaries."""
import pandas as pd
from typing import Dict
from config import RISK_WEIGHTS
from utils.logger import setup_logger

logger = setup_logger(__name__)

class RiskScorer:
    """Calculate risk scores for beneficiaries."""
    
    def __init__(self, weights: Dict[str, int] = None):
        """
        Initialize risk scorer.
        
        Args:
            weights: Dictionary of feature weights for risk calculation
        """
        self.weights = weights or RISK_WEIGHTS
        logger.info(f"Initialized RiskScorer with weights={self.weights}")
    
    def calculate_risk(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate risk scores for all beneficiaries.
        
        Args:
            df: Input DataFrame with features
            
        Returns:
            DataFrame with risk_score column added
        """
        try:
            required_cols = ['same_bank_count', 'same_address_count', 'anomaly']
            if not all(col in df.columns for col in required_cols):
                missing = [col for col in required_cols if col not in df.columns]
                logger.error(f"Missing required columns: {missing}")
                return df
            
            df['risk_score'] = (
                df['same_bank_count'] * self.weights['same_bank_count'] +
                df['same_address_count'] * self.weights['same_address_count'] +
                (df['anomaly'] == -1).astype(int) * self.weights['anomaly_multiplier']
            )
            
            high_risk = (df['risk_score'] > 10).sum()
            logger.info(f"Calculated risk scores. {high_risk} high-risk beneficiaries found")
            
            return df
        
        except Exception as e:
            logger.error(f"Error calculating risk scores: {str(e)}")
            return df
