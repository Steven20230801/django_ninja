# api/schemas.py
from ninja import Schema
from typing import Optional


class UserSchema(Schema):
    id: int
    username: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserRegisterSchema(Schema):
    username: str
    email: str
    password: str


class TokenSchema(Schema):
    access_token: str
    token_type: str
