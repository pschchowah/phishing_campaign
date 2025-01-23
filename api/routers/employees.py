from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, database
from pydantic import BaseModel, EmailStr
from datetime import datetime
import pandas as pd

class EmployeeResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    business_unit: str
    team_name: str
    score: int
    created_at: datetime


class EmployeeCreate(BaseModel):
    
    email: EmailStr
    first_name: str
    last_name: str
    business_unit: str = ""
    team_name: str = ""
    score: int = 0
    

    class Config:
        from_attributes = True

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("/",response_model=EmployeeResponse)
def create_employee(employee: EmployeeCreate, db: Session = Depends(database.get_db)):
    try:
        db_employee = models.Employee(**employee.model_dump())
        
        # Check if employee exists
        existing_employee = db.query(models.Employee).filter(
            models.Employee.email == employee.email
        ).first()
        if existing_employee:
            raise HTTPException(status_code=400, detail="Email already registered")
            
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    except Exception as e:
        db.rollback()  # Add rollback on error
        print(f"Error creating employee: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/", response_model=List[EmployeeResponse])
def get_employees(db: Session = Depends(database.get_db)):
    return db.query(models.Employee).all()