from sqlalchemy import Table

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse
from starlette.routing import Route

from columbus.framework.constants import RESPONSES, ERROR_RESPONSES, RAW_QUERIES
from columbus.framework.utils import import_file
import databases
from columbus.framework.requests import (
    get_request,
    post_request,
    put_request,
    delete_request,
)


def create_app(validated_config) -> Starlette:
    # replace the database url in the config with the actual Database object
    database = databases.Database(validated_config["database"])
    validated_config["database"] = database

    if not database:
        welcome = "Welcome to Columbus. This is demo mode. Please set up the database to generate APIs."
        route = [Route("/", endpoint=lambda request: PlainTextResponse(welcome))]
        return Starlette(routes=route)

    all_routes = create_routes_list(validated_config)
    app = Starlette(
        routes=all_routes,
        on_startup=[database.connect],
        on_shutdown=[database.disconnect],
    )

    return app


def create_routes_list(config):
    """Creates a list of all routes for the app with the data from the views config"""
    apis = config.get("apis")
    apis_list = list(apis.keys())
    views_config = [create_views_config(api, config) for api in apis_list]
    views = sum(  # views_config is a list of lists, so we must flatten it
        views_config, []
    )
    routes = list(map(create_route, views))
    return routes


def create_views_config(api, config):
    """Transforms initial config into a new data structure with all the necessary info to create routes and view functions"""

    table = config["apis"][api]["table"]
    methods = config["apis"][api]["methods"]
    models = config["models"]
    url = "/" + str(table)
    views = []
    for method in methods:
        if method == "POST":
            view = create_view_dict(
                method, url, config["database"], table, models
            )

        else:
            view = create_view_dict(
                method, url + "/{id:int}", config["database"], table, models
            )

        views.append(view)

    views.append(
        create_view_dict("GET", url, config["database"], table, models)
    )  # add the root url

    return views


def create_view_dict(method, url, database, table, models):
    """Creates the dict and populates it with the necessary objects (database, table)"""
    models_file = import_file(models)
    table = getattr(models_file, table)
    view_dict = {
        "method": method,
        "url": url,
        "database": database,
        "table": table,
    }

    return view_dict


def create_route(specs):
    """Creates a Route and maps it to the appropriate view function"""

    method = specs["method"]
    url = specs["url"]
    table = specs["table"]
    database = specs["database"]
    table = specs["table"]

    async def view_function(request: Request):
        match method:
            case "GET":
                return await get_request(request, table, database)
            case "POST":
                return await post_request(request, table, database)
            case "PUT":
                return await put_request(request, table, database)
            case "DELETE":
                return await delete_request(request, table, database)

    route = Route(url, endpoint=view_function, methods=[method])
    return route