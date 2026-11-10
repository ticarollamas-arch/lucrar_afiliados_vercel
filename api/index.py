"""Entrada HTTP para Vercel. Expõe o Flask como função serverless."""
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Em Vercel, SQLite fica apenas em /tmp e NÃO é armazenamento persistente.
os.environ.setdefault("LUCRAR_DB", "/tmp/lucrar.sqlite3")

from database import init_db
from redirect_engine import create_app

init_db()
app = create_app()

@app.get("/")
def home():
    return {
        "app": "LUCRAR.PY",
        "status": "online",
        "health": "/health",
        "redirect_example": "/r/SEU_ID_DE_CAMPANHA?q=nome-do-produto",
        "notice": "Configure armazenamento persistente antes de usar em produção."
    }
