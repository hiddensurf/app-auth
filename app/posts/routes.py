from fastapi import APIRouter,HTTPException,Query,Depends
from .models import Post,PostUpdate,PostCreate
from app.users.models import UserPublic
from app.database.database import SessionDep
from typing import Annotated
from app.auth.security import get_current_user_active
from sqlmodel import select
from app.users.models import UserDB
router=APIRouter(dependencies=[Depends(get_current_user_active)])
@router.post("/posts/",status_code=201)
def add_posts(post:PostCreate,session:SessionDep,user:UserDB=Depends(get_current_user_active)):
    if user.id is None:
        raise ValueError("User has no id")
    db_post=Post(**post.model_dump(),user_id=user.id)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post
@router.get("/posts/{post_id}")
def get_post(post_id:int,session:SessionDep):
    postdb=session.get(Post,post_id)
    if not postdb:
        raise HTTPException(status_code=404,detail="Post Not Found")
    return postdb
@router.get('/posts/',response_model=list[Post])
def get_posts(session:SessionDep,limit:Annotated[int,Query(le=100)]=100,offset:int=0):
    postsdb=session.exec(select(Post).limit(limit).offset(offset))
    return postsdb
@router.patch("/posts/{post_id}")
def update_post(session:SessionDep,post_id:int,post:PostUpdate,user:UserDB=Depends(get_current_user_active)):
    post_db=session.exec(select(Post).where(Post.post_id==post_id,Post.user_id==user.id)).first()
    if post_db is None:
        raise HTTPException(status_code=404,detail="Post Not Found")
    post_request=post.model_dump(exclude_unset=True)
    post_db.sqlmodel_update(post_request)
    session.commit()
    session.refresh(post_db)
    return post_db
@router.delete("/posts/{post_id}")
def delete_post(post_id:int,session:SessionDep,user:UserDB=Depends(get_current_user_active)):
    post=session.exec(select(Post).where(Post.post_id==post_id,Post.user_id==user.id)).first()
    if not post:
        raise HTTPException(status_code=404,detail="Post Not Found")
    session.delete(post)
    session.commit()
    return{"ok" : True}
@router.get("/getowner/{post_id}", response_model=UserPublic)
def get_owner(post_id:int,session:SessionDep):
    post=session.get(Post,post_id)
    if not post:
        raise HTTPException(status_code=404,detail="Post Not Found")
    return post.owner