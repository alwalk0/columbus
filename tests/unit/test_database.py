from columbus.framework.database import do_database_setup, import_from_file, import_all_database_tables
import pytest 

class ClassTestColumn:
    def __init__(self, key):
        self.key = key

class ClassTestTable:
    def __repr__(self):
        return 'table'
    columns = [ClassTestColumn('foo'), ClassTestColumn('bar'), ClassTestColumn('test')]
    name = 'test'

MAIN_CONFIG_NAME = 'tests/main.yml'


# def test_do_databse_setup(mocker):

#     mocker.patch('columbus.framework.database.MAIN_CONFIG_NAME', return_value='tests/main.yml')

#     mocker.patch('columbus.framework.database.import_from_file', return_value='database')
#     mocker.patch('columbus.framework.database.import_all_database_tables', return_value='database')
#     database, database_tables = do_database_setup()


# def test_import_from_file():
#     import_from_file('tests/test_file.py', 'object')


def test_import_all_database_tables(mocker):
    mocker.patch('columbus.framework.database.import_from_file', return_value=ClassTestTable())
    tables_dict = import_all_database_tables(apis={'api': {'table': 'table_name'} }, models_file=' ')
    print(tables_dict)

