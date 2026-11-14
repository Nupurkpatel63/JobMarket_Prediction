# Job Market Prediction: Tasks 5–8

This repository now has a runnable structure for job recommendations, monthly market monitoring, and the two analysis reports requested in tasks 5–8.

## Project layout

```text
app.py                                  Gradio recommendation + monthly tables
dashboard.py                            Streamlit monthly dynamics dashboard
src/job_market_prediction/
  data.py                               CSV loading and normalization
  recommendations.py                    TF-IDF recommendation service
  analytics.py                           Monthly aggregates and scenarios
  api.py                                 FastAPI endpoints
scripts/build_recommendation_artifacts.py  Rebuild TF-IDF model artifacts
docs/api.md                              API reference
reports/task7_remote_work.md             Remote-work analysis and scenarios
reports/task8_future_trends.md            Forecasting report and limitations
```

## Run the interfaces

Install dependencies in your preferred Python environment:

```powershell
pip install -r requirements.txt
```

Start the interactive recommendation prototype:

```powershell
python app.py
```

Start the monthly dashboard:

```powershell
streamlit run dashboard.py
```

Start the API:

```powershell
uvicorn src.job_market_prediction.api:app --reload
```

The API's interactive docs are at `http://127.0.0.1:8000/docs`. Endpoint details and example payloads are in [docs/api.md](docs/api.md).

## Monthly refresh process

1. Update `data/job_postings_with_categories.csv` with a consistently collected and categorized export.
2. Rebuild the saved recommendation matrix and prepared records with `python scripts/build_recommendation_artifacts.py`.
3. Restart the recommendation interface/API. The dashboard reloads the configured CSV on rerun.

To point analytics at another CSV, set the `JOB_MARKET_DATA` environment variable before starting the dashboard/API. The recommendation service uses the matching artifacts stored in `Job_Recommendation/artifacts`.

## Data coverage

The bundled snapshot contains 244,827 postings dated November 2, 2023 through March 24, 2024. It is historical, not a current live feed. March 2024 is partial. The source has no reliable remote/hybrid/on-site field; Task 7 therefore reports an explicitly labeled title-keyword signal and scenarios rather than claiming a measured remote-work rate. Task 8 likewise distinguishes observed category mix from illustrative captured-volume scenarios.
