from . import db, movie_producer, movie_studio
import uuid

class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(256), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    winner = db.Column(db.Boolean, default=False, nullable=False)
    producers = db.relationship('Producer', secondary=movie_producer, back_populates='movies')
    studios = db.relationship('Studio', secondary=movie_studio, back_populates='movies')
