from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
import database, schemas.department, models.department, dependencies

router = APIRouter(prefix="/departments", tags=['Departments'])

@router.get("/", response_model=List[schemas.department.DepartmentOut]) 
def get_all(db: Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_user)):
    return db.query(models.department.Department).all()

@router.post("/", status_code=status.HTTP_201_CREATED) 
def create(request: schemas.department.DepartmentCreate, db: Session = Depends(database.get_db), current_admin=Depends(dependencies.admin_required)):
    new_dept = models.department.Department(**request.dict())
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept) 
    return new_dept

@router.put("/{id}", response_model=schemas.department.DepartmentOut)
def update_department(id: int, request: schemas.department.DepartmentCreate, db: Session = Depends(database.get_db), current_admin=Depends(dependencies.admin_required)):
    dept_query = db.query(models.department.Department).filter(models.department.Department.id == id)
    dept = dept_query.first()
    
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
        
    dept_query.update(request.dict())
    db.commit()
    return dept_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(id: int, db: Session = Depends(database.get_db), current_admin=Depends(dependencies.admin_required)):
    dept = db.query(models.department.Department).filter(models.department.Department.id == id).first()
    
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
        
    db.delete(dept)
    db.commit()
    return {"detail": "Department deleted"}