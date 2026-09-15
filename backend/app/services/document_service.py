from pathlib import Path
from uuid import UUID, uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.document import Document
from app.models.user import User
from app.services.audit_service import create_audit_log
from app.services.complaint_service import create_ai_complaint, get_complaint, populate_complaint_from_ai
from app.services.llm_service import LLMServiceError, extract_and_assess_complaint
from app.utils.text_extractor import extract_text_from_pdf


class DocumentUploadError(ValueError):
	pass


def _validate_upload(upload: UploadFile, file_content: bytes) -> None:
	filename = upload.filename or ""
	if Path(filename).suffix.lower() != ".pdf":
		raise DocumentUploadError("Only PDF files are accepted")
	if upload.content_type != "application/pdf":
		raise DocumentUploadError("The uploaded file must have MIME type application/pdf")
	max_size = settings.max_file_size_mb * 1024 * 1024
	if len(file_content) > max_size:
		raise DocumentUploadError(f"The uploaded file exceeds the {settings.max_file_size_mb} MB limit")


async def create_document_from_upload(
	db: Session,
	user: User,
	complaint_id: UUID,
	upload: UploadFile,
) -> Document:
	complaint = get_complaint(db, user, complaint_id)
	file_content, extracted_text = await _read_and_extract_upload(upload)
	return _persist_document(db, user, complaint, upload, file_content, extracted_text)


async def _read_and_extract_upload(upload: UploadFile) -> tuple[bytes, str]:
	file_content = await upload.read(settings.max_file_size_mb * 1024 * 1024 + 1)
	_validate_upload(upload, file_content)
	extracted_text = extract_text_from_pdf(file_content)
	return file_content, extracted_text


def _persist_document(
	db: Session,
	user: User,
	complaint,
	upload: UploadFile,
	file_content: bytes,
	extracted_text: str,
) -> Document:

	upload_dir = Path(settings.upload_dir).resolve()
	upload_dir.mkdir(parents=True, exist_ok=True)
	safe_filename = f"{uuid4().hex}.pdf"
	file_path = upload_dir / safe_filename
	file_path.write_bytes(file_content)

	document = Document(
		complaint_id=complaint.id,
		filename=safe_filename,
		file_path=str(file_path),
		file_type="application/pdf",
		file_size=len(file_content),
		extracted_text=extracted_text,
	)
	db.add(document)
	create_audit_log(
		db,
		complaint_id=complaint.id,
		user_id=user.id,
		action="document_uploaded",
		new_data={
			"filename": safe_filename,
			"file_type": "application/pdf",
			"file_size": len(file_content),
		},
	)
	try:
		db.commit()
	except Exception:
		db.rollback()
		file_path.unlink(missing_ok=True)
		raise
	db.refresh(document)
	return document


async def extract_document_for_new_complaint(
	db: Session,
	user: User,
	upload: UploadFile,
):
	file_content, extracted_text = await _read_and_extract_upload(upload)
	ai_response = extract_and_assess_complaint(extracted_text)
	complaint, risk_assessment = create_ai_complaint(db, user, ai_response)
	document = _persist_document(db, user, complaint, upload, file_content, extracted_text)
	return document, complaint, risk_assessment


async def extract_document_for_complaint(
	db: Session,
	user: User,
	complaint_id: UUID,
	upload: UploadFile,
):
	document = await create_document_from_upload(db, user, complaint_id, upload)
	try:
		ai_response = extract_and_assess_complaint(document.extracted_text or "")
		complaint, risk_assessment = populate_complaint_from_ai(
			db,
			user,
			complaint_id,
			ai_response,
			document_id=document.id,
		)
	except LLMServiceError:
		db.rollback()
		raise
	return document, complaint, risk_assessment
