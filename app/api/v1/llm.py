import os
import copy
import orjson
import picologging as logging
from openai import AzureOpenAI

from litestar.exceptions import HTTPException
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR

LLM_DRIVER_LIMIT = int(os.getenv('LLM_DRIVER_LIMIT', '2'))

OPENAI_API_MODEL = os.getenv('OPENAI_API_MODEL')
openai_client = AzureOpenAI()

def call_llm(sys_msg, usr_msg) -> dict:
    if not sys_msg[-1]['content']:
        sys_msg[-1]['content'] = usr_msg

    completion = openai_client.chat.completions.create(
                    model = OPENAI_API_MODEL,
                    messages = sys_msg,
                    temperature = 0.7,
                    max_tokens = 4096,
                    top_p = 0.95,
                    frequency_penalty = 0,
                    presence_penalty = 0,
                    stop = None
                 )

    return sys_msg, completion

def llm_driver(system_msg, text) -> dict:
    full_text = ''
    chat_limit = LLM_DRIVER_LIMIT
    try:
        while chat_limit > 0:
            message, completion = call_llm(system_msg, text)
            llm_reply = completion.choices[0].message.content.replace("\n", "").replace('```json{', '{').replace('}```', '}')
            if llm_reply.endswith('```'):
                llm_reply = llm_reply.replace('```', '')

            if llm_reply[-1] == '}':
                chat_limit = 0
            else:
                system_msg = message
                system_msg.append({"role":"assistant", "content":llm_reply})
                system_msg.append({"role":"user", "content":"Continue where you left off"})
                chat_limit -= 1

            full_text += llm_reply

        if full_text[-1] != '}':
            logging.warn("llm_driver: LLM Response Invalid.")
            raise HTTPException(detail="Internal Server Error.", status_code=HTTP_500_INTERNAL_SERVER_ERROR)

        system_msg.append({"role":"assistant", "content":full_text})
        return system_msg

    except Exception as e:
        logging.error(f"llm_driver: Exception occurred: {e}", exc_info=True)
        raise HTTPException(detail="Internal Server Error.", status_code=HTTP_500_INTERNAL_SERVER_ERROR)

def llm_txt2json(text, openai_system_msg) -> dict:
    system_msg_base = copy.deepcopy(openai_system_msg)
    message = llm_driver(system_msg_base, text)

    try:
        form = orjson.loads(message[-1]['content'])
        return message, form
    except Exception as e:
        logging.error(f"llm_txt2json: Exception occurred: {e}", exc_info=True)
        raise HTTPException(detail="Internal Server Error.", status_code=HTTP_500_INTERNAL_SERVER_ERROR)
