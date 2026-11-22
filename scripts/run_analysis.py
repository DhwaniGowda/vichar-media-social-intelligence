from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from vichar_intel.data_loader import load_all
from vichar_intel.validation import run_validation
from vichar_intel.analytics import content_kpis
from vichar_intel.forecasting import forecast_daily_metric
from vichar_intel.nlp import cluster_content_topics
from vichar_intel.modeling import run_content_model
from vichar_intel.recommendations import generate_flags

d=load_all(); c=d["content"]
print("\nDATASET KPIs:", content_kpis(c))
print("\nVALIDATION:")
for x in run_validation(): print(x)
print("\nFORECAST:", forecast_daily_metric(d["daily_metrics"], "views")["message"])
print("\nNLP topic clusters (exploratory):")
print(cluster_content_topics(c).head(12).to_string(index=False))
print("\nML feasibility:", run_content_model(c)["message"])
print("\nDECISION FLAGS:")
print(generate_flags(c).head(15).to_string(index=False))
