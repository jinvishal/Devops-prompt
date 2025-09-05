from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core import crud, schemas
from core.database import get_db

router = APIRouter(
    prefix="/schools",
    tags=["Schools & Branches"],
)

@router.post("/", response_model=schemas.School, status_code=status.HTTP_201_CREATED)
def create_new_school(school: schemas.SchoolCreate, db: Session = Depends(get_db)):
    """
    Create a new school.
    """
    return crud.create_school(db=db, school=school)

@router.get("/", response_model=List[schemas.School])
def read_all_schools(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all schools.
    """
    schools = crud.get_schools(db, skip=skip, limit=limit)
    return schools

@router.get("/{school_id}", response_model=schemas.School)
def read_single_school(school_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single school by its ID.
    """
    db_school = crud.get_school(db, school_id=school_id)
    if db_school is None:
        raise HTTPException(status_code=404, detail="School not found")
    return db_school

@router.post("/{school_id}/branches/", response_model=schemas.Branch, status_code=status.HTTP_201_CREATED)
def create_new_branch_for_school(
    school_id: int, branch: schemas.BranchCreate, db: Session = Depends(get_db)
):
    """
    Create a new branch for a specific school.
    """
    db_school = crud.get_school(db, school_id=school_id)
    if db_school is None:
        raise HTTPException(status_code=404, detail="School not found")
    return crud.create_branch_for_school(db=db, branch=branch, school_id=school_id)
