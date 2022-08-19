from fastapi import APIRouter
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from authentication.crud import user_crud
from authentication.models import user_model
from authentication.schemas import user_schema

from authentication.api.deps import get_db

router = APIRouter()

@router.get("/login")
def login():
  return {"message":"hello from login endpoint"}

@router.post("/users/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db=db, user=user)