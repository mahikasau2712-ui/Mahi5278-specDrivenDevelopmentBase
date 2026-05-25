# Vibe Reports API

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/fastapi-0.110.0-4BC0C0.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-pytest-brightgreen.svg)](#tests)

A polished Python FastAPI service for managing structured reports with rich filtering, sorting, pagination, and analytics.

## What makes this project better

- Fully typed and modular design
- Clean domain separation: data, models, repository, API
- Advanced filter support and metadata in responses
- Report summary, detail, and statistics endpoints
- Built-in validation and OpenAPI docs
- Unit tests with FastAPI `TestClient`

## Requirements

- Python 3.10+

## Setup

```powershell
cd c:\Users\Dell\OneDrive\Desktop\vibe_coding
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -e .
```

## Run the app

```powershell
uvicorn app.api:app --reload --port 8000
```

Then open `http://127.0.0.1:8000/docs` for interactive API documentation.

## Endpoints

- `GET /health` — service health check
- `GET /reports` — list reports with filters, sorting, and pagination
- `GET /reports/{report_id}` — fetch a single report by ID
- `GET /reports/stats` — aggregated report statistics by status

## Example queries

```powershell
curl "http://127.0.0.1:8000/reports?status=approved&search=Q2&limit=10"
curl "http://127.0.0.1:8000/reports/stats"
```

## Tests

```powershell
pytest
```
