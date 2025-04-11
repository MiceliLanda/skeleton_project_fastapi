from sqlmodel import select, Session
from models import Permissions
from database.db import engine

list_permissions_default:list[Permissions] = [
    {
        "name": "Administrador",
        "module": "ADMIN",
        "prefix": "ADM",
        "status": True
    },
    {
        "name": "Asignar Permisos",
        "module": "PERMISOS",
        "prefix": "PE-A",
        "status": True
    },
]

def create_initial_permissions():
    """Crea los permisos si no existen en la base de datos."""
    with Session(engine) as session:
        created = False

        for perm in list_permissions_default:
            existing = session.exec(
                select(Permissions).where(
                    (Permissions.prefix == perm["prefix"]) |
                    (Permissions.module == perm["module"])
                )
            ).first()

            if not existing:
                new_perm = Permissions(**perm)
                session.add(new_perm)
                created = True

        if created:
            session.commit()

        return created
