
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

