import pandas as pd
import numpy as np

def generate_flags(content: pd.DataFrame) -> pd.DataFrame:
    df=content[(content.platform=="Instagram") & (content.content_type.isin(["Reel","Carousel"]))].copy()
    df["engagement_rate_reach_pct"]=np.where(df.reach>0,df.interactions/df.reach*100,np.nan)
    df["share_rate_reach_pct"]=np.where(df.reach>0,df.shares/df.reach*100,np.nan)
    df["save_rate_reach_pct"]=np.where(df.reach>0,df.saves/df.reach*100,np.nan)
    # Relative flags use this small sample's medians; they are descriptive, not universal benchmarks.
    med_views=float(df.views.median()); med_eng=float(df.engagement_rate_reach_pct.median())
    med_share=float(df.share_rate_reach_pct.median())
    flags=[]
    for _,r in df.iterrows():
        reasons=[]
        if r.views>=med_views*2 and pd.notna(r.engagement_rate_reach_pct) and r.engagement_rate_reach_pct<med_eng:
            reasons.append("High views relative to sample but below-median engagement per reach")
        if pd.notna(r.share_rate_reach_pct) and r.share_rate_reach_pct>=med_share*2:
            reasons.append("Share rate is at least twice the sample median")
        if pd.notna(r.follows_or_subs_net) and r.follows_or_subs_net>=5:
            reasons.append("Generated at least 5 follows (as reported)")
        if reasons:
            flags.append({"content_id":r.content_id,"date":r.publish_date,"format":r.content_type,"topic":r.title_or_topic,
                          "views":r.views,"reach":r.reach,"engagement_rate_reach_pct":r.engagement_rate_reach_pct,
                          "share_rate_reach_pct":r.share_rate_reach_pct,"reported_follows":r.follows_or_subs_net,
                          "decision_support_flag":"; ".join(reasons)})
    return pd.DataFrame(flags)
