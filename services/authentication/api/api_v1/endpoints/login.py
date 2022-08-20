from fastapi import APIRouter,Depends, HTTPException, Depends,status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from authentication.crud import user_crud
from authentication.models import user_model
from authentication.schemas import user_schema,token_schema

from authentication.api.deps import get_db

#jwt
from typing import MutableMapping, List, Union
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta


JWTPayloadMapping = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/login")
def login():
  return {"message":"hello from login endpoint"}

@router.post("/token", response_model=token_schema.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    user = user_crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=user_crud.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = user_crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get('/users/{username}',response_model=user_schema.User)
async def read_users_by_username(username: str, db: Session = Depends(get_db)):
  db_user = user_crud.get_user_by_username(db,username)
  if db_user is None:
      raise HTTPException(status_code=404, detail="User not found")
  return db_user

@router.get("/users/me/", response_model=user_schema.User)
async def read_users_me(current_user: user_schema.User = Depends(user_crud.get_current_active_user)):
    return current_user

@router.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}