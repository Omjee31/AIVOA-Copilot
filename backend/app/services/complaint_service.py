from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.complaint import Complaint
from app.models.risk_assessment import RiskAssessment
from app.models.user import User
from app.schemas.complaint import ComplaintCreate, ComplaintUpdate
from app.services.audit_service import (
	complaint_state,
	create_audit_log,
	risk_assessment_state,
)
from app.services.llm_service import ComplaintAIResponse, ComplaintData, edit_complaint as edit_with_ai


def _get_user_complaint(db: Session, complaint_id: UUID, user_id: UUID) -> Complaint:
	complaint = db.scalar(
		select(Complaint).where(
			Complaint.id == complaint_id,
			Complaint.user_id == user_id,
		)
	)
	if complaint is None:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")
	return complaint


def create_complaint(db: Session, user: User, payload: ComplaintCreate) -> Complaint:
	complaint = Complaint(user_id=user.id, **payload.model_dump())
	db.add(complaint)
	db.flush()
	create_audit_log(
		db,
		complaint_id=complaint.id,
		user_id=user.id,
		action="complaint_created",
		new_data=complaint_state(complaint),
	)
	db.commit()
	db.refresh(complaint)
	return complaint


def upsert_risk_assessment(
	db: Session,
	complaint: Complaint,
	risk_data: dict[str, str],
	user_id: UUID,
) -> RiskAssessment:
	risk_assessment = db.scalar(
		select(RiskAssessment).where(RiskAssessment.complaint_id == complaint.id)
	)
	if risk_assessment is None:
		risk_assessment = RiskAssessment(complaint_id=complaint.id, **risk_data)
		db.add(risk_assessment)
		action = "risk_assessment_created"
	else:
		action = "risk_assessment_updated"
		for field, value in risk_data.items():
			setattr(risk_assessment, field, value)
	complaint.risk_assessment = risk_assessment
	create_audit_log(
		db,
		complaint_id=complaint.id,
		user_id=user_id,
		action=action,
		new_data=risk_assessment_state(risk_assessment),
	)
	return risk_assessment


def create_ai_complaint(
	db: Session,
	user: User,
	ai_response: ComplaintAIResponse,
) -> tuple[Complaint, RiskAssessment]:
	complaint_data = ai_response.complaint.model_dump()
	if complaint_data["product_name"] is None or complaint_data["problem_description"] is None:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail="AI could not extract the required product name and problem description",
		)

	complaint_payload = ComplaintCreate.model_validate({**complaint_data, "status": "draft"})
	complaint = Complaint(user_id=user.id, **complaint_payload.model_dump())
	db.add(complaint)
	db.flush()

	risk_assessment = upsert_risk_assessment(
		db,
		complaint,
		ai_response.risk_assessment.model_dump(),
		user.id,
	)

	create_audit_log(
		db,
		complaint_id=complaint.id,
		user_id=user.id,
		action="ai_extraction",
		new_data=ai_response.model_dump(mode="json"),
	)
	create_audit_log(
		db,
		complaint_id=complaint.id,
		user_id=user.id,
		action="complaint_created",
		new_data=complaint_state(complaint),
	)
	db.commit()
	db.refresh(complaint)
	db.refresh(risk_assessment)
	return complaint, risk_assessment


def populate_complaint_from_ai(
	db: Session,
	user: User,
	complaint_id: UUID,
	ai_response: ComplaintAIResponse,
	document_id: UUID | None = None,
) -> tuple[Complaint, RiskAssessment]:
	complaint = _get_user_complaint(db, complaint_id, user.id)
	current_values = {
		field: getattr(complaint, field)
		for field in ComplaintData.model_fields
	}
	updated_values = ai_response.complaint.model_dump()
	merged_values = {
		field: value if value is not None or current_values[field] is None else current_values[field]
		for field, value in updated_values.items()
	}
	updated_payload = ComplaintCreate.model_validate({**merged_values, "status": complaint.status})
	old_state = {
		"complaint": complaint_state(complaint),
		"risk_assessment": risk_assessment_state(complaint.risk_assessment),
	}

	for field, value in updated_payload.model_dump(exclude={"status"}).items():
		if getattr(complaint, field) != value:
			setattr(complaint, field, value)
	risk_assessment = upsert_risk_assessment(
		db,
		complaint,
		ai_response.risk_assessment.model_dump(),
		user.id,
	)
	create_audit_log(
		db,
		complaint_id=complaint.id,
		user_id=user.id,
		action="ai_extraction",
		new_data={
			"document_id": str(document_id) if document_id is not None else None,
			"complaint": updated_payload.model_dump(mode="json", exclude={"status"}),
			"status": complaint.status,
			"risk_assessment": ai_response.risk_assessment.model_dump(mode="json"),
		},
		old_data=old_state,
	)
	db.commit()
	db.refresh(complaint)
	db.refresh(risk_assessment)
	return complaint, risk_assessment


def edit_complaint_with_ai(
	db: Session,
	user: User,
	complaint_id: UUID,
	instruction: str,
) -> tuple[Complaint, RiskAssessment]:
	complaint = _get_user_complaint(db, complaint_id, user.id)
	current_data = ComplaintData.model_validate(
		{
			field: getattr(complaint, field)
			for field in ComplaintData.model_fields
		}
	)
	current_risk = complaint.risk_assessment
	current_risk_data = (
		{
			"severity_level": current_risk.severity_level,
			"suggested_action": current_risk.suggested_action,
			"reasoning": current_risk.reasoning,
		}
		if current_risk is not None
		else None
	)
	old_state = {"complaint": complaint_state(complaint), "risk_assessment": current_risk_data}

	ai_response = edit_with_ai(current_data, instruction, current_risk_data)
	updated_data = ai_response.complaint.model_dump()
	current_values = current_data.model_dump()
	merged_data = {
		field: value if value is not None or current_values[field] is None else current_values[field]
		for field, value in updated_data.items()
	}
	updated_payload = ComplaintCreate.model_validate({**merged_data, "status": complaint.status})

	for field, value in updated_payload.model_dump(exclude={"status"}).items():
		if getattr(complaint, field) != value:
			setattr(complaint, field, value)

	risk_assessment = upsert_risk_assessment(
		db,
		complaint,
		ai_response.risk_assessment.model_dump(),
		user.id,
	)
	new_state = {
		"complaint": updated_payload.model_dump(mode="json", exclude={"status"}),
		"status": complaint.status,
		"risk_assessment": ai_response.risk_assessment.model_dump(mode="json"),
	}
	create_audit_log(
		db,
		complaint_id=complaint.id,
		user_id=user.id,
		action="ai_edit",
		old_data=old_state,
		new_data=new_state,
	)
	db.commit()
	db.refresh(complaint)
	db.refresh(risk_assessment)
	return complaint, risk_assessment


def list_complaints(db: Session, user: User) -> list[Complaint]:
	return list(
		db.scalars(
			select(Complaint)
			.where(Complaint.user_id == user.id)
			.order_by(Complaint.created_at.desc())
		).all()
	)


def get_complaint(db: Session, user: User, complaint_id: UUID) -> Complaint:
	return _get_user_complaint(db, complaint_id, user.id)


def update_complaint(
	db: Session,
	user: User,
	complaint_id: UUID,
	payload: ComplaintUpdate,
) -> Complaint:
	complaint = _get_user_complaint(db, complaint_id, user.id)
	old_state = complaint_state(complaint)
	old_status = complaint.status
	changes = payload.model_dump(exclude_unset=True)
	manufacturing_date = changes.get("manufacturing_date", complaint.manufacturing_date)
	expiry_date = changes.get("expiry_date", complaint.expiry_date)
	if manufacturing_date and expiry_date and manufacturing_date > expiry_date:
		raise HTTPException(
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
			detail="manufacturing_date must be before or equal to expiry_date",
		)
	for field, value in changes.items():
		setattr(complaint, field, value)
	create_audit_log(
		db,
		complaint_id=complaint.id,
		user_id=user.id,
		action="complaint_updated",
		old_data=old_state,
		new_data=complaint_state(complaint),
	)
	if old_status != complaint.status:
		create_audit_log(
			db,
			complaint_id=complaint.id,
			user_id=user.id,
			action="complaint_status_changed",
			old_data={"status": old_status},
			new_data={"status": complaint.status},
		)
	db.commit()
	db.refresh(complaint)
	return complaint


def delete_complaint(db: Session, user: User, complaint_id: UUID) -> None:
	complaint = _get_user_complaint(db, complaint_id, user.id)
	create_audit_log(
		db,
		complaint_id=complaint.id,
		user_id=user.id,
		action="complaint_deleted",
		old_data=complaint_state(complaint),
	)
	db.delete(complaint)
	db.commit()
