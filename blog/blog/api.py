import json
import os
import pandas as pd
from ninja import NinjaAPI
from django.shortcuts import redirect, render
from .authentication import TokenAuth
from ninja import Schema
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User  # 添加此行
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegisterForm
from ninja.security import HttpBearer, django_auth, SessionAuth

api = NinjaAPI()


@api.get("/hello")
def hello(request):
    return {"message": "Hello World!"}


@api.get("/")
def home(request):
    context = {"message": "Hello, Django Ninja Templates!"}
    return render(request, "home.html", context)


class AuthSchema(Schema):
    username: str
    password: str


# 註冊頁面
@api.get("/register", auth=None)
def register_view(request):
    form = UserRegisterForm()
    return render(request, "register.html", {"form": form})


@api.post("/register", auth=None)
def register(request):
    form = UserRegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        username = form.cleaned_data.get("username")
        # 您可以在此处登录用户或执行其他操作
        return redirect("/login")
    else:
        return render(request, "register.html", {"form": form})


# 登录页面（GET 请求）
@api.get("/login", auth=None)
def login_view(request):
    if request.user.is_authenticated:
        return redirect("/protected")
    return render(request, "login.html")


@api.post("/login", auth=None)
def login_post(request):

    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)  # 使用 Django 的 login 函数
        return redirect("/protected")  # 登录成功后重定向
    else:
        error = "Invalid credentials"
        return render(request, "login.html", {"error": error})


# 注销
@api.get("/logout")
def logout_view(request):
    logout(request)
    return redirect("/login")


@api.get("/protected", auth=SessionAuth())
def protected(request):
    return render(request, "home.html", {"username": request.auth.username})


# show
@api.get("/show")
def show(request):
    pwd = os.getcwd()
    # 設定工作目錄在/home/steven/python/django_ninja/blog

    os.chdir("/home/steven/python/django_ninja/blog")

    # 讀取ivr.xlsx
    test = pd.read_excel("ivr.xlsx")
    columns = test.columns
    # return columns
    return {"message": columns}
