from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel, Field, validator
from datetime import datetime, date
from typing import Optional, Dict, Any
import numpy as np
from app.config import supabase, templates
from app.anomaly_service import get_anomaly_detector

router = APIRouter()

class Transaction(BaseModel):
    amount: float = Field(..., gt=0)
    date: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')
    category: str = Field(..., pattern=r'^(food|transport|entertainment|bills|other)$')
    description: str = Field(..., min_length=1, max_length=255)
    user_id: str = Field(..., min_length=1)

    @validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Invalid date format. Use YYYY-MM-DD')

    @validator('user_id')
    def validate_user_id(cls, v):
        if not v or v == 'null' or v == 'undefined':
            raise ValueError('Invalid user_id')
        return v

def serialize_for_json(obj: Any) -> Any:
    """Convert objects to JSON-serializable format"""
    if isinstance(obj, np.bool_):
        return bool(obj)  # Convert numpy.bool_ to Python bool
    elif isinstance(obj, np.integer):
        return int(obj)  # Convert numpy integers to Python int
    elif isinstance(obj, np.floating):
        return float(obj)  # Convert numpy floats to Python float
    elif isinstance(obj, (np.ndarray, list)):
        return [serialize_for_json(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: serialize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return obj

@router.post("/api/anomaly/detect")
async def detect_anomaly(transaction: Transaction, background_tasks: BackgroundTasks):
    try:
        print(f"Received transaction data: {transaction.dict()}")

        # Validate date
        try:
            datetime.strptime(transaction.date, '%Y-%m-%d')
        except ValueError:
            raise HTTPException(status_code=422, detail="Invalid date format. Use YYYY-MM-DD")

        # Validate category
        valid_categories = ['food', 'transport', 'entertainment', 'bills', 'other']
        if transaction.category.lower() not in valid_categories:
            raise HTTPException(status_code=422, detail="Invalid category")

        # Validate amount
        if transaction.amount <= 0:
            raise HTTPException(status_code=422, detail="Amount must be greater than 0")
        
        # Save transaction
        trans_data = {
            'amount': float(transaction.amount),  # Ensure float type
            'date': transaction.date,
            'category': transaction.category,
            'description': transaction.description,
            'user_id': transaction.user_id,
            'created_at': datetime.utcnow().isoformat()
        }
        
        # Save to database
        result = supabase.table('transactions').insert(trans_data).execute()
        if not result.data:
            raise HTTPException(status_code=500, detail="Failed to save transaction")
            
        transaction_id = result.data[0]['id']
        
        # Get detector and analyze transaction
        detector = get_anomaly_detector()
        analysis = detector.analyze_transaction(trans_data)
        
        # Ensure all values are JSON serializable
        serialized_analysis = serialize_for_json(analysis)
        
        # Prepare anomaly data
        anomaly_data = {
            'transaction_id': transaction_id,
            'is_anomaly': bool(serialized_analysis['is_anomaly']),  # Ensure Python bool
            'confidence_score': float(serialized_analysis['confidence_score']),  # Ensure Python float
            'insights': serialized_analysis['insights'],
            'detected_at': datetime.utcnow().isoformat()
        }
        
        # Save analysis results
        anomaly_result = supabase.table('anomaly_results').insert(anomaly_data).execute()
        if not anomaly_result.data:
            raise HTTPException(status_code=500, detail="Failed to save anomaly results")
        
        return {
            "transaction_id": transaction_id,
            "analysis": serialized_analysis
        }
        
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        print(f"Error processing transaction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/anomaly/history/{user_id}")
async def get_history(user_id: str):
    try:
        response = supabase.table('transactions')\
            .select('*, anomaly_results(*)')\
            .eq('user_id', user_id)\
            .order('created_at', desc=True)\
            .execute()
        
        # Ensure all response data is JSON serializable
        return serialize_for_json(response.data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/anomaly")
async def anomaly_page(request: Request):
    return templates.TemplateResponse("anomaly.html", {"request": request})