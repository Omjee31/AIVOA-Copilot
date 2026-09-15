from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.complaint import ComplaintResponse, RiskAssessmentResponse


class ChatLogRequest(BaseModel):
	message: str = Field(min_length=1, max_length=10_000)


class ChatLogResponse(BaseModel):
	complaint: ComplaintResponse
	risk_assessment: RiskAssessmentResponse


class ChatEditRequest(BaseModel):
	complaint_id: UUID
	message: str = Field(min_length=1, max_length=10_000)


class ChatEditResponse(ChatLogResponse):
	pass
