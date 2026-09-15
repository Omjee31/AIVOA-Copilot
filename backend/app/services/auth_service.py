from datetime import datetime, timedelta, timezone
from hashlib import sha256
from uuid import UUID

import bcrypt
from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User
from app.schemas.auth import UserRegister


def hash_password(password: str) -> str:
	password_digest = sha256(password.encode("utf-8")).digest()
	return bcrypt.hashpw(password_digest, bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
	password_digest = sha256(password.encode("utf-8")).digest()
	return bcrypt.checkpw(password_digest, hashed_password.encode("utf-8"))


def create_access_token(user_id: UUID) -> str:
	expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
	payload = {"sub": str(user_id), "exp": expires_at}
	return jwt.encode(payload, settings.secret_key.get_secret_value(), algorithm=settings.algorithm)


def register_user(db: Session, user_data: UserRegister) -> User:
	email = str(user_data.email).lower()
	existing_user = db.scalar(select(User).where(User.email == email))
	if existing_user is not None:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")

	user = User(
		email=email,
		full_name=user_data.full_name.strip(),
		hashed_password=hash_password(user_data.password),
	)
	db.add(user)
	try:
		db.commit()
	except IntegrityError:
		db.rollback()
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered") from None

	db.refresh(user)
	return user


def authenticate_user(db: Session, email: str, password: str) -> User:
	user = db.scalar(select(User).where(User.email == email.lower()))
	if user is None or not verify_password(password, user.hashed_password):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
	if not user.is_active:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
	return user


def get_current_user(db: Session, token: str) -> User:
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
		headers={"WWW-Authenticate": "Bearer"},
	)
	try:
		payload = jwt.decode(
			token,
			settings.secret_key.get_secret_value(),
			algorithms=[settings.algorithm],
		)
		subject = payload.get("sub")
		if not isinstance(subject, str):
			raise credentials_exception
		user_id = UUID(subject)
	except (JWTError, ValueError):
		raise credentials_exception from None

	user = db.get(User, user_id)
	if user is None or not user.is_active:
		raise credentials_exception
	return user
