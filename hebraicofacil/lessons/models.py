from .. import db

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    module_number = db.Column(db.Integer, unique=True, nullable=False)
    hebrew_text = db.Column(db.String(255), nullable=False, default='')
    consonants = db.Column(db.String(255), default='')
    vowels = db.Column(db.String(255), default='')
    syllables = db.Column(db.String(255), default='')
    visible = db.Column(db.Boolean, default=False)

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    module_id = db.Column(db.Integer, nullable=False)
    test_type = db.Column(db.String(20), nullable=False)  # 'consonants', 'vowels', 'syllables'
    correct_answers = db.Column(db.Integer, nullable=False, default=0)
    total_questions = db.Column(db.Integer, nullable=False, default=0)