from typing import List
from fastapi import Depends,APIRouter, HTTPException,status
from schemas import LoginRequest, Token, UserCreate,UserAddPermissions, UserLoginResponse, User, PermissionsResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from database.db import get_db
from repositories import create_user, get_users,login_user, add_permission_to_user, get_user_permissions_list

router = APIRouter()

@router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)) -> UserLoginResponse:
    try: 
        user_token = login_user(db, login_data)
        if not user_token:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrecta"
            )
        return user_token
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error con la base de datos"
        )
    except Exception as e:
        raise HTTPException (
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
        
    
@router.post('/create')
def new_user(user_data: UserCreate, db : Session = Depends(get_db)) -> User:
    try:
        return create_user(db, user_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating user: {str(e)}"
        )

@router.get("/")
def users(db:Session=Depends(get_db)) -> List[UserLoginResponse]:
    try:
        return get_users(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving users: {str(e)}"
        )
        
@router.post("/{user_id}/permissions")
def add_permission_user(user_id: int, request:UserAddPermissions, db: Session = Depends(get_db)) -> PermissionsResponse:
    try:
        permissions = add_permission_to_user(db,user_id, request.permissions_ids)
        return permissions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error setting permissions: {str(e)}"
        )
        
@router.get("/{user_id}/get_permissions")
def get_user_permissions(user_id:int, db: Session = Depends(get_db)) -> List[PermissionsResponse]:
    try:
        return get_user_permissions_list(db, user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving permissions user: {str(e)}"
        )
        