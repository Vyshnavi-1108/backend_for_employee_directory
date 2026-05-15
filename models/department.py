from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True) 
    name = Column(String(100), unique=True, nullable=False) 
    location = Column(String(100), default='HQ') 
    
    employees = relationship("Employee", back_populates="department")