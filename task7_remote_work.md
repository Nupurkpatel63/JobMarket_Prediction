# Task 7: Remote work landscape

## Executive summary

The available project dataset does not record whether a posting is remote, hybrid, or on-site. A conservative scan of posting titles finds **1,371 of 244,827 titles (0.56%)** containing an explicit remote-work term. This is a lower-bound text signal, not an estimate of remote work prevalence: postings often omit work mode from the title, and no posting description or location-mode field is available to check them. The data therefore cannot support a reliable forecast of remote-work adoption.

## Dataset and method

- Source: the project's categorized job-posting export, containing 244,827 dated postings.
- Date coverage: November 2, 2023 to March 24, 2024. March is partial.
- Signal: case-insensitive title scan for `remote`, `work from home`, `work-from-home`, `WFH`, `telecommute`, `distributed team`, and `anywhere`.
- Results: 1,371 title matches overall; 579 of 101,886 postings in February (0.57%); 789 of 142,834 postings through March 24 (0.55%).

The signal share is nearly unchanged between the two high-volume months, but this comparison covers only two adjacent months and depends on words used in titles. It should not be interpreted as a trend in actual remote work.

## What the data supports

The dataset supports an auditable count of explicit remote-related title language over time. That metric can be refreshed each month and used as a monitoring indicator if future exports preserve the same collection and classification rules. It does not identify remote eligibility when the title does not say so, and it cannot distinguish fully remote from hybrid or occasional work-from-home arrangements.

## Forecast scenarios

Because there is no reliable work-mode label or description text, no statistically defensible remote-work forecast can be fitted from this source. For planning only, a title-signal baseline scenario would hold the observed rate near 0.56%; a higher-visibility scenario would double the rate to about 1.12%; and a lower-visibility scenario would halve it to about 0.28%. These are sensitivity assumptions, not predicted adoption rates. They measure title wording only.

## Recommendations for a valid next edition

Collect full posting descriptions and an explicit work arrangement label (remote, hybrid, on-site, or unspecified). Normalize duplicate postings and retain source and collection dates. Validate a labeled sample manually, measure precision and recall for the keyword/model classifier, and report results by job category and geography with sample sizes. A longer history is needed before forecasting changes over time.

## Limitations

The postings stop in March 2024, are concentrated on one freelance marketplace, and may not represent the wider labor market. The large share of postings classified as `Other` also limits category-level interpretation. Counts reflect captured listings, not unique vacancies, hires, or workforce outcomes.
