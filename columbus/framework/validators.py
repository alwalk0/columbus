
import os
import databases
from columbus.framework.utils import import_file
from columbus.framework.constants import (
    EXCEPTIONS,
    ALLOWED_KEYS,
    ALLOWED_METHODS_API,
    ALLOWED_KEYS_API,
)


def validate_config(config):
    keys = list(config.keys())
    if 'demo' in keys and config.get('demo') == True:
        return 'demo'
    missing_keys = [key for key in ALLOWED_KEYS if key not in keys]
    if missing_keys:
        return Exception(EXCEPTIONS["MISSING_KEYS"](missing_keys))

    extra_keys = [key for key in keys if key not in ALLOWED_KEYS]
    if extra_keys:
        return Exception(EXCEPTIONS["WRONG_KEYS"](extra_keys))

    for key in keys:
        validated_key = validate_config_key(config, key)
        if isinstance(validated_key, Exception):
            return validated_key

    return config


def validate_config_key(config, key):
    match key:
        case "models":
            models_validator = validate_models(config)
            return models_validator

        case "database":
            database_validator = validate_database(config)
            return database_validator
        case "apis":
            api_validator = validate_api_config(config)
            return api_validator
    return key


def validate_models(config):
    models_file_name = config.get("models")
    if models_file_name is None:
        return Exception(EXCEPTIONS["NO_VALUE_FOR_KEY"]("models"))
    if not os.path.exists(models_file_name):
        return Exception("No such file: {}".format(models_file_name))
    return models_file_name


def validate_database(config):
    database_url = config.get("database")
    if database_url == "demo":
        return "demo"
    if database_url is None:
        return Exception(EXCEPTIONS["NO_VALUE_FOR_KEY"]("database"))
    try:
        database = databases.Database(database_url)
    except KeyError: 
        return Exception(EXCEPTIONS["INVALID_DB_URL"]())

    return database_url


def validate_api_config(config):
    apis = config.get("apis")
    models_file = config.get("models")
    if apis is None:
        return Exception(EXCEPTIONS["NO_VALUE_FOR_KEY"]("apis"))

    for api in apis:
        api_dict = apis.get(api)
        if api_dict is None:
            return Exception(EXCEPTIONS["NO_VALUE_FOR_KEY"](api))
        api_validator = validate_api(models_file, api_dict)
        if isinstance(api_validator, Exception):
            return api_validator

    return apis


def validate_api(models_file, api):
    keys = list(api.keys())
    missing_keys = [key for key in ALLOWED_KEYS_API if key not in keys]
    if missing_keys:
        return Exception(EXCEPTIONS["MISSING_KEYS"](missing_keys))

    extra_keys = [key for key in keys if key not in ALLOWED_KEYS_API]
    if extra_keys:
        return Exception(EXCEPTIONS["WRONG_KEYS"](extra_keys))

    table_name = api.get("table")
    methods = api.get("methods")

    if table_name is None:
        return Exception(EXCEPTIONS["NO_VALUE_FOR_KEY"]("table"))

    models_module = import_file(models_file)
    if not hasattr(models_module, table_name):
        return Exception(EXCEPTIONS["NO_DB_TABLE"](models_file, table_name))

    if methods is None:
        return Exception(EXCEPTIONS["NO_VALUE_FOR_KEY"]("methods"))

    invalid_methods = [
        method for method in methods if method not in ALLOWED_METHODS_API
    ]
    if invalid_methods:
        return Exception(EXCEPTIONS["INVALID_METHODS"](invalid_methods))

    return api