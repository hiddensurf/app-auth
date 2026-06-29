from app.users.models import UserDB
from app.auth.models import TokenData
from app.database.database import SessionDep
from pwdlib import PasswordHash
from fastapi import Depends,HTTPException
from sqlmodel import select,Session
from datetime import datetime,timezone,timedelta
import jwt
from typing import Annotated
from app.auth.exceptions import credentials_exception_security,disabled_user_exception
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from config import settings
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
TIME_TO_EXPIRE=settings.time_to_expire
password_hash=PasswordHash.recommended()
DUMMY_PASSWORD=password_hash.hash("dummypassword223")
def verify_password(password,hash):
    return password_hash.verify(password,hash)
def hash_password(password):
    hashed_password=password_hash.hash(password)
    return hashed_password
def get_userfrom_db(session:Session,username):
    user=session.exec(select(UserDB).where(UserDB.user_name==username)).first()
    return user
def authenticate_user(session:SessionDep,user_name,password):
    user=get_userfrom_db(session=session,username=user_name)
    if not user:
        verify_password(password,DUMMY_PASSWORD)
        return None
    if not verify_password(password,user.hashed_password):
        return None
    return user
def create_token(data:dict,expire_time:timedelta|None):
    to_encode=data.copy()
    if expire_time:
        exp=datetime.now(tz=timezone.utc)+expire_time
    else:
        exp=datetime.now(tz=timezone.utc)+timedelta(minutes=TIME_TO_EXPIRE)
    to_encode["exp"]=exp
    encoded_jwt= jwt.encode(to_encode,key=SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
async def get_current_user(session:SessionDep,token:Annotated[str,Depends(oauth2_scheme)]):
    try:
        payload=jwt.decode(token,key=SECRET_KEY,algorithms=[ALGORITHM])
        username=payload.get("sub")
        if not username:
            raise credentials_exception_security
        token_data=TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception_security
    user=get_userfrom_db(session=session,username=token_data.username)
    if user is None:
        raise credentials_exception_security
    return user
async def get_current_user_active(user:Annotated[UserDB,Depends(get_current_user)]):
    if user.disabled:
        raise disabled_user_exception
    return user