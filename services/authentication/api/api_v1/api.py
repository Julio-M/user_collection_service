from fastapi import APIRouter
from .endpoints import login, signup

api_router = APIRouter()

api_router.include_router(login.router, tags=["authentication"])
api_router.include_router(signup.router, tags=["authentication"])
