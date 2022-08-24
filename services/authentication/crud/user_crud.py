# Import Session from sqlalchemy.orm, this will allow you to declare the type of the db parameters and have better type checks and completion in your functions.
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from models import user_model
from schemas import user_schema
from core.config import logger

from .base_crud import CRUDBase
from typing import Any, Dict, Optional, Union

# jwt related
from schemas import token_schema
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from typing import Union
from api.deps import get_db
from core.hashing import Hasher
from core.config import SECRET_KEY, logger, REFRESH_TOKEN, oauth2_scheme
import traceback

# jwt
# PWD Authentication
# in production use .env for these
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = SECRET_KEY
REFRESH_TOKEN = REFRESH_TOKEN
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

class CRUDUser(CRUDBase[user_model.User, user_schema.User, user_schema.UserUpdate]):

    # get user by username
    def get_user_by_username(self, db: Session, username: str) -> Optional[user_model.User]:
        return db.query(user_model.User).filter(user_model.User.username == username).first()

    # get user by email
    def get_user_by_email(self, db: Session, email: str) -> Optional[user_model.User]:
        return db.query(user_model.User).filter(user_model.User.email == email).first()

    # Create user
    # Create a SQLAlchemy model instance with your data.
    # add that instance object to your database session.
    # commit the changes to the database (so that they are saved).
    # refresh your instance (so that it contains any new data from the database, like the generated ID).
    def create_user(self, db: Session, user: user_schema.UserCreate,request_id: str = "") -> user_model.User:
        _extra = {'context': {'request_id': request_id}}
        try:
            hashed_password = Hasher.get_password_hash(user.password)
            db_user = user_model.User(first_name=user.first_name, last_name=user.last_name,
                                    username=user.username, email=user.email, hashed_password=hashed_password)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            print("#######################from curd user",db_user)
            return True, 201, db_user
        except Exception as e:
            logger.error(e, extra=_extra)
            logger.error(traceback.format_exc(), extra=_extra)
            return False, 500, "Server Exception"

    def update(
        self, db: Session, *, db_obj: user_model.User, obj_in: Union[user_schema.UserUpdate, Dict[str, Any]]
    ) -> user_model.User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate_user(self, db: Session, username: str, password: str) -> Optional[user_model.User]:
        user = self.get_user_by_username(db, username)
        if not user:
            return False
        if not Hasher.verify_password(password, user.hashed_password):
            return False
        return user


user = CRUDUser(user_model.User)


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> Optional[user_model.User]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = token_schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    db_user = user.get_user_by_username(db, username=token_data.username)
    if db_user is None:
        raise credentials_exception
    return db_user

# Access and refresh token
# code below can be refactored (create_access_token & create_refresh_token)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_TOKEN, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_active_user(current_user: user_schema.User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
