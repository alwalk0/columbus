from sqlalchemy import Table


def create_put_request_query(table: Table) -> str:
    fields = [column.key for column in table.columns if column.key != "id"]
    fields_string = [f"{field} = :{field}".format(field) for field in fields]
    query = "UPDATE {} SET {} WHERE id = :id".format(table,
        ", ".join(fields_string)
    )
    return query


raw_queries = {
    "GET_one": lambda table: f"SELECT * FROM {table} WHERE id = :id".format(table),
    "DELETE": lambda table: f"DELETE FROM {table} WHERE id = :id".format(table),
    "PUT": create_put_request_query,
}