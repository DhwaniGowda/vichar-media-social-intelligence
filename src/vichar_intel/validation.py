"""Validation checks; findings are surfaced, not silently auto-corrected."""
from .data_loader import load_all

def run_validation() -> list[dict]:
    d = load_all()
    c, s, daily, fmt, traffic = d["content"], d["stories"], d["daily_metrics"], d["format_summary"], d["traffic_sources"]
    issues=[]
    ig=c[c.platform.eq("Instagram")]
    yt=c[c.platform.eq("YouTube")]
    issues.append({"check":"Instagram feed rows", "observed":int(len(ig)), "expected":43, "passed":len(ig)==43, "note":"35 Reels + 8 carousels in supplied audit."})
    issues.append({"check":"Instagram archived Stories", "observed":int(len(s)), "expected":32, "passed":len(s)==32, "note":"Source audit labels these records complete."})
    issues.append({"check":"Instagram daily-series row count", "observed":int(len(daily)), "expected":28, "passed":len(daily)==28, "note":"28 rows are present; date series ends Nov 19 although source window label says through Nov 20."})
    issues.append({"check":"YouTube top-content rows", "observed":int(len(yt)), "expected":"11 supplied shortlist rows", "passed":len(yt)==11, "note":"Shortlist only; not a complete channel inventory."})
    if not ig.empty:
        issues.append({"check":"Instagram post-level views sum", "observed":int(ig.views.sum()), "expected":891574, "passed":int(ig.views.sum())==891574, "note":"Sum of post-level views, not account-level rolling views."})
    return issues
