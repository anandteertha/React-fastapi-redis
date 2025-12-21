"""
Redis client for caching and session management
Follows SOLID principles - Single Responsibility
"""
import redis
import json
from typing import Optional, Any
from app.core.config import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


class CacheService:
    """
    Service for Redis caching operations
    Follows SOLID principles - Single Responsibility
    """
    
    @staticmethod
    def get(key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            value = redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception:
            return None
    
    @staticmethod
    def set(key: str, value: Any, expire: int = 3600) -> bool:
        """Set value in cache with expiration"""
        try:
            redis_client.setex(
                key,
                expire,
                json.dumps(value, default=str)
            )
            return True
        except Exception:
            return False
    
    @staticmethod
    def delete(key: str) -> bool:
        """Delete key from cache"""
        try:
            redis_client.delete(key)
            return True
        except Exception:
            return False
    
    @staticmethod
    def exists(key: str) -> bool:
        """Check if key exists in cache"""
        try:
            return bool(redis_client.exists(key))
        except Exception:
            return False

