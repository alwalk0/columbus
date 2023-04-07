import pytest


@pytest.fixture()
def mock_table():
    class MockColumn:
        def __init__(self, key):
            self.key = key

    class MockTable:
        def __repr__(self):
            return "table"

        columns = [MockColumn("foo"), MockColumn("bar"), MockColumn("test")]

    yield MockTable


@pytest.fixture()
def mock_database_record():
    class MockDatabaseRecord:
        def __init__(self):
            self.fields = {"foo": "1", "bar": "2", "test": "3"}

        def __getitem__(self, item):
            return self.fields[item]

    yield MockDatabaseRecord


@pytest.fixture()
def mock_database():
    class MockDatabase:
        pass

    yield MockDatabase


@pytest.fixture()
def mock_route():
    class MockRoute:
        pass

    yield MockRoute
