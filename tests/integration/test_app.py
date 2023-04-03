from starlette.testclient import TestClient
from httpx import AsyncClient
from columbus.framework.main import create_app
from sqlalchemy import create_engine
from testcontainers.postgres import PostgresContainer
import sqlalchemy
import pytest
from .models import metadata, dogs
# from columbus.app2 import metadata
import databases
from sqlalchemy_utils import database_exists, create_database, drop_database
from columbus.framework.main import create_routes_list
from starlette.applications import Starlette
import contextlib
from starlette.routing import Route
from starlette.responses import PlainTextResponse
# from columbus.app import app
from columbus.framework.main import create_app
import json

config = {'models': 'tests/integration/models.py', 'database': 'postgresql://newuser:postgres@localhost/test2', 'apis': {'hello_world': {'table': 'dogs', 'methods':['GET', 'POST'] }}}

app = create_app(config)
@pytest.fixture(scope="session", autouse=True)
def create_test_database():

    url = 'postgresql://newuser:postgres@localhost/test2'
    engine = create_engine(url)
    create_database(url)             # Create the test database.
    metadata.create_all(engine) 
    data = {'id': 1, 'name': 'boo', 'breed': 'labrador', 'age': 3}
    insert_query = dogs.insert().values(data)  
    engine.execute(insert_query) 
    yield                            # Run the tests.
    drop_database(url)    
               # Drop the test database.
@pytest.fixture()
def client(mocker):

    with TestClient(app) as client:
        yield client




def test_homepage(client, mocker):
    # url = app.url_path_for('/dogs')
    response = client.get('/dogs')
    print(response.text)
    assert response.status_code == 200

def test_post(client, mocker):
    # url = app.url_path_for('/dogs')
    response = client.post('/dogs', data=json.dumps({'id': 3, 'name': 'fifi', 'breed': 'labrador', 'age': 3}))
    print(response.text)
    assert response.status_code == 200    