import pytest
from testcontainers.postgres import PostgresContainer
import sqlalchemy
import databases
import uvicorn
import sys
import os
import psutil
import time
import requests
from multiprocessing import Process
from unittest import mock

from .models import dogs, metadata
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from columbus.framework.main import create_app
from sqlalchemy.orm import sessionmaker
from columbus.run import start



@pytest.fixture(scope='session')
def connection():
    postgres_container = PostgresContainer(image='postgres:latest')
    with postgres_container as postgres:
        engine = sqlalchemy.create_engine(postgres.get_connection_url())
        url = postgres.get_connection_url()
        with engine.begin() as connection:
            result = connection.execute(sqlalchemy.text("select version()"))
            version, = result.fetchone()
            metadata.create_all(engine)
            data = {'id': 1, 'name': 'boo', 'breed': 'labrador', 'age': 3}
            insert_query = dogs.insert().values(data)
            result = connection.execute(insert_query)

            yield url



@pytest.fixture(scope='module')
def config(connection):
    config = {'models': 'tests/integration/models.py', 'database': connection, 'apis': {'hello_world': {'table': 'dogs', 'methods':['GET'] }}}
    yield config
 
@pytest.fixture()
def server(mocker, config, connection):
    print(config)
    mocker.patch('columbus.app.validate_config', config)
    # app = create_app(config)
    proc = Process(
    target=uvicorn.run,
    args=('columbus.app:app',),
    kwargs={
        "host":'0.0.0.0',
        "port": 8080,
        "workers": 3,
    },
)
    proc.start()
    time.sleep(10)
    assert proc.is_alive()
    try:
        yield
    finally:
        pid = os.getpid()
        parent = psutil.Process(pid)
        for child in parent.children(recursive=True):
            child.kill()




def test_connection(server):
    pass

    # mocker.patch("columbus.framework.utils.MAIN_CONFIG_NAME", 'tests/integration/main.yml')
    # engine = server[0]
    # config_dict = server[1]
    # query = dogs.select()
    # rows = engine.execute(query) 
    # q1 = rows.fetchall()
    # print(q1)
    # start()
   
    # response = requests.get('http://0.0.0.0:8080')

