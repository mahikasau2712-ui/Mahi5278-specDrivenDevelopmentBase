from datetime import datetime
from pydantic import BaseModel
from enum import Enum
from typing import List


class Status(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    archived = "archived"


class ReportPublic(BaseModel):
    id: int
    title: str
    status: Status
    owner: str
    amount: float
    created_at: datetime


class ReportListResponse(BaseModel):
    total: int
    offset: int
    limit: int
    items: List[ReportPublic]


class ReportCreate(BaseModel):
    title: str
    status: Status = Status.pending
    owner: str
    amount: float

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Quarterly revenue",
                "status": "pending",
                "owner": "alice",
                "amount": 1234.56,
            }
        }
