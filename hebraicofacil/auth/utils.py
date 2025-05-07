import re
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from .. import login_manager
from .models import User

def validate_cpf(cpf):
    """Valida um CPF com base nos dígitos verificadores."""
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    
    total = 0
    for i in range(9):
        total += int(cpf[i]) * (10 - i)
    remainder = total % 11
    digit1 = 0 if remainder < 2 else 11 - remainder
    
    total = 0
    for i in range(10):
        total += int(cpf[i]) * (11 - i)
    remainder = total % 11
    digit2 = 0 if remainder < 2 else 11 - remainder
    
    is_valid = cpf[-2:] == f"{digit1}{digit2}"
    return is_valid

def validate_birth_date(birth_date):
    try:
        birth_date = datetime.strptime(birth_date, '%d/%m/%Y')
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return 18 <= age <= 120
    except ValueError:
        return False

def validate_cep(cep):
    cep = ''.join(filter(str.isdigit, cep))
    return len(cep) == 8

def validate_phone(phone):
    """Valida o número de telefone com base no código do país."""
    phone_patterns = {
        '+55': r'^\+55\d{2}\d{9}$',  # Brazil: +55DDNNNNNNNNN
        '+1': r'^\+1\d{10}$',        # USA: +1NNNNNNNNNN
        '+54': r'^\+54\d{10}$',       # Argentina: +54NNNNNNNNNN
        '+351': r'^\+351\d{9}$'      # Portugal: +351NNNNNNNNN
        # Add more patterns as needed
    }
    
    for country_code, pattern in phone_patterns.items():
        if phone.startswith(country_code) and re.match(pattern, phone):
            return True
    return False

def hash_password(password):
    """Cria um hash seguro da senha fornecida."""
    return generate_password_hash(password)

def check_password(hashed_password, password):
    """Verifica se a senha fornecida corresponde ao hash armazenado."""
    return check_password_hash(hashed_password, password)

def generate_confirmation_token(email):
    """Gera um token de confirmação para o email fornecido."""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config.get('SECURITY_PASSWORD_SALT', 'email-confirm-salt'))

def confirm_token(token, expiration=3600):
    """Confirma um token de confirmação e retorna o email associado."""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config.get('SECURITY_PASSWORD_SALT', 'email-confirm-salt'),
            max_age=expiration
        )
        return email
    except:
        return False

# Adicionar o user_loader para o Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Carrega o usuário a partir do ID armazenado na sessão."""
    return User.query.get(int(user_id))