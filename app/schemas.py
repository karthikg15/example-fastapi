from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field

class UserCreate(BaseModel): #user create schema
    email: EmailStr
    password: str
    # created_at : date
    
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    
    class Config:
        from_attributes = True
        
class UserLogin(BaseModel):
    email: str
    password: str


class PostBase(BaseModel):
    title: str
    content : str
    published: bool = True
    
    
class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    
    class Config:
        from_attributes = True
        
        
class PostOut(BaseModel):
    post: PostResponse
    votes: int
    
    class Config:
        from_attributes = True
        
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    
class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, le=1)]
           
    
    