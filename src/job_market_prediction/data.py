from __future__ import annotations

import os
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA = ROOT / "Job_Recommendation" / "artifacts" / "jobs_data.csv"


def get_data_path() -> Path:
    return Path(os.environ.get("JOB_MARKET_DATA", DEFAULT_DATA)).expanduser()


def load_jobs(path: str | Path | None = None) -> pd.DataFrame:
    """Load and normalize posting records from the configured CSV."""
    source = Path(path) if path else get_data_path()
    if not source.exists():
        raise FileNotFoundError(
            f"Job data not found at {source}. Set JOB_MARKET_DATA to a CSV file."
        )
    jobs = pd.read_csv(source, low_memory=False)
    required = {"title", "published_date"}
    missing = required - set(jobs.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {sorted(missing)}")
    jobs["title"] = jobs["title"].fillna("").astype(str).str.strip()
    jobs["published_date"] = pd.to_datetime(
        jobs["published_date"], errors="coerce", utc=True
    )
    jobs = jobs[jobs["title"].ne("") & jobs["published_date"].notna()].copy()
    jobs["year_month"] = jobs["published_date"].dt.strftime("%Y-%m")
    for column in ("hourly_low", "hourly_high", "hourly_midpoint", "budget"):
        if column in jobs:
            jobs[column] = pd.to_numeric(jobs[column], errors="coerce")
    for column, default in (("country", "Unknown"), ("job_category", "Other"), ("job_type", "Unknown")):
        if column not in jobs:
            jobs[column] = default
        jobs[column] = jobs[column].fillna(default).astype(str).str.strip()
    if "recommendation_text" not in jobs:
        jobs["recommendation_text"] = jobs["title"] + " " + jobs["job_category"]
    return jobs.reset_index(drop=True)
