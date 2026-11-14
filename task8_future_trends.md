# Task 8: Future job market trends

## Executive summary

This project contains 244,827 postings dated November 2, 2023 to March 24, 2024. Almost all records fall in February and March: 101,886 in February and 142,834 through March 24. March is incomplete, and the sharp difference in captured volume cannot be treated as labor-market growth. The data provides a useful snapshot of category mix, but its short history is insufficient for a validated predictive model.

## Observed category mix

The largest coded categories in March were Digital Marketing & SEO (9,518 postings; 6.66%), Software & Web Development (8,582; 6.01%), E-commerce & Online Marketplace (6,437; 4.51%), Writing, Translation & Editing (6,431; 4.50%), and Graphic & UI/UX Design (5,583; 3.91%). `Other` accounted for 88,394 postings (61.89%), so the category classifier leaves substantial demand unclassified.

Comparing category shares in February and March offers a composition signal rather than a volume forecast. The largest categories stayed broadly similar. For example, Digital Marketing & SEO moved from 6.36% to 6.66%, Software & Web Development from 5.92% to 6.01%, and Writing, Translation & Editing from 5.70% to 4.50%. These two-month changes are descriptive and may reflect sampling or classification changes.

## Six-month scenario frame

To make uncertainty explicit, the companion analytics module normalizes the last observed month's captured volume to a 30-day equivalent (about 184,494 postings) and produces three arithmetic scenarios. The table below shows the six months after the source cutoff. These are retrospective, illustrative scenarios from the March 2024 data vintage, not forecasts for today's market.

| Month after snapshot | Low: -10% monthly | Flat | High: +10% monthly |
| --- | ---: | ---: | ---: |
| 2024-04 | 166,045 | 184,494 | 202,943 |
| 2024-05 | 149,440 | 184,494 | 223,238 |
| 2024-06 | 134,496 | 184,494 | 245,562 |
| 2024-07 | 121,047 | 184,494 | 270,118 |
| 2024-08 | 108,942 | 184,494 | 297,129 |
| 2024-09 | 98,048 | 184,494 | 326,842 |

These scenarios describe **captured postings under a fixed collection process**, not total job-market demand. Since the source ends on March 24, 2024 and has only two high-volume months, the ranges are stress cases rather than a trained forecast. Re-run them against a longer, consistently collected series before using them for operational decisions.

Category scenarios should be treated as directional: digital marketing, software/web development, e-commerce, writing, design, and video/content creation were the leading coded groups in the snapshot. Their future ranking is unknown. A persistent `Other` share above 60% means improving classification is a priority before fine-grained predictions.

## Model readiness and next steps

The repository's earlier notebook attempts a random-forest forecast from a very short weekly series. Such a short holdout is not enough to establish stable forecast accuracy. A production report should compare seasonal-naive and trend baselines against a rolling-origin backtest, publish MAE and WAPE over several held-out weeks, and forecast category counts only after enough consistent weekly history has accumulated. Track dataset coverage and category-definition changes alongside each forecast.

## Limitations

This is a single-marketplace posting sample, not a census of jobs or employment. Duplicate listings, collection intensity, incomplete months, and classifier drift can change observed counts. It contains no reliable remote-work label. All forecasts and scenarios should be refreshed and revalidated when a new monthly export is available.
