import numpy as np
import pandas as pd

def safe_divide(a, b):
    return np.where(pd.Series(b).astype(float).to_numpy()!=0, pd.Series(a).astype(float).to_numpy()/pd.Series(b).astype(float).to_numpy(), np.nan)

def content_kpis(content: pd.DataFrame) -> dict:
    ig = content[(content.platform=="Instagram") & (content.content_type.isin(["Reel","Carousel"]))]
    yt = content[content.platform=="YouTube"]
    return {
        "instagram_posts_in_dataset": int(len(ig)),
        "instagram_post_level_views": int(ig.views.sum()),
        "instagram_post_level_interactions_reported": int(ig.interactions.sum(skipna=True)),
        "youtube_top_content_rows": int(len(yt)),
        "youtube_top_content_views_only": int(yt.views.sum()),
        "youtube_top_content_watch_hours_only": float(yt.watch_time_seconds.sum(skipna=True)/3600),
    }

def enrich_content(content: pd.DataFrame) -> pd.DataFrame:
    df=content.copy()
    for col in ["views","reach","likes","comments","shares","saves","interactions","follows_or_subs_net"]:
        if col not in df: df[col]=np.nan
    df["engagement_per_reach_pct"] = np.where(df.reach>0, df.interactions/df.reach*100, np.nan)
    df["engagement_per_view_pct"] = np.where(df.views>0, df.interactions/df.views*100, np.nan)
    df["subscriber_or_follow_per_1000_views"] = np.where(df.views>0, df.follows_or_subs_net/df.views*1000, np.nan)
    return df
