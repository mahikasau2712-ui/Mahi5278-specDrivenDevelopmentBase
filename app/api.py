from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

from app.models import (
    PageInfo,
    ReportDetail,
    ReportListResponse,
    ReportStats,
    ReportStatus,
)
from app.repository import get_report_by_id, list_reports, stats_for_reports

app = FastAPI(
    title="Vibe Reports API",
    description="A high-quality reports service with rich filtering, sorting, and analytics.",
    version="0.1.0",
)


class SortField(str, Enum):
    id = "id"
    title = "title"
    status = "status"
    owner = "owner"
    amount = "amount"
    created_at = "created_at"


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat() + "Z"}


@app.get("/reports", response_model=ReportListResponse, tags=["Reports"])
def read_reports(
    status: Optional[ReportStatus] = Query(None, description="Filter by report status."),
    owner: Optional[str] = Query(None, min_length=2, description="Filter by report owner."),
    search: Optional[str] = Query(None, min_length=2, description="Search title and description."),
    date_from: Optional[datetime] = Query(None, description="Include reports created on or after this date."),
    date_to: Optional[datetime] = Query(None, description="Include reports created on or before this date."),
    min_amount: Optional[float] = Query(None, ge=0.0, description="Minimum amount filter."),
    max_amount: Optional[float] = Query(None, ge=0.0, description="Maximum amount filter."),
    sort: SortField = Query(SortField.created_at, description="Field to sort by."),
    descending: bool = Query(True, description="Sort direction."),
    offset: int = Query(0, ge=0, description="Pagination offset."),
    limit: int = Query(20, ge=1, le=200, description="Pagination limit."),
) -> ReportListResponse:
    return list_reports(
        status=status,
        owner=owner,
        search=search,
        date_from=date_from,
        date_to=date_to,
        min_amount=min_amount,
        max_amount=max_amount,
        sort=sort.value,
        descending=descending,
        offset=offset,
        limit=limit,
    )


@app.get("/reports/stats", response_model=ReportStats, tags=["Reports"])
def report_statistics(
    status: Optional[ReportStatus] = Query(None, description="Optional status filter for stats."),
    owner: Optional[str] = Query(None, description="Optional owner filter for stats."),
):
    return stats_for_reports(status=status, owner=owner)


@app.get("/reports/{report_id}", response_model=ReportDetail, tags=["Reports"])
def get_report(report_id: int):
    report = get_report_by_id(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
