# views.py
import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
import pandas as pd
from .forms import UserRegisterForm


class HomeView(View):
    def get(self, request):
        context = {"message": "歡迎來到 Django Ninja 模板！"}
        return render(request, "home.html", context)


class TestView(View):
    def get(self, request):
        context = {"message": "這是一個測試頁面！"}
        return render(request, "test.html", context)


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("/login")
        else:
            return render(request, "register.html", {"form": form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/protected")
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            error = "請輸入用戶名和密碼。"
            return render(request, "login.html", {"error": error})

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/protected")
        else:
            error = "用戶名或密碼不正確。"
            return render(request, "login.html", {"error": error})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/login")


class ProtectedView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("/login")
        return render(request, "home.html", {"username": request.user.username})


class ShowView(View):
    def get(self, request):
        try:
            project_root = settings.BASE_DIR
            excel_path = os.path.join(project_root, "ivr.xlsx")
            df = pd.read_excel(excel_path)

            rebate_account_counts = {}
            if "rebate_account" in df.columns:
                rebate_account_counts = df["rebate_account"].value_counts()
                rebate_account_counts = rebate_account_counts[rebate_account_counts > 2]
                rebate_account_counts = rebate_account_counts.head(20)
                rebate_account_counts = rebate_account_counts.to_dict()

            rebate_account_counts_json = rebate_account_counts
        except Exception as e:
            print(f"Error: {e}")
            rebate_account_counts_json = {}

        return render(
            request,
            "test.html",
            {
                "rebate_account_counts_json": rebate_account_counts_json,
                "username": request.user.username if request.user.is_authenticated else None,
            },
        )


class AccountView(View):
    def get(self, request):
        # 回傳account_demo.html, server_option
        server_options = ["pui3report", "pui4report"]
        return render(request, "account_demo.html", {"server_options": server_options})

    def post(self, request):
        # 接收表單資料
        server = request.POST.get("server")
        login = request.POST.get("account")

        # try:
        #     project_root = settings.BASE_DIR
        #     excel_path = os.path.join(project_root, "accounts.xlsx")
        #     df = pd.read_excel(excel_path)

        #     rebate_account_counts = {}
        #     if "rebate_account" in df.columns:
        #         rebate_account_counts = df["rebate_account"].value_counts()
        #         rebate_account_counts = rebate_account_counts[rebate_account_counts > 2]
        #         rebate_account_counts = rebate_account_counts.head(20)
        #         rebate_account_counts = rebate_account_counts.to_dict()

        #     rebate_account_counts_json = rebate_account_counts
        # except Exception as e:
        #     print(f"Error: {e}")
        #     rebate_account_counts_json = {}

        # return render(
        #     request,
        #     "test.html",
        #     {
        #         "rebate_account_counts_json": rebate_account_counts_json,
        #         "username": request.user.username if request.user.is_authenticated else None,
        #     },
        # )
