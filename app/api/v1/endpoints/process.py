import os
from typing import Annotated

from litestar import post
from litestar.params import Body
from litestar.enums import RequestEncodingType
from litestar.datastructures import UploadFile

from app.api.v1.services import process_ocr
from app.core.config.config import openai_system_msg_raw
from app.core.security import api_auth

@post(path="/process", cache=False, sync_to_thread=True, guards=[api_auth], opt={"API_KEY": os.environ.get("API_KEY")})
def handle_process(data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)]) -> dict:
    form = process_ocr(data, openai_system_msg_raw)
    return form

@post(path="/process/demo", cache=False, sync_to_thread=True, guards=[api_auth], opt={"API_KEY": os.environ.get("API_KEY")})
def handle_process_demo(data: Annotated[UploadFile, Body(media_type=RequestEncodingType.MULTI_PART)]) -> dict:
    return [{' _ _ ':' _ _ '}]
