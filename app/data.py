from datetime import datetime, timezone, timedelta

STATUSES = ["pending", "approved", "rejected", "archived"]
OWNERS = ["alice", "bob", "carol", "dave", "eve"]

REPORTS = []
start = datetime(2024, 1, 1, tzinfo=timezone.utc)
for i in range(1, 121):
    created = start + timedelta(days=(i - 1) % 28)
    REPORTS.append({
        "id": i,
        "title": f"Report {i}",
        "status": STATUSES[i % len(STATUSES)],
        "owner": OWNERS[i % len(OWNERS)],
        "amount": round(100 + i * 3.5, 2),
        "created_at": created,
        "internal_notes": f"Internal note for report {i}",
    })
