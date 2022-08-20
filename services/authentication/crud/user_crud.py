from sqlalchemy.orm import Session #Import Session from sqlalchemy.orm, this will allow you to declare the type of the db parameters and have better type checks and completion in your functions.
from fastapi import HTTPException,status, Depends
from authentication.models import user_model
from authentication.schemas import user_schema

#jwt related
from authentication.schemas import token_schema
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from typing import Union
from authentication.api.deps import get_db

#jwt
#PWD Authentication
#in production use .env for these
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "d6841e0339cd901d2540c60bbd66cbc857ae46e9465c27bd37a9021f90276d13"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

#get user by username

def get_user_by_username(db: Session, username: str):
    return db.query(user_model.User).filter(user_model.User.username == username).first()

def authenticate_user(db:Session, username: str, password: str):
    user = get_user_by_username(db,username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# def get_user(db:Session, user_id:int):
#   return db.query(user_model.User).filter(user_model.User.id == user_id).first()

async def get_current_user(db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
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
    user = get_user_by_username(db,username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: user_schema.User = Depends(get_current_user)):
  if not current_user.is_active:
      raise HTTPException(status_code=400, detail="Inactive user")
  return current_user


def get_user_by_email(db:Session, email:str):
  return db.query(user_model.User).filter(user_model.User.email==email).first()

# # Read all users
#   def get_users(db:Session, skip:int=0,limit:int=100):
#     return db.query(user_model.User).offset(skip).limit(limit).all()

# Create user
# Create a SQLAlchemy model instance with your data.
# add that instance object to your database session.
# commit the changes to the database (so that they are saved).
# refresh your instance (so that it contains any new data from the database, like the generated ID).
def create_user(db:Session, user: user_schema.UserCreate):
  fake_hashed_password = user.password
  db_user = user_model.User(first_name=user.first_name,last_name=user.last_name,username=user.username,date_of_birth=user.date_of_birth,email=user.email, hashed_password=fake_hashed_password)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user


