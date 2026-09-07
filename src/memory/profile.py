import sqlite3
from pathlib import Path
from typing import Dict, Any, Optional

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "secure_vault.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def init_memory_vault():
    """Initializes the relational user profile and knowledge schema."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # User profile matrix (Preferences, names, habits)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            confidence_score REAL DEFAULT 1.0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        # Relational knowledge graph
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS relational_graph (
            subject TEXT NOT NULL,
            predicate TEXT NOT NULL,
            object TEXT NOT NULL,
            temporal_anchor TEXT,
            PRIMARY KEY (subject, predicate, object)
        );
        """)
        
        # Episodic conversation history
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS episodic_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_utterance TEXT NOT NULL,
            assistant_reply TEXT NOT NULL,
            detected_mood TEXT
        );
        """)
        conn.commit()

class ProfileStore:
    def __init__(self):
        init_memory_vault()

    def set_fact(self, key: str, value: str, confidence: float = 1.0):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO user_profile (key, value, confidence_score, last_updated) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
                (key, value, confidence)
            )
            conn.commit()

    def get_fact(self, key: str) -> Optional[str]:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute("SELECT value FROM user_profile WHERE key = ?", (key,))
            row = cursor.fetchone()
            return row[0] if row else None

    def get_all_facts(self) -> Dict[str, str]:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute("SELECT key, value FROM user_profile")
            return {row[0]: row[1] for row in cursor.fetchall()}