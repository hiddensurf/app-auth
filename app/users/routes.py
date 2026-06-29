from .models import (UserDB,UserPublic,UserUpdate)
from fastapi import APIRouter,Query,HTTPException,Depends
from app.database.database import SessionDep
from app.auth.security import hash_password,get_current_user_active
from typing import Annotated
from sqlmodel import select
router=APIRouter(dependencies=[Depends(get_current_user_active)])
@router.get("/user",response_model=list[UserPublic])
def get_users(session:SessionDep, offset:int=0,limit:Annotated[int,Query(le=100)]=100):
    users=session.exec(select(UserDB).limit(limit).offset(offset))
    return users
@router.get("/users/{user_id}",response_model=UserPublic)
def get_user(user_id:int,session:SessionDep):
    user=session.get(UserDB,user_id)
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user
@router.patch("/users/me/update",response_model=UserPublic)
def update_user(user:UserUpdate, session:SessionDep,db_user:UserDB=Depends(get_current_user_active)):
    user_model=user.model_dump(exclude_unset=True)
    if user.password is not None:
        user_model.pop("password",None)
        user_model["hashed_password"]=hash_password(user.password.get_secret_value())
    db_user.sqlmodel_update(user_model)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
@router.delete("/users/me/delete",response_model=UserPublic)
def delete_user(session:SessionDep,user:UserDB=Depends(get_current_user_active)):
    session.delete(user)
    session.commit()
    return {"ok":True}
@router.get("/getposts/{user_id}")
def get_posts(user_id:int,session:SessionDep):
    user=session.get(UserDB,user_id)
    if not user:
        raise HTTPException(status_code=404,detail="User Not Found")
    return user.posts