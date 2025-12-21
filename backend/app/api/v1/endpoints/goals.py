"""
Goal endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.api.v1.dependencies import get_current_user
from app.schemas.goal import GoalCreate, GoalResponse
from app.models.goal import Goal
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
async def create_goal(
    goal_data: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new goal"""
    from app.models.goal import GoalType
    
    db_goal = Goal(
        user_id=current_user.id,
        goal_type=GoalType(goal_data.goal_type),
        target_weight_kg=goal_data.target_weight_kg,
        current_weight_kg=goal_data.current_weight_kg,
        target_date=goal_data.target_date
    )
    db.add(db_goal)
    db.commit()
    db.refresh(db_goal)
    return db_goal


@router.get("/", response_model=List[GoalResponse])
async def get_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's goals"""
    goals = db.query(Goal).filter(Goal.user_id == current_user.id).all()
    return goals


@router.get("/active", response_model=GoalResponse)
async def get_active_goal(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's active goal"""
    goal = db.query(Goal).filter(
        Goal.user_id == current_user.id,
        Goal.is_active == True
    ).first()
    
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active goal found"
        )
    return goal

