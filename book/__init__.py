# book/__init__.py
from flask import Blueprint
bp = Blueprint('book', __name__,url_prefix='/book')
from book import views