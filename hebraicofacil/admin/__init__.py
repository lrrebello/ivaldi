from flask import Blueprint

admin_bp = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

# Importar rotas após a definição do blueprint para evitar importações circulares
from . import routes