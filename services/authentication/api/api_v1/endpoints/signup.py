from fastapi import APIRouter, Depends, HTTPException, Depends, status
from sqlalchemy.orm import Session

from crud import user_crud
from models import user_model
from schemas import user_schema, token_schema

from api.deps import get_db, get_correlation_id

router = APIRouter()


@router.post("/signup/", response_model=user_schema.User, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db),request_id: str = Depends(get_correlation_id)):
    # db_user = user_crud.user.get_user_by_email(db, email=user.email)
    # db_username = user_crud.user.get_user_by_username(
    #     db, username=user.username)
    # print('FROM SIGNUP',db_user)
    # if db_user or db_username:
    #     raise HTTPException(
    #         status_code=400, detail="Credentials already registered")
    # else:
    #     return user_crud.user.create_user(db=db, user=user)
    is_successful, response_code, reason = user_crud.user.create_user(db=db,
                                                                  user=user,request_id=request_id)

    if is_successful:
        return {"status": "Done", "message": "User Created"}

    else:
        raise HTTPException(status_code=response_code, detail=reason)
