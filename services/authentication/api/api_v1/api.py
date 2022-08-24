from fastapi import APIRouter
from .endpoints import login, signup, users

api_router = APIRouter()

api_router.include_router(login.router, tags=["authentication"])
api_router.include_router(signup.router, tags=["authentication"])
api_router.include_router(users.router, tags=["authentication"])
