# myapp/authentication.py

from ninja.security import HttpBearer, django_auth
from rest_framework.authtoken.models import Token


class TokenAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            token_obj = Token.objects.get(key=token)
            return token_obj.user
        except Token.DoesNotExist:
            return None
