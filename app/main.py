from litestar import Litestar
from litestar.exceptions import HTTPException

from core.config.config import logging_config, gzip_compression, openapi_config, app_debug
from db.mongodb import db_connection
from core.middleware import ProcessTimeHeader
from utils.exceptions import exception_handler
from api.router import api_router

app = Litestar(route_handlers=[api_router], debug=app_debug, compression_config=gzip_compression,
               middleware=[ProcessTimeHeader], openapi_config=openapi_config,
               exception_handlers={HTTPException: exception_handler},
               logging_config=logging_config, # response_cache_config=cache_config,
               lifespan=[db_connection]
               )
