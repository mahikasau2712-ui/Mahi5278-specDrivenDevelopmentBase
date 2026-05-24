# Improved Reports API

A small FastAPI-based example inspired by SpecDrivenDevelopmentBase `app` but refactored to be stricter and more testable.

Run locally (create a virtualenv first):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app:app --reload --port 8000
```

API:

- `GET /health` — simple liveness
- `GET /reports` — list reports with filtering, sorting, pagination
- `GET /reports/{id}` — retrieve a single report by id
- `POST /reports` — create a new report

Examples:

Get list of reports:

```powershell
curl "http://localhost:8000/reports?offset=0&limit=5"
```

Get a single report:

```powershell
curl "http://localhost:8000/reports/1"
```

Create a report:

```powershell
curl -X POST http://localhost:8000/reports -H "Content-Type: application/json" -d '{"title":"New","owner":"alice","amount":12.34}'
```

Run unit tests (no extra deps required):

```powershell
python -m unittest discover -v
```

CI:

This repository includes a GitHub Actions workflow at `.github/workflows/ci.yml` that runs the unit tests on push and pull requests.

Docker:

Build and run the app in Docker:

```powershell
docker build -t improved-reports .
docker run -p 8000:8000 improved-reports
```
