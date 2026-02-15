"""Find duplicate beneficiaries."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import PROCESSED_DATA
from utils.data_loader import load_csv
from utils.logger import setup_logger
from models import DuplicateDetector

logger = setup_logger(__name__)

def find_duplicates() -> bool:
    """
    Find potential duplicate beneficiaries.
    
    Returns:
        True if successful, False otherwise
    """
    logger.info("Starting duplicate detection")
    
    # Load processed data
    df = load_csv(PROCESSED_DATA)
    if df is None:
        return False
    
    # Find duplicates
    detector = DuplicateDetector()
    duplicates = detector.find_duplicates(df)
    
    # Display results
    if duplicates:
        logger.info(f"Found {len(duplicates)} potential duplicates")
        logger.info("Top 10 duplicates:")
        for id1, id2, score in duplicates[:10]:
            logger.info(f"  IDs {id1} and {id2} (similarity: {score})")
    else:
        logger.info("No duplicates found")
    
    return True

if __name__ == "__main__":
    success = find_duplicates()
    exit(0 if success else 1)
