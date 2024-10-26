# api/security.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from django.conf import settings
from ninja.security import HttpBearer
from ninja.errors import AuthenticationError, ValidationError
from django.contrib.auth.models import User

# 設定參數
SECRET_KEY = settings.SECRET_KEY  # 使用 Django 的 SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None


class JWTBearer(HttpBearer):
    def authenticate(self, request, token):
        username = verify_token(token)
        if username is None:
            raise AuthenticationError("無效的認證憑證")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError("使用者不存在")
        return user
