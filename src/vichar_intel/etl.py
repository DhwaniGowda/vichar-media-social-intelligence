"""Simple, reproducible ETL: CSV staging -> validated SQLite tables."""
from pathlib import Path
import sqlite3
import pandas as pd
from .data_loader import load_all
from .config import DB_PATH

TABLES = {
    "content": "content", "stories": "stories", "daily_metrics": "daily_metrics",
    "traffic_sources": "traffic_sources", "format_summary": "format_summary",
    "platform_summary": "platform_summary", "audience_activity": "audience_activity",
    "data_quality_issues": "data_quality_issues"
}

def build_database(db_path: Path | str = DB_PATH) -> Path:
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    frames = load_all()
    with sqlite3.connect(db_path) as con:
        for key, table in TABLES.items():
            frames[key].to_sql(table, con, if_exists="replace", index=False)
        con.execute("CREATE INDEX IF NOT EXISTS idx_content_platform ON content(platform)")
        con.execute("CREATE INDEX IF NOT EXISTS idx_content_type ON content(content_type)")
        con.execute("CREATE INDEX IF NOT EXISTS idx_daily_date ON daily_metrics(date)")
        con.commit()
    return db_path
