from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Annotated

class UserSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponseModel(BaseModel): 
    id: int
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class NotesSchema(BaseModel):
    title: str
    content: str

class Notes_Response_Schema(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    owner: UserResponseModel
    class Config:
        from_attributes  = True

    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
   id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1)]