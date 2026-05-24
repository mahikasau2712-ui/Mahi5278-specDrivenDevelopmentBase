from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone

from .schemas import ReportInternal, ReportStatus

_OWNERS: list[tuple[str, str]] = [
    ("Aarav Singh", "aarav.singh@example.com"),
    ("Mina Patel", "mina.patel@example.com"),
    ("Riya Mehta", "riya.mehta@example.com"),
    ("Karan Desai", "karan.desai@example.com"),
    ("Zara Khan", "zara.khan@example.com"),
    ("Noah Bose", "noah.bose@example.com"),
    ("Lina Roy", "lina.roy@example.com"),
    ("Ishaan Verma", "ishaan.verma@example.com"),
]

_TITLES: list[str] = [
    "Quarterly spending summary",
    "Customer success dashboard",
    "Vendor payment review",
    "Security audit checklist",
    "Regional compliance status",
    "Product launch budget forecast",
    "Support ticket escalation report",
    "Revenue retention analysis",
    "Contract renewal summary",
    "Engineering capacity plan",
]

_STATUSES: list[ReportStatus] = ["pending", "approved", "rejected", "archived"]


def _build_seed_reports() -> list[ReportInternal]:
    rng = random.Random(20260525)
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    reports: list[ReportInternal] = []
    for number in range(1, 121):
        owner, email = rng.choice(_OWNERS)
        reports.append(
            ReportInternal(
                id=number,
                secret_tag=f"TAG-{number:05d}-{rng.randrange(1000, 10000)}",
                title=rng.choice(_TITLES),
                status=rng.choice(_STATUSES),
                owner=owner,
                owner_email=email,
                amount=round(rng.uniform(150.0, 48000.0), 2),
                created_at=start + timedelta(hours=rng.randrange(0, 24 * 130)),
            )
        )
    return reports


REPORTS: list[ReportInternal] = _build_seed_reports()


def all_reports() -> list[ReportInternal]:
    """Return a fresh copy of the in-memory dataset."""
    return list(REPORTS)
