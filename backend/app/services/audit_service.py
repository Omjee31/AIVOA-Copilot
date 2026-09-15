from typing import Any
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.audit import AuditLog
from app.models.complaint import Complaint
from app.models.risk_assessment import RiskAssessment


def complaint_state(complaint: Complaint) -> dict[str, Any]:
	state = {
		field: getattr(complaint, field)
		for field in (
			"product_name",
			"product_strength_or_grade",
			"batch_number",
			"manufacturing_date",
			"expiry_date",
			"affected_quantity",
			"problem_description",
			"reporter_information",
			"status",
		)
	}
	for field in ("manufacturing_date", "expiry_date"):
		if state[field] is not None:
			state[field] = state[field].isoformat()
	return state


def risk_assessment_state(risk_assessment: RiskAssessment | None) -> dict[str, Any] | None:
	if risk_assessment is None:
		return None
	return {
		"severity_level": risk_assessment.severity_level,
		"suggested_action": risk_assessment.suggested_action,
		"reasoning": risk_assessment.reasoning,
	}


def create_audit_log(
	db: Session,
	*,
	complaint_id: UUID,
	user_id: UUID | None,
	action: str,
	new_data: dict[str, Any] | None = None,
	old_data: dict[str, Any] | None = None,
) -> AuditLog:
	audit_log = AuditLog(
		complaint_id=complaint_id,
		user_id=user_id,
		action=action,
		old_data=old_data,
		new_data=new_data,
	)
	db.add(audit_log)
	return audit_log


def list_complaint_audit_history(
	db: Session,
	user_id: UUID,
	complaint_id: UUID,
) -> list[AuditLog]:
	complaint_exists = db.scalar(
		select(Complaint.id).where(
			Complaint.id == complaint_id,
			Complaint.user_id == user_id,
		)
	)
	if complaint_exists is None:
		deleted_complaint_owner = db.scalar(
			select(AuditLog.id).where(
				AuditLog.complaint_id == complaint_id,
				AuditLog.user_id == user_id,
			)
		)
		if deleted_complaint_owner is None:
			raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Complaint not found")

	return list(
		db.scalars(
			select(AuditLog)
			.where(AuditLog.complaint_id == complaint_id)
			.order_by(desc(AuditLog.created_at), desc(AuditLog.id))
		).all()
	)
