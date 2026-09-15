from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AuditResponse(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: UUID
	complaint_id: UUID
	user_id: UUID | None
	action: str
	old_data: dict[str, Any] | None
	new_data: dict[str, Any] | None
	created_at: datetime
