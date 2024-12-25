from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..services.capsule_service import CapsuleService
from ..models.capsule import Capsule, CapsuleCreate
from authentication.oauth import get_current_user

router = APIRouter()
capsule_service = CapsuleService()

@router.post("/capsules/", response_model=Capsule)
async def create_capsule(
    capsule: CapsuleCreate,
    current_user = Depends(get_current_user)
):
    return await capsule_service.create_capsule(capsule, current_user.id)

@router.get("/capsules/", response_model=List[Capsule])
async def get_capsules(current_user = Depends(get_current_user)):
    return await capsule_service.get_user_capsules(current_user.id)

@router.get("/capsules/{capsule_id}", response_model=Capsule)
async def get_capsule(
    capsule_id: UUID4,
    current_user = Depends(get_current_user)
):
    return await capsule_service.get_capsule(capsule_id, current_user.id)

@router.post("/capsules/{capsule_id}/content")
async def add_content(
    capsule_id: UUID4,
    content: ContentCreate,
    current_user = Depends(get_current_user)
):
    return await capsule_service.add_content(capsule_id, content, current_user.id)
