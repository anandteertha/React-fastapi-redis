"""
Preference service - follows SOLID principles
Single Responsibility: Handles user preference business logic
"""
from sqlalchemy.orm import Session
from typing import Optional
from app.models.preference import UserPreference, DietaryRestriction
from app.schemas.preference import PreferenceCreate
from app.core.redis_client import CacheService


class PreferenceService:
    """Service for preference operations"""
    
    @staticmethod
    def create_or_update_preferences(
        db: Session,
        user_id: int,
        preference_data: PreferenceCreate
    ) -> UserPreference:
        """Create or update user preferences"""
        existing = db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).first()
        
        if existing:
            # Update existing preferences
            if preference_data.target_calories is not None:
                existing.target_calories = preference_data.target_calories
            if preference_data.target_protein is not None:
                existing.target_protein = preference_data.target_protein
            if preference_data.target_carbs is not None:
                existing.target_carbs = preference_data.target_carbs
            if preference_data.target_fats is not None:
                existing.target_fats = preference_data.target_fats
            if preference_data.preferred_meal_times is not None:
                existing.preferred_meal_times = preference_data.preferred_meal_times
            
            db_preference = existing
        else:
            # Create new preferences
            db_preference = UserPreference(
                user_id=user_id,
                **preference_data.model_dump(exclude={"dietary_restrictions"})
            )
            db.add(db_preference)
            db.flush()
        
        # Handle dietary restrictions
        if preference_data.dietary_restrictions is not None:
            # Delete existing restrictions
            db.query(DietaryRestriction).filter(
                DietaryRestriction.preference_id == db_preference.id
            ).delete()
            
            # Add new restrictions
            for restriction_data in preference_data.dietary_restrictions:
                restriction = DietaryRestriction(
                    preference_id=db_preference.id,
                    **restriction_data.model_dump()
                )
                db.add(restriction)
        
        db.commit()
        db.refresh(db_preference)
        CacheService.delete(f"preferences:user:{user_id}")
        return db_preference
    
    @staticmethod
    def get_user_preferences(db: Session, user_id: int) -> Optional[UserPreference]:
        """Get user preferences"""
        cache_key = f"preferences:user:{user_id}"
        cached_pref = CacheService.get(cache_key)
        if cached_pref:
            return db.query(UserPreference).filter(
                UserPreference.id == cached_pref["id"]
            ).first()
        
        preference = db.query(UserPreference).filter(
            UserPreference.user_id == user_id
        ).first()
        
        if preference:
            CacheService.set(cache_key, {"id": preference.id}, expire=1800)
        return preference

