# Viva Preparation Guide

Use this as a study aid. The student should run the project, inspect the source tables and be able to explain each step in their own words. Do not claim to have personally completed work that was not done.

## 1. Project in 60 seconds

“This project is a social media intelligence platform for Vichar Media. It takes Instagram and YouTube analytics audit data, standardises the different datasets with Python and Pandas, validates data quality, stores the prepared tables in SQLite, and presents the results through a Streamlit dashboard. It also contains exploratory analysis, a small time-series baseline, an NLP topic-clustering experiment, an exploratory content-performance model and a rule-based decision-support module. The project deliberately records missing data and conflicting totals rather than silently changing them.”

## 2. Common viva questions and answer prompts

### Q1. What problem does the project solve?
It brings fragmented platform analytics into a consistent analysis workflow so a digital publisher can inspect content performance, audience growth, traffic sources and data-quality issues in one place.

### Q2. Why did you use Python?
Python has mature libraries for data manipulation, analysis, visualisation and machine learning. Pandas handles tabular data, NumPy supports numerical operations, Scikit-learn provides ML and NLP tools, and Streamlit can turn Python analytics into an interactive application.

### Q3. What is ETL?
ETL stands for Extract, Transform and Load. Here, Extract means reading the supplied audit tables, Transform means cleaning dates and numeric values and arranging them into standardised tables, and Load means writing the processed tables into SQLite.

### Q4. Why keep raw data separately?
The raw audit snapshots preserve the original source. If a transformation is incorrect, the pipeline can be rebuilt from the source without losing provenance. It also makes changes auditable.

### Q5. How did you handle missing values?
Values such as “No figure” and “Unavailable” are converted to null/blank values. They are not replaced with zero because zero means a measured absence while null means no value was supplied.

### Q6. What is a relational database?
A relational database stores data in tables with rows and columns. In this project, content, Stories, daily metrics, traffic sources and data-quality issues are separate tables so each dataset has a clear grain and purpose.

### Q7. Why SQLite?
SQLite is a lightweight, file-based relational database. It is easy to distribute with a local prototype and supports SQL without requiring a separate database server.

### Q8. What is EDA?
Exploratory Data Analysis is the process of inspecting a dataset using summary statistics and visualisations to understand distributions, missing values, outliers and relationships before attempting more complex modelling.

### Q9. Why show both mean and median?
The Instagram Reel views are strongly right-skewed because one Reel has 737,214 views. The mean is pulled upward by this outlier, while the median describes the middle observation and is more representative of a typical Reel in this sample.

### Q10. What is an outlier?
An outlier is an observation that is unusually far from the rest of the data. It can represent a genuine viral event, a data error or a special circumstance. It should be investigated rather than automatically deleted.

### Q11. Does correlation mean causation?
No. Correlation measures how two variables move together. It does not prove that one causes the other. For example, views and likes may be correlated because both are influenced by audience exposure.

### Q12. What is a time series?
A time series is a sequence of observations indexed in time, such as daily views or daily follower changes. The order matters because observations are not independent of their time position.

### Q13. Why was a trailing-mean forecast used?
The supplied Instagram daily series is short. A trailing mean provides a transparent baseline that is easy to evaluate against a chronological holdout. It does not assume a complex seasonal pattern that the data cannot reliably support.

### Q14. What is TF-IDF?
Term Frequency–Inverse Document Frequency assigns higher weight to terms that are frequent in a particular document but less common across the full collection. It converts text into numerical features for tasks such as clustering.

### Q15. What is K-Means?
K-Means is an unsupervised clustering algorithm. It assigns observations to a specified number of clusters based on distance in feature space. In this project, TF-IDF text vectors are clustered to explore similarities between content labels.

### Q16. Why are the NLP clusters exploratory?
The Instagram text values are topic paraphrases supplied in an audit, not original captions. The YouTube set is only a top-content shortlist. The result helps explore possible groupings but is not a verified editorial taxonomy.

### Q17. What is the difference between classification and regression?
Classification predicts a category or class, while regression predicts a numerical value. The content-view experiment is a regression task because the target is a view count.

### Q18. What is overfitting?
Overfitting happens when a model learns patterns specific to its training data, including noise, and performs poorly on unseen examples. A chronological holdout helps test performance on later observations.

### Q19. What do MAE and RMSE measure?
Mean Absolute Error is the average absolute difference between predictions and actual values. Root Mean Squared Error is the square root of mean squared error and penalises large errors more heavily.

### Q20. Why is the machine-learning model not production-ready?
There are only 43 Instagram feed records, the target is highly skewed, and the available pre-publication features are limited to content type and calendar fields. More historical posts and creative metadata would be needed for a meaningful predictive model.

### Q21. Why shouldn't Instagram and YouTube views simply be added together?
The source metrics have different platform definitions, scopes and date windows. Instagram post-level sums, Instagram account-level IG+FB aggregates and YouTube channel totals are not identical measurement units.

### Q22. What is the main data-quality issue?
Several audit summaries do not reconcile exactly. For example, the YouTube format view totals are 58 below the reported channel total, and the listed traffic sources are 243 below the channel total. The project records these as unresolved instead of allocating the difference without evidence.

### Q23. What would you improve next?
Obtain complete official exports from both platforms, especially full YouTube video-level data, daily series and retention data. Then add a stable metric-fact model, more robust topic labels, and richer pre-publication features for modelling.

## 3. Live demonstration sequence

1. Start the Streamlit application.
2. Open Executive Overview and explain why platform totals have different scopes.
3. Open Content Explorer and filter Instagram Reels.
4. Sort by views and inspect the October 5 viral Reel.
5. Open Instagram Trends and explain the IG+FB scope of the daily series.
6. Open Traffic & Formats and point out the unresolved YouTube source total difference.
7. Open EDA and explain the skewed distribution and outlier effect.
8. Open Forecasting Lab and explain the trailing-mean baseline and limitations.
9. Open NLP Topic Intelligence and explain TF-IDF and K-Means.
10. Open Data Quality & Coverage and explain how inconsistencies are preserved.

## 4. Things not to claim

- Do not say the prototype is connected to live Instagram or YouTube APIs.
- Do not say the 11 YouTube content rows represent every channel upload.
- Do not call the sum of per-post reach unique account reach.
- Do not claim the experimental model reliably predicts viral performance.
- Do not present TF-IDF clusters as verified news categories.
- Do not claim causation from correlations.
- Do not state that unavailable retention or demographic metrics were analysed.
