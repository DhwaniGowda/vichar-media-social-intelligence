from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "processed"
DB_DIR = ROOT / "database"
DB_PATH = DB_DIR / "vichar_media_intelligence.db"
