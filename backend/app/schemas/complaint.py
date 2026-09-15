from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


ComplaintStatus = Literal["draft", "submitted", "under_review", "resolved", "closed"]


class ComplaintFields(BaseModel):
	product_name: str = Field(min_length=1, max_length=255)
	product_strength_or_grade: str | None = Field(default=None, max_length=100)
	batch_number: str | None = Field(default=None, max_length=100)
	manufacturing_date: date | None = None
	expiry_date: date | None = None
	affected_quantity: int | None = Field(default=None, ge=0)
	problem_description: str = Field(min_length=1, max_length=10_000)
	reporter_information: str | None = Field(default=None, max_length=10_000)

	@field_validator("product_name", "problem_description", mode="before")
	@classmethod
	def validate_required_text(cls, value: str) -> str:
		if not isinstance(value, str) or not value.strip():
			raise ValueError("must not be blank")
		return value.strip()

	@field_validator("product_strength_or_grade", "batch_number", "reporter_information", mode="before")
	@classmethod
	def normalize_optional_text(cls, value: str | None) -> str | None:
		if value is None:
			return None
		if not isinstance(value, str):
			raise ValueError("must be a string")
		value = value.strip()
		return value or None

	@model_validator(mode="after")
	def validate_dates(self) -> "ComplaintFields":
		if self.manufacturing_date and self.expiry_date and self.manufacturing_date > self.expiry_date:
			raise ValueError("manufacturing_date must be before or equal to expiry_date")
		return self


class ComplaintCreate(ComplaintFields):
	status: ComplaintStatus = "draft"


class ComplaintUpdate(BaseModel):
	status: ComplaintStatus | None = None
	product_name: str | None = Field(default=None, min_length=1, max_length=255)
	product_strength_or_grade: str | None = Field(default=None, max_length=100)
	batch_number: str | None = Field(default=None, max_length=100)
	manufacturing_date: date | None = None
	expiry_date: date | None = None
	affected_quantity: int | None = Field(default=None, ge=0)
	problem_description: str | None = Field(default=None, min_length=1, max_length=10_000)
	reporter_information: str | None = Field(default=None, max_length=10_000)

	@field_validator("product_name", "problem_description", mode="before")
	@classmethod
	def validate_optional_required_text(cls, value: str | None) -> str | None:
		if value is None:
			raise ValueError("must not be null")
		if not isinstance(value, str) or not value.strip():
			raise ValueError("must not be blank")
		return value.strip()

	@field_validator("product_strength_or_grade", "batch_number", "reporter_information", mode="before")
	@classmethod
	def normalize_optional_update_text(cls, value: str | None) -> str | None:
		if value is None:
			return None
		if not isinstance(value, str):
			raise ValueError("must be a string")
		value = value.strip()
		return value or None

	@model_validator(mode="after")
	def validate_dates(self) -> "ComplaintUpdate":
		if self.manufacturing_date and self.expiry_date and self.manufacturing_date > self.expiry_date:
			raise ValueError("manufacturing_date must be before or equal to expiry_date")
		if not self.model_fields_set:
			raise ValueError("at least one field is required")
		return self


class RiskAssessmentResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: UUID
	severity_level: str
	suggested_action: str
	reasoning: str
	created_at: datetime
	updated_at: datetime


class ComplaintResponse(ComplaintFields):
	model_config = ConfigDict(from_attributes=True)

	id: UUID
	user_id: UUID
	status: ComplaintStatus
	created_at: datetime
	updated_at: datetime
	risk_assessment: RiskAssessmentResponse | None = None
