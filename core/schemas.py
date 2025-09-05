from pydantic import BaseModel
from typing import Optional

# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None


# --- User Schemas ---
class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    phone_number: Optional[str] = None

# Schema for creating a new user (request)
class UserCreate(UserBase):
    password: str

# --- Role Schemas ---
class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int
    school_id: Optional[int] = None

    class Config:
        from_attributes = True

# --- UserRoleAssignment Schemas ---
class UserRoleAssignmentBase(BaseModel):
    user_id: int
    role_id: int
    branch_id: int

class UserRoleAssignmentCreate(UserRoleAssignmentBase):
    pass

class UserRoleAssignment(UserRoleAssignmentBase):
    id: int

    class Config:
        from_attributes = True

# Schema for updating a user
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None

# Schema for reading a user (response)
class User(UserBase):
    id: int
    is_active: bool
    role_assignments: list[UserRoleAssignment] = []

    class Config:
        # This allows the model to be created from an ORM object
        # (e.g. our SQLAlchemy User model)
        from_attributes = True


# --- Branch Schemas ---
class BranchBase(BaseModel):
    name: str

class BranchCreate(BranchBase):
    pass

class Branch(BranchBase):
    id: int
    school_id: int

    class Config:
        from_attributes = True


# --- School Schemas ---
class SchoolBase(BaseModel):
    name: str

class SchoolCreate(SchoolBase):
    pass

class School(SchoolBase):
    id: int
    branches: list[Branch] = []

    class Config:
        from_attributes = True
