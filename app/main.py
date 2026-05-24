from fastapi import HTTPException, Query, Body
from datetime import datetime
from typing import Optional
from .reports import get_reports
from .reports import get_report_by_id, create_report
from .models import ReportListResponse, ReportPublic, Status, ReportCreate
from . import app


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/reports", response_model=ReportListResponse)
def list_reports(
    status: Optional[Status] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    sort: str = "created_at",
    descending: bool = True,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=200),
):
    try:
        total, items = get_reports(
            status=status.value if status else None,
            date_from=date_from,
            date_to=date_to,
            sort=sort,
            descending=descending,
            offset=offset,
            limit=limit,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return ReportListResponse(
        total=total,
        offset=offset,
        limit=limit,
        items=[ReportPublic(**r) for r in items],
    )



@app.get(
    "/reports/{report_id}",
    response_model=ReportPublic,
    responses={
        200: {
            "description": "A single report",
            "content": {
                "application/json": {
                    "examples": {
                        "report": {
                            "summary": "A sample report",
                            "value": {
                                "id": 1,
                                "title": "Report 1",
                                "status": "pending",
                                "owner": "alice",
                                "amount": 103.5,
                                "created_at": "2024-01-01T00:00:00+00:00"
                            },
                        }
                    }
                }
            },
        },
        404: {"description": "Report not found"},
    },
)
def get_report(report_id: int):
    r = get_report_by_id(report_id)
    if not r:
        raise HTTPException(status_code=404, detail="report not found")
    return ReportPublic(**r)


@app.post(
    "/reports",
    response_model=ReportPublic,
    status_code=201,
    responses={
        201: {
            "description": "Created report",
            "content": {
                "application/json": {
                    "examples": {
                        "created": {
                            "summary": "Created report example",
                            "value": {
                                "id": 121,
                                "title": "New Test",
                                "status": "pending",
                                "owner": "alice",
                                "amount": 10.5,
                                "created_at": "2024-01-01T00:00:00+00:00"
                            },
                        }
                    }
                }
            },
        }
    },
)
def post_report(
    payload: ReportCreate = Body(
        ...,
        examples={
            "default": {
                "summary": "Create a new report",
                "value": {
                    "title": "Quarterly revenue",
                    "status": "pending",
                    "owner": "alice",
                    "amount": 1234.56,
                },
            }
        },
    )
):
    report = create_report(payload.dict())
    return ReportPublic(**report)
