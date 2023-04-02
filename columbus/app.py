from columbus.framework.main import create_app
from columbus.framework.utils import read_config
from columbus.framework.validators import validate_config

MAIN_CONFIG_NAME = "tests/integration/main.yml"

config_dict = read_config(MAIN_CONFIG_NAME)
if isinstance(config_dict, Exception):
    raise Exception(
        "No main.yml  config. Please add a main.yml config in the root directory."
    )


validated_config = validate_config(config_dict)
if isinstance(validated_config, Exception):
    raise Exception(
        "This app will not run due to errors in config. Errors: {}".format(
            validated_config
        )
    )


app = create_app(config_dict)