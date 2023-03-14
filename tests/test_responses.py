from columbus.framework.responses import make_json_object


class ClassTestColumn:
    def __init__(self, key):
        self.key = key


class ClassTestTable:
    columns = [ClassTestColumn('foo'), ClassTestColumn('bar'), ClassTestColumn('test')]

result = {'foo':'1', 'bar': '2', 'test': '3'}


def test_make_json_object():
    table = ClassTestTable()
    json_object = make_json_object(table, result)
