from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        description="Password must be at least 8 characters long"
    )

class User(BaseModel):
    id: str
    email: str
    is_active: bool = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None