from columbus.framework.utils import make_json_object, create_put_request_query

ALLOWED_KEYS = ["database", "models", "apis"]
ALLOWED_KEYS_API = ["table", "methods"]
ALLOWED_METHODS_API = ["GET", "PUT", "POST", "DELETE"]



EXCEPTIONS = {
    "MISSING_KEYS": lambda keys: "Missing keys in config: {}".format(*keys),
    "WRONG_KEYS": lambda keys: "Wrong keys in config: {}".format(*keys),
    "NO_VALUE_FOR_KEY": lambda key: "No value for key {} in config".format(key),
    "INVALID_METHODS": lambda methods: "Invalid methods in methods key: {}".format(
        *methods
    ),
    "NO_DB_TABLE": lambda models_file, table_name: "No database table {} in {}".format(
        table_name, models_file
    ),
    "INVALID_DB_URL": lambda: "Invalid database url in config",
}


RESPONSES = {
    "GET_ONE": make_json_object,
    "GET_ALL": lambda table, results: [
        make_json_object(table, result) for result in results
    ],
    "PUT": lambda id: f"Successfully updated item with id {id}".format(id),
    "DELETE": lambda id: f"Successfully deleted item with id {id}".format(id),
    "POST": lambda id: f"Successfully created item with id {id}".format(id),
}

ERROR_RESPONSES = {
    "GET": "Error getting object(s).",
    "PUT": "Error updating objects.",
    "DELETE": "Error deleting objects.",
    "POST": "Error creating object.",
}


RAW_QUERIES = {
    "GET_ONE": lambda table: f"SELECT * FROM {table} WHERE id = :id".format(table),
    "DELETE": lambda table: f"DELETE FROM {table} WHERE id = :id".format(table),
    "PUT": create_put_request_query,
}