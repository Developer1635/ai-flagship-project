import re
from typing import Dict, Any, List
from src.memory.profile import ProfileStore
from src.memory.graph_store import GraphStore

class MemoryExtractor:
    def __init__(self):
        self.profile = ProfileStore()
        self.graph = GraphStore()

    def extract_and_persist(self, user_text: str):
        """Parses user input for core identity markers, preferences, and relationships."""
        text = user_text.strip()

        # Extract name
        name_match = re.search(r"\bmy name is ([A-Za-z]+)\b", text, re.IGNORECASE)
        if name_match:
            self.profile.set_fact("user_name", name_match.group(1).capitalize())

        # Extract favorite items
        fav_match = re.search(r"\bmy favorite (\w+) is ([A-Za-z\s]+?)(?:\.|$)", text, re.IGNORECASE)
        if fav_match:
            key = f"favorite_{fav_match.group(1).lower().strip()}"
            val = fav_match.group(2).strip()
            self.profile.set_fact(key, val)

        # Extract relational triplets (e.g., "Eleanor is my daughter")
        relation_match = re.search(r"\b([A-Za-z]+) is my (daughter|son|doctor|nurse|neighbor|friend|wife|husband)\b", text, re.IGNORECASE)
        if relation_match:
            entity_name = relation_match.group(1).capitalize()
            relation_role = f"has_{relation_match.group(2).lower()}"
            user_name = self.profile.get_fact("user_name") or "User"
            self.graph.add_relation(user_name, relation_role, entity_name)