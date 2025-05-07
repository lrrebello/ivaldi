from flask_login import UserMixin
from .. import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(1), nullable=False, default='n')  # 'n' = aluno, 's' = professor, 'a' = admin
    email_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    confirmation_token = db.Column(db.String(100))
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    birth_date = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    cep = db.Column(db.String(8), nullable=False)
    phone_number = db.Column(db.String(14), nullable=False)
    country = db.Column(db.String(100), nullable=False)  # New field for country
    state = db.Column(db.String(100), nullable=False)    # New field for state

    def get_id(self):
        return str(self.id)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)

class GameConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visible = db.Column(db.Boolean, default=False)  # Jogo oculto por padrão