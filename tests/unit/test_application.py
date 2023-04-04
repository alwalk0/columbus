
from unittest.mock import patch
from columbus.framework.application import create_route, create_view_dict, create_views_config, create_routes_list
import databases
from starlette.routing import Route
import pytest



class MockRoute():
    pass

def MockDatabase():
    pass

def MockTable():
    pass

@pytest.fixture()
def views_config():
    views_config = {'method': 'POST', 'url': '/dogs', 'database': MockDatabase(), 'table': MockTable()}
    yield views_config

@pytest.fixture()
def config():
    config = {'models': 'tests/integration/models.py', 'database': 'mock_url', 'apis': {'dogs': {'table': 'dogs', 'methods':['GET', 'POST'] }}}
    yield config    
              



def test_create_route(views_config):

    route = create_route(views_config)
    print(route)
    assert isinstance(route, Route)
    assert route.path == '/dogs'
    assert route.methods == {'POST'}


def test_create_view_dict(mocker):
    mocker.patch('columbus.framework.application.import_file', return_value= 'mock_file.py')
    mocker.patch('columbus.framework.application.getattr', return_value= MockTable())
    view_dict = create_view_dict(method='POST', url='/dogs', database=MockDatabase(), table=MockTable(), models='models.py')
    assert view_dict['method'] == 'POST'
    assert view_dict['url'] == '/dogs'
    assert view_dict['database'] == MockDatabase()
    assert view_dict['table'] == MockTable()

def test_create_views_config(mocker, config):
    mocker.patch('columbus.framework.application.create_view_dict', return_value={})
    views_config = create_views_config('dogs', config)
    assert isinstance(views_config, list)
    assert len(views_config) == 3

def test_create_routes_list(mocker, config):
    mocker.patch('columbus.framework.application.create_views_config', return_value=[])
    mocker.patch('columbus.framework.application.map', return_value=[MockRoute()])
    routes_list = create_routes_list(config)
    assert isinstance(routes_list, list)
    assert isinstance(routes_list[0], MockRoute)