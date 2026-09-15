from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import oauth2_scheme
from app.models.user import User
from app.schemas.chat import ChatEditRequest, ChatEditResponse, ChatLogRequest, ChatLogResponse
from app.services.auth_service import get_current_user
from app.services.complaint_service import create_ai_complaint, edit_complaint_with_ai
from app.services.llm_service import (
	ComplaintAIResponse,
	ModelUnavailableError,
	ProviderUnavailableError,
	RateLimitError,
	ResponseError,
	APITimeoutError,
	InvalidAPIKeyError,
	LLMServiceError,
	extract_and_assess_complaint,
)


router = APIRouter(prefix="/api/chat", tags=["chat"])


def current_user(
	token: str = Depends(oauth2_scheme),
	db: Session = Depends(get_db),
) -> User:
	return get_current_user(db, token)


def _ai_error_response(exc: LLMServiceError) -> HTTPException:
	if isinstance(exc, InvalidAPIKeyError):
		return HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc))
	if isinstance(exc, RateLimitError):
		return HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(exc))
	if isinstance(exc, APITimeoutError):
		return HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=str(exc))
	if isinstance(exc, ModelUnavailableError | ProviderUnavailableError):
		return HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc))
	if isinstance(exc, ResponseError):
		return HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc))
	return HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="AI service request failed")


@router.post("/log", response_model=ChatLogResponse, status_code=status.HTTP_201_CREATED)
def log_complaint(
	payload: ChatLogRequest,
	db: Session = Depends(get_db),
	user: User = Depends(current_user),
) -> ChatLogResponse:
	try:
		ai_response: ComplaintAIResponse = extract_and_assess_complaint(payload.message)
		complaint, risk_assessment = create_ai_complaint(db, user, ai_response)
		return ChatLogResponse(complaint=complaint, risk_assessment=risk_assessment)
	except ValueError as exc:
		raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
	except LLMServiceError as exc:
		raise _ai_error_response(exc) from exc


@router.post("/edit", response_model=ChatEditResponse)
def edit_logged_complaint(
	payload: ChatEditRequest,
	db: Session = Depends(get_db),
	user: User = Depends(current_user),
) -> ChatEditResponse:
	try:
		complaint, risk_assessment = edit_complaint_with_ai(
			db,
			user,
			payload.complaint_id,
			payload.message,
		)
		return ChatEditResponse(complaint=complaint, risk_assessment=risk_assessment)
	except ValueError as exc:
		raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
	except LLMServiceError as exc:
		raise _ai_error_response(exc) from exc
