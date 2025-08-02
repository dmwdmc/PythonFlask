from flask import Blueprint
bp = Blueprint('permission', __name__, url_prefix='/permission')
from permission import views