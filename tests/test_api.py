from fastapi.testclient import TestClient

from app.api import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_read_reports_default():
    response = client.get("/reports")
    assert response.status_code == 200
    data = response.json()
    assert data["page"]["offset"] == 0
    assert data["page"]["limit"] == 20
    assert len(data["data"]) == 20
    assert data["page"]["total"] >= 120


def test_read_reports_filter_and_sort():
    response = client.get("/reports?status=approved&limit=5&sort=amount&descending=false")
    assert response.status_code == 200
    page = response.json()["page"]
    assert page["returned"] == 5
    assert all(report["status"] == "approved" for report in response.json()["data"])


def test_get_report_by_id():
    response = client.get("/reports/5")
    assert response.status_code == 200
    payload = response.json()
    assert payload["id"] == 5
    assert "title" in payload
    assert payload["amount"] >= 0


def test_get_report_not_found():
    response = client.get("/reports/9999")
    assert response.status_code == 404


def test_report_stats():
    response = client.get("/reports/stats")
    assert response.status_code == 200
    stats = response.json()
    assert stats["total_reports"] >= 120
    assert isinstance(stats["breakdown"], list)
    assert any(item["count"] >= 0 for item in stats["breakdown"])
