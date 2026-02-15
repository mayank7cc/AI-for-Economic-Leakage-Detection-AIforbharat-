"""Run anomaly detection on processed data."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import PROCESSED_DATA, ANOMALY_OUTPUT
from utils.data_loader import load_csv, save_csv
from utils.logger import setup_logger
from models import AnomalyDetector

logger = setup_logger(__name__)

def run_anomaly_detection() -> bool:
    """
    Run anomaly detection on processed data.
    
    Returns:
        True if successful, False otherwise
    """
    logger.info("Starting anomaly detection")
    
    # Load processed data
    df = load_csv(PROCESSED_DATA)
    if df is None:
        return False
    
    # Run anomaly detection
    detector = AnomalyDetector()
    features = ['amount', 'same_bank_count', 'same_address_count']
    df = detector.detect(df, features)
    
    # Save results
    if save_csv(df, ANOMALY_OUTPUT):
        logger.info("Anomaly detection complete")
        return True
    
    return False

if __name__ == "__main__":
    success = run_anomaly_detection()
    exit(0 if success else 1)
