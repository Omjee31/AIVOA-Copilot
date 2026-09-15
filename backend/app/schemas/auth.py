from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRegister(BaseModel):
	email: EmailStr
	full_name: str = Field(min_length=1, max_length=255)
	password: str = Field(min_length=8, max_length=128)

	@field_validator("full_name")
	@classmethod
	def validate_full_name(cls, value: str) -> str:
		value = value.strip()
		if not value:
			raise ValueError("must not be blank")
		return value


class UserResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: UUID
	email: EmailStr
	full_name: str
	is_active: bool


class TokenResponse(BaseModel):
	access_token: str
	token_type: str
