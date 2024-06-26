from app.database import db

class novels(db.Model):
    __tablename__ = 'novels'

    novel_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_url = db.Column(db.String(255))
    title = db.Column(db.String(255))
    genre = db.Column(db.Integer)
    synopsis = db.Column(db.Text)
    last_chapter = db.Column(db.Integer, default=0)
    chapters = db.relationship('chapters', backref='novel', lazy=True)

    def __repr__(self):
        return '<Novel {}>'.format(self.title)

class chapters(db.Model):
    __tablename__ = 'chapters'

    chapter_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.novel_id'), nullable=False)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=db.func.now())
    index = db.Column(db.Integer)

    def __repr__(self):
        return '<Chapter {}>'.format(self.title)
