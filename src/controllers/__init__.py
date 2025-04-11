from fastapi import APIRouter
# Configuración de router
router = APIRouter()
# Importación de todas las rutas por archivo
from .users import router as user_router

# Inicializar rutas al router
router.include_router(user_router, prefix="/users", tags=["UserController"])