from typing import List, Union, Optional

from pydantic import BaseModel, EmailStr

# USER pydantic
class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserCreate(UserBase):
    password: str


# Notice that the User, the Pydantic model that will be used when reading a user (returning it from the API) doesn't include the password
class User(UserBase):
    id: int

    # This Config class is used to provide configurations to Pydantic.
    class Config:
        orm_mode = True


# Properties to receive via API on update
class UserUpdate(BaseModel):
    username: str


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
