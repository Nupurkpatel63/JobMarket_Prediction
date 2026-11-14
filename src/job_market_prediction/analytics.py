from __future__ import annotations

import pandas as pd


REMOTE_TERMS = r"\b(?:remote|work from home|work-from-home|wfh|telecommut(?:e|ing)|distributed team|anywhere)\b"


def monthly_summary(jobs: pd.DataFrame) -> pd.DataFrame:
    """Aggregate posting counts and mix by calendar month."""
    summary = jobs.groupby("year_month").agg(
        postings=("title", "size"),
        categories=("job_category", "nunique"),
        countries=("country", "nunique"),
    )
    summary["month_over_month_pct"] = summary["postings"].pct_change() * 100
    return summary.reset_index()


def category_monthly(jobs: pd.DataFrame) -> pd.DataFrame:
    return (
        jobs.groupby(["year_month", "job_category"])
        .size()
        .rename("postings")
        .reset_index()
    )


def remote_signal_summary(jobs: pd.DataFrame) -> dict:
    """Count title-only mentions; these are not a validated remote-work label."""
    matches = jobs["title"].str.contains(REMOTE_TERMS, case=False, regex=True, na=False)
    return {
        "postings": int(len(jobs)),
        "title_signal_count": int(matches.sum()),
        "title_signal_share_pct": float(matches.mean() * 100) if len(jobs) else 0.0,
        "monthly": (
            jobs.assign(remote_title_signal=matches)
            .groupby("year_month")["remote_title_signal"]
            .agg(postings="size", title_signals="sum")
            .reset_index()
        ),
    }


def scenario_projection(jobs: pd.DataFrame, horizon_months: int = 6) -> pd.DataFrame:
    """Create transparent flat/low/high scenarios from the latest observed month.

    Scenarios are arithmetic extrapolations, not a validated forecasting model.
    They are deliberately bounded to avoid compounding a short, partial snapshot.
    """
    monthly = monthly_summary(jobs)
    if monthly.empty:
        return pd.DataFrame(columns=["year_month", "flat", "base", "high"])
    last_value = float(monthly.iloc[-1]["postings"])
    # March may be incomplete; normalize the last month to a 30-day equivalent.
    last_month = pd.Period(monthly.iloc[-1]["year_month"], freq="M")
    observed_days = int(jobs.loc[jobs["year_month"].eq(str(last_month)), "published_date"].dt.day.max())
    normalized_last = last_value * (last_month.days_in_month / max(observed_days, 1))
    # Use fixed stress-test bands; the brief history is too short to estimate trend.
    dates = pd.period_range(last_month + 1, periods=horizon_months, freq="M")
    return pd.DataFrame({
        "year_month": dates.astype(str),
        "flat": [round(normalized_last)] * horizon_months,
        "low_minus_10pct_monthly": [round(normalized_last * 0.9 ** i) for i in range(1, horizon_months + 1)],
        "high_plus_10pct_monthly": [round(normalized_last * 1.1 ** i) for i in range(1, horizon_months + 1)],
    })
