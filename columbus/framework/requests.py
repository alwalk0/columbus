from sqlalchemy import Table

from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from databases import Database

from columbus.framework.constants import RESPONSES, ERROR_RESPONSES, RAW_QUERIES


async def get_request(request: Request, table: Table, database: Database) -> Response:
    try:
        if request.path_params:
            query = RAW_QUERIES["GET_ONE"](table)
            pk = request.path_params["id"]
            result = await database.fetch_one(query=query, values={"id": pk})
            response = RESPONSES["GET_ONE"](table, result)
            json_response = JSONResponse(response)
        else:
            query = table.select()
            results = await database.fetch_all(query)
            response = RESPONSES["GET_ALL"](table, results)
            json_response = JSONResponse(response)

        return json_response
    except Exception as e:
        return Response(content=ERROR_RESPONSES["GET"], status_code=500)


async def post_request(request: Request, table: Table, database: Database) -> Response:
    try:
        data = await request.json()
        query = table.insert().values(data)
        result = await database.execute(query)
        response = RESPONSES["POST"](data["id"])
        return JSONResponse(response)
    except Exception as e:
        return Response(content=ERROR_RESPONSES["POST"], status_code=500)


async def put_request(request: Request, table: Table, database: Database) -> Response:
    try:
        data = await request.json()
        query = RAW_QUERIES["PUT"](table)
        pk = pk = request.path_params["id"]
        values = {"id": pk} | data
        result = await database.execute(query=query, values=values)
        response = RESPONSES["PUT"](pk)
        return JSONResponse(response)
    except Exception as e:
        return Response(content=ERROR_RESPONSES["PUT"], status_code=500)


async def delete_request(
    request: Request, table: Table, database: Database
) -> Response:
    try:
        query = RAW_QUERIES["DELETE"](table)
        pk = request.path_params["id"]
        result = await database.execute(query=query, values={"id": pk})
        response = RESPONSES["DELETE"](pk)
        return JSONResponse(response)
    except Exception as e:
        return Response(content=ERROR_RESPONSES["DELETE"], status_code=500)
