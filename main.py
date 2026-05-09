import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from database import Base, engine
from routers import auth, departments, employees

import models.user 
import models.department
import models.employee

load_dotenv() 

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173") 
Base.metadata.create_all(bind=engine) 
app = FastAPI(title="Employee Management API", version="1.0.0") 

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(departments.router)
app.include_router(employees.router)

@app.get("/")
def root():
    return {"message": "Employee Directory API is running"}


