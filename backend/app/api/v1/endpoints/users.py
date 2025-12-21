"""
User endpoints
"""
from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.dependencies import get_current_user
from app.core.security import decode_access_token
from app.schemas.user import UserResponse
from app.models.user import User

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@router.get("/debug-token")
async def debug_token(authorization: str = Header(None)):
    """Debug endpoint to test token extraction and decoding"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No Authorization header"
        )
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header must start with 'Bearer '"
        )
    
    token = authorization.replace("Bearer ", "").strip()
    payload = decode_access_token(token)
    
    return {
        "token_received": bool(token),
        "token_length": len(token) if token else 0,
        "payload": payload,
        "user_id": payload.get("sub") if payload else None
    }

