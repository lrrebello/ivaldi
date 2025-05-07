from .. import db

class BibleBook(db.Model):
    __tablename__ = 'bible_books'
    
    id = db.Column(db.Integer, primary_key=True)
    name_hebrew = db.Column(db.String(100), nullable=False)
    name_portuguese = db.Column(db.String(100), nullable=False)
    name_transliterated = db.Column(db.String(100), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    testament = db.Column(db.String(10), nullable=False)  # 'tanakh' ou 'brit_hadasha'
    
    # Relacionamento com capítulos
    chapters = db.relationship('BibleChapter', backref='book', lazy=True)
    
    def __repr__(self):
        return f'<BibleBook {self.name_portuguese}>'

class BibleChapter(db.Model):
    __tablename__ = 'bible_chapters'
    
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('bible_books.id'), nullable=False)
    chapter_number = db.Column(db.Integer, nullable=False)
    
    # Relacionamento com versículos
    verses = db.relationship('BibleVerse', backref='chapter', lazy=True)
    
    def __repr__(self):
        return f'<BibleChapter {self.book.name_portuguese} {self.chapter_number}>'

class BibleVerse(db.Model):
    __tablename__ = 'bible_verses'
    
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('bible_chapters.id'), nullable=False)
    verse_number = db.Column(db.Integer, nullable=False)
    text_hebrew = db.Column(db.Text, nullable=False)
    text_transliterated = db.Column(db.Text, nullable=False)
    text_portuguese = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return f'<BibleVerse {self.chapter.book.name_portuguese} {self.chapter.chapter_number}:{self.verse_number}>'
