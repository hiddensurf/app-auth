from typing import TYPE_CHECKING
from sqlmodel import SQLModel,Field,Relationship
from pydantic import EmailStr,field_validator,SecretStr
if TYPE_CHECKING:
    from app.posts.models import Post
class UserBase(SQLModel):
    full_name:str=Field(max_length=70)
    user_name:str=Field(min_length=3,max_length=30,unique=True)
    email:EmailStr=Field(unique=True)
    @field_validator("user_name")
    @classmethod
    def user_name_validator(cls,value):
        if " " in value:
            raise ValueError("Spaces not allowed in username")
        return value
class UserDB(UserBase,table=True):
    __tablename__="usersdb"
    id: int|None=Field(primary_key=True,default=None)
    hashed_password:str
    posts:list["Post"]=Relationship(back_populates="owner",sa_relationship_kwargs={"cascade":"all,delete-orphan"})
    disabled:bool|None=None
class UserPublic(UserBase):
    id:int
class UserCreate(UserBase):
    password:SecretStr=Field(min_length=15)
class UserUpdate(UserBase):
    password:SecretStr|None=Field(min_length=15,default=None)
    full_name:str|None=None
    user_name:str|None=None
    email:EmailStr|None=None
print(UserDB.__annotations__)