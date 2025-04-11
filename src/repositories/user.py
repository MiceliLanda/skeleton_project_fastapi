from fastapi import HTTPException,status
from pymysql import IntegrityError
from sqlalchemy.orm import Session
from models import User, UserCredentials
from schemas import UserCreate
from schemas import LoginRequest, Token
from provider import authorization

def create_user(db: Session, user_data : UserCreate):
    try:        
        user = User(
            username=user_data.username,
            email=user_data.email,
            credentials= UserCredentials(
                password=authorization.get_password_hash(user_data.password)
            )
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario o email ya existe"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear el usuario: {str(e)}"
        )

    
def get_users(db: Session):
    try:
        return db.query(User).all()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo usuarios: {str(e)}"
        )

def get_user(db: Session, username: str):
    try:
        return db.query(User).filter(User.username == username).first()
    except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obterner el usuario: {str(e)}"
            )
            
def get_user_by_id(db: Session, user_id: int):
    try:
        return db.query(User).filter(User.id == user_id).first()
    except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obterner el usuario: {str(e)}"
            )

def login_user(db: Session, form: LoginRequest) -> Token:
    try:
        user = db.query(User).filter(User.username == form.username).first()    
        if not user:
            return None
        
        if not authorization.verify_password(form.password, user.credentials.password):
            return None
        
        access_token = authorization.create_access_token(data={
            "sub": user.username
        })
        
        return Token(token=access_token, user=user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante el login de usuario: {str(e)}"
        )

