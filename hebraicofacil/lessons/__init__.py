from flask import Blueprint

lessons_bp = Blueprint('lessons', __name__, url_prefix='/lessons')

from . import routes
