from columbus.framework.utils import make_json_object, create_put_request_query


class ClassTestColumn:
    def __init__(self, key):
        self.key = key


class ClassTestTable:
    def __repr__(self):
        return 'table'
    columns = [ClassTestColumn('foo'), ClassTestColumn('bar'), ClassTestColumn('test')]

result = {'foo':'1', 'bar': '2', 'test': '3'}


def test_make_json_object():
    table = ClassTestTable()
    json_object = make_json_object(table, result)


def test_put_request_query():
    query = create_put_request_query(table=ClassTestTable())
    print(query)
