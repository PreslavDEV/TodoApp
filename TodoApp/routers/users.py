from fastapi import APIRouter, Depends, HTTPException, Path
from ..models import Todos, Users
from typing import Annotated 
from sqlalchemy.orm import Session
from ..database import  SessionLocal
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(prefix='/users', tags=['users'])

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class ChangeUserPasswordRequest(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

class ChangeUserPhoneNumberRequest(BaseModel):
    new_phone_number: str = Field(min_length=6)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_depedency = Annotated[dict, Depends(get_current_user)]

@router.get("/user", status_code=status.HTTP_200_OK)
async def read_user(user: user_depedency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    return db.query(Users).filter(Users.id==user.get('id')).first()

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_user_passowrd(user: user_depedency, db: db_dependency,user_request: ChangeUserPasswordRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    user_model = db.query(Users).filter(Users.id==user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail='User not found')
    if not bcrypt_context.verify(user_request.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Error on password change")
    
    user_model.hashed_password = bcrypt_context.hash(user_request.new_password)
    
    db.add(user_model)
    db.commit()

@router.put("/phone_number", status_code=status.HTTP_204_NO_CONTENT)
async def change_user_phone_number(user: user_depedency, db: db_dependency, user_request: ChangeUserPhoneNumberRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    user_model = db.query(Users).filter(Users.id==user.get('id')).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail='User not found')
    user_model.phone_number = user_request.new_phone_number

    db.add(user_model)
    db.commit()