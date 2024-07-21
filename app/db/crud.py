import base64
import orjson
from typing import List
from datetime import datetime
import picologging as logging
from tzlocal import get_localzone

from models import Processed
from mongodb import mdb_collection

def safe_base64_decode(string) -> dict | str:
    try:
        decoded_bytes = base64.b64decode(string, validate=True)
        return orjson.loads(decoded_bytes.decode('utf-8'))
    except Exception:
        return string

def handle_base64_filename(filename) -> List[str]:
    filename_json = safe_base64_decode(filename)
    if isinstance(filename_json, str):
        return ['test', filename]
    return [filename_json.get('userId', 'test'), filename_json.get('fileName', filename)]

def save2db(file_name, file_format, file_content, file_text, llm_chat, form) -> None:
    try:
        filename = handle_base64_filename(file_name)
        data = Processed(
                    userId=filename[0],
                    timeStamp=datetime.now(get_localzone()).strftime("%Y-%m-%d %H:%M:%S %z"),
                    OriginalFileName=filename[1],
                    OriginalFileFormat=file_format,
                    OriginalFileContent=file_content,
                    ProcessedOCRText=file_text,
                    ProcessedLLMCompletion=llm_chat,
                    ProcessedJSON=form
               )

        result = mdb_collection.insert_one(data.__dict__)

        logging.info(f"save2db: DB Updated Successfully, ID: {str(result.inserted_id)}.")
    except Exception as e:
        logging.error(f"save2db: DB Update Failed.\nException occurred: {e}", exc_info=True)
