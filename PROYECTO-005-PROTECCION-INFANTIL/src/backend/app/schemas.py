from pydantic import BaseModel, Field, field_validator
from typing import Literal


class Evidence(BaseModel):
    type: Literal["text", "image"]
    content: str = Field(..., min_length=1, max_length=50000)


class ReportCreate(BaseModel):
    reported_identifier: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1, max_length=5000)
    evidence: Evidence | None = None

    @field_validator("reported_identifier")
    @classmethod
    def strip_identifier(cls, v: str) -> str:
        return v.strip()


class ReportResponse(BaseModel):
    report_hash: str
    reported_at: str
