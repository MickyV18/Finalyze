from datetime import datetime
from fastapi import HTTPException

def validate_opening_date(opening_date: datetime):
    if opening_date <= datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Opening date must be in the future"
        )

def validate_capsule_access(capsule, user_id: str):
    if capsule.owner_id != user_id and user_id not in capsule.inheritance_rules.get("beneficiaries", []):
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this capsule"
        )