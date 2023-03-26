import pytest
from testcontainers.postgres import PostgresContainer
import sqlalchemy
import databases
from columbus.run import run
import uvicorn
import sys
import os
import psutil
import time
import requests
from multiprocessing import Process


metadata = sqlalchemy.MetaData()

dogs = sqlalchemy.Table(
    "dogs",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("breed", sqlalchemy.String),
    sqlalchemy.Column("age", sqlalchemy.Integer)
)


@pytest.fixture(scope='session')
def server():
    proc = Process(
    target=uvicorn.run,
    args=("columbus.framework.main:app",),
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


@pytest.fixture(scope='session')
def database():
    pass         



# @pytest.fixture(scope='module')
def test_connection(mocker, server):
    postgres_container = PostgresContainer("postgres:9.5")
    with postgres_container as postgres:
        engine = sqlalchemy.create_engine(postgres.get_connection_url())
        with engine.begin() as connection:
            result = connection.execute(sqlalchemy.text("select version()"))
            version, = result.fetchone()
            metadata.create_all(engine)
            data = {'id': 1, 'name': 'boo', 'breed': 'labrador', 'age': 3}
            insert_query = dogs.insert().values(data)
            result = connection.execute(insert_query)
            query = dogs.select()
            rows = connection.execute(query) 
            q1 = rows.fetchall()
            mocker.patch('columbus.framework.main.MAIN_CONFIG_NAME', 'tests/integration/main.yml')
            mocker.patch('columbus.framework.database.MAIN_CONFIG_NAME', 'tests/integration/main.yml')
            response = requests.get('http://0.0.0.0:8080')

