import os
import io
import httpx
import pymupdf
from PIL import Image
import picologging as logging

from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_406_NOT_ACCEPTABLE, HTTP_500_INTERNAL_SERVER_ERROR

from llm import llm_txt2json
from app.db.crud import save2db

HTTPX_HTTP1 = os.getenv('HTTPX_HTTP1', 'True').lower() in ('enable', 'true', '1')
HTTPX_HTTP2 = os.getenv('HTTPX_HTTP2', 'True').lower() in ('enable', 'true', '1')
HTTPX_API_TIMEOUT = float(os.getenv('HTTPX_API_TIMEOUT', '40'))
HTTPX_TIMEOUT_API = httpx.Timeout(connect=HTTPX_API_TIMEOUT * 1.5, read=HTTPX_API_TIMEOUT * 2, write=HTTPX_API_TIMEOUT * 2, pool=HTTPX_API_TIMEOUT * 1.5)

USE_PDF2TEXT = os.getenv('USE_PDF2TEXT', 'False').lower() in ('enable', 'true', '1')
USE_PDF2IMAGE_DS2O = os.getenv('USE_PDF2IMAGE_DS2O', 'True').lower() in ('enable', 'true', '1')

ACCEPTABLE_IMAGE_FORMAT = ["image/jpeg", "image/png", "image/bmp"]
ACCEPTABLE_DOCS_FORMAT = ["application/pdf"]

OCR_SERVICE_NAME = os.getenv('OCR_SERVICE_NAME')
OCR_SERVICE_DOMAIN = os.getenv('OCR_SERVICE_DOMAIN')
OCR_SERVICE_API_VER = os.getenv('OCR_SERVICE_API_VER')
ocr_headers = {
                'Content-Type': 'application/octet-stream',
                'Ocp-Apim-Subscription-Key': os.getenv('OCR_SERVICE_KEY'),
}
ocr_params = {
                'features': 'read',
                'model-version': os.getenv('OCR_SERVICE_MODEL_VER', 'latest'),
                'language': os.getenv('OCR_SERVICE_LANG', 'en'),
}

def pdf2text(data):
    try:
        pdf_file = io.BytesIO(data)
        with pymupdf.open("pdf", pdf_file) as doc:
            text = chr(12).join([page.get_text() for page in doc])

        return text
    except Exception as e:
        print(f"Failed to convert PDF to text: {e}")

def pil2jpeg(image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr.read()

def combine_images(images, vertical):
    if not images:
        raise ValueError("No images to combine.")

    if vertical:
        total_width = max(img.width for img in images)
        total_height = sum(img.height for img in images)
        combined_image = Image.new('RGB', (total_width, total_height))
        y_offset = 0
        for img in images:
            combined_image.paste(img, (0, y_offset))
            y_offset += img.height
    else:
        total_width = sum(img.width for img in images)
        total_height = max(img.height for img in images)
        combined_image = Image.new('RGB', (total_width, total_height))
        x_offset = 0
        for img in images:
            combined_image.paste(img, (x_offset, 0))
            x_offset += img.width
    return combined_image

def pdf2image(data, ds2o):
    images = []

    pdf_file = io.BytesIO(data)
    with pymupdf.open("pdf", pdf_file) as doc:
        for page in doc:
            pix = page.get_pixmap(matrix=pymupdf.Matrix(300/72, 300/72))
            img_data = pix.tobytes("png")
            images.append(Image.open(io.BytesIO(img_data)))

    if len(images) > 1 and ds2o:
        images[0] = combine_images(images, True)

    return pil2jpeg(images[0])

def azure_ocr(img_content) -> str:
    try:
        with httpx.Client(http1=HTTPX_HTTP1, http2=HTTPX_HTTP2, timeout=HTTPX_TIMEOUT_API) as client:
            response = client.post(f"https://{OCR_SERVICE_NAME}.{OCR_SERVICE_DOMAIN}{OCR_SERVICE_API_VER}", params=ocr_params, headers=ocr_headers, content=img_content)

            response.raise_for_status()
            data = response.json()

            ocr_text = '\n'.join([line['text'] for blocks in data['readResult']['blocks'] if len(blocks) > 0 for line in blocks['lines']])
            return ocr_text

    except Exception as e:
        logging.error(f"azure_ocr: Exception occurred: {e}.")

def process_ocr(data, openai_system_msg) -> dict:
    file_format = data.content_type
    if not(file_format in ACCEPTABLE_IMAGE_FORMAT or file_format in ACCEPTABLE_DOCS_FORMAT):
        logging.warn(f"handle_image_upload: Invalid file format, {file_format}.")
        raise HTTPException(detail="Invalid File Format.", status_code=HTTP_406_NOT_ACCEPTABLE)

    try:
        file_content = data.file.read()
        file_name = data.filename

        if file_format in ACCEPTABLE_DOCS_FORMAT:
            if USE_PDF2TEXT:
                file_text = pdf2text(file_content)
            else:
                try:
                    file_content = pdf2image(file_content, USE_PDF2IMAGE_DS2O)
                except Exception as e:
                    logging.error(f"Failed to convert PDF to image: {e}", exc_info=True)

                file_text = azure_ocr(file_content)
        else:
            file_text = azure_ocr(file_content)

        llm_chat, form = llm_txt2json(file_text, openai_system_msg)

        save2db(file_name, file_format, file_content, file_text, llm_chat, form)
        return form

    except Exception as e:
        logging.error(f"process_ocr: Exception occurred: {e}", exc_info=True)
        raise HTTPException(detail="Internal Server Error.", status_code=HTTP_500_INTERNAL_SERVER_ERROR)
