from unittest.mock import patch
from columbus.framework.application import (
    create_route,
    create_view_dict,
    create_views_config,
    create_routes_list,
)
import databases
from starlette.routing import Route
import pytest


@pytest.fixture()
def views_config(mock_table, mock_database):
    views_config = {
        "method": "POST",
        "url": "/dogs",
        "database": mock_database,
        "table": mock_table,
        "auth": False
    }
    yield views_config


@pytest.fixture()
def config():
    config = {
        "models": "tests/integration/models.py",
        "database": "mock_url",
        "APIs": {"dogs": {"table": "dogs", "methods": ["GET", "POST"], "auth": ["POST"]}},
    }
    yield config


def test_create_routes_list(mocker, config, mock_route):
    mocker.patch("columbus.framework.application.create_views_config", return_value=[])
    mocker.patch("columbus.framework.application.map", return_value=[mock_route()])
    routes_list = create_routes_list(config)
    assert isinstance(routes_list, list)
    assert isinstance(routes_list[0], mock_route)


def test_create_views_config(mocker, config):
    mocker.patch("columbus.framework.application.create_view_dict", return_value={})
    views_config = create_views_config("dogs", config)
    assert isinstance(views_config, list)
    assert len(views_config) == 3


def test_create_view_dict(mocker, mock_table, mock_database):
    mocker.patch(
        "columbus.framework.application.import_file", return_value="mock_file.py"
    )
    mocker.patch("columbus.framework.application.getattr", return_value=mock_table)
    view_dict = create_view_dict(
        method="POST",
        url="/dogs",
        database=mock_database,
        table=mock_table,
        models="models.py",
        auth_required=False
    )
    assert view_dict["method"] == "POST"
    assert view_dict["url"] == "/dogs"
    assert view_dict["database"] == mock_database
    assert view_dict["table"] == mock_table


def test_create_route(views_config):
    route = create_route(views_config)
    assert isinstance(route, Route)
    assert route.path == "/dogs"
    assert route.methods == {"POST"}
