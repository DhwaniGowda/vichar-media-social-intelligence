from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from vichar_intel.data_loader import load_all
from vichar_intel.validation import run_validation
from vichar_intel.analytics import content_kpis

def test_expected_dataset_sizes():
    d=load_all()
    assert len(d["content"].query("platform == 'Instagram'")) == 43
    assert len(d["stories"]) == 32
    assert len(d["content"].query("platform == 'YouTube'")) == 11

def test_instagram_post_views_sum():
    d=load_all()
    ig=d["content"].query("platform == 'Instagram'")
    assert int(ig.views.sum()) == 891574

def test_missing_values_are_not_filled_as_zero():
    d=load_all()
    yt=d["content"].query("platform == 'YouTube'")
    row=yt[yt.content_id.eq("YH8MUo3_FOs")].iloc[0]
    assert str(row.follows_or_subs_net) == "nan"

def test_validation_surfaces_daily_series_gap():
    checks={x["check"]:x for x in run_validation()}
    assert checks["Instagram daily-series row count"]["passed"] is True
    daily=load_all()["daily_metrics"]
    assert daily.date.max() == "2026-11-19"
