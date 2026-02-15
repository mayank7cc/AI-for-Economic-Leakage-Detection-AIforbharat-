"""Calculate risk scores for beneficiaries."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import ANOMALY_OUTPUT, RISK_OUTPUT
from utils.data_loader import load_csv, save_csv
from utils.logger import setup_logger
from models import RiskScorer

logger = setup_logger(__name__)

def calculate_risk_scores() -> bool:
    """
    Calculate risk scores for all beneficiaries.
    
    Returns:
        True if successful, False otherwise
    """
    logger.info("Starting risk score calculation")
    
    # Load anomaly data
    df = load_csv(ANOMALY_OUTPUT)
    if df is None:
        return False
    
    # Calculate risk scores
    scorer = RiskScorer()
    df = scorer.calculate_risk(df)
    
    # Save results
    if save_csv(df, RISK_OUTPUT):
        logger.info("Risk calculation complete")
        return True
    
    return False

if __name__ == "__main__":
    success = calculate_risk_scores()
    exit(0 if success else 1)
