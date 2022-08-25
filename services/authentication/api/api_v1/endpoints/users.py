from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status

from crud import user_crud
from schemas import user_schema

from api.deps import get_db
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("/users/", response_model=List[user_schema.User])
def read_users(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve users.
    """
    users = user_crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.get("/users/{username}", response_model=user_schema.User)
async def read_users_by_username(username: str, db: Session = Depends(get_db)):
    db_user = user_crud.user.get_user_by_username(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/me/", response_model=user_schema.User)
async def read_users_me(
    current_user: user_schema.User = Depends(user_crud.get_current_active_user),
):
    return current_user


@router.put("/update/me/{user_id}", status_code=status.HTTP_201_CREATED)
async def read_users_by_id(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: user_schema.UserUpdate,
    current_user: user_schema.User = Depends(user_crud.get_current_active_user)
) -> Any:
    """
    Update a user.
    """
    print(current_user)
    user = user_crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = user_crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
