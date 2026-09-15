from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import oauth2_scheme
from app.models.user import User
from app.schemas.audit import AuditResponse
from app.services.audit_service import list_complaint_audit_history
from app.services.auth_service import get_current_user


router = APIRouter(prefix="/api/audit", tags=["audit"])


def current_user(
	token: str = Depends(oauth2_scheme),
	db: Session = Depends(get_db),
) -> User:
	return get_current_user(db, token)


@router.get("/{complaint_id}", response_model=list[AuditResponse])
def get_complaint_audit_history(
	complaint_id: UUID,
	db: Session = Depends(get_db),
	user: User = Depends(current_user),
) -> list[AuditResponse]:
	return list_complaint_audit_history(db, user.id, complaint_id)
