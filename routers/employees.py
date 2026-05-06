from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import database, models.employee, schemas.employee, dependencies

router = APIRouter(prefix="/employees", tags=['Employees'])

@router.get("/", response_model=List[schemas.employee.EmployeeOut])
def get_employees(db: Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_user)):
    return db.query(models.employee.Employee).all()

@router.get("/{id}", response_model=schemas.employee.EmployeeOut)
def get_employee(id: int, db: Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_user)):
    employee = db.query(models.employee.Employee).filter(models.employee.Employee.id == id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.employee.EmployeeOut)
def create_employee(request: schemas.employee.EmployeeCreate, db: Session = Depends(database.get_db), current_admin=Depends(dependencies.admin_required)):
    new_employee = models.employee.Employee(
        name=request.name,
        email=request.email,
        department_id=request.department_id,
        designation=request.designation,
        phone=request.phone
    )
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@router.put("/{id}", response_model=schemas.employee.EmployeeOut)
def update_employee(id: int, request: schemas.employee.EmployeeCreate, db: Session = Depends(database.get_db), current_user=Depends(dependencies.get_current_user)):
    
    employee_query = db.query(models.employee.Employee).filter(models.employee.Employee.id == id)
    employee = employee_query.first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    if current_user.role != "admin" and current_user.username.lower() not in employee.email.lower():
        raise HTTPException(
            status_code=403, 
            detail=f"Blocked! You are logged in as '{current_user.username}', but you are trying to edit '{employee.email}'."
        )
    
    employee_query.update(request.dict())
    db.commit()
    return employee_query.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(id: int, db: Session = Depends(database.get_db), current_admin=Depends(dependencies.admin_required)):
    employee = db.query(models.employee.Employee).filter(models.employee.Employee.id == id).first()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(employee)
    db.commit()
    return {"detail": "Employee deleted"}