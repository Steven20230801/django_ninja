from ninja import Router
import re
from typing import Self

from django.core.exceptions import ValidationError
from ninja import Field, Schema
from pydantic import field_validator, model_validator

from django.contrib.auth import authenticate, login
from django.http import HttpRequest
from ninja import File, Router, UploadedFile
from ninja.errors import HttpError


class LoginRequest(Schema):
    username: str = Field(examples=["Alice"])
    password: str = Field(examples=["password123"])


router = Router()


@router.get(path="/")
def get_users(request):
    return {"message": "Hello World"}


# 登入
@router.post(path="/login/", summary="登入使用者", auth=None)
def login_user(request: HttpRequest, payload: LoginRequest) -> dict[str, str]:
    """
    登入使用者
    """
    user = authenticate(request, username=payload.username, password=payload.password)
    if user is None:
        raise HttpError(401, "帳號或密碼錯誤")

    login(request, user)  # 將使用者登入狀態保存至 session
    return {"message": "登入成功"}


# 查詢自己的資訊
@router.get(path="/me/", summary="查詢自己的資訊")
def get_me(request: HttpRequest) -> dict[str, str]:
    """
    查詢自己的資訊
    """
    if request.user.is_authenticated:
        return {"username": request.user.username}
    else:
        raise HttpError(401, "未登入")
