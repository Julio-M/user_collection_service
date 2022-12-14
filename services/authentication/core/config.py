# in-built
import os
import traceback
from sys import exit
import logging
from pythonjsonlogger import jsonlogger

# 3rd party
from fastapi.security import OAuth2PasswordBearer

try:

    class CustomJsonFormatter(jsonlogger.JsonFormatter):
        def add_fields(self, log_record, record, message_dict):
            super(CustomJsonFormatter, self).add_fields(
                log_record, record, message_dict
            )
            if not log_record.get("log_type"):
                log_record["log_type"] = "application"

    logger = logging.getLogger("homeapp")
    logger.setLevel(logging.INFO)
    json_handler = logging.StreamHandler()
    formatter = CustomJsonFormatter(
        fmt="%(thread)d %(threadName)s %(process)d %(processName)s "
        "%(asctime)s %(msecs)d %(levelname)-8s %(name)s "
        "[%(module)s::%(funcName)s::%(lineno)d] - %(message)s"
    )
    json_handler.setFormatter(formatter)
    logger.addHandler(json_handler)

    API_V1_STR = "/api/v1"
    ENDPOINT = "test"
    PROJECT_NAME = "HomeApp"
    TZ = "America/New_York"
    LOGIN_ENDPOINT = "login"

    # Env variables

    DATABASE_URL = os.environ.get("DB_URI")
    SECRET_KEY = os.environ.get("SECRET_KEY")
    REFRESH_TOKEN = os.environ.get("REFRESH_TOKEN")

    # OAuth2PasswordBearer takes two required parameters. tokenUrl is the URL in your application that handles user login and return tokens. scheme_name set to JWT will allow the frontend swagger docs to call tokenUrl from the frontend and save tokens in memory.
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_V1_STR}/{LOGIN_ENDPOINT}")

    print(f"Configs initialized for {API_V1_STR}")


except Exception as e:
    print(e)
    print(traceback.format_exc())
    exit(1)
