from sqlalchemy.orm import Session
from typing import Optional
from core import schemas
from core.models import User, School, Branch, Role, UserRoleAssignment
from core.security import get_password_hash

# --- User CRUD ---

def get_user_by_email(db: Session, email: str):
    """
    Fetches a user from the database by their email address.
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    """
    Creates a new user in the database.
    - Hashes the password before storing.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        phone_number=user.phone_number,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: User, user_in: schemas.UserUpdate):
    update_data = user_in.model_dump(exclude_unset=True)
    for field in update_data:
        setattr(db_user, field, update_data[field])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- School CRUD ---

def get_school(db: Session, school_id: int):
    return db.query(School).filter(School.id == school_id).first()

def get_schools(db: Session, skip: int = 0, limit: int = 100):
    return db.query(School).offset(skip).limit(limit).all()

def create_school(db: Session, school: schemas.SchoolCreate):
    db_school = School(name=school.name)
    db.add(db_school)
    db.commit()
    db.refresh(db_school)
    return db_school


# --- Branch CRUD ---

def get_branches_by_school(db: Session, school_id: int, skip: int = 0, limit: int = 100):
    return db.query(Branch).filter(Branch.school_id == school_id).offset(skip).limit(limit).all()

def create_branch_for_school(db: Session, branch: schemas.BranchCreate, school_id: int):
    db_branch = Branch(**branch.model_dump(), school_id=school_id)
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch

# --- Role & Assignment CRUD ---

def create_role(db: Session, role: schemas.RoleCreate, school_id: Optional[int] = None):
    db_role = Role(name=role.name, school_id=school_id)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def assign_role_to_user(db: Session, assignment: schemas.UserRoleAssignmentCreate):
    db_assignment = UserRoleAssignment(**assignment.model_dump())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment
