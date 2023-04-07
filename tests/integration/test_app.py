from starlette.testclient import TestClient
from sqlalchemy import create_engine
import sqlalchemy
import pytest
from tests.integration.models import metadata, dogs
from sqlalchemy_utils import database_exists, create_database, drop_database
import json


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    url = "postgresql://newuser:postgres@localhost/test4"
    engine = create_engine(url)
    create_database(url)
    data = [
        {"id": 1, "name": "boo", "breed": "labrador", "age": 3},
        {"id": 2, "name": "moo", "breed": "terrier", "age": 5},
    ]
    insert_query = dogs.insert(data)
    engine.execute(insert_query)
    yield
    drop_database(url)


@pytest.fixture()
def client(mocker):
    mocker.patch("columbus.start.MAIN_CONFIG_NAME", "tests/integration/main.yml")
    from columbus.main import app

    with TestClient(app) as client:
        yield client


def test_get(client):
    response = client.get("/dogs")
    print(response.text)
    assert response.status_code == 200


def test_post(client):
    response = client.post(
        "/dogs",
        content=json.dumps({"id": 3, "name": "fifi", "breed": "labrador", "age": 3}),
    )
    print(response.text)
    assert response.status_code == 200


def test_put(client):
    response = client.put("dogs/1", content=json.dumps({"name": "alfred"}))
    assert response.status_code == 200


def test_delete(client):
    response = client.delete("dogs/2")
    assert response.status_code == 200
