"""Exploratory NLP clustering of audit-provided titles/topic paraphrases."""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def cluster_content_topics(content: pd.DataFrame, n_clusters: int=4) -> pd.DataFrame:
    df=content[content.title_or_topic.fillna("").str.strip().ne("")].copy()
    if len(df)<4: raise ValueError("At least four non-empty content labels are required.")
    # Captions are not supplied; for Instagram, these are descriptive audit paraphrases.
    n_clusters=max(2,min(int(n_clusters),len(df)-1))
    vectorizer=TfidfVectorizer(stop_words="english",ngram_range=(1,2),max_features=400,min_df=1)
    X=vectorizer.fit_transform(df.title_or_topic.astype(str))
    model=KMeans(n_clusters=n_clusters,random_state=42,n_init=10)
    df["topic_cluster"]=model.fit_predict(X)
    return df[["platform","content_id","content_type","publish_date","title_or_topic","topic_cluster","views"]]
