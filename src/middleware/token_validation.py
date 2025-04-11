import os
import re
from fastapi import Request
from fastapi.responses import JSONResponse
import jwt
from starlette.middleware.base import BaseHTTPMiddleware
from database.db import get_db
from utilities.helper import authorized_routes
from repositories import get_user
from sqlalchemy.orm import Session
import logging
logger = logging.getLogger(__name__)

class TokenValidationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Verificando token para: {request.url.path}")
        # Verifica si la ruta está en las rutas públicas
        for route in authorized_routes:
            if route == request.url.path:
                return await call_next(request)
        
        # Extraer el token del header Authorization
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                content={"detail": "No se proporcionó el token de autenticación"},
                status_code=401
            )
        
        token = auth_header.split(" ")[1]

        try:
            # Decodificar el token para validar su contenido
            payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
            username = payload.get("sub")
            if username is None:
                return JSONResponse(
                    content={"detail": "Token inválido: no se encontró el usuario"},
                    status_code=401
                )
            
            # Validar el usuario
            db: Session = next(get_db())
            user = get_user(db,username)
            
            if user is None:
                return JSONResponse(
                    content={"detail": "Usuario no encontrado en la base de datos"},
                    status_code=401
                )
            request.state.user = user
        
        except jwt.ExpiredSignatureError:
            return JSONResponse(
                content={"detail": "El token ha expirado"},
                status_code=401
            )
        
        except jwt.InvalidTokenError:
            return JSONResponse(
                content={"detail": "Token inválido"},
                status_code=401
            )
        
        except Exception as e:
            # Manejo de excepciones genéricas
            return JSONResponse(
                content={"detail": f"Error al validar el token: {str(e)}"},
                status_code=500
            )
            
        # Si el token es válido, se llama al siguiente middleware
        response = await call_next(request)
        return response
