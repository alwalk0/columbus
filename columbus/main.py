from columbus.framework.application import create_routes_list
from columbus.framework.utils import read_config
from columbus.framework.validators import validate_config
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import PlainTextResponse
import databases
import contextlib
from columbus.start import MAIN_CONFIG_NAME
import base64
from starlette.authentication import SimpleUser, AuthCredentials, AuthenticationError, AuthenticationBackend
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
import binascii


@contextlib.asynccontextmanager
async def lifespan(app):
    await database.connect()
    yield
    await database.disconnect()

class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            return

        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                return
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            raise AuthenticationError('Invalid basic auth credentials')

        username, _, password = decoded.partition(":")
        # TODO: You'd want to verify the username and password here.
        return AuthCredentials(["authenticated"]), SimpleUser(username)




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


database = databases.Database(validated_config["database"])
validated_config["database"] = database #replace the database url in config with the actual Database object

routes = create_routes_list(validated_config)

middleware = [
    Middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
]

app = Starlette(routes=routes, lifespan=lifespan, middleware=middleware)