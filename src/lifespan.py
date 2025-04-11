from contextlib import asynccontextmanager
from typing import AsyncIterator
from fastapi import FastAPI
from observer import create_initial_admin, create_initial_permissions

@asynccontextmanager
async def get_lifespan(app: FastAPI) -> AsyncIterator[None]:    
        
    try:
        if create_initial_permissions():
            print("✅ Permisos creados exitosamente")
        else:
            print("ℹ️ Los permisos ya existían, no se creó ninguno nuevo")
    except Exception as e:
        print(f"❌ Error al crear permisos: {str(e)}")
    
    try:
        if create_initial_admin():
            print("✅ Usuario admin creado exitosamente")
        else:
            print("ℹ️ Usuario admin ya existe, no se creó uno nuevo")
    except Exception as e:
        print(f"Error al crear usuario admin: {str(e)}")
        
    yield