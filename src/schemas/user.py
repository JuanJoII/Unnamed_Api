from pydantic import BaseModel, EmailStr, UUID4


class UserBase(BaseModel):
    id: UUID4
    email: EmailStr
    password: str
    username: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserRead(BaseModel):
    id: UUID4
    email: EmailStr
    username: str

    class Config:
        from_attributes = True
