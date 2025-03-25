from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import get_current_user
from app.models.user import User
from app.repositories.auth_respository import AuthRepository, get_auth_repository
from app.schemas.auth import LoginRequest
from app.schemas.user import Token

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_repo: AuthRepository = Depends(get_auth_repository),
):
    creds = LoginRequest(
        username_or_email=form_data.username, password=form_data.password
    )
    result = auth_repo.user_login(creds)
    return {"access_token": result["access_token"], "token_type": "bearer"}


@router.get("/protected")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Welcome, {current_user.username}!"}


@router.post("/logout")
def logout(
    current_user: User = Depends(get_current_user),
    auth_repo: AuthRepository = Depends(get_auth_repository),
):
    return auth_repo.user_logout(current_user)
