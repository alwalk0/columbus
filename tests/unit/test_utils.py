from columbus.framework.utils import read_config, import_file, make_json_object, create_put_request_query

def test_read_config():
    config_dict = read_config('tests/integration/main.yml')
    assert 'models' in config_dict
    assert 'database' in config_dict
    assert 'APIs' in config_dict

def test_read_config_nonexistant_config():
    config_dict = read_config('nonexistant.yml')
    assert isinstance(config_dict, Exception)
    assert 'No config file in the root directory' in str(config_dict)

def test_import_file():
    filename = 'tests/integration/models.py'
    imported_file = import_file(filename)
    assert filename in str(imported_file)

def test_make_json_object(mock_table, mock_database_record):
    json_object = make_json_object(table=mock_table(), result=mock_database_record())
    assert json_object == {"foo": '1', "bar": '2', "test": '3'}


def test_put_request_query(mock_table):
    query = create_put_request_query(table=mock_table())
    assert query == 'UPDATE table SET foo = :foo, bar = :bar, test = :test WHERE id = :id'
