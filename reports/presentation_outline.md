# Suggested Viva Presentation (12 Slides)

1. **Title** — Social Media Intelligence & Data Analytics Platform; Vichar Media; student and programme details.
2. **Problem statement** — fragmented analytics across Instagram and YouTube; need for a consolidated, reproducible workflow.
3. **Objectives and scope** — ETL, quality checks, SQLite, dashboard, EDA, forecasting, NLP, ML feasibility and decision support.
4. **Data sources** — Instagram: 43 feed posts, 32 Stories, 28 daily rows; YouTube: lifetime aggregates and 11 top-content records. Explain the coverage limitations.
5. **System architecture** — raw source snapshots → transformation → validation → SQLite → analytics modules → Streamlit.
6. **ETL and database design** — CSV staging tables, normalisation, null policy, SQLite schema and provenance.
7. **Dashboard demonstration** — executive overview, content explorer, traffic and Stories modules.
8. **EDA findings** — skewed Instagram views, mean versus median, viral outlier and metric relationships.
9. **Advanced analytics** — trailing-mean baseline, TF-IDF/K-Means topic exploration, regression feasibility experiment.
10. **Data quality and limitations** — platform metric scopes, unreconciled YouTube aggregates, incomplete YouTube content inventory and unavailable fields.
11. **Recommendations and future scope** — obtain complete exports, enrich metadata, build stronger data model and revisit modelling with more records.
12. **Conclusion and Q&A** — demonstrate end-to-end analytical workflow and transparent data handling.

Use the actual application and outputs for the demonstration. Avoid presenting model experiments as production systems.
