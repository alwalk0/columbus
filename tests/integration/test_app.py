from starlette.testclient import TestClient
from sqlalchemy import create_engine
import sqlalchemy
import pytest
from tests.integration.models import metadata, dogs
from sqlalchemy_utils import database_exists, create_database, drop_database
import json


@pytest.fixture(scope="session", autouse=True)
def create_test_database():

    url = 'postgresql://newuser:postgres@localhost/test4'
    engine = create_engine(url)
    create_database(url)             # Create the test database.
    print(metadata.create_all(engine))
    data = {'id': 1, 'name': 'boo', 'breed': 'labrador', 'age': 3}
    insert_query = dogs.insert().values(data)  
    engine.execute(insert_query) 
    yield                            # Run the tests.
    drop_database(url)    
               # Drop the test database.
@pytest.fixture()
def client(mocker):
    mocker.patch('columbus.start.MAIN_CONFIG_NAME', 'tests/integration/main.yml')
    from columbus.main import app

    with TestClient(app) as client:
        yield client


def test_homepage(client, mocker):

    response = client.get('/dogs')
    print(response.text)
    assert response.status_code == 200

def test_post(client, mocker):
    response = client.post('/dogs', data=json.dumps({'id': 3, 'name': 'fifi', 'breed': 'labrador', 'age': 3}))
    print(response.text)
    assert response.status_code == 200    