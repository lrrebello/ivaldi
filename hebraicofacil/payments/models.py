from .. import db
from datetime import datetime
from ..auth.models import User  # Importar User para a relação

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(20), default='pending')
    transaction_id = db.Column(db.String(100))
    order_id = db.Column(db.String(100))  # Nova coluna para PIX
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Definir a relação com User
    user = db.relationship('User', backref=db.backref('payments', lazy=True))

class CoursePrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False, default=29.90)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)