from flask import Blueprint
bible_bp = Blueprint('bible', __name__, url_prefix='/bible')
from . import routes
from .routes import bible_bp
