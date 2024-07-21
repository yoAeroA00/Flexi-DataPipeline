import os
import picologging as logging
from litestar.connection import ASGIConnection
from litestar.handlers.base import BaseRouteHandler
from litestar.exceptions import NotAuthorizedException

API_KEY_AUTH = os.getenv('API_KEY_AUTH', "True").lower() in ('enable', 'true', '1')
API_KEY_HEADER_NAME = os.getenv('API_KEY_HEADER_NAME')

async def api_auth(connection: ASGIConnection, route_handler: BaseRouteHandler) -> None:
    if API_KEY_AUTH:
        if connection.headers.get(API_KEY_HEADER_NAME, '') != route_handler.opt.get("API_KEY", 'none'):
            logging.warn('Invalid API Key.')
            raise NotAuthorizedException()
