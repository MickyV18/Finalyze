from ..config import supabase
from ..models.capsule import Capsule, CapsuleCreate
from ..models.content import Content, ContentCreate
from datetime import datetime
import uuid

class CapsuleService:
    async def create_capsule(self, capsule: CapsuleCreate, owner_id: uuid.UUID):
        capsule_data = {
            "id": str(uuid.uuid4()),
            "owner_id": str(owner_id),
            "title": capsule.title,
            "description": capsule.description,
            "opening_date": capsule.opening_date.isoformat(),
            "created_at": datetime.utcnow().isoformat(),
            "status": "active",
            "type": capsule.type
        }
        
        result = supabase.table("capsules").insert(capsule_data).execute()
        return Capsule(**result.data[0])

    async def get_user_capsules(self, user_id: uuid.UUID):
        result = supabase.table("capsules")\
            .select("*")\
            .eq("owner_id", str(user_id))\
            .execute()
        return [Capsule(**capsule) for capsule in result.data]

    async def get_capsule(self, capsule_id: uuid.UUID, user_id: uuid.UUID):
        result = supabase.table("capsules")\
            .select("*")\
            .eq("id", str(capsule_id))\
            .eq("owner_id", str(user_id))\
            .execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Capsule not found")
        return Capsule(**result.data[0])

    async def add_content(self, capsule_id: uuid.UUID, content: ContentCreate, user_id: uuid.UUID):
        # Verify capsule ownership first
        capsule = await self.get_capsule(capsule_id, user_id)
        
        content_data = {
            "id": str(uuid.uuid4()),
            "capsule_id": str(capsule_id),
            "content_type": content.content_type,
            "content_url": content.content_url,
            "content_size": content.content_size,
            "upload_date": datetime.utcnow().isoformat()
        }
        
        result = supabase.table("capsule_contents").insert(content_data).execute()
        return Content(**result.data[0])