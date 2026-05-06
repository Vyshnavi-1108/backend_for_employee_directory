from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True) #
    name = Column(String(100), nullable=False) #
    email = Column(String(100), unique=True, nullable=False) #
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False) #
    designation = Column(String(100), nullable=False) #
    phone = Column(String(15), nullable=True) #

    department = relationship("Department", back_populates="employees")