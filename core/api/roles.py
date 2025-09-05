from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core import crud, schemas
from core.database import get_db
from core.api.deps import get_current_user
from core.models import User # For type hinting current_user

router = APIRouter(
    prefix="/roles",
    tags=["Roles & Permissions"],
)

@router.post("/", response_model=schemas.Role, status_code=status.HTTP_201_CREATED)
def create_new_role(
    role: schemas.RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new role.
    In a real app, you would add logic here to ensure the current_user
    has permission to create roles (e.g., is a platform or school admin).
    """
    return crud.create_role(db=db, role=role)

@router.post("/assign", response_model=schemas.UserRoleAssignment, status_code=status.HTTP_201_CREATED)
def assign_role_to_user_endpoint(
    assignment: schemas.UserRoleAssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Assign a role to a user for a specific branch.
    In a real app, you would add logic here to ensure the current_user
    has permission to assign roles for the given school/branch.
    """
    # Here you would add validation to check if user, role, and branch exist
    return crud.assign_role_to_user(db=db, assignment=assignment)
