"""
Preference endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.dependencies import get_current_user
from app.schemas.preference import PreferenceCreate, PreferenceResponse
from app.services.preference_service import PreferenceService
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=PreferenceResponse, status_code=status.HTTP_201_CREATED)
@router.put("/", response_model=PreferenceResponse)
async def create_or_update_preferences(
    preference_data: PreferenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create or update user preferences"""
    return PreferenceService.create_or_update_preferences(
        db, current_user.id, preference_data
    )


@router.get("/", response_model=PreferenceResponse)
async def get_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user preferences"""
    preferences = PreferenceService.get_user_preferences(db, current_user.id)
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Preferences not found. Please create them first."
        )
    return preferences

