from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel

from .data import ROOT, load_jobs

ARTIFACT_DIR = ROOT / "Job_Recommendation" / "artifacts"


@lru_cache(maxsize=1)
def load_engine():
    vectorizer_path = ARTIFACT_DIR / "tfidf_vectorizer.pkl"
    matrix_path = ARTIFACT_DIR / "job_vectors.pkl"
    if not vectorizer_path.exists() or not matrix_path.exists():
        raise FileNotFoundError(
            "Recommendation artifacts are missing. Run `python scripts/build_recommendation_artifacts.py`."
        )
    vectorizer = joblib.load(vectorizer_path)
    vectors = joblib.load(matrix_path)
    jobs = load_jobs(ARTIFACT_DIR / "jobs_data.csv")
    if vectors.shape[0] != len(jobs):
        raise ValueError("Recommendation matrix and jobs_data.csv row counts do not match.")
    return vectorizer, vectors, jobs


def recommend_jobs(
    profile: str,
    *,
    country: str | None = None,
    job_type: str | None = None,
    category: str | None = None,
    min_rate: float | None = None,
    max_rate: float | None = None,
    top_n: int = 10,
) -> pd.DataFrame:
    if not isinstance(profile, str) or not profile.strip():
        raise ValueError("Enter a job title, skills, or experience summary.")
    if not 1 <= int(top_n) <= 50:
        raise ValueError("top_n must be between 1 and 50.")
    if min_rate is not None and max_rate is not None and min_rate > max_rate:
        raise ValueError("min_rate cannot exceed max_rate.")
    vectorizer, vectors, jobs = load_engine()
    query = vectorizer.transform([profile.strip()])
    scores = linear_kernel(query, vectors).ravel()
    results = jobs.copy()
    results["similarity_score"] = scores
    results = results[results["similarity_score"] > 0]
    if country:
        results = results[results["country"].str.casefold() == country.strip().casefold()]
    if job_type:
        results = results[results["job_type"].str.casefold() == job_type.strip().casefold()]
    if category:
        results = results[results["job_category"].str.casefold() == category.strip().casefold()]
    if min_rate is not None or max_rate is not None:
        if job_type is None:
            raise ValueError("Choose Hourly or Fixed-price before applying a rate filter.")
        normalized_type = job_type.strip().casefold()
        if normalized_type not in {"hourly", "fixed-price"}:
            raise ValueError("Rate filters support only Hourly or Fixed-price jobs.")
        amount_column = "hourly_midpoint" if normalized_type == "hourly" else "budget"
        if amount_column not in results:
            raise ValueError(f"The dataset does not contain {amount_column} values.")
        if min_rate is not None:
            results = results[results[amount_column] >= min_rate]
        if max_rate is not None:
            results = results[results[amount_column] <= max_rate]
    columns = [c for c in [
        "title", "job_category", "country", "job_type", "hourly_low",
        "hourly_high", "hourly_midpoint", "budget", "similarity_score", "published_date", "link"
    ] if c in results]
    return results.sort_values("similarity_score", ascending=False)[columns].head(int(top_n)).reset_index(drop=True)
