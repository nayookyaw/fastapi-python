from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

# validation exception handler: wrapper matches the general ExceptionHandler signature
async def validation_exception_handler(request: Request, exc: Exception):
	if isinstance(exc, RequestValidationError):
		return await __validation_exception(request, exc)
	raise exc

async def __validation_exception(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": exc.body,
            "message": "Validation error occurred",
        },
    )