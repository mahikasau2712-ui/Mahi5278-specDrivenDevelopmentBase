from __future__ import annotations

from datetime import datetime
from typing import Iterable

from .data_store import all_reports
from .schemas import ReportInternal, ReportStatus

SORT_OPTIONS = {"id", "title", "status", "owner", "amount", "created_at"}


def search_reports(
    *,
    status: ReportStatus | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    sort: str = "created_at",
    descending: bool = True,
) -> list[ReportInternal]:
    """Return filtered and sorted report rows."""

    if sort not in SORT_OPTIONS:
        raise ValueError(f"Unsupported sort field: {sort!r}")

    results: Iterable[ReportInternal] = all_reports()

    if status is not None:
        results = (item for item in results if item.status == status)
    if date_from is not None:
        results = (item for item in results if item.created_at >= date_from)
    if date_to is not None:
        results = (item for item in results if item.created_at <= date_to)

    return sorted(results, key=lambda item: getattr(item, sort), reverse=descending)
