from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ReportStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    archived = "archived"


class ReportBase(BaseModel):
    id: int
    title: str = Field(..., min_length=5)
    description: str = Field(..., min_length=10)
    owner: str
    status: ReportStatus
    amount: float = Field(..., ge=0.0)
    created_at: datetime


class ReportDetail(ReportBase):
    pass


class PageInfo(BaseModel):
    offset: int
    limit: int
    total: int
    returned: int


class ReportListResponse(BaseModel):
    data: List[ReportDetail]
    page: PageInfo


class StatusAggregate(BaseModel):
    status: ReportStatus
    count: int
    total_amount: float


class ReportStats(BaseModel):
    total_reports: int
    total_amount: float
    breakdown: List[StatusAggregate]
