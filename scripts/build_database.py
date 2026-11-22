from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from vichar_intel.etl import build_database
print(f"SQLite database created: {build_database()}")
