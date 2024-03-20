from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

movie_producer = db.Table('movie_producer',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('producer_id', db.Integer, db.ForeignKey('producer.id'), primary_key=True)
)

movie_studio = db.Table('movie_studio',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'), primary_key=True),
    db.Column('studio_id', db.Integer, db.ForeignKey('studio.id'), primary_key=True)
)
from .movie import Movie
from .producer import Producer
from .studio import Studio
