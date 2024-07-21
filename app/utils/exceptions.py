from litestar import Request, Response
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR

def exception_handler(_: Request, exc: Exception) -> Response:
    status_code = getattr(exc, "status_code", HTTP_500_INTERNAL_SERVER_ERROR)
    detail = getattr(exc, "detail", None)

    return Response(
        content={
            "status_code": exc.status_code,
            "detail": detail
        },
        status_code=status_code,
    )
