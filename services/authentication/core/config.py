# in-built
import os
import traceback
from sys import exit
import logging
from pythonjsonlogger import jsonlogger

try:
    class CustomJsonFormatter(jsonlogger.JsonFormatter):
        def add_fields(self, log_record, record, message_dict):
            super(CustomJsonFormatter, self).add_fields(log_record, record,
                                                        message_dict)
            if not log_record.get('log_type'):
                log_record['log_type'] = 'application'

    logger = logging.getLogger('homeapp')
    logger.setLevel(logging.INFO)
    json_handler = logging.StreamHandler()
    formatter = CustomJsonFormatter(
        fmt="%(thread)d %(threadName)s %(process)d %(processName)s "
            "%(asctime)s %(msecs)d %(levelname)-8s %(name)s "
            "[%(module)s::%(funcName)s::%(lineno)d] - %(message)s"
    )
    json_handler.setFormatter(formatter)
    logger.addHandler(json_handler)

    API_V1_STR = "/api/v1/auth"
    LOGIN_ENDPOINT = "login"
    PROJECT_NAME = "HomeApp"
    TZ = ""

except Exception as e:
    print(e)
    print(traceback.format_exc())
    exit(1)
