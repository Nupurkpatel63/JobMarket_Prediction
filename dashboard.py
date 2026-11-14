"""Streamlit dashboard for refreshing monthly market dynamics from CSV."""
import streamlit as st
import plotly.express as px

from src.job_market_prediction.analytics import category_monthly, monthly_summary, remote_signal_summary
from src.job_market_prediction.data import get_data_path, load_jobs

st.set_page_config(page_title="Job Market Dynamics", page_icon="📈", layout="wide")
st.title("Job Market Dynamics")
st.caption("Aggregates refresh from the configured CSV on each rerun. Set JOB_MARKET_DATA to use an updated monthly export.")

try:
    jobs = load_jobs()
except (FileNotFoundError, ValueError) as exc:
    st.error(str(exc))
    st.stop()

summary = monthly_summary(jobs)
if summary.empty:
    st.info("No valid dated postings are available.")
    st.stop()

first = jobs["published_date"].min().strftime("%Y-%m-%d")
last = jobs["published_date"].max().strftime("%Y-%m-%d")
a, b, c = st.columns(3)
a.metric("Postings in source", f"{len(jobs):,}")
b.metric("Months covered", len(summary))
c.metric("Source date range", f"{first} to {last}")
st.caption(f"Source: `{get_data_path()}`. Refresh the CSV and rerun the dashboard to add a new month.")

st.subheader("Monthly posting volume")
st.plotly_chart(px.bar(summary, x="year_month", y="postings", title="Observed job postings by month"), use_container_width=True)
st.dataframe(summary, use_container_width=True, hide_index=True)

st.subheader("Category mix")
cats = category_monthly(jobs)
available_months = cats["year_month"].unique().tolist()
selected = st.selectbox("Month", available_months, index=len(available_months)-1)
month_data = cats[cats["year_month"].eq(selected)].nlargest(15, "postings")
st.plotly_chart(px.bar(month_data.sort_values("postings"), x="postings", y="job_category", orientation="h", title=f"Top categories in {selected}"), use_container_width=True)

remote = remote_signal_summary(jobs)
st.subheader("Remote-work signal coverage")
st.metric("Title-only remote keyword matches", f"{remote['title_signal_count']:,}", f"{remote['title_signal_share_pct']:.2f}% of titles")
st.warning("This is only a keyword scan of job titles, not a remote/hybrid/on-site label. The source does not include a work-location-mode field, so remote adoption cannot be estimated reliably from these records.")
