"""FastAPI service for searching report data."""

from __future__ import annotations

from datetime import datetime

from fastapi import FastAPI, HTTPException, Query

from .query import search_reports
from .schemas import ReportPage, ReportResponse, ReportStatus

app = FastAPI(title="Report Service", version="0.1.0")


@app.get("/ping")
def ping() -> dict[str, str]:
    return {"status": "alive"}


@app.get("/reports", response_model=ReportPage)
def list_reports(
    status: ReportStatus | None = Query(None, description="Filter by report status"),
    date_from: datetime | None = Query(None, description="Start date/time inclusive"),
    date_to: datetime | None = Query(None, description="End date/time inclusive"),
    sort: str = Query("created_at", description="Field to sort by"),
    descending: bool = Query(True, description="Sort newest first when true"),
    offset: int = Query(0, ge=0, description="Result offset"),
    limit: int = Query(20, ge=1, le=200, description="Maximum number of items"),
) -> ReportPage:
    try:
        all_rows = search_reports(
            status=status,
            date_from=date_from,
            date_to=date_to,
            sort=sort,
            descending=descending,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    page = all_rows[offset : offset + limit]
    return ReportPage(
        items=[ReportResponse.from_internal(row) for row in page],
        total=len(all_rows),
        offset=offset,
        limit=limit,
    )
