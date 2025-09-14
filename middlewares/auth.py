"""
Authentication middleware for JWT token validation
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from config.database import get_db
from models.database import User, UserRole
from helpers.auth import verify_token

# JWT Token Bearer
security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token."""
    email = verify_token(credentials.credentials)
    user = db.query(User).filter(User.email == email).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require admin role."""
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

def require_buyer(current_user: User = Depends(get_current_user)) -> User:
    """Require buyer role."""
    if current_user.role != UserRole.buyer:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Buyer access required"
        )
    return current_user

def require_normal_user(current_user: User = Depends(get_current_user)) -> User:
    """Require normal user role."""
    if current_user.role != UserRole.normal_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Normal user access required"
        )
    return current_user

def require_role(allowed_roles: list):
    """Create a dependency that requires specific roles."""
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[role.value for role in allowed_roles]}"
            )
        return current_user
    return role_checker
