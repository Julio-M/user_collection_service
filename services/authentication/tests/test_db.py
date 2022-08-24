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
from schemas.user_schema import UserCreate, UserUpdate
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
        self.sample_username = 'john37'
        self.sample_email = 'johndoe37@example.com'
        self.sample_is_active = True
        self.sample_pwd = 'password123'
        self.sample_is_superuser = False

        self.user_schema = UserCreate(first_name=self.sample_first_name, last_name=self.sample_last_name, username=self.sample_username,email=self.sample_email,password=self.sample_pwd)

        self.wrong_email = 'wrong@email.com'
        self.wrong_password = 'wrongpassword123'

    @staticmethod
    def get_induced_error():
        raise Exception("Intentionally raised error")
        
    def test_create_user_with_valid_user_schema(self):
        response = self.events.create_user(db=self.db, user=self.user_schema)

        db_user=self.events.get_user_by_username(db=self.db, username=self.sample_username)

        # Check if the method returned expected value.
        self.assertTrue(response)

         # Check if the DB inserts were successful
        self.assertIsNotNone(db_user)

        # Check if the DB password is hashed
        self.assertTrue(self.utils.verify_password(
            plain_password=self.sample_pwd, hashed_password=db_user.hashed_password))
        
        # Check that it returns as expected
        self.assertEqual(response.first_name,self.sample_first_name)
        self.assertEqual(response.last_name,self.sample_last_name)
        self.assertEqual(response.username,self.sample_username)
        self.assertEqual(response.email,self.sample_email)
        self.assertEqual(response.username,self.sample_username)
        self.assertEqual(response.is_active,self.sample_is_active)
        self.assertEqual(response.is_superuser,self.sample_is_superuser)

    def test_create_user_with_invalid_user_schema(self):
        with self.assertRaises(ValidationError):
                user_schema = UserCreate()
                self.events.create_user(db=self.db, user=user_schema)

    # def test_update_user_info(self):
    #     self.user_update = UserUpdate
    #     response = self.events.user_update(db=self.db, user=self.user_schema)
    def tearDown(self) -> None:
        try:
            self.postgresql.stop()
        except Exception as e:
            print("Couldn't clean test DB")