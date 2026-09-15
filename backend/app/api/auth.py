from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import oauth2_scheme
from app.schemas.auth import TokenResponse, UserRegister, UserResponse
from app.services.auth_service import (
	authenticate_user,
	create_access_token,
	get_current_user,
	register_user,
)


router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)) -> UserResponse:
	return register_user(db, payload)


@router.post("/login", response_model=TokenResponse)
def login(
	form_data: OAuth2PasswordRequestForm = Depends(),
	db: Session = Depends(get_db),
) -> TokenResponse:
	user = authenticate_user(db, form_data.username, form_data.password)
	return TokenResponse(access_token=create_access_token(user.id), token_type="bearer")


@router.get("/me", response_model=UserResponse)
def me(
	token: str = Depends(oauth2_scheme),
	db: Session = Depends(get_db),
) -> UserResponse:
	return get_current_user(db, token)
