from app import create_app
from models.movie import db
from services.movie_service import import_csv_to_database


app = create_app()

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        import_csv_to_database("../data/movielist.csv")
        query = """
            SELECT * FROM movie

        """


        for row in db.engine.execute(query):
            print(dict(row))
