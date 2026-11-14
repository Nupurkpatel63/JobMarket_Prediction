# API reference

Run the API from the repository root:

```powershell
uvicorn src.job_market_prediction.api:app --reload
```

Interactive OpenAPI documentation is available at `http://127.0.0.1:8000/docs`.

## `GET /health`

Returns `{"status":"ok"}` when the service is running.

## `POST /recommendations`

Ranks postings by TF-IDF cosine similarity to a skills/role profile. Optional filters narrow the returned results.

```json
{
  "profile": "Python SQL data analyst Power BI",
  "country": "India",
  "job_type": "Hourly",
  "category": "Data Science & Analytics",
  "min_rate": 10,
  "max_rate": 80,
  "top_n": 10
}
```

`country`, `job_type`, `category`, `min_rate`, `max_rate`, and `top_n` are optional. Rate filters require `job_type` to be `Hourly` or `Fixed-price`; hourly filters use the midpoint of the low/high rate, while fixed-price filters use the budget. `top_n` is 1–50. Response shape:

```json
{
  "count": 1,
  "results": [
    {
      "title": "Example role",
      "job_category": "Data Science & Analytics",
      "country": "India",
      "similarity_score": 0.42,
      "link": "https://example.com/posting"
    }
  ]
}
```

Actual result fields depend on source columns and may also include rate, budget, and publication date. Invalid inputs return HTTP 400.

## `GET /analytics/monthly`

Returns posting counts, number of represented categories and countries, and month-over-month percentage change for each month in the source CSV.

## `GET /analytics/categories?month=2024-03`

Returns the top 20 categories by count. `month` is optional and must use `YYYY-MM`.

## Data and refresh

The default data file is `Job_Recommendation/artifacts/jobs_data.csv`. Set `JOB_MARKET_DATA` to another CSV path to use a refreshed export. Rebuild recommendation artifacts after changing the underlying dataset:

```powershell
python scripts/build_recommendation_artifacts.py
```

The default bundled data ends on 2024-03-24. It is a historical snapshot, not a live feed.
