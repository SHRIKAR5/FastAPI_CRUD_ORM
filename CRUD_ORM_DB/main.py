from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from core.database import get_db, engine
from core.models import EmployeeBase, EmployeeDB, CompanyBase, CompanyDB, DeleteEmployeeBase
import traceback
from core import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post('/add_employee/', response_model=EmployeeBase)
async def add_employee(employee: EmployeeBase, db: Session = Depends(get_db)):
    try:
        db_employee = EmployeeDB(**dict(employee))
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee

    except Exception as e:
        print("ERROR FOUND")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/list_employees/', response_model=list[EmployeeBase])
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
            for attr, value in employee.dict().items():
                setattr(db_employee, attr, value)
            db.commit()
            db.refresh(db_employee)
            return db_employee
        else:
            raise HTTPException(status_code=404, detail='Employee not found')

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
            print(db_employee)
            # return db_employee
            return {'message' : 'Employee deleted successfully'}
        else:
            raise HTTPException(status_code=404, detail='Employee not found')

    except Exception as e:
        print('ERROR FOUND')
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


