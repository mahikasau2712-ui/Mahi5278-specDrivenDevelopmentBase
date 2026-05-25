from datetime import datetime
from typing import Any, Dict, List, Optional

from app.data import REPORTS
from app.models import ReportDetail, ReportStats, ReportStatus, StatusAggregate


def get_report_by_id(report_id: int) -> Optional[ReportDetail]:
    for report in REPORTS:
        if report["id"] == report_id:
            return ReportDetail(**report)
    return None


def _matches_filters(report: Dict[str, Any], **filters: Any) -> bool:
    status = filters.get("status")
    owner = filters.get("owner")
    search = filters.get("search")
    date_from = filters.get("date_from")
    date_to = filters.get("date_to")
    min_amount = filters.get("min_amount")
    max_amount = filters.get("max_amount")

    if status is not None and report["status"] != status.value:
        return False

    if owner is not None and report["owner"].lower() != owner.lower().strip():
        return False

    if search is not None:
        text = f"{report['title']} {report['description']}".lower()
        if search.lower().strip() not in text:
            return False

    if date_from is not None and report["created_at"] < date_from:
        return False

    if date_to is not None and report["created_at"] > date_to:
        return False

    if min_amount is not None and report["amount"] < min_amount:
        return False

    if max_amount is not None and report["amount"] > max_amount:
        return False

    return True


def _apply_sort(reports: List[Dict[str, Any]], sort: str, descending: bool) -> List[Dict[str, Any]]:
    return sorted(reports, key=lambda item: item[sort], reverse=descending)


def list_reports(
    status: Optional[ReportStatus] = None,
    owner: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    sort: str = "created_at",
    descending: bool = True,
    offset: int = 0,
    limit: int = 20,
) -> ReportStats | Any:
    filtered = [
        report
        for report in REPORTS
        if _matches_filters(
            report,
            status=status,
            owner=owner,
            search=search,
            date_from=date_from,
            date_to=date_to,
            min_amount=min_amount,
            max_amount=max_amount,
        )
    ]

    sorted_reports = _apply_sort(filtered, sort, descending)
    page_data = sorted_reports[offset : offset + limit]
    return {
        "data": [ReportDetail(**report) for report in page_data],
        "page": {
            "offset": offset,
            "limit": limit,
            "total": len(filtered),
            "returned": len(page_data),
        },
    }


def stats_for_reports(status: Optional[ReportStatus] = None, owner: Optional[str] = None) -> ReportStats:
    filtered = [
        report
        for report in REPORTS
        if _matches_filters(report, status=status, owner=owner)
    ]

    total_amount = sum(report["amount"] for report in filtered)
    counts = {status.value: 0 for status in ReportStatus}
    amounts = {status.value: 0.0 for status in ReportStatus}

    for report in filtered:
        counts[report["status"]] += 1
        amounts[report["status"]] += report["amount"]

    breakdown = [
        StatusAggregate(status=ReportStatus(status_key), count=counts[status_key], total_amount=round(amounts[status_key], 2))
        for status_key in counts
    ]

    return ReportStats(
        total_reports=len(filtered),
        total_amount=round(total_amount, 2),
        breakdown=breakdown,
    )
