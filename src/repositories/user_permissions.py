from sqlmodel import select
from typing import Dict, List
from fastapi import HTTPException,status
from sqlalchemy.orm import Session, joinedload
from models import User, Permissions

def add_permission_to_user(db: Session, user_id: int, permission_ids: List[int]):
    try:
        # Obtener el usuario
        user = db.query(User).get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        # Validar que los permission_ids sean una lista de enteros
        if not isinstance(permission_ids, list) or not all(isinstance(x, int) for x in permission_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="permission_ids debe ser una lista de enteros"
            )

        # Obtener los permisos existentes
        existing_permissions = db.query(Permissions).filter(
            Permissions.id.in_(permission_ids)
        ).all()

        # Verificar si todos los permisos solicitados existen
        existing_ids = {p.id for p in existing_permissions}
        missing_ids = set(permission_ids) - existing_ids
        
        if missing_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Los siguientes IDs de permisos no existen: {missing_ids}"
            )
            
        # Obtener permisos nuevos
        user_permission_ids = {p.id for p in user.permissions}
        new_permissions = [p for p in existing_permissions if p.id not in user_permission_ids]
        # Se agregan los permisos nuevos a los existentes
        user.permissions.extend(new_permissions)
        db.commit()
        db.refresh(user)

        return "Se agregó correctamente"

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al agregar permisos: {str(e)}"
        )

def get_user_permissions_list(db: Session, user_id: int):
    try:
        # Obtener usuario con sus permisos (carga eager)
        user = db.exec(
            select(User)
            .where(User.id == user_id)
            .options(joinedload(User.permissions))
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )

        # Convertir permisos a formato diccionario
        return [p.model_dump() for p in user.permissions]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al recuperar permisos: {str(e)}"
        )