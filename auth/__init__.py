# auth/__init__.py
from flask import Blueprint
bp = Blueprint('auth', __name__,url_prefix='/auth')
from auth import views