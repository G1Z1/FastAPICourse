from pydantic import BaseModel, EmailStr, conint

from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
     title: str
     content: str
     published: bool = True


class UserOut(BaseModel):
     id: int
     email: EmailStr
     class Config: # Avoiding type errors
          # orm_mode = True
          form_attributes = True


class Post(PostBase):
     id: int
     created_at: datetime
     owner_id: int
     owner : UserOut
     class Config:
          # orm_mode = True
          form_attributes = True


class PostCreate(PostBase):
     pass


class PostOut(BaseModel):
     Post: Post
     votes: int
     class Config:
          form_attributes = True


class UserCreate(BaseModel):
     email: EmailStr
     password: str


class UserLogin(BaseModel):
     email: EmailStr
     password: str


class Token(BaseModel):
     access_token: str
     token_type: str


class TokenData(BaseModel):
     id: Optional[str] = None


class Vote(BaseModel):
     post_id: int
     dir: int