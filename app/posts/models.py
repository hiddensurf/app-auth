from typing import TYPE_CHECKING,Optional
from sqlmodel import Relationship, SQLModel, Field
from sqlalchemy import Column,ForeignKey
from fastapi import HTTPException,status
from pydantic import field_validator
if TYPE_CHECKING:
    from app.users.models import UserDB
class PostBase(SQLModel):
    title:str|None=None
    @field_validator("title")
    @classmethod
    def title_validator(cls,value):
        if value==None:
            return value
        if len(value)>100:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                                detail="Exceeded maximum character limit of 100")
        return value
class PostCreate(PostBase):
    pass
class Post(PostBase,table=True):
    __tablename__="post"
    user_id:int=Field(sa_column=Column(ForeignKey("usersdb.id",ondelete="CASCADE"),nullable=False))
    post_id:int|None=Field(primary_key=True,default=None)
    owner:Optional["UserDB"]=Relationship(back_populates="posts")
    @field_validator("title")
    @classmethod
    def title_validator(cls,value):
        if value==None:
            return value
        if len(value)>100:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                                detail="Exceeded maximum character limit of 100")
        return value
class PostUpdate(PostBase):
    pass
print(Post.__annotations__)