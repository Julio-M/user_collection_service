from fastapi import FastAPI, Depends
from functools import lru_cache
from pythonjsonlogger import jsonlogger 
from fastapi.middleware.cors import CORSMiddleware

from authentication.api.api_v1.api import api_router
from authentication.core.config import PROJECT_NAME, API_V1_STR,logger, TZ

app = FastAPI(title=PROJECT_NAME)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router,prefix=API_V1_STR)
