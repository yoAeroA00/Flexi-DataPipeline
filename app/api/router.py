from litestar import Router, get

from v1.endpoints.process import handle_process, handle_process_demo

@get()
async def index() -> str:
    return "Server is Running."

v1_router = Router(path="/v1", route_handlers=[handle_process, handle_process_demo])

api_router = Router(path="/api", route_handlers=[index, v1_router])
