from sqlmodel import select, Session
from models import User, UserCredentials, Permissions
from database.db import engine
from schemas.security import UserRole
from provider.authorization import get_password_hash
import os
from dotenv import load_dotenv
import typer

load_dotenv()

def create_initial_admin():
    """Función para crear admin automáticamente"""
    creds = validate_admin_credentials()
    
    with Session(engine) as session:
        existing_user = session.exec(
            select(User).where(
                (User.username == creds['ADMIN_USERNAME']) | 
                (User.email == creds['ADMIN_EMAIL'])
            )
        ).first()
        
        admin_permission = session.exec(
            select(Permissions).where(Permissions.prefix == "ADM")
        ).first()
        
        if not admin_permission:
            raise ValueError("Permiso ADMIN no encontrado")
        
        if existing_user:
            if admin_permission not in existing_user.permissions:
                existing_user.permissions.append(admin_permission)
                session.add(existing_user)
                session.commit()
                return "updated" 
            return False
       
        new_admin = User(
            username=creds['ADMIN_USERNAME'],
            email=creds['ADMIN_EMAIL'],
            status=True,
            roles=[UserRole.ADMIN],
            credentials=UserCredentials(password=get_password_hash(creds['ADMIN_PASSWORD'])),
        )
        new_admin.permissions.append(admin_permission)
        
        session.add(new_admin)
        session.commit()
        return True

def validate_admin_credentials():
    """Valida las credenciales de admin"""
    required_vars = {
        'ADMIN_USERNAME': os.getenv('ADMIN_USERNAME'),
        'ADMIN_EMAIL': os.getenv('ADMIN_EMAIL'),
        'ADMIN_PASSWORD': os.getenv('ADMIN_PASSWORD')
    }
    
    missing = [k for k, v in required_vars.items() if not v]
    if missing:
        raise ValueError(f"Missing required env vars: {', '.join(missing)}")
    
    return required_vars

# CLI (para correr por comando xd)
user_observer = typer.Typer(help="Administración de usuarios CLI")

@user_observer.command()
def create_admin_cli(
    skip_existing: bool = typer.Option(True, "--skip-existing", help="Saltar si el usuario ya existe")
):
    """Versión CLI para crear admin"""
    try:
        if result := create_initial_admin():
            if result is True:
                typer.echo("✅ Usuario admin creado exitosamente")
            elif result == "updated":
                typer.echo("🔐 Usuario admin ya existía, permisos actualizados")
        else:
            typer.echo("⚠️  El usuario admin ya existía con los permisos necesarios")
    except Exception as e:
        typer.echo(f"❌ Error: {str(e)}")
        raise typer.Exit(code=1)