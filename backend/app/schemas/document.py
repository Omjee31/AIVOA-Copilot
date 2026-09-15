from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.complaint import ComplaintResponse, RiskAssessmentResponse


class DocumentResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: UUID
	complaint_id: UUID
	filename: str
	file_type: str
	file_size: int
	extracted_text: str
	uploaded_at: datetime


class DocumentExtractionResponse(BaseModel):
	complaint: "ComplaintResponse"
	risk_assessment: "RiskAssessmentResponse"
	document: DocumentResponse
