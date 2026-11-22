from pathlib import Path
import sys
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from vichar_intel.data_loader import load_all
from vichar_intel.analytics import content_kpis, enrich_content
from vichar_intel.forecasting import forecast_daily_metric
from vichar_intel.nlp import cluster_content_topics
from vichar_intel.modeling import run_content_model
from vichar_intel.recommendations import generate_flags
from vichar_intel.validation import run_validation

st.set_page_config(page_title="Vichar Media | Social Intelligence",page_icon="📊",layout="wide")
st.title("Vichar Media — Social Media Intelligence Platform")
st.caption("Instagram + YouTube analytics | Supplied audit data | 2026")

@st.cache_data
def get_data(): return load_all()
d=get_data(); content=enrich_content(d["content"])

with st.sidebar:
    st.header("Navigation")
    page=st.radio("Select module",["Executive Overview","Content Explorer","Instagram Trends","Traffic & Formats","Stories Analytics","Exploratory Data Analysis","Forecasting Lab","NLP Topic Intelligence","ML Experiment","Decision Support","Data Quality & Coverage"])
    st.divider()
    st.caption("Dataset scope")
    st.write("Instagram: 43 feed posts, 32 archived Stories, 27 daily rows supplied.")
    st.write("YouTube: lifetime aggregate + 11-row top-content shortlist.")
    st.caption("Some source values are snapshots, rolling windows or cross-posted aggregates. Read notes before comparing.")

if page=="Executive Overview":
    st.subheader("Channel performance at a glance")
    yt=d["platform_summary"]; ig=yt[yt.platform.eq("Instagram")]; y=yt[yt.platform.eq("YouTube")]
    def val(df,metric,period=None):
        q=df[df.metric.eq(metric)]
        if period: q=q[q.reporting_period.eq(period)]
        return q.iloc[-1].value if not q.empty else "N/A"
    c1,c2,c3,c4=st.columns(4)
    c1.metric("Instagram post-level views",f"{int(val(ig,'Post-level lifetime views')):,}")
    c2.metric("Instagram followers (insights snapshot)",f"{int(val(ig,'Followers account insights snapshot')):,}")
    c3.metric("YouTube lifetime views",f"{int(val(y,'Lifetime views')):,}")
    c4.metric("YouTube subscribers",f"{int(val(y,'Subscribers')):,}")
    c5,c6,c7,c8=st.columns(4)
    c5.metric("Instagram feed interactions",f"{int(val(ig,'Interactions')):,}")
    c6.metric("YouTube watch time",f"{float(val(y,'Watch time hours')):.2f} h")
    c7.metric("Instagram feed assets",int((content.platform=="Instagram").sum()))
    c8.metric("YouTube sampled top content",int((content.platform=="YouTube").sum()))
    st.warning("Cross-platform totals are not directly additive: post-level Instagram views, Instagram account-level rolling IG+FB views, and YouTube lifetime views have different scopes.")
    col1,col2=st.columns(2)
    with col1:
        st.markdown("#### Instagram feed format mix")
        igf=d["format_summary"].query("platform == 'Instagram'")
        st.plotly_chart(px.bar(igf,x="content_format",y="views",title="Instagram post-level views by format"),use_container_width=True)
    with col2:
        st.markdown("#### YouTube format mix as reported")
        ytf=d["format_summary"].query("platform == 'YouTube'")
        st.plotly_chart(px.bar(ytf,x="content_format",y="views",title="YouTube lifetime views by format (reported)"),use_container_width=True)
    st.markdown("#### Data coverage")
    st.dataframe(pd.DataFrame([
      ["Instagram feed content",43,"Reported complete post-level fetch"],["Instagram archived Stories",32,"Reported complete Story archive fetch"],
      ["Instagram daily metrics",len(d['daily_metrics']),"28 rows supplied; report window label mentions Nov 20 but table ends Nov 19"],
      ["YouTube video records",len(content[content.platform.eq('YouTube')]),"Top-content shortlist only; not full upload inventory"]
    ],columns=["Dataset","Rows","Coverage note"]),use_container_width=True,hide_index=True)

elif page=="Content Explorer":
    st.subheader("Individual content performance")
    p=st.selectbox("Platform",["All","Instagram","YouTube"])
    df=content.copy()
    if p!="All": df=df[df.platform.eq(p)]
    types=sorted(df.content_type.dropna().unique().tolist())
    selected=st.multiselect("Content format",types,default=types)
    if selected: df=df[df.content_type.isin(selected)]
    search=st.text_input("Search title / topic")
    if search: df=df[df.title_or_topic.str.contains(search,case=False,na=False)]
    sort=st.selectbox("Sort by",["views","watch_time_seconds","likes","interactions","reach"],index=0)
    if sort in df: df=df.sort_values(sort,ascending=False,na_position="last")
    cols=[c for c in ["platform","content_id","content_type","publish_date","title_or_topic","views","reach","impressions","likes","comments","shares","saves","reposts","interactions","follows_or_subs_net","watch_time_seconds","avg_watch_time_seconds","skip_rate_pct","engagement_per_reach_pct","engagement_per_view_pct","data_completeness","notes"] if c in df.columns]
    st.dataframe(df[cols],use_container_width=True,hide_index=True,height=560)
    st.caption("Instagram rows contain the supplied 43 feed records. YouTube rows are only 11 top-content records. Missing values remain blank rather than being treated as zero.")
    st.download_button("Download filtered content CSV",df.to_csv(index=False).encode(),file_name="vichar_content_filtered.csv",mime="text/csv")

elif page=="Instagram Trends":
    st.subheader("Instagram account daily series")
    daily=d["daily_metrics"].copy();daily["date"]=pd.to_datetime(daily.date)
    metric=st.selectbox("Metric",["views","accounts_reached","interactions","profile_visits","net_follower_change"])
    st.plotly_chart(px.line(daily,x="date",y=metric,markers=True,title=f"Daily {metric.replace('_',' ').title()}"),use_container_width=True)
    st.dataframe(daily,use_container_width=True,hide_index=True)
    st.info("The source defines daily Views as aggregated Instagram + Facebook cross-posted account views. These are not Instagram-only post-level totals. The source describes a 28-day range but supplies 27 dates (Oct 23–Nov 19, 2026).")
    windows=d["platform_summary"].query("platform == 'Instagram' and reporting_period in ['Last 7 days','Last 14 days','Last 28 days','Last 90 days']")
    st.markdown("#### Account-level rolling windows")
    st.dataframe(windows,use_container_width=True,hide_index=True)

elif page=="Traffic & Formats":
    st.subheader("YouTube discovery sources")
    t=d["traffic_sources"].copy();t["share_of_listed_views_pct"]=t.views/t.views.sum()*100
    st.plotly_chart(px.bar(t.sort_values("views",ascending=True),x="views",y="traffic_source",orientation="h",title="Listed YouTube lifetime views by traffic source"),use_container_width=True)
    st.dataframe(t,use_container_width=True,hide_index=True)
    st.warning(f"Listed traffic-source views sum to {int(t.views.sum()):,}, which is {144167-int(t.views.sum()):,} below the reported channel lifetime total of 144,167. The unexplained remainder has not been allocated.")
    st.markdown("#### Format summaries")
    st.dataframe(d["format_summary"],use_container_width=True,hide_index=True)
    st.info("Instagram Reels watch time is summed from per-post fields and is not directly comparable to YouTube watch time. Instagram carousel watch time is unavailable.")

elif page=="Stories Analytics":
    st.subheader("Instagram archived Stories")
    s=d["stories"].copy();s["publish_date"]=pd.to_datetime(s.publish_date)
    a,b,c=st.columns(3);a.metric("Archived Stories in dataset",len(s));b.metric("Story views",f"{int(s.views.sum()):,}");c.metric("Story reach (summed per Story)",f"{int(s.reach.sum()):,}")
    st.plotly_chart(px.bar(s.sort_values("views",ascending=False).head(15),x="story_id",y="views",title="Top 15 archived Stories by views"),use_container_width=True)
    st.dataframe(s.sort_values("publish_date",ascending=False),use_container_width=True,hide_index=True)
    st.info("Navigation is an aggregate in the source. Individual forward, back, exit, reply, sticker and completion metrics were not supplied.")

elif page=="Exploratory Data Analysis":
    st.subheader("Exploratory Data Analysis")
    ig=content[(content.platform=="Instagram") & content.content_type.isin(["Reel","Carousel"])].copy()
    x=st.selectbox("Content metric for distribution",["views","reach","likes","shares","saves","interactions"])
    st.plotly_chart(px.histogram(ig,x=x,nbins=20,title=f"Instagram {x} distribution (includes viral outliers)"),use_container_width=True)
    st.plotly_chart(px.scatter(ig,x="reach",y="interactions",color="content_type",size="views",hover_name="title_or_topic",title="Reach vs interactions"),use_container_width=True)
    corr=ig[["views","reach","impressions","likes","comments","shares","saves","reposts","interactions"]].corr(numeric_only=True)
    st.plotly_chart(px.imshow(corr,text_auto=".2f",aspect="auto",title="Metric correlation matrix"),use_container_width=True)
    st.write("Median views:",f"{ig.views.median():,.0f}","| Mean views:",f"{ig.views.mean():,.0f}")
    st.caption("These are descriptive associations from a small, skewed sample. Correlation is not evidence of causation. The very high-view October 5 Reel strongly affects mean-based statistics.")

elif page=="Forecasting Lab":
    st.subheader("Time-series baseline experiment")
    daily=d["daily_metrics"].copy()
    metric=st.selectbox("Daily metric",["views","accounts_reached","interactions","profile_visits","net_follower_change"])
    result=forecast_daily_metric(daily,metric,horizon=7)
    if result["status"]!="experimental_baseline": st.warning(result["message"])
    else:
        a,b,c=st.columns(3);a.metric("Holdout MAE",f"{result['mae']:,.1f}");b.metric("Holdout RMSE",f"{result['rmse']:,.1f}");c.metric("Holdout rows",result["holdout_size"])
        hist=daily.copy();hist["date"]=pd.to_datetime(hist.date)
        plot=pd.concat([hist[["date",metric]].rename(columns={metric:"value"}),result["forecast"].rename(columns={"forecast":"value"})],ignore_index=True)
        plot["series"]=["Observed"]*len(hist)+["7-day mean baseline"]*len(result["forecast"])
        st.plotly_chart(px.line(plot,x="date",y="value",color="series",markers=True,title=f"Experimental {metric} baseline"),use_container_width=True)
        st.info(result["message"])

elif page=="NLP Topic Intelligence":
    st.subheader("Exploratory topic clustering")
    n=st.slider("Number of clusters",2,8,4)
    try:
        clustered=cluster_content_topics(content,n)
        st.dataframe(clustered.sort_values(["topic_cluster","platform"]),use_container_width=True,hide_index=True)
        counts=clustered.groupby(["platform","topic_cluster"]).size().reset_index(name="records")
        st.plotly_chart(px.bar(counts,x="topic_cluster",y="records",color="platform",barmode="group",title="Records per text cluster"),use_container_width=True)
        st.caption("These clusters are machine-generated groupings of supplied title/topic labels. Instagram text is a paraphrase, not original captions. Clusters are exploratory and need human interpretation; they are not verified editorial categories.")
    except Exception as e: st.error(str(e))

elif page=="ML Experiment":
    st.subheader("Content views modelling feasibility")
    result=run_content_model(content)
    st.info(result["message"])
    if "results" in result:
        st.write(f"Training population: {result['n_rows']} Instagram feed records.")
        st.dataframe(result["results"],use_container_width=True,hide_index=True)
        st.warning("Exploratory chronological holdout only. The available pre-publication fields are limited to content format and publication calendar fields; the model is not production-ready and should not guide editorial decisions.")
    else: st.warning(result["status"])

elif page=="Decision Support":
    st.subheader("Evidence-based content flags")
    flags=generate_flags(content)
    if flags.empty: st.write("No content met the sample-relative flag conditions.")
    else: st.dataframe(flags,use_container_width=True,hide_index=True)
    st.caption("Flags use this small dataset's own medians as reference points. They are prioritisation prompts, not causal explanations or universal benchmarks.")

elif page=="Data Quality & Coverage":
    st.subheader("Audit checks")
    checks=pd.DataFrame(run_validation())
    st.dataframe(checks,use_container_width=True,hide_index=True)
    st.markdown("#### Recorded source issues")
    st.dataframe(d["data_quality_issues"],use_container_width=True,hide_index=True)
    st.markdown("#### Dataset coverage notes")
    st.write("- Instagram: 43 feed posts are reported complete within the fetched date scope; 32 archived Stories are reported complete.")
    st.write("- YouTube: 11 top-content records only. The full upload inventory is not included.")
    st.write("- No audience demographics, detailed retention curves, or full platform daily history were included in the supplied audits.")
    st.write("- Conflicting totals are retained as source-reported values and flagged rather than silently reconciled.")

st.divider()
st.caption("Vichar Media Social Intelligence Platform · Portfolio/research prototype · Source data: supplied Instagram and YouTube audit summaries · Not an official Meta or YouTube integration.")
