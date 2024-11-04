# views.py
import json
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

    def __init__(self):
        self.server_options = ["pui3report", "pui4report"]

    def get(self, request):
        return render(
            request,
            "account_demo.html",
            {
                "server_options": self.server_options,
                "data_json": json.dumps([]),  # 初始載入時為空數據
                "trades_json": json.dumps([]),
                "username": request.user.username if request.user.is_authenticated else None,
            },
        )

    def post(self, request):
        server = request.POST.get("server")
        login = request.POST.get("login")

        try:
            login = int(login)
            project_root = settings.BASE_DIR
            excel_path = os.path.join(project_root, "accounts.xlsx")
            daily = pd.read_excel(excel_path, sheet_name="daily")
            trades = pd.read_excel(excel_path, sheet_name="trades")

            # 根據 login 過濾數據
            daily = daily[daily["LOGIN"] == login]
            trades = trades[trades["LOGIN"] == login]

            if daily.empty:
                return render(
                    request,
                    "account_demo.html",
                    {
                        "error": "查無資料",
                        "server_options": self.server_options,
                        "data_json": json.dumps([]),
                        "trades_json": json.dumps([]),
                        "username": request.user.username if request.user.is_authenticated else None,
                    },
                )

            # 處理 trades，將 CLOSE_TIME 轉換為字符串格式
            trades["TIME"] = trades["CLOSE_TIME"].dt.strftime("%Y-%m-%d")  # 根據需要調整格式

            # 正確使用 groupby 進行多列分組
            trades_grouped = trades.groupby(["TIME", "SYMBOL"]).agg({"PROFIT": "sum"}).reset_index()

            # 處理所有 datetime 列，將 Timestamp 轉換為字符串
            for col in daily.select_dtypes(include=["datetime", "datetime64[ns]"]).columns:
                daily[col] = daily[col].dt.strftime("%Y-%m-%d")  # 根據需要調整格式

            # 將 NaN 替換為 None（JSON 中的 null）
            daily = daily.where(pd.notnull(daily), None)
            trades_grouped = trades_grouped.where(pd.notnull(trades_grouped), None)

            # 重命名列以匹配 JavaScript 中的鍵名
            daily = daily.rename(columns={"PROFIT_CLOSED": "CLOSE_PNL"})  # 根據需要進行修改
            # 假設你希望保留 "PROFIT" 鍵名，否則可以重命名

            # 將 DataFrame 轉換為 JSON 字符串
            data_json = daily.to_json(orient="records")
            trades_json = trades_grouped.to_json(orient="records")

            return render(
                request,
                "account_demo.html",
                {"data_json": data_json, "trades_json": trades_json, "server_options": self.server_options, "username": request.user.username if request.user.is_authenticated else None},
            )

        except Exception as e:
            print(f"Error: {e}")
            return render(
                request,
                "account_demo.html",
                {
                    "error": str(e),
                    "server_options": self.server_options,
                    "data_json": json.dumps([]),
                    "trades_json": json.dumps([]),
                    "username": request.user.username if request.user.is_authenticated else None,
                },
            )

from django.views.generic import TemplateView

from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date

class PEIVRTableView(TemplateView):
    template_name = 'pe_ivr_table.html'

    def get_context_data(self, **kwargs):
        # 調用父類別的方法來取得原有的上下文
        context = super().get_context_data(**kwargs)

        # 獲取 GET 請求中的日期範圍參數
        request = self.request
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')
        page_number = request.GET.get('page')

        # 讀取 Excel 檔案
        file_path = 'pe_ivr.xlsx'  # 請使用您的實際檔案路徑
        # 確認檔案存在
        if not os.path.exists(file_path):
            context['error'] = '數據檔案不存在。'
            context['data'] = []
            context['paginator'] = None
            context['page_obj'] = None
            context['start_date'] = start_date_str
            context['end_date'] = end_date_str
            return context

        try:
            df = pd.read_excel(file_path)
        except Exception as e:
            context['error'] = f'讀取數據檔案時發生錯誤：{e}'
            context['data'] = []
            context['paginator'] = None
            context['page_obj'] = None
            context['start_date'] = start_date_str
            context['end_date'] = end_date_str
            return context

        # 確保 'date' 欄位存在並轉換為日期對象
        if 'date' not in df.columns:
            context['error'] = "'date' 欄位在數據中不存在。"
            context['data'] = []
            context['paginator'] = None
            context['page_obj'] = None
            context['start_date'] = start_date_str
            context['end_date'] = end_date_str
            return context

        # 轉換 'date' 欄位為日期對象
        df['date'] = pd.to_datetime(df['date']).dt.date

        # 解析日期字符串為日期對象
        start_date = parse_date(start_date_str) if start_date_str else None
        end_date = parse_date(end_date_str) if end_date_str else None

        # 根據日期範圍過濾數據
        if start_date:
            df = df[df['date'] >= start_date]
        if end_date:
            df = df[df['date'] <= end_date]

        # 將 DataFrame 轉換為列表形式
        data = df.to_dict(orient='records')

        # 實現分頁
        paginator = Paginator(data, 20)  # 每頁顯示 20 條數據
        page_obj = paginator.get_page(page_number)

        # 將資料加入上下文
        context['data'] = page_obj.object_list
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        context['start_date'] = start_date_str
        context['end_date'] = end_date_str

        return context