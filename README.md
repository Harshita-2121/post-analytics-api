# POST Analytics API

FastAPI service for the TDS POST analytics endpoint exercise.

## Endpoint

`POST /analytics`

Send JSON in the form:

```json
{
  "events": [
    {"user": "alice", "amount": 42.5, "ts": 1700000000},
    {"user": "bob", "amount": -2, "ts": 1700000001}
  ]
}
```

Supply the exact assigned key in the `X-API-Key` request header. Missing or incorrect keys return HTTP 401. The successful response includes `email`, `total_events`, `unique_users`, `revenue` (strictly positive amounts only), and `top_user` (largest aggregate of strictly positive amounts).

CORS allows cross-origin browser requests.

## Run locally

```bash
python -m pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Deploy on Render

Create a new Web Service connected to this repository, use `pip install -r requirements.txt` as the build command, and `uvicorn main:app --host 0.0.0.0 --port $PORT` as the start command. The assigned API key and student email are defaults in `main.py`; optional environment variables `ANALYTICS_API_KEY` and `STUDENT_EMAIL` can override them.
