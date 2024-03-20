import pytest
from app import create_app
from models import db, Movie, Producer

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })
    
    with app.app_context():
        db.create_all()
    
    yield app
    
    with app.app_context():
        db.drop_all()



@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def sample_data(app):
    with app.app_context():

        producer1 = Producer(name="Producer One")
        producer2 = Producer(name="Producer Two")
        producer3 = Producer(name="Producer Three")

        movie1 = Movie(title="Movie One", year=2000, winner=True, producers=[producer1])
        movie2 = Movie(title="Movie Two", year=2005, winner=True, producers=[producer1])
        movie3 = Movie(title="Movie Three", year=2010, winner=True, producers=[producer2])
        movie4 = Movie(title="Movie Four", year=2011, winner=True, producers=[producer2])
        movie5 = Movie(title="Movie Five", year=2022, winner=True, producers=[producer3])
        movie6 = Movie(title="Movie Six", year=2023, winner=True, producers=[producer3])


        db.session.add_all([movie1, movie2, movie3, movie4, movie5, movie6])
        db.session.commit()

def test_json_response_contract(client, sample_data):
    response = client.get("/producers/intervals")
    
    assert response.status_code == 200
    
    json_data = response.json
    
    assert 'max' in json_data
    assert 'min' in json_data
    
    assert isinstance(json_data['max'], list)
    assert isinstance(json_data['min'], list)
    
    for item in json_data['max']:
        for key in ['producer', 'interval', 'previousWin', 'followingWin']:
            assert key in item

    for item in json_data['min']:
        for key in ['producer', 'interval', 'previousWin', 'followingWin']:
            assert key in item

def test_producers_intervals(client, sample_data):
    json_data = client.get("/producers/intervals").json

    assert len(json_data['max']) == 1
    assert json_data['max'][0]['producer'] == "Producer One"
    assert json_data['max'][0]['interval'] == 5
    
    
    assert len(json_data['min']) == 2
    assert json_data['min'][0]['producer'] == "Producer Two"
    assert json_data['min'][0]['interval'] == 1

    assert json_data['min'][1]['producer'] == "Producer Three"
    assert json_data['min'][1]['interval'] == 1


def test_import_data_without_body(client, sample_data):
    response = client.post("/import-data")
    
    status_code = response.status_code
    assert status_code == 400

    json_data = response.json
    assert json_data['status'] == 'failed'
    assert json_data['reason'] == '400 Bad Request: The browser (or proxy) sent a request that this server could not understand.'


def test_import_data_with_correct_data(client, sample_data):
    response = client.post("/import-data", json={ "file_path_or_url": "../data/movielist.csv" })
    
    status_code = response.status_code
    assert status_code == 200

    json_data = response.json
    assert json_data['status'] == 'succeeded'
