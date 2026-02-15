"""Duplicate detection using fuzzy string matching."""
import pandas as pd
from rapidfuzz import fuzz
from typing import List, Tuple
from config import DUPLICATE_THRESHOLD
from utils.logger import setup_logger

logger = setup_logger(__name__)

class DuplicateDetector:
    """Detect duplicate beneficiaries using fuzzy name matching."""
    
    def __init__(self, threshold: int = DUPLICATE_THRESHOLD):
        """
        Initialize duplicate detector.
        
        Args:
            threshold: Similarity threshold (0-100) for considering duplicates
        """
        self.threshold = threshold
        logger.info(f"Initialized DuplicateDetector with threshold={threshold}")
    
    def find_duplicates(
        self,
        df: pd.DataFrame,
        name_column: str = 'name',
        id_column: str = 'beneficiary_id',
        batch_size: int = 100
    ) -> List[Tuple[int, int, int]]:
        """
        Find potential duplicate beneficiaries.
        
        Args:
            df: Input DataFrame
            name_column: Column containing names
            id_column: Column containing IDs
            batch_size: Process in batches to manage memory
            
        Returns:
            List of tuples (id1, id2, similarity_score)
        """
        try:
            if name_column not in df.columns or id_column not in df.columns:
                logger.error(f"Required columns not found")
                return []
            
            duplicates = []
            total = len(df)
            
            # Process in batches for better performance
            for i in range(0, total, batch_size):
                batch_end = min(i + batch_size, total)
                for j in range(i, batch_end):
                    for k in range(j + 1, total):
                        score = fuzz.token_sort_ratio(
                            str(df[name_column].iloc[j]),
                            str(df[name_column].iloc[k])
                        )
                        if score > self.threshold:
                            duplicates.append((
                                df[id_column].iloc[j],
                                df[id_column].iloc[k],
                                score
                            ))
                
                if (i // batch_size) % 10 == 0:
                    logger.info(f"Processed {batch_end}/{total} records")
            
            logger.info(f"Found {len(duplicates)} potential duplicates")
            return duplicates
        
        except Exception as e:
            logger.error(f"Error finding duplicates: {str(e)}")
            return []
