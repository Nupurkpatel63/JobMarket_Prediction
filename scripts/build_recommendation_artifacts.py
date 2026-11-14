"""Rebuild the TF-IDF recommendation artifacts from the categorized CSV."""
from pathlib import Path
import sys

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.job_market_prediction.data import ROOT, load_jobs

output = ROOT / "Job_Recommendation" / "artifacts"
source = ROOT / "data" / "job_postings_with_categories.csv"
jobs = load_jobs(source)
vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), max_features=50_000, min_df=2, max_df=0.95)
vectors = vectorizer.fit_transform(jobs["recommendation_text"])
output.mkdir(parents=True, exist_ok=True)
joblib.dump(vectorizer, output / "tfidf_vectorizer.pkl")
joblib.dump(vectors, output / "job_vectors.pkl")
jobs.to_csv(output / "jobs_data.csv", index=False)
print(f"Built TF-IDF artifacts for {len(jobs):,} postings in {output}")
