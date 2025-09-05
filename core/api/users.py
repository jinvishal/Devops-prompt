from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core import crud
from core import crud, schemas
from core.schemas import User, UserCreate, UserUpdate
from core.database import get_db
from core.api.deps import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new user.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return crud.create_user(db=db, user=user)

@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current user.
    """
    return current_user

@router.put("/me", response_model=User)
def update_user_me(
    user_in: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update current user.
    """
    user = crud.update_user(db, db_user=current_user, user_in=user_in)
    return user
