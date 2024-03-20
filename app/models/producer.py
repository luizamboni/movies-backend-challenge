from . import db, movie_producer
import uuid

class Producer(db.Model):
    __tablename__ = 'producer'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(256), nullable=False, unique=True, primary_key=True)
    movies = db.relationship('Movie', secondary=movie_producer, back_populates='producers')
