import os
import json
import picologging as logging
from dotenv import load_dotenv

from litestar.openapi import OpenAPIConfig
from litestar.logging import LoggingConfig
# from litestar.stores.redis import RedisStore
from litestar.config.compression import CompressionConfig
# from litestar.config.response_cache import ResponseCacheConfig

dot_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(dotenv_path=dot_env_path, verbose=True, override=True, encoding='utf-8')

with open(os.path.join(os.path.dirname(__file__), os.getenv('OPENAI_PRES_REQ_FILENAME', 'llm_prompts/sample.json')), 'rb') as file:
    openai_request_content = file.read()
    openai_system_msg_raw = json.loads(openai_request_content)

logging_config = LoggingConfig(
    disable_existing_loggers = True, 
    root = {"level": logging.getLevelName(int(os.getenv('LOGGING_LEVEL', '20'))), "handlers": ["console"]},
    formatters = {
        "standard": {"format": "[%(asctime)s] %(levelname)s - %(name)s - %(module)s - %(lineno)d - %(message)s",
                     "datefmt": "%Y-%m-%d %H:%M:%S %z"
        }
    },
)

# redis_store = RedisStore(url="redis://localhost/", port=6379, db=0)
# cache_config = ResponseCacheConfig(store=redis_store)

if os.getenv('ENABLE_GZIP_MW', 'True').lower() in ('enable', 'true', '1'):
    gzip_compression = CompressionConfig(backend="gzip",
                                         minimum_size=int(os.getenv('GZIP_MIN_SIZE', '1460')),
                                         gzip_compress_level=int(os.getenv('GZIP_COMPRESSION_LVL', '9')))
else:
    gzip_compression = None

if os.getenv('IS_PRODUCTION', 'True').lower() in ('enable', 'true', '1'):
    openapi_config = None
    app_debug = False
else:
    openapi_config = OpenAPIConfig(title="Flexi-DataPipeline", version="1.0.0")
    app_debug = True
