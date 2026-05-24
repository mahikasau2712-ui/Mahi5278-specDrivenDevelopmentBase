from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ReportStatus = Literal["pending", "approved", "rejected", "archived"]


class ReportInternal(BaseModel):
    """Internal report structure including private fields."""

    model_config = ConfigDict(frozen=True)

    id: int
    secret_tag: str
    title: str
    status: ReportStatus
    owner: str
    owner_email: str
    amount: float
    created_at: datetime


class ReportResponse(BaseModel):
    """Public report payload without private fields."""

    id: int
    title: str
    status: ReportStatus
    owner: str
    amount: float
    created_at: datetime

    @classmethod
    def from_internal(cls, report: ReportInternal) -> "ReportResponse":
        return cls(
            id=report.id,
            title=report.title,
            status=report.status,
            owner=report.owner,
            amount=report.amount,
            created_at=report.created_at,
        )


class ReportPage(BaseModel):
    """Paginated response for report results."""

    items: list[ReportResponse]
    total: int = Field(description="Total number of reports matching the filters")
    offset: int
    limit: int
