"""Main pipeline orchestrator for fraud detection system."""
import sys
from utils.logger import setup_logger
from notebooks.preprocess import preprocess_data
from notebooks.detect_anomalies import run_anomaly_detection
from notebooks.calculate_risk import calculate_risk_scores

logger = setup_logger(__name__)

def run_pipeline():
    """Execute the complete fraud detection pipeline."""
    logger.info("=" * 60)
    logger.info("Starting Fraud Detection Pipeline")
    logger.info("=" * 60)
    
    steps = [
        ("Data Preprocessing", preprocess_data),
        ("Anomaly Detection", run_anomaly_detection),
        ("Risk Score Calculation", calculate_risk_scores)
    ]
    
    for step_name, step_func in steps:
        logger.info(f"\n--- {step_name} ---")
        if not step_func():
            logger.error(f"Pipeline failed at: {step_name}")
            return False
    
    logger.info("\n" + "=" * 60)
    logger.info("Pipeline completed successfully!")
    logger.info("=" * 60)
    return True

if __name__ == "__main__":
    success = run_pipeline()
    sys.exit(0 if success else 1)
