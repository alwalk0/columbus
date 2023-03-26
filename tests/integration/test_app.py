import pytest
from testcontainers.postgres import PostgresContainer
import sqlalchemy
import databases


metadata = sqlalchemy.MetaData()

dogs = sqlalchemy.Table(
    "dogs",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("breed", sqlalchemy.String),
    sqlalchemy.Column("age", sqlalchemy.Integer)
)




# @pytest.fixture(scope='module')
def test_connection():
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
            print(q1)
            