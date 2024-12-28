from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.config import supabase
from app.anomaly_service import detect_transaction_anomaly
from app.config import templates


router = APIRouter()

class Transaction(BaseModel):
    amount: float
    date: str
    category: str
    description: str
    user_id: str

@router.post("/api/anomaly/detect")
async def detect_anomaly(transaction: Transaction):
    try:
        # Save transaction
        trans_data = {
            'amount': transaction.amount,
            'date': transaction.date,
            'category': transaction.category,
            'description': transaction.description,
            'user_id': transaction.user_id,
            'created_at': datetime.utcnow().isoformat()
        }
        
        result = supabase.table('transactions').insert(trans_data).execute()
        transaction_id = result.data[0]['id']
        
        # Detect anomaly
        is_anomaly, confidence_score = detect_transaction_anomaly(trans_data)
        
        # Save result
        anomaly_data = {
            'transaction_id': transaction_id,
            'is_anomaly': is_anomaly,
            'confidence_score': float(confidence_score),
            'detected_at': datetime.utcnow().isoformat()
        }
        supabase.table('anomaly_results').insert(anomaly_data).execute()
        
        return {
            "transaction_id": transaction_id,
            "is_anomaly": is_anomaly,
            "confidence_score": confidence_score
        }
    except Exception as e:
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

