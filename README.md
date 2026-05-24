# Report Service

A small FastAPI service that exposes a paginated `/reports` endpoint backed by a deterministic in-memory dataset.

## Setup

```bash
cd report_service
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## Run

```bash
uvicorn reports_app.main:app --reload --port 8000
```

## Endpoints

- `GET /ping` — health check
- `GET /reports` — list reports with filtering, sorting, and pagination

### Query parameters for `/reports`

- `status`: pending | approved | rejected | archived
- `date_from`: ISO datetime inclusive
- `date_to`: ISO datetime inclusive
- `sort`: `id`, `title`, `status`, `owner`, `amount`, `created_at`
- `descending`: `true` or `false`
- `offset`: integer >= 0
- `limit`: integer 1..200
