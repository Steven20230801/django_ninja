"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from .api import api
from .views import HomeView, TestView, RegisterView, LoginView, LogoutView, ProtectedView, ShowView, AccountView


urlpatterns = [
    path("admin/", admin.site.urls),
    # 傳統網頁視圖
    path("", HomeView.as_view(), name="home"),
    path("test/", TestView.as_view(), name="test"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("protected/", ProtectedView.as_view(), name="protected"),
    path("show/", ShowView.as_view(), name="show"),
    path("account/", AccountView.as_view(), name="account"),
    # API 端點
    path("api/", api.urls),
    path("__reload__/", include("django_browser_reload.urls")),
]
