# api/views.py
from ninja import Router
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .schemas import UserRegisterSchema, TokenSchema
from .security import create_access_token
from datetime import timedelta
from ninja.security import HttpBearer, APIKeyHeader
from typing import Optional
from ninja import Request

router = Router()


# 簡單的 Hello World 端點
@router.get("/hello")
def hello(request):
    return {"message": "Hello World!"}


@router.post("/register", response={201: UserRegisterSchema})
def register(request, payload: UserRegisterSchema):
    if User.objects.filter(username=payload.username).exists():
        return 400, {"message": "用戶名已存在"}
    user = User.objects.create_user(username=payload.username, email=payload.email, password=payload.password)
    return 201, {"id": user.id, "username": user.username, "email": user.email, "first_name": user.first_name, "last_name": user.last_name}


@router.post("/token", response=TokenSchema)
def login(request, username: str, password: str):
    user = authenticate(request, username=username, password=password)
    if not user:
        return 401, {"detail": "使用者名稱或密碼不正確"}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
