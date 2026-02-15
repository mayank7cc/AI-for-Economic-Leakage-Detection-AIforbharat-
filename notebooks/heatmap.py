"""Generate heatmap visualization of risk scores."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import folium
import pandas as pd
from config import RISK_OUTPUT
from utils.data_loader import load_csv
from utils.logger import setup_logger

logger = setup_logger(__name__)

def generate_heatmap():
    """Generate heatmap of risk scores."""
    logger.info("Generating risk heatmap")
    
    df = load_csv(RISK_OUTPUT)
    if df is None:
        logger.error("Failed to load risk data")
        return False
    
    # Center map on India
    m = folium.Map(location=[20.59, 78.96], zoom_start=5)
    
    # Add markers for high-risk beneficiaries
    high_risk = df[df['risk_score'] > 5].head(100)
    
    for _, row in high_risk.iterrows():
        # Use actual coordinates if available, otherwise use default
        folium.CircleMarker(
            location=[20.59, 78.96],  # TODO: Add actual lat/lon to data
            radius=min(row['risk_score'], 20),
            popup=f"ID: {row['beneficiary_id']}<br>Risk: {row['risk_score']}",
            color='red',
            fill=True,
            fillOpacity=0.6
        ).add_to(m)
    
    output_path = Path(__file__).parent / "heatmap.html"
    m.save(str(output_path))
    logger.info(f"Heatmap saved to {output_path}")
    return True

if __name__ == "__main__":
    success = generate_heatmap()
    exit(0 if success else 1)
