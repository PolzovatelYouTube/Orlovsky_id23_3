from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.cruds.user import authenticate_user, create_user, get_user_by_email
from app.schemas.user import UserCreate, UserResponse, UserWithToken, UserLogin
from app.core.security import create_access_token, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/sign-up/", response_model=UserWithToken)
def sign_up(user_data: UserCreate, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user = create_user(db, user_data)
    token = create_access_token(str(user.id))
    
    return {
        "id": user.id,
        "email": user.email,
        "token": token
    }

@router.post("/login/", response_model=UserWithToken)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = create_access_token(str(user.id))
    
    return {
        "id": user.id,
        "email": user.email,
        "token": token
    }

@router.get("/users/me/", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user