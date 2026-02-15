"""Anomaly detection using Isolation Forest."""
import pandas as pd
from sklearn.ensemble import IsolationForest
from typing import List
from config import ANOMALY_CONTAMINATION
from utils.logger import setup_logger

logger = setup_logger(__name__)

class AnomalyDetector:
    """Detect anomalies in beneficiary data using Isolation Forest."""
    
    def __init__(self, contamination: float = ANOMALY_CONTAMINATION):
        """
        Initialize anomaly detector.
        
        Args:
            contamination: Expected proportion of outliers
        """
        self.contamination = contamination
        self.model = IsolationForest(contamination=contamination, random_state=42)
        logger.info(f"Initialized AnomalyDetector with contamination={contamination}")
    
    def detect(self, df: pd.DataFrame, features: List[str]) -> pd.DataFrame:
        """
        Detect anomalies in the dataset.
        
        Args:
            df: Input DataFrame
            features: List of feature column names
            
        Returns:
            DataFrame with anomaly column added (-1 for anomalies, 1 for normal)
        """
        try:
            if not all(f in df.columns for f in features):
                missing = [f for f in features if f not in df.columns]
                logger.error(f"Missing features: {missing}")
                return df
            
            feature_data = df[features]
            df['anomaly'] = self.model.fit_predict(feature_data)
            
            anomaly_count = (df['anomaly'] == -1).sum()
            logger.info(f"Detected {anomaly_count} anomalies out of {len(df)} records")
            
            return df
        
        except Exception as e:
            logger.error(f"Error detecting anomalies: {str(e)}")
            return df
