from datetime import datetime, timedelta

STATUSES = ["pending", "approved", "rejected", "archived"]
OWNERS = [
    "Aarav",
    "Bianca",
    "Carmen",
    "Dev",
    "Elena",
    "Faiz",
    "Gita",
    "Hassan",
]


def build_reports() -> list[dict]:
    base_date = datetime(2024, 1, 3, 8, 0, 0)
    reports = []

    for report_id in range(1, 121):
        status = STATUSES[(report_id * 3) % len(STATUSES)]
        owner = OWNERS[(report_id * 5) % len(OWNERS)]
        amount = 150.0 + ((report_id * 29) % 1750) / 10.0
        created_at = base_date + timedelta(days=(report_id * 2) % 95, hours=(report_id * 7) % 18)

        reports.append(
            {
                "id": report_id,
                "title": f"Quarterly review #{report_id}",
                "description": f"Summary for report {report_id} owned by {owner}.",
                "owner": owner,
                "status": status,
                "amount": round(amount, 2),
                "created_at": created_at,
            }
        )

    return reports


REPORTS = build_reports()
