import json
import os
from django.conf import settings
import pandas as pd
from ninja import NinjaAPI, Schema
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User  # User 模型用於用戶註冊表單
from .forms import UserRegisterForm
from ninja.security import SessionAuth

from ninja import NinjaAPI

from api.views import router as api_router  # 導入app api.api的二級路由
from user.api import router as user_router  # 導入app user.api的二級路由


api = NinjaAPI()  # 建立一級路由 整合所有 app 的 API

api.add_router(prefix="/api/", router=api_router)  # 將app層級的二級路由加入一級路由
api.add_router(prefix="/user/", router=user_router)  # 將app層級的二級路由加入一級路由


# # 首頁端點
# @api.get("/")
# def home(request):
#     context = {"message": "歡迎來到 Django Ninja 模板！"}
#     return render(request, "home.html", context)


# # 測試頁面端點
# @api.get("/test")
# def test_view(request):
#     context = {"message": "這是一個測試頁面！"}
#     return render(request, "test.html", context)


# # 認證資料模式
# class AuthSchema(Schema):
#     username: str
#     password: str


# # 註冊頁面（GET 請求）
# @api.get("/register", auth=None)
# def register_view(request):
#     form = UserRegisterForm()
#     return render(request, "register.html", {"form": form})


# # 處理註冊表單提交（POST 請求）
# @api.post("/register", auth=None)
# def register(request):
#     form = UserRegisterForm(request.POST)
#     if form.is_valid():
#         user = form.save()
#         # 這裡可以添加登入用戶或其他操作
#         return redirect("/login")
#     else:
#         # 如果表單無效，重新渲染註冊頁面並顯示錯誤
#         return render(request, "register.html", {"form": form})


# # 登入頁面（GET 請求）
# @api.get("/login", auth=None)
# def login_view(request):
#     if request.user.is_authenticated:
#         # 如果用戶已登入，重定向到受保護頁面
#         return redirect("/protected")
#     return render(request, "login.html")


# # 處理登入表單提交（POST 請求）
# @api.post("/login", auth=None)
# def login_post(request):
#     username = request.POST.get("username")
#     password = request.POST.get("password")

#     # 檢查是否提供了用戶名和密碼
#     if not username or not password:
#         error = "請輸入用戶名和密碼。"
#         return render(request, "login.html", {"error": error})

#     user = authenticate(request, username=username, password=password)
#     if user:
#         login(request, user)  # 使用 Django 的 login 函數登入用戶
#         return redirect("/protected")  # 登入成功後重定向
#     else:
#         error = "用戶名或密碼不正確。"
#         return render(request, "login.html", {"error": error})


# # 登出端點
# @api.get("/logout", auth=None)
# def logout_view(request):
#     logout(request)
#     return redirect("/login")


# # 需要身份驗證的受保護頁面
# @api.get("/protected", auth=SessionAuth())
# def protected(request):
#     # 渲染受保護的頁面，並傳遞用戶名
#     return render(request, "home.html", {"username": request.auth.username})


# # 顯示 ivr.xlsx 中的資料
# @api.get("/show")
# def show(request):
#     try:
#         # 獲取項目根目錄（確保在 settings.py 中定義了 BASE_DIR）
#         project_root = settings.BASE_DIR

#         # 構建 ivr.xlsx 的絕對路徑
#         excel_path = os.path.join(project_root, "ivr.xlsx")

#         # 讀取 ivr.xlsx
#         df = pd.read_excel(excel_path)

#         # 準備 'rebate_account' 欄位的出現次數資料
#         rebate_account_counts = {}
#         if "rebate_account" in df.columns:
#             # 統計 'rebate_account' 值的出現次數
#             rebate_account_counts = df["rebate_account"].value_counts()
#             # 只篩選出現次數大於 2 的資料
#             rebate_account_counts = rebate_account_counts[rebate_account_counts > 2]
#             # 獲取按降序排列的前 20 筆資料
#             rebate_account_counts = rebate_account_counts.head(20)
#             # 轉換為字典
#             rebate_account_counts = rebate_account_counts.to_dict()

#         # 將 rebate_account_counts 轉換為 JSON 格式
#         rebate_account_counts_json = rebate_account_counts

#     except Exception as e:
#         # 處理錯誤並傳遞空的資料或錯誤訊息
#         print(f"Error: {e}")
#         rebate_account_counts_json = {}

#     # 渲染 test.html，並傳遞資料和用戶名（如果已登入）
#     return render(
#         request,
#         "test.html",
#         {
#             "rebate_account_counts_json": rebate_account_counts_json,
#             "username": request.user.username if request.user.is_authenticated else None,
#         },
#     )
