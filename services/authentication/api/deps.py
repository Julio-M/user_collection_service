# from db.session import SessionLocal  # 1

from db.session import db_session


# We import the ORM session class SessionLocal from app/db/session.py
# We instantiate the session
# We yield the session, which returns a generator. Why do this? Well, the yield statement suspends the function’s execution and sends a value back to the caller, but retains enough state to enable the function to resume where it is left off. In short, it’s an efficient way to work with our database connection. Python generators primer for those unfamiliar.
# We make sure we close the DB connection by using the finally clause of the try block - meaning that the DB session is always closed. This releases connection objects associated with the session and leaves the session ready to be used again.


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()
