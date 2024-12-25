from pydantic import BaseModel, UUID4
from datetime import datetime

class ContentBase(BaseModel):
    content_type: str
    content_url: str
    content_size: int

class ContentCreate(ContentBase):
    capsule_id: UUID4

class Content(ContentBase):
    id: UUID4
    upload_date: datetime
    encryption_key: Optional[str]

    class Config:
        orm_mode = True