from starlette.testclient import TestClient
from sqlalchemy import create_engine
import pytest
from tests.integration.models import metadata, dogs
from sqlalchemy_utils import database_exists, create_database, drop_database
import json

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    db_url = 'postgresql://newuser:postgres@localhost/test4'
    engine = create_engine(db_url)
    if not database_exists(db_url):
        create_database(db_url)             
    metadata.create_all(engine)
    data = [
        {"id": 1, "name": "boo", "breed": "labrador", "age": 3},
        {"id": 2, "name": "moo", "breed": "terrier", "age": 5},
        {"id": 3, "name": "cloudy", "breed": "hound", "age": 7}
    ]
    insert_query = dogs.insert().values(data)  
    engine.execute(insert_query) 
    yield
    drop_database(db_url)


@pytest.fixture()
def client(mocker):
    mocker.patch("columbus.start.MAIN_CONFIG_NAME", "tests/integration/main.yml")
    from columbus.main import app

    with TestClient(app) as client:
        yield client


def test_get_all(client):
    response = client.get("/dogs")
    assert response.status_code == 200
    assert len(json.loads(response.text)) == 3

def test_get_one(client):
    response = client.get("/dogs/1")
    assert response.status_code == 200
    assert json.loads(response.text)['id'] == 1
    assert json.loads(response.text)['name'] == 'boo'

def test_post(client):
    response = client.post(
        "/dogs",
        content=json.dumps({"id": 4, "name": "fifi", "breed": "labrador", "age": 3}),
    )
    assert response.status_code == 200
    assert 'Successfully created item with id 4' in response.text


def test_put(client):
    response = client.put("dogs/1", content=json.dumps({"name": "alfred"}))
    assert response.status_code == 200
    assert 'Successfully updated item with id 1' in response.text


def test_delete(client):
    response = client.delete("dogs/2")
    assert response.status_code == 200
    assert 'Successfully deleted item with id 2' in response.text
