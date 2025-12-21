"""
User service - follows SOLID principles
Single Responsibility: Handles user-related business logic
"""
from sqlalchemy.orm import Session
from typing import Optional
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password
from app.core.redis_client import CacheService


class UserService:
    """Service for user operations"""
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create a new user"""
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            age=user_data.age,
            gender=user_data.gender,
            height_cm=user_data.height_cm,
            weight_kg=user_data.weight_kg
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        cache_key = f"user:email:{email}"
        cached_user = CacheService.get(cache_key)
        if cached_user:
            return db.query(User).filter(User.id == cached_user["id"]).first()
        
        user = db.query(User).filter(User.email == email).first()
        if user:
            CacheService.set(cache_key, {"id": user.id}, expire=300)
        return user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username"""
        cache_key = f"user:username:{username}"
        cached_user = CacheService.get(cache_key)
        if cached_user:
            return db.query(User).filter(User.id == cached_user["id"]).first()
        
        user = db.query(User).filter(User.username == username).first()
        if user:
            CacheService.set(cache_key, {"id": user.id}, expire=300)
        return user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        cache_key = f"user:id:{user_id}"
        cached_user = CacheService.get(cache_key)
        if cached_user:
            return db.query(User).filter(User.id == user_id).first()
        
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            CacheService.set(cache_key, {"id": user.id}, expire=300)
        return user
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """Authenticate user"""
        user = UserService.get_user_by_username(db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

