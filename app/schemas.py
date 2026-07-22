from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Annotated

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(Post):
    pass

class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
        
class PostResponse(Post):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponseSchema

    class Config:
        from_attributes  = True

class PostOut(BaseModel):
    Post: PostResponse
    vote:int 

    class Config:
        from_attributes = True

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
    dir: Annotated[int, Field(ge=0, le=1)]