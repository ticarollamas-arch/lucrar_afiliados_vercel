import sqlite3
from config import DB_PATH

SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS products (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT NOT NULL,
 category TEXT NOT NULL,
 original_url TEXT NOT NULL,
 affiliate_url TEXT NOT NULL,
 platform TEXT NOT NULL,
 keywords TEXT NOT NULL,
 campaign_id TEXT NOT NULL UNIQUE,
 created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE TABLE IF NOT EXISTS clicks (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
 campaign_id TEXT NOT NULL,
 source TEXT,
 referrer TEXT,
 destination TEXT NOT NULL,
 reference_id TEXT NOT NULL UNIQUE,
 clicked_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now'))
);
CREATE TABLE IF NOT EXISTS conversions (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 platform TEXT NOT NULL,
 external_order_id TEXT NOT NULL,
 campaign_id TEXT,
 product_id INTEGER REFERENCES products(id) ON DELETE SET NULL,
 amount REAL,
 commission REAL,
 converted_at TEXT,
 imported_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
 UNIQUE(platform, external_order_id)
);
"""
def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys=ON")
    return con

def init_db():
    with connect() as con:
        con.executescript(SCHEMA)
