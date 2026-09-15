from uuid import UUID

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import oauth2_scheme
from app.models.user import User
from app.schemas.complaint import ComplaintCreate, ComplaintResponse, ComplaintUpdate
from app.services.auth_service import get_current_user
from app.services.complaint_service import (
	create_complaint,
	delete_complaint,
	get_complaint,
	list_complaints,
	update_complaint,
)


router = APIRouter(prefix="/api/complaints", tags=["complaints"])


def current_user(
	token: str = Depends(oauth2_scheme),
	db: Session = Depends(get_db),
) -> User:
	return get_current_user(db, token)


@router.post("", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
def create(
	payload: ComplaintCreate,
	db: Session = Depends(get_db),
	user: User = Depends(current_user),
) -> ComplaintResponse:
	return create_complaint(db, user, payload)


@router.get("", response_model=list[ComplaintResponse])
def list_all(
	db: Session = Depends(get_db),
	user: User = Depends(current_user),
) -> list[ComplaintResponse]:
	return list_complaints(db, user)


@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_one(
	complaint_id: UUID,
	db: Session = Depends(get_db),
	user: User = Depends(current_user),
) -> ComplaintResponse:
	return get_complaint(db, user, complaint_id)


@router.put("/{complaint_id}", response_model=ComplaintResponse)
def update(
	complaint_id: UUID,
	payload: ComplaintUpdate,
	db: Session = Depends(get_db),
	user: User = Depends(current_user),
) -> ComplaintResponse:
	return update_complaint(db, user, complaint_id, payload)


@router.delete("/{complaint_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
	complaint_id: UUID,
	db: Session = Depends(get_db),
	user: User = Depends(current_user),
) -> Response:
	delete_complaint(db, user, complaint_id)
	return Response(status_code=status.HTTP_204_NO_CONTENT)
