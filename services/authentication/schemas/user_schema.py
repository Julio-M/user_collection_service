from typing import List, Union

from pydantic import BaseModel

#USER pydantic
class UserBase(BaseModel):
  first_name:str
  last_name:str
  username:str
  email:str
  is_active:Union[bool, None] = None

class UserCreate(UserBase):
  password:str

# Notice that the User, the Pydantic model that will be used when reading a user (returning it from the API) doesn't include the password
class User(UserBase):
  id: int
  is_active: bool

  # This Config class is used to provide configurations to Pydantic.
  class Config:
    orm_mode=True