from . import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class novels(db.Model):
    novel_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image_url = db.Column(db.String(255))
    title = db.Column(db.String(255))
    genre = db.Column(db.Integer)
    chapters = db.relationship('chapters', backref='novel', lazy=True)

    def __repr__(self):
        return '<Novel {}>'.format(self.title)

class chapters(db.Model):
    chapter_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    novel_id = db.Column(db.Integer, db.ForeignKey('novels.novel_id'), nullable=False)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return '<Chapter {}>'.format(self.title)
