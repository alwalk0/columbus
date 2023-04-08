from starlette.requests import Request
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


def create_routes_list(config) -> list[Route]:
    """Creates a list of all routes for the app using the data from the views config"""

    apis = config.get("APIs")
    apis_list = list(apis.keys())
    views_config = [create_views_config(api, config) for api in apis_list]
    views = sum(  # views_config is a list of lists, so we must flatten it
        views_config, []
    )
    routes = list(map(create_route, views))
    return routes


def create_views_config(api: str, config: dict) -> list[dict]:
    """Transforms initial config into a new data structure with all the necessary info to create routes and view functions"""

    table = config["APIs"][api]["table"]
    methods = config["APIs"][api]["methods"]
    models = config["models"]
    url = "/" + str(table)
    views = []
    for method in methods:
        if method == "POST":
            view = create_view_dict(method, url, config["database"], table, models)

        else:
            view = create_view_dict(
                method, url + "/{id:int}", config["database"], table, models
            )

        views.append(view)

    views.append(
        create_view_dict("GET", url, config["database"], table, models)
    )  # add the root url

    return views


def create_view_dict(
    method: str, url: str, database: databases.Database, table: str, models: str
) -> dict:
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


def create_route(specs: dict) -> Route:
    """Creates a Route object and maps it to the appropriate view function"""

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
