from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import dependencies
import database
import schemas.user
import models.user
import utils.hashing
import utils.jwt

router = APIRouter(prefix="/auth", tags=['Authentication'])

@router.post('/register', response_model=schemas.user.UserOut)
def register(request: schemas.user.UserCreate, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.user.User).filter(models.user.User.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    hashed_pwd = utils.hashing.Hash.bcrypt(request.password)
    
    new_user = models.user.User(
        username=request.username, 
        hashed_password=hashed_pwd, 
        role="user" 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/login')
def login(request: schemas.user.UserLogin, db: Session = Depends(database.get_db)):
    user = db.query(models.user.User).filter(models.user.User.username == request.username).first()
    
    if not user or not utils.hashing.Hash.verify(user.hashed_password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    
    access_token = utils.jwt.create_access_token(data={"sub": user.username, "role": user.role})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get('/me', response_model=schemas.user.UserOut)
def get_current_logged_in_user(current_user: models.user.User = Depends(dependencies.get_current_user)):
    return current_user

