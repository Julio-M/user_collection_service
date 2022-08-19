from sqlalchemy.orm import Session #Import Session from sqlalchemy.orm, this will allow you to declare the type of the db parameters and have better type checks and completion in your functions.

from authentication.models import user_model
from authentication.schemas import user_schema

# Read a single user by ID and by email.
def get_user(db:Session, user_id:int):
  return db.query(user_model.User).filter(user_model.User.id == user_id).first()

def get_user_by_email(db:Session, email:str):
  return db.query(user_model.User).filter(user_model.User.email==email).first()

# Read all users
def get_users(db:Session, skip:int=0,limit:int=100):
  return db.query(user_model.User).offset(skip).limit(limit).all()

# Create user
# Create a SQLAlchemy model instance with your data.
# add that instance object to your database session.
# commit the changes to the database (so that they are saved).
# refresh your instance (so that it contains any new data from the database, like the generated ID).
def create_user(db:Session, user: user_schema.UserCreate):
  fake_hashed_password = user.password + "notreallyhashed"
  db_user = user_model.User(email=user.email, hashed_password=fake_hashed_password)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user


