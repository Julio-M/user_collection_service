from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from crud import user_crud
from schemas import user_schema

from api.deps import get_db

router = APIRouter()


@router.post(
    "/signup/", response_model=user_schema.User, status_code=status.HTTP_201_CREATED
)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.user.get_user_by_email(db, email=user.email)
    db_username = user_crud.user.get_user_by_username(db, username=user.username)
    if db_user or db_username:
        raise HTTPException(status_code=400, detail="Credentials already registered")
    else:
        return user_crud.user.create_user(db=db, user=user)
