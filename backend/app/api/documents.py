from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import oauth2_scheme
from app.models.user import User
from app.schemas.document import DocumentExtractionResponse
from app.services.auth_service import get_current_user
from app.services.document_service import (
	DocumentUploadError,
	extract_document_for_complaint,
	extract_document_for_new_complaint,
)
from app.services.llm_service import (
	ModelUnavailableError,
	ProviderUnavailableError,
	RateLimitError,
	ResponseError,
	APITimeoutError,
	InvalidAPIKeyError,
	LLMServiceError,
)
from app.utils.text_extractor import EmptyPDFError, PDFExtractionError


router = APIRouter(prefix="/api/document", tags=["documents"])


def current_user(
	token: str = Depends(oauth2_scheme),
	db: Session = Depends(get_db),
) -> User:
	return get_current_user(db, token)


@router.post("/extract", response_model=DocumentExtractionResponse, status_code=status.HTTP_201_CREATED)
async def extract_document(
	complaint_id: UUID | None = Form(default=None),
	file: UploadFile = File(...),
	db: Session = Depends(get_db),
	user: User = Depends(current_user),
) -> DocumentExtractionResponse:
	try:
		if complaint_id is None:
			document, complaint, risk_assessment = await extract_document_for_new_complaint(db, user, file)
		else:
			document, complaint, risk_assessment = await extract_document_for_complaint(
				db,
				user,
				complaint_id,
				file,
			)
		return DocumentExtractionResponse(
			complaint=complaint,
			risk_assessment=risk_assessment,
			document=document,
		)
	except (DocumentUploadError, EmptyPDFError) as exc:
		raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
	except PDFExtractionError as exc:
		raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
	except ValueError as exc:
		raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
	except InvalidAPIKeyError as exc:
		raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
	except RateLimitError as exc:
		raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=str(exc)) from exc
	except APITimeoutError as exc:
		raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=str(exc)) from exc
	except (ModelUnavailableError, ProviderUnavailableError) as exc:
		raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
	except ResponseError as exc:
		raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(exc)) from exc
	except LLMServiceError as exc:
		raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="AI service request failed") from exc
