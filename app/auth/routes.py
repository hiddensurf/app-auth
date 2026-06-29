from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
import app.auth.security as security
from datetime import timedelta
from app.auth.security import hash_password
from app.auth.exceptions import credentials_exception_routes
from app.database.database import SessionDep
from app.auth.models import Token
from app.users.models import UserCreate,UserDB, UserPublic
from sqlmodel import select
router=APIRouter()
@router.post("/token")
async def login(session:SessionDep,form_data:Annotated[OAuth2PasswordRequestForm,Depends()]):
    user=security.authenticate_user(session=session,user_name=form_data.username,password=form_data.password)
    if not user:
        raise credentials_exception_routes
    data={"sub":user.user_name}
    access_token=security.create_token(data=data,expire_time=timedelta(minutes=30))
    return Token(access_token=access_token,token_type="bearer")
@router.post("/signup",status_code=status.HTTP_201_CREATED,response_model=UserPublic)
def signup(session:SessionDep,user:UserCreate):
    db_user=session.exec(select(UserDB).where(UserDB.user_name==user.user_name)).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already taken")
    db_user=UserDB(**user.model_dump(exclude={"password"}),hashed_password=hash_password(user.password.get_secret_value()))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

    
    


    