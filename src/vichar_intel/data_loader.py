from pathlib import Path
import pandas as pd

PROCESSED = Path(__file__).resolve().parents[2] / "data" / "processed"

def load_csv(name: str) -> pd.DataFrame:
    path = PROCESSED / name
    if not path.exists():
        raise FileNotFoundError(f"Missing data file: {path}")
    return pd.read_csv(path)

def load_all() -> dict[str, pd.DataFrame]:
    names = ["content.csv", "stories.csv", "daily_metrics.csv", "traffic_sources.csv", "format_summary.csv", "platform_summary.csv", "audience_activity.csv", "data_quality_issues.csv"]
    return {Path(n).stem: load_csv(n) for n in names}
