from fastapi import APIRouter, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel, Field, validator
from datetime import datetime, date
from typing import Optional, Dict, Any
from app.config import supabase, templates
from app.anomaly_service import get_anomaly_detector

router = APIRouter()

class Transaction(BaseModel):
    amount: float = Field(..., gt=0)  # harus lebih besar dari 0
    date: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')  # format YYYY-MM-DD
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
    if isinstance(obj, bool):
        return int(obj)  # Convert boolean to 0 or 1
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: serialize_for_json(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [serialize_for_json(item) for item in obj]
    return obj

@router.post("/api/anomaly/detect")
async def detect_anomaly(transaction: Transaction, background_tasks: BackgroundTasks):
    try:
        # Log incoming data for debugging
        print(f"Received transaction data: {transaction.dict()}")

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
            'amount': transaction.amount,
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
        
        # Prepare anomaly data with serialization
        anomaly_data = {
            'transaction_id': transaction_id,
            'is_anomaly': int(analysis['is_anomaly']),  # Convert boolean to integer
            'confidence_score': float(analysis['confidence_score']),
            'insights': serialize_for_json(analysis['insights']),
            'detected_at': datetime.utcnow().isoformat()
        }
        
        # Save analysis results
        anomaly_result = supabase.table('anomaly_results').insert(anomaly_data).execute()
        if not anomaly_result.data:
            raise HTTPException(status_code=500, detail="Failed to save anomaly results")
        
        return {
            "transaction_id": transaction_id,
            "analysis": serialize_for_json(analysis)
        }
        
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        print(f"Error processing transaction: {str(e)}")  # Log error for debugging
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/anomaly/history/{user_id}")
async def get_history(user_id: str):
    try:
        response = supabase.table('transactions')\
            .select('*, anomaly_results(*)')\
            .eq('user_id', user_id)\
            .order('created_at', desc=True)\
            .execute()
        
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/anomaly")
async def anomaly_page(request: Request):
    return templates.TemplateResponse("anomaly.html", {"request": request})