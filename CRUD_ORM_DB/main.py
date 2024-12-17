from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from core.database import get_db, engine
from core.models import EmployeeBase, EmployeeDB, CompanyBase, CompanyDB, DeleteEmployeeBase
import traceback
from core import models
from typing import List 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post('/add_employee/', response_model=EmployeeBase)
async def add_employee(employee: EmployeeBase, db: Session = Depends(get_db)):
    try:
        print("employee : ", employee)
        db_employee = EmployeeDB(**dict(employee))
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee

    except Exception as e:
        print("ERROR FOUND")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/list_employees/', response_model=List[EmployeeBase])
async def list_employees(db: Session = Depends(get_db)):
    try:
        db_employee = db.query(EmployeeDB).all()
        return db_employee
    except Exception as e:
        print("ERROR FOUND")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/get_employee/{id}', response_model = EmployeeBase)
async def get_employee(id: int, db: Session = Depends(get_db)):
    try:
        db_employee = db.query(EmployeeDB).filter(EmployeeDB.id == id).first()
        if db_employee:
            return db_employee
        else:
            raise HTTPException(status_code=404, detail='Employee not found')
        
    except Exception as e:
        print('ERROR FOUND')
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.put('/update_employee/{id}', response_model=EmployeeBase)
async def update_employee(id:int, employee: EmployeeBase, db: Session = Depends(get_db)):
    try:
        db_employee = db.query(EmployeeDB).filter(EmployeeDB.id == id).first()
        if db_employee:
            for key, value in employee.model_dump().items():
                setattr(db_employee, key, value)
            print("employee.model_dump() : ",employee.model_dump())
            db.commit()
            db.refresh(db_employee)
            return db_employee
        else:
            raise HTTPException(status_code=404, detail='Employee not found')

    except Exception as e:
        print('ERROR FOUND')
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.patch('/patch_update_employee/{id}', response_model=EmployeeBase)
async def patch_update_employee(id:int, employee:EmployeeBase, db: Session = Depends(get_db)):
    try:
        db_employee = db.query(EmployeeDB).filter(EmployeeDB.id == id).first()
        if db_employee:
            update_employee = employee.model_dump(exclude_unset=True)
            print("update_employee : ",update_employee)
            for key, value in update_employee.items():
                setattr(db_employee, key, value)
            db.commit()
            db.refresh(db_employee)
            return db_employee
        else:
            raise HTTPException(status_code=404, details="Employee does not exist")
            
    except Exception as e:
        print('ERROR FOUND')
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.delete('/delete_employee/{id}', response_model = DeleteEmployeeBase)
async def delete_employee(id:int, db: Session=Depends(get_db)):
    try:
        db_employee = db.query(EmployeeDB).filter(EmployeeDB.id == id).first()
        if db_employee:
            db.delete(db_employee)
            db.commit()
            return {'message' : 'Employee deleted successfully'}
        else:
            raise HTTPException(status_code=404, detail='Employee not found')

    except Exception as e:
        print('ERROR FOUND')
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


