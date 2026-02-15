"""FastAPI backend for fraud detection system."""
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
import pandas as pd
from config import ANOMALY_OUTPUT, RISK_OUTPUT, API_HOST, API_PORT
from utils.data_loader import load_csv
from utils.logger import setup_logger

logger = setup_logger(__name__)
app = FastAPI(title="Beneficiary Fraud Detection API", version="1.0.0")

class Beneficiary(BaseModel):
    """Beneficiary data model."""
    beneficiary_id: int
    name: str
    phone: str
    address: str
    bank_account: int
    scheme: str
    amount: int
    district: str
    date: str
    anomaly: Optional[int] = None
    risk_score: Optional[float] = None

@app.get("/")
def home():
    """Health check endpoint."""
    return {"status": "API running", "version": "1.0.0"}

@app.get("/anomalies", response_model=List[Beneficiary])
def get_anomalies(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    min_risk: Optional[float] = Query(None, ge=0, description="Minimum risk score filter")
):
    """
    Get beneficiaries flagged as anomalies.
    
    Args:
        limit: Maximum number of results to return
        min_risk: Optional minimum risk score filter
        
    Returns:
        List of anomalous beneficiaries
    """
    try:
        df = load_csv(ANOMALY_OUTPUT)
        if df is None:
            raise HTTPException(status_code=500, detail="Failed to load anomaly data")
        
        # Filter anomalies
        anomalies = df[df['anomaly'] == -1]
        
        # Apply risk filter if provided
        if min_risk is not None and 'risk_score' in anomalies.columns:
            anomalies = anomalies[anomalies['risk_score'] >= min_risk]
        
        # Limit results
        anomalies = anomalies.head(limit)
        
        logger.info(f"Returning {len(anomalies)} anomalies")
        return anomalies.to_dict(orient="records")
    
    except Exception as e:
        logger.error(f"Error fetching anomalies: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/risk", response_model=List[Beneficiary])
def get_high_risk(
    threshold: float = Query(10.0, ge=0, description="Risk score threshold"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results")
):
    """
    Get high-risk beneficiaries.
    
    Args:
        threshold: Minimum risk score threshold
        limit: Maximum number of results to return
        
    Returns:
        List of high-risk beneficiaries
    """
    try:
        df = load_csv(RISK_OUTPUT)
        if df is None:
            raise HTTPException(status_code=500, detail="Failed to load risk data")
        
        # Filter by risk threshold
        high_risk = df[df['risk_score'] >= threshold]
        high_risk = high_risk.sort_values('risk_score', ascending=False).head(limit)
        
        logger.info(f"Returning {len(high_risk)} high-risk beneficiaries")
        return high_risk.to_dict(orient="records")
    
    except Exception as e:
        logger.error(f"Error fetching high-risk beneficiaries: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/beneficiary/{beneficiary_id}", response_model=Beneficiary)
def get_beneficiary(beneficiary_id: int):
    """
    Get details for a specific beneficiary.
    
    Args:
        beneficiary_id: Beneficiary ID
        
    Returns:
        Beneficiary details
    """
    try:
        df = load_csv(RISK_OUTPUT)
        if df is None:
            raise HTTPException(status_code=500, detail="Failed to load data")
        
        beneficiary = df[df['beneficiary_id'] == beneficiary_id]
        if beneficiary.empty:
            raise HTTPException(status_code=404, detail="Beneficiary not found")
        
        return beneficiary.iloc[0].to_dict()
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching beneficiary {beneficiary_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting API server on {API_HOST}:{API_PORT}")
    uvicorn.run(app, host=API_HOST, port=API_PORT)
