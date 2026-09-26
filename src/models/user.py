from pydantic import BaseModel, EmailStr, UUID4

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: UUID4
    email: EmailStr
    username: str
    password_hash: str

    class Config:
        from_attributes = True