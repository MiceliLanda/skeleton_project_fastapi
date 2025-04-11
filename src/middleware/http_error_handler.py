from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import status
import traceback
import logging
import traceback

logger = logging.getLogger(__name__)

class HttpErrorHandler(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        logger.info(f"Entrando al middleware de manejo de errores: {request.url.path}")
        print(f"Entrando al middleware de manejo de errores: {request.url.path}")
        try:
            return await call_next(request)
        
        except StarletteHTTPException as http_exc:
            logger.error(f"HTTPException: {http_exc.detail}")
            return JSONResponse(
                content={
                    "error": http_exc.detail,
                    "type": "http_error",
                    "status_code": http_exc.status_code
                },
                status_code=http_exc.status_code,
            )
        except Exception as exc:
            logger.error(f"Unhandled exception: {str(exc)}\n{traceback.format_exc()}")
            return JSONResponse(
                content={
                    "error": "Internal server error",
                    "type": "server_error",
                    "detail": str(exc),
                    "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
                },
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
