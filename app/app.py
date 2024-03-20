from flask import Flask
from models.movie import db
from controllers.movie_controller import movie_blueprint

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    
    if test_config is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
    else:
        app.config.update(test_config)
    
    db.init_app(app)
    app.register_blueprint(movie_blueprint)
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()

    app.run(debug=True)
