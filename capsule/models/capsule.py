from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, UUID4

class CapsuleBase(BaseModel):
    title: str
    description: str
    opening_date: datetime
    type: str = "personal"  # personal or inherited

class CapsuleCreate(CapsuleBase):
    pass

class Capsule(CapsuleBase):
    id: UUID4
    owner_id: UUID4
    created_at: datetime
    status: str
    contents: List[str] = []
    inheritance_rules: Optional[dict] = None

    class Config:
        orm_mode = True