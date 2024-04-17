from pydantic import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class EmployeeBase(BaseModel):
    name: str
    email: str
    position: str

    class Config:
        from_attributes = True

class DeleteEmployeeBase(BaseModel):
    message: str

class CompanyBase(BaseModel):
    employee_id: int
    company: str

    class Config:
        from_attributes = True


class EmployeeDB(Base):
    __tablename__ = 'employee' 

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    email = Column(String(255))
    position = Column(String(255))

    # Establish relationship with Company table
    company = relationship("CompanyDB", back_populates="employee")


class CompanyDB(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    company_name = Column(String(255))

    # Define relationship with Employee table
    employee = relationship("EmployeeDB", back_populates="company")