import unittest
from app.reports import get_reports
from app.data import REPORTS


class TestReports(unittest.TestCase):
    def test_pagination(self):
        total, items = get_reports(offset=0, limit=10)
        self.assertEqual(len(items), 10)
        self.assertEqual(total, len(REPORTS))

    def test_status_filter(self):
        total, items = get_reports(status="approved")
        self.assertTrue(all(r["status"] == "approved" for r in items))

    def test_get_by_id(self):
        # existing id
        r = REPORTS[0]
        found = None
        for item in REPORTS:
            if item["id"] == r["id"]:
                found = item
                break
        self.assertIsNotNone(found)

    def test_create_report(self):
        from app.reports import create_report

        payload = {"title": "New Test", "owner": "alice", "amount": 10.5}
        new = create_report(payload)
        self.assertEqual(new["title"], "New Test")
        self.assertEqual(new["owner"], "alice")
        self.assertGreaterEqual(new["id"], 1)

    def test_create_report_invalid_owner(self):
        from app.reports import create_report

        payload = {"title": "Bad", "owner": "mallory", "amount": 1.0}
        with self.assertRaises(ValueError):
            create_report(payload)


if __name__ == "__main__":
    unittest.main()
