import sqlite3
from pathlib import Path
from typing import List, Dict, Tuple, Optional

DB_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "secure_vault.db"

class GraphStore:
    def __init__(self):
        self.db_path = DB_PATH

    def add_relation(self, subject: str, predicate: str, obj: str, temporal_anchor: Optional[str] = None):
        """Inserts or updates an entity relation triplet."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO relational_graph (subject, predicate, object, temporal_anchor)
                VALUES (?, ?, ?, ?)
                """,
                (subject.strip(), predicate.strip(), obj.strip(), temporal_anchor)
            )
            conn.commit()

    def get_relations_for_entity(self, entity: str) -> List[Dict[str, str]]:
        """Finds all relations where the entity is the subject or object."""
        entity_clean = entity.strip()
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT subject, predicate, object, temporal_anchor 
                FROM relational_graph 
                WHERE subject = ? OR object = ?
                """,
                (entity_clean, entity_clean)
            )
            rows = cursor.fetchall()
            return [
                {
                    "subject": r[0],
                    "predicate": r[1],
                    "object": r[2],
                    "temporal_anchor": r[3] or ""
                }
                for r in rows
            ]

    def format_context_string(self, entity: str) -> str:
        """Formats entity graph triplets into a compact natural language string for prompt injection."""
        relations = self.get_relations_for_entity(entity)
        if not relations:
            return ""
        lines = []
        for r in relations:
            anchor = f" ({r['temporal_anchor']})" if r['temporal_anchor'] else ""
            lines.append(f"- {r['subject']} {r['predicate']} {r['object']}{anchor}.")
        return "\n".join(lines)