from datetime import datetime, timezone
from typing import Optional, List, Tuple
from .data import REPORTS, STATUSES, OWNERS


ALLOWED_SORT_KEYS = {"id", "title", "status", "owner", "amount", "created_at"}


def get_reports(
    status: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    sort: str = "created_at",
    descending: bool = True,
    offset: int = 0,
    limit: int = 20,
) -> Tuple[int, List[dict]]:
    results = list(REPORTS)

    # Validate status
    if status:
        if status not in STATUSES:
            raise ValueError(f"unknown status: {status}")
        results = [r for r in results if r["status"] == status]

    # Filter by date range
    if date_from:
        results = [r for r in results if r["created_at"] >= date_from]
    if date_to:
        results = [r for r in results if r["created_at"] <= date_to]

    # Validate sort key
    if sort not in ALLOWED_SORT_KEYS:
        raise ValueError(f"invalid sort field: {sort}")

    # Sort
    results.sort(key=lambda r: r[sort], reverse=descending)

    # Pagination
    total = len(results)
    results = results[offset: offset + limit]

    return total, results


def get_report_by_id(report_id: int) -> Optional[dict]:
    for r in REPORTS:
        if r["id"] == report_id:
            return r
    return None


def create_report(data: dict) -> dict:
    # Basic validation
    status = data.get("status")
    if status and status not in STATUSES:
        raise ValueError(f"unknown status: {status}")

    amount = data.get("amount", 0)
    if amount < 0:
        raise ValueError("amount must be non-negative")

    owner = data.get("owner")
    if owner not in OWNERS:
        raise ValueError(f"unknown owner: {owner}")

    # Assign new ID and created_at if missing
    new_id = max(r["id"] for r in REPORTS) + 1 if REPORTS else 1
    report = {
        "id": new_id,
        "title": data["title"],
        "status": status or "pending",
        "owner": data["owner"],
        "amount": float(amount),
        "created_at": data.get("created_at") or datetime.now(timezone.utc),
        "internal_notes": data.get("internal_notes", ""),
    }
    REPORTS.append(report)
    return report
