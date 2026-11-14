from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from .analytics import monthly_summary
from .data import load_jobs
from .recommendations import recommend_jobs

app = FastAPI(
    title="Job Market Insights API",
    version="1.0.0",
    description="Job recommendations and historical monthly posting analytics.",
)


class RecommendationRequest(BaseModel):
    profile: str = Field(min_length=1, description="Skills, role, or experience text")
    country: str | None = None
    job_type: str | None = Field(default=None, description="Hourly or Fixed-price")
    category: str | None = None
    min_rate: float | None = Field(default=None, ge=0)
    max_rate: float | None = Field(default=None, ge=0)
    top_n: int = Field(default=10, ge=1, le=50)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/recommendations")
def recommendations(request: RecommendationRequest):
    try:
        payload = request.model_dump() if hasattr(request, "model_dump") else request.dict()
        result = recommend_jobs(**payload)
        return {"count": len(result), "results": result.astype(object).where(result.notna(), None).to_dict("records")}
    except (ValueError, FileNotFoundError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.get("/analytics/monthly")
def monthly_analytics():
    try:
        summary = monthly_summary(load_jobs())
        return {"months": summary.astype(object).where(summary.notna(), None).to_dict("records")}
    except (ValueError, FileNotFoundError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/analytics/categories")
def category_analytics(month: str | None = Query(default=None, pattern=r"^\d{4}-\d{2}$")):
    jobs = load_jobs()
    if month:
        jobs = jobs[jobs["year_month"].eq(month)]
    counts = jobs.groupby("job_category").size().sort_values(ascending=False).head(20)
    return {"month": month, "categories": [{"category": k, "postings": int(v)} for k, v in counts.items()]}
