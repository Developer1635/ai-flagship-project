import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "secure_vault.db"

class EpisodicMemory:
    def __init__(self):
        self.db_path = DB_PATH

    def record_turn(self, user_text: str, assistant_text: str, detected_mood: str = "neutral") -> int:
        """Logs a single conversation turn into episodic storage."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO episodic_logs (user_utterance, assistant_reply, detected_mood)
                VALUES (?, ?, ?)
                """,
                (user_text.strip(), assistant_text.strip(), detected_mood)
            )
            conn.commit()
            return cursor.lastrowid

    def get_recent_history(self, limit: int = 5) -> List[Dict[str, str]]:
        """Retrieves the most recent N interactions for short-term working context."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT user_utterance, assistant_reply, detected_mood, timestamp
                FROM episodic_logs
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,)
            )
            rows = cursor.fetchall()
            # Reverse so the dialogue is chronological
            return [
                {
                    "user": r[0],
                    "assistant": r[1],
                    "mood": r[2],
                    "timestamp": r[3]
                }
                for r in reversed(rows)
            ]

    def format_recent_dialogue_context(self, limit: int = 3) -> str:
        """Formats the last interactions into dialogue context for prompt injection."""
        history = self.get_recent_history(limit=limit)
        if not history:
            return ""
        dialogue_lines = []
        for turn in history:
            dialogue_lines.append(f"Elder: {turn['user']}\nJARVIS: {turn['assistant']}")
        return "\n".join(dialogue_lines)