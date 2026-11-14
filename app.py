"""Gradio interface for job recommendations and monthly trend snapshots."""
import gradio as gr

from src.job_market_prediction.analytics import category_monthly, monthly_summary
from src.job_market_prediction.data import load_jobs
from src.job_market_prediction.recommendations import recommend_jobs

jobs = load_jobs()
countries = sorted(c for c in jobs["country"].dropna().unique() if c)
categories = sorted(c for c in jobs["job_category"].dropna().unique() if c)


def recommend(profile, country, job_type, category, minimum, maximum, count):
    try:
        result = recommend_jobs(
            profile,
            country=None if country == "All countries" else country,
            job_type=None if job_type == "All types" else job_type,
            category=None if category == "All categories" else category,
            min_rate=minimum,
            max_rate=maximum,
            top_n=int(count),
        )
        if "similarity_score" in result:
            result["similarity_score"] = result["similarity_score"].round(3)
        return result
    except Exception as exc:
        raise gr.Error(str(exc)) from exc


def monthly_view():
    return monthly_summary(load_jobs()), category_monthly(load_jobs())


with gr.Blocks(title="Job Market Explorer") as demo:
    gr.Markdown("# Job Market Explorer\nRecommendations and monthly posting trends from the configured dataset.")
    with gr.Tab("Job recommendations"):
        profile = gr.Textbox(label="Your skills or target role", lines=3, placeholder="Python, SQL, data analysis")
        with gr.Row():
            country = gr.Dropdown(["All countries"] + countries, value="All countries", label="Country")
            job_type = gr.Dropdown(["All types", "Hourly", "Fixed-price"], value="All types", label="Job type")
            category = gr.Dropdown(["All categories"] + categories, value="All categories", label="Category")
        with gr.Row():
            minimum = gr.Number(label="Minimum rate or budget", minimum=0)
            maximum = gr.Number(label="Maximum rate or budget", minimum=0)
            count = gr.Slider(1, 50, value=10, step=1, label="Results")
        button = gr.Button("Find matching jobs", variant="primary")
        output = gr.Dataframe(label="Recommended postings", interactive=False, wrap=True)
        button.click(recommend, [profile, country, job_type, category, minimum, maximum, count], output)
    with gr.Tab("Monthly market dynamics"):
        gr.Markdown("Refresh the configured CSV to update the aggregates. The dashboard displays observed data only.")
        refresh = gr.Button("Refresh from CSV")
        monthly = gr.Dataframe(label="Monthly totals", interactive=False)
        by_category = gr.Dataframe(label="Monthly category counts", interactive=False)
        refresh.click(monthly_view, outputs=[monthly, by_category])


if __name__ == "__main__":
    demo.launch()
