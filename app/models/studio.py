from . import db, movie_studio
import uuid

class Studio(db.Model):
    __tablename__ = 'studio'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(256), nullable=False, unique=True)
    movies = db.relationship('Movie', secondary=movie_studio, back_populates='studios')
