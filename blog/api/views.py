# api/views.py
from ninja import Router
from ninja.errors import HttpError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .schemas import LoginSchema, UserRegisterSchema, TokenSchema, UserSchema
from .security import ACCESS_TOKEN_EXPIRE_MINUTES, JWTBearer, create_access_token
from datetime import timedelta
from ninja.security import HttpBearer, APIKeyHeader, django_auth
from typing import Optional

# from ninja import Request

from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


router = Router()


# 簡單的 Hello World 端點
@router.get("/hello")
def hello(request):
    return {"message": "Hello World!"}


@router.post("/login")
def login(request, login_request: LoginRequest):
    user = authenticate(request, username=login_request.username, password=login_request.password)
    if not user:
        raise HttpError(401, "使用者名稱或密碼不正確")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", auth=JWTBearer())
def get_current_user(request):
    return request.state.user  # 假設 JWTBearer 將 user 放在 state


from ninja.security import HttpBearer


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


@router.get("/bearer", auth=AuthBearer())
def bearer(request):
    return {"token": request.auth}


# @router.post("/register", response={201: UserRegisterSchema})
# def register(request, payload: UserRegisterSchema):
#     if User.objects.filter(username=payload.username).exists():
#         return 400, {"message": "用戶名已存在"}
#     user = User.objects.create_user(username=payload.username, email=payload.email, password=payload.password)
#     return 201, {"id": user.id, "username": user.username, "email": user.email, "first_name": user.first_name, "last_name": user.last_name}


# @router.post("/token", response=TokenSchema)
# def login(request, payload: LoginSchema):
#     user = authenticate(request, username=payload.username, password=payload.password)
#     if not user:
#         return 401, {"detail": "使用者名稱或密碼不正確"}
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
#     return {"access_token": access_token, "token_type": "bearer"}


# @router.get("/users/me", response=UserSchema, auth=JWTBearer())
# def get_current_user(request, user: User):
#     return {"id": user.id, "username": user.username, "email": user.email, "first_name": user.first_name, "last_name": user.last_name}
