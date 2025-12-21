"""
API dependencies - follows SOLID principles
Dependency Injection for authentication and database
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception
    
    print(f"DEBUG: Received token: {token[:20]}... (length: {len(token)})")
    payload = decode_access_token(token)
    if payload is None:
        print("DEBUG: Token decode returned None")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"DEBUG: Payload: {payload}")
    user_id = payload.get("sub")
    print(f"DEBUG: User ID from token: {user_id} (type: {type(user_id)})")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing user identifier",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Ensure user_id is an integer (JWT might encode it as string)
    try:
        user_id = int(user_id)
        print(f"DEBUG: Converted user_id to int: {user_id}")
    except (ValueError, TypeError) as e:
        print(f"DEBUG: Failed to convert user_id: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user identifier in token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = UserService.get_user_by_id(db, user_id)
    print(f"DEBUG: User lookup result: {user is not None}")
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

