from sqlalchemy import (
    Column, Integer, String, Boolean, ForeignKey, Table
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Association table for Role -> Permission relationship (many-to-many)
role_permission_association = Table(
    'role_permission_association', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

# Association table for Parent -> Child relationship (many-to-many)
parent_child_association = Table(
    'parent_child_association', Base.metadata,
    Column('parent_user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('child_user_id', Integer, ForeignKey('users.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    phone_number = Column(String, unique=True, nullable=True)
    is_active = Column(Boolean, default=True)

    # Relationships
    role_assignments = relationship("UserRoleAssignment", back_populates="user")
    student_profile = relationship("StudentProfile", uselist=False, back_populates="user", cascade="all, delete-orphan")
    teacher_profile = relationship("TeacherProfile", uselist=False, back_populates="user", cascade="all, delete-orphan")
    parent_profile = relationship("ParentProfile", uselist=False, back_populates="user", cascade="all, delete-orphan")

    # This user (as a parent) has many children
    children = relationship(
        "User",
        secondary=parent_child_association,
        primaryjoin=id == parent_child_association.c.parent_user_id,
        secondaryjoin=id == parent_child_association.c.child_user_id,
        backref="parents"
    )

class School(Base):
    __tablename__ = 'schools'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    branches = relationship("Branch", back_populates="school", cascade="all, delete-orphan")

class Branch(Base):
    __tablename__ = 'branches'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    school_id = Column(Integer, ForeignKey('schools.id'), nullable=False)

    school = relationship("School", back_populates="branches")
    role_assignments = relationship("UserRoleAssignment", back_populates="branch")

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, comment="A granular permission, e.g., 'user:create'")

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, comment="A role name, e.g., 'Admin', 'Teacher'")
    school_id = Column(Integer, ForeignKey('schools.id'), nullable=True, comment="Null for platform-wide roles, set for school-specific custom roles")

    permissions = relationship("Permission", secondary=role_permission_association, backref="roles")
    assignments = relationship("UserRoleAssignment", back_populates="role")

class UserRoleAssignment(Base):
    __tablename__ = 'user_role_assignments'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    branch_id = Column(Integer, ForeignKey('branches.id'), nullable=False)

    user = relationship("User", back_populates="role_assignments")
    role = relationship("Role", back_populates="assignments")
    branch = relationship("Branch", back_populates="role_assignments")

class StudentProfile(Base):
    __tablename__ = 'student_profiles'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    # Add student-specific fields here in the future

    user = relationship("User", back_populates="student_profile")

class TeacherProfile(Base):
    __tablename__ = 'teacher_profiles'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    # Add teacher-specific fields here in the future

    user = relationship("User", back_populates="teacher_profile")

class ParentProfile(Base):
    __tablename__ = 'parent_profiles'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    # Add parent-specific fields here in the future

    user = relationship("User", back_populates="parent_profile")
