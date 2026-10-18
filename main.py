from collections import defaultdict
from decimal import Decimal, InvalidOperation
import os
import secrets
from typing import Any

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict

# Assigned by the course question. An environment variable can override it on
# the hosting platform, but the default is ready for this specific exercise.
API_KEY = os.getenv("ANALYTICS_API_KEY", "ak_tiepkw1t47bmowb5vvpt6ttd")
EMAIL = os.getenv("STUDENT_EMAIL", "24f3002072@ds.study.iitm.ac.in")

app = FastAPI(title="POST Analytics API", version="1.0.0")

# The exam page calls this API from a browser origin. Wildcard CORS is suitable
# here because this endpoint does not use cookie-based credentials.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Event(BaseModel):
    model_config = ConfigDict(extra="allow")
    user: str
    amount: float
    ts: int | float | str | None = None


class AnalyticsRequest(BaseModel):
    model_config = ConfigDict(extra="allow")
    events: list[Event]


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "post-analytics-api", "endpoint": "POST /analytics"}


@app.post("/analytics")
def analytics(
    payload: AnalyticsRequest,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> dict[str, Any]:
    if not x_api_key or not secrets.compare_digest(x_api_key, API_KEY):
        raise HTTPException(status_code=401, detail="Unauthorized")

    events = payload.events
    positive_totals: dict[str, Decimal] = defaultdict(Decimal)
    revenue = Decimal("0")
    unique_users: set[str] = set()

    for event in events:
        user = event.user
        unique_users.add(user)
        # Sum only strictly positive event amounts; zero and negatives are ignored.
        amount = Decimal(str(event.amount))
        if amount > 0:
            revenue += amount
            positive_totals[user] += amount

    top_user = ""
    if positive_totals:
        # The assignment states that the grader ensures there are no ties.
        top_user = max(positive_totals, key=positive_totals.get)

    return {
        "email": EMAIL,
        "total_events": len(events),
        "unique_users": len(unique_users),
        "revenue": float(revenue),
        "top_user": top_user,
    }
