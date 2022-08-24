from fastapi import APIRouter, Depends, HTTPException, Depends, status
from sqlalchemy.orm import Session

from crud import user_crud
from schemas import user_schema, token_schema

from api.deps import get_db

# jwt
from typing import MutableMapping, List, Union, Any
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from core.config import oauth2_scheme

router = APIRouter()

@router.post("/login", response_model=token_schema.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Any:
    user = user_crud.user.authenticate_user(
        db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # code below re tokens can be refactored
    access_token_expires = timedelta(
        minutes=user_crud.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(
        minutes=user_crud.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = user_crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = user_crud.create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


