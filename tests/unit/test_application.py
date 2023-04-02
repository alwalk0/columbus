
# from columbus.framework.main import create_routes_list, create_app, create_route
# import columbus
# columbus.framework.main.MAIN_CONFIG_NAME = 'columbus/tests/integration/main.yml
from unittest.mock import patch
import columbus

class MockRoute:
    def __init__(self, route_url, endpoint, methods):
        self.route_url = route_url
        self.endpoint = endpoint
        self.methodd = methods



# def test_create_app(mocker):
#     pass
#     # mocker.patch('columbus.framework.application.create_routes_list', return_value = [])
#     # app = create_app(0)


# def test_create_routes_list(mocker):
#     mocker.patch("columbus.framework.utils.MAIN_CONFIG_NAME", 'tests/integration/main.yml')
#     from columbus.framework.main import create_routes_list
#     routes = create_routes_list(specs={'table':'test_table', 'methods': []})


# def test_create_route(mocker):
#     mocker.patch('columbus.framework.application.create_view_function', return_value = None )
#     route = create_route(method='GET', url='/test', table_name='test')
    

