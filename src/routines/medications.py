import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "secure_vault.db"

def init_medication_tables():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS medication_regimen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medication_name TEXT NOT NULL,
            dosage TEXT NOT NULL,
            scheduled_time TEXT NOT NULL, -- Format: HH:MM
            criticality_level INTEGER DEFAULT 1
        );
        """)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS medication_intake_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medication_name TEXT NOT NULL,
            scheduled_for TIMESTAMP NOT NULL,
            confirmed_at TIMESTAMP,
            status TEXT DEFAULT 'PENDING' -- PENDING, CONFIRMED, MISSED, ESCALATED
        );
        """)
        conn.commit()

class MedicationManager:
    def __init__(self):
        init_medication_tables()

    def add_regimen(self, medication: str, dosage: str, scheduled_time: str, criticality: int = 1):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO medication_regimen (medication_name, dosage, scheduled_time, criticality_level) VALUES (?, ?, ?, ?)",
                (medication, dosage, scheduled_time, criticality)
            )
            conn.commit()

    def prompt_medication_alert(self, medication: str, dosage: str) -> str:
        return f"Arthur, it is time for your {dosage} of {medication}. Please confirm once you have taken it."

    def confirm_intake(self, medication: str) -> bool:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute(
                """
                UPDATE medication_intake_log 
                SET status = 'CONFIRMED', confirmed_at = CURRENT_TIMESTAMP 
                WHERE medication_name = ? AND status = 'PENDING'
                """,
                (medication,)
            )
            conn.commit()
            return cursor.rowcount > 0

    def get_pending_alerts(self) -> List[Dict[str, str]]:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute("SELECT medication_name, scheduled_time FROM medication_regimen")
            return [{"medication": r[0], "time": r[1]} for r in cursor.fetchall()]