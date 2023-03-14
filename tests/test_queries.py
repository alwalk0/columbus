from columbus.framework.queries import create_put_request_query

class ClassTestColumn:
    def __init__(self, key):
        self.key = key

class ClassTestTable:
    def __repr__(self):
        return 'table'
    columns = [ClassTestColumn('foo'), ClassTestColumn('bar'), ClassTestColumn('test')]


def test_put_request_query():
    query = create_put_request_query(table=ClassTestTable())
    print(query)
