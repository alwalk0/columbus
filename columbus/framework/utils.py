import importlib
import importlib.machinery
import os
import yaml
from sqlalchemy import Table
from types import ModuleType
from databases.backends.postgres import Record


def read_config(config_path: str) -> dict:
    if not os.path.exists(config_path):
        return Exception(
            "No config file in the root directory. Please add a main.yml config."
        )

    with open(config_path, "r") as file:
        config_dict = yaml.load(file, Loader=yaml.BaseLoader)
        return config_dict


def import_file(path: str) -> ModuleType:
    file_path = os.path.abspath(path)
    modulename = importlib.machinery.SourceFileLoader(
        path.removesuffix(".py"), file_path
    ).load_module()
    return modulename


def make_json_object(table: Table, result: Record) -> dict:
    fields = [column.key for column in table.columns]
    content = {field: result[field] for field in fields}
    return content


def create_put_request_query(table: Table) -> str:
    fields = [column.key for column in table.columns if column.key != "id"]
    fields_string = [f"{field} = :{field}".format(field) for field in fields]
    query = "UPDATE {} SET {} WHERE id = :id".format(table, ", ".join(fields_string))
    return query


def create_error_message(message: str, keys: list) -> str:
    if len(keys) == 1:
        final_string = (message + ": {}").format(keys[0])
    else:
        keys_strings = [f"{key}".format(key) for key in keys]
        final_string = (message + ": {}").format(", ".join(keys_strings))
    return final_string
