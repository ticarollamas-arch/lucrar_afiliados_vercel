from pathlib import Path
import os

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
EXPORT_DIR = ROOT / "exports"
DB_PATH = Path(os.environ.get("LUCRAR_DB", DATA_DIR / "lucrar.sqlite3"))
MATCH_THRESHOLD = float(os.environ.get("LUCRAR_MATCH_THRESHOLD", "0.68"))
MAX_QUERY_LENGTH = 500
