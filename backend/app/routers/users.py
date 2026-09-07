from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()

VALID_LEVELS = {"beginner", "intermediate", "advanced"}
VALID_STYLES = {"visual", "auditory", "reading", "kinesthetic"}


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserResponse)
def update_my_profile(
    updates: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if updates.name is not None:
        name = updates.name.strip()
        if not name:
            raise HTTPException(status_code=400, detail="Name cannot be empty")
        current_user.name = name

    if updates.learning_level is not None:
        if updates.learning_level not in VALID_LEVELS:
            raise HTTPException(
                status_code=400,
                detail=f"learning_level must be one of: {', '.join(VALID_LEVELS)}",
            )
        current_user.learning_level = updates.learning_level

    if updates.learning_style is not None:
        if updates.learning_style not in VALID_STYLES:
            raise HTTPException(
                status_code=400,
                detail=f"learning_style must be one of: {', '.join(VALID_STYLES)}",
            )
        current_user.learning_style = updates.learning_style

    db.commit()
    db.refresh(current_user)
    return current_user
