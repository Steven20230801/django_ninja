import json
import os
from django.conf import settings
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


@api.get("/test")
def home(request):
    context = {"message": "Hello, Django Ninja Templates!"}
    return render(request, "test.html", context)


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
    try:
        # 獲取項目根目錄
        project_root = settings.BASE_DIR  # 確保在 settings.py 中定義了 BASE_DIR

        # 構建 ivr.xlsx 的絕對路徑
        excel_path = os.path.join(project_root, "ivr.xlsx")

        # 讀取 ivr.xlsx
        test = pd.read_excel(excel_path)

        # 準備 rebate_account 欄位的出現次數資料
        rebate_account_counts = {}
        if "rebate_account" in test.columns:
            rebate_account_counts = test["rebate_account"].value_counts()
            # 只篩選出現次數大於 2 的資料
            rebate_account_counts = rebate_account_counts[rebate_account_counts > 2]
            # 降序排列前20筆資料
            rebate_account_counts = rebate_account_counts.head(20)

            rebate_account_counts = rebate_account_counts.to_dict()

        # 將 rebate_account_counts 序列化為 JSON
        rebate_account_counts_json = rebate_account_counts
        # rebate_account_counts_json = json.dumps(rebate_account_counts)
    except Exception as e:
        # 處理錯誤並傳遞空的資料或錯誤訊息
        print(f"Error: {e}")
        rebate_account_counts_json = json.dumps({})

    # 導向 test.html，並傳遞 rebate_account_counts_json 資料
    return render(request, "test.html", {"rebate_account_counts_json": rebate_account_counts_json, "username": request.user.username if request.user.is_authenticated else None})
