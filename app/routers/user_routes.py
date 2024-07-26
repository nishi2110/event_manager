from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db, pwd_context
from app.models import User
from app.schemas import UserCreate, UserProfileUpdate, UserResponse
from app.services.user_service import UserService

router = APIRouter()

@router.post("/register/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await UserService.get_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    hashed_password = pwd_context.hash(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.put("/profile/update/{user_id}", response_model=UserResponse)
async def update_profile(user_id: str, user_update: UserProfileUpdate, db: AsyncSession = Depends(get_db)):
    user = await UserService.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user_update.bio:
        user.bio = user_update.bio
    if user_update.profile_picture_url:
        user.profile_picture_url = user_update.profile_picture_url
    
    await db.commit()
    await db.refresh(user)
    return user
