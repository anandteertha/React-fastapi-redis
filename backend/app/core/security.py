"""
Security utilities for authentication and authorization
Follows SOLID principles - Single Responsibility
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    # Ensure password is a string and encode to bytes
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    
    # Bcrypt has a 72-byte limit, truncate if necessary
    if len(plain_password) > 72:
        plain_password = plain_password[:72]
    
    # Ensure hashed_password is bytes
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    
    try:
        return bcrypt.checkpw(plain_password, hashed_password)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt"""
    # Ensure password is a string and encode to bytes
    if isinstance(password, str):
        password_bytes = password.encode('utf-8')
    else:
        password_bytes = password
    
    # Bcrypt has a 72-byte limit, truncate if necessary
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Generate salt and hash
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    # Return as string for storage
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    # Ensure SECRET_KEY is a string
    secret_key = settings.SECRET_KEY
    if isinstance(secret_key, bytes):
        secret_key = secret_key.decode('utf-8')
    
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=settings.ALGORITHM)
    # python-jose returns a string, ensure it's a string
    if isinstance(encoded_jwt, bytes):
        return encoded_jwt.decode('utf-8')
    return str(encoded_jwt)


def decode_access_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT token"""
    try:
        # Ensure token is a string and strip whitespace
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        token = token.strip()
        
        if not token:
            print("DEBUG: Token is empty")
            return None
        
        # Ensure SECRET_KEY is a string
        secret_key = settings.SECRET_KEY
        if isinstance(secret_key, bytes):
            secret_key = secret_key.decode('utf-8')
        
        if not secret_key:
            print("DEBUG: SECRET_KEY is empty")
            return None
        
        payload = jwt.decode(token, secret_key, algorithms=[settings.ALGORITHM])
        print(f"DEBUG: Token decoded successfully, payload: {payload}")
        return payload
    except JWTError as e:
        print(f"DEBUG: JWTError: {e}")
        return None
    except Exception as e:
        # Log exception for debugging
        print(f"DEBUG: Token decode error: {type(e).__name__}: {e}")
        return None

