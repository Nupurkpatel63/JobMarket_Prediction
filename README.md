# Job Market Prediction

A job-market analytics project built around freelance job postings. The project covers eight tasks: salary analysis, emerging categories, demand forecasting, country comparisons, personalized recommendations, monthly monitoring, remote-work signals, and future scenarios.

## Project contents

```text
job_market_prediction01.ipynb                Tasks 1–4: analysis and forecasting
job_market_prediction02.ipynb                Task 5: recommendation-engine development
data/job_postings_with_categories.csv        Categorized posting-level dataset
Job_Recommendation/artifacts/jobs_data.csv   Prepared data used by the recommender
Job_Recommendation/artifacts/tfidf_vectorizer.pkl
Job_Recommendation/artifacts/job_vectors.pkl
app.py                                        Gradio recommender and monthly tables
dashboard.py                                  Streamlit market-dynamics dashboard
src/job_market_prediction/
  data.py                                     CSV loading and normalization
  analytics.py                                Monthly metrics and scenario projections
  recommendations.py                          TF-IDF recommendation service
  api.py                                      FastAPI service
scripts/build_recommendation_artifacts.py     Rebuild model artifacts from categorized CSV
docs/api.md                                   Endpoint reference
reports/task7_remote_work.md                 Remote-work report
reports/task8_future_trends.md                Forecasting and scenario report
output/Job_Market_Prediction_Project_Submission.pptx
                                              Presentation covering the full project
```

## Tasks and results

### Task 1 — Job-title keywords and hourly rates

The notebook cleans hourly-rate records, calculates hourly midpoints, extracts frequent words and phrases from job titles, and measures their association with offered rates. Pearson correlations are adjusted for multiple comparisons with Benjamini–Hochberg correction.

Some higher average midpoint examples were Consultant (51.51), Machine Learning (41.14), Engineer (37.89), Senior (37.80), and Data Scientist (37.74). Assistant (13.44) and Virtual (12.84) were lower. Most correlations were weak: Consultant was 0.0680 and Assistant was −0.1076. The analysis shows associations, not causal effects. The dataset does not specify the currency.

### Task 2 — Emerging job categories

Posting counts are grouped by job category and month. To account for March being incomplete, the notebook compares average daily posting rates for February and March 2024.

Digital Marketing & SEO had the largest absolute increase (+173.10 average postings per day), followed by Software & Web Development (+149.45), E-commerce & Online Marketplace (+113.45), Graphic & UI/UX Design (+100.97), and Video & Content Creation (+100.59). Cybersecurity & IT Infrastructure had the largest percentage growth (88.98%) from a smaller base. This is a short period and categories are assigned from posting text, so the findings are signals rather than confirmed long-term trends.

### Task 3 — Predicting high-demand roles

The notebook aggregates postings into weekly category counts and trains a Random Forest regressor using prior-week demand, two-week lag, a three-week rolling average, and a week index. The sample forecast for the week of March 18, 2024 ranked Digital Marketing & SEO first (2,925), Software & Web Development second (2,604), Writing & Translation third (1,995), E-commerce fourth (1,929), and Graphic & UI/UX fifth (1,697).

The notebook reports overall MAE 120.65 and RMSE 151.34. The reported R² of 0.9586 is not reliable evidence of forecast quality: the test set contains only one week. More history and rolling-origin validation are needed before using this model for decisions.

### Task 4 — Hourly rates by country

The notebook calculates the mean and median of valid hourly midpoints by country, retaining countries with at least 30 postings. It analyzes 96,825 hourly jobs from 191 countries and retains 91 countries for the comparison.

The highest displayed averages were Malaysia (48.10), Thailand (42.21), and Jordan (36.15). The United States averaged 32.58 across 46,620 jobs, the United Kingdom 29.49 across 8,113, and India 23.68 across 4,337. Malaysia and Thailand both had a median of 22.50, indicating that high-rate postings influence their means. Currency is not specified.

### Task 5 — Personalized job recommendations

The prototype converts the candidate’s skills or target role and each posting’s title plus assigned category into TF-IDF vectors. It ranks postings by cosine similarity and supports filters for country, category, job type, hourly midpoint, and fixed-price budget. It returns the top 1–50 matches with similarity score and posting link.

Deliverables include the Gradio interface (`app.py`), FastAPI endpoints (`src/job_market_prediction/api.py`), saved vectorizer and sparse job matrix, and a rebuild script. The recommender’s text features do not include full job descriptions; similarity is a ranking measure, not a probability of hiring.

### Task 6 — Monthly job-market dynamics

The Streamlit dashboard (`dashboard.py`) summarizes monthly posting totals, month-over-month change, category mix, country coverage, and title-only remote-work signals. It reloads the configured CSV when the dashboard reruns. The Gradio app also provides monthly summary tables.

The current export has 1 posting in November 2023, 10 in December, 96 in January 2024, 101,887 in February, and 142,834 through March 24. The abrupt volume shift should not be read as market growth; it may reflect a change in collection coverage.

### Task 7 — Remote-work landscape

The available dataset has no reliable remote, hybrid, or on-site field. A keyword scan of titles finds 1,371 explicit remote-work signals among 244,827 prepared postings (about 0.56%). This measures wording in titles, not remote-work prevalence. The report gives sensitivity scenarios and explains what data is needed for a valid remote-work forecast.

See [reports/task7_remote_work.md](reports/task7_remote_work.md).

### Task 8 — Future job-market scenarios

The analytics module creates flat, −10% monthly, and +10% monthly scenarios after normalizing the March 1–24 posting count to a 30-day equivalent. These are arithmetic stress scenarios for captured posting volume from the March 2024 data vintage, not validated predictions of current job-market demand.

Digital Marketing, Software/Web Development, E-commerce, Writing, Design, and Video were leading coded categories in the snapshot. “Other” represents about 61.9% of March postings, limiting detailed category forecasts. See [reports/task8_future_trends.md](reports/task8_future_trends.md).

## Setup

Use Python 3.10 or newer. Install the project dependencies in a virtual environment or another preferred Python environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

The recommendation interface, dashboard, and API are separate processes. Run the command for the component you want from the repository root.

### Recommendation interface

```powershell
python app.py
```

### Monthly dashboard

```powershell
streamlit run dashboard.py
```

### API

```powershell
uvicorn src.job_market_prediction.api:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API documentation. Endpoint parameters and examples are in [docs/api.md](docs/api.md).

## Monthly data refresh

1. Replace or update `data/job_postings_with_categories.csv` with a consistently collected and categorized export.
2. Rebuild the recommendation artifacts:

   ```powershell
   python scripts/build_recommendation_artifacts.py
   ```

3. Restart the Gradio interface and API so the recommender reloads the model artifacts. Rerun the Streamlit dashboard to load refreshed analytics data.

Set `JOB_MARKET_DATA` to a CSV path before starting the dashboard or API to use another analytics dataset. Recommendation artifacts must be built from the corresponding data and remain aligned by row order.

## Data and interpretation notes

- The bundled snapshot contains 244,828 raw records dated November 2, 2023 through March 24, 2024. The prepared recommendation dataset has 244,827 usable records.
- March 2024 is partial. The source is historical and is not a live feed.
- This is a single freelance-marketplace sample; counts are postings, not unique hires or employment outcomes.
- Currency is not established for rate fields.
- Category labels come from text classification; a large “Other” category remains.
- No reliable work arrangement label exists. Remote-work statistics are title-keyword indicators only.
- The notebook forecast uses a very small training and testing window. Validate future models using more complete history and multiple time-based test periods.
