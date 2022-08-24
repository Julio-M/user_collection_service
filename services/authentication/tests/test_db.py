# in-built
from unittest import TestCase

# 3rd party
from pydantic import ValidationError
import testing.postgresql
from sqlalchemy import create_engine

# custom
from models.user_model import Base
from db.session import db_engine
from core.config import DATABASE_URL
from schemas.user_schema import UserCreate
from api.deps import get_db
from core.hashing import Hasher
from crud.user_crud import user 

# Launch new PostgreSQL server
with testing.postgresql.Postgresql() as postgresql:
    # connect to PostgreSQL
    engine = create_engine(postgresql.url())

class MockUtilsWithError:
    def hash_password(self):
        raise Exception("Intentionally induced error")

class TestDb(TestCase):
    def setUp(self) -> None:
        Base.metadata.create_all(bind=db_engine)
        self.DB_URL = DATABASE_URL

         # class members
        self.events = user
        self.db = next(get_db())
        self.utils = Hasher()

        self.sample_first_name = 'john'
        self.sample_last_name = 'doe'
        self.sample_username = 'john2'
        self.sample_email = 'johndoe2@example.com'
        self.sample_is_active = True
        self.sample_pwd = 'password123'

        self.user_schema = UserCreate(first_name=self.sample_first_name, last_name=self.sample_last_name, username=self.sample_username,email=self.sample_email,password=self.sample_pwd)

        self.wrong_email = 'wrong@email.com'
        self.wrong_password = 'wrongpassword123'

    @staticmethod
    def get_induced_error():
        raise Exception("Intentionally raised error")
        
    def test_create_user_with_valid_user_schema(self):
        response = self.events.create_user(db=self.db, user=self.user_schema)

        # Check if the method returned expected value.
        self.assertTrue(response)
        self.assertEqual(response.first_name,self.sample_username)
        self.assertEqual(response.username,self.sample_username)
        # self.assertEqual(response.json(), {
        #     "first_name": self.sample_first_name,
        #     "last_name": self.sample_last_name,
        #     "username": self.sample_username,
        #     "email": self.sample_email ,
        #     "is_active": self.sample_is_active,
        # })