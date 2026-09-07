from src.memory.profile import ProfileStore
from src.memory.graph_store import GraphStore
from src.memory.episodic import EpisodicMemory

class ContextBuilder:
    def __init__(self):
        self.profile = ProfileStore()
        self.graph = GraphStore()
        self.episodic = EpisodicMemory()

    def assemble_context(self, user_input: str) -> str:
        """Collects relevant memory, entity triplets, and dialogue history."""
        facts = self.profile.get_all_facts()
        user_name = facts.get("user_name", "the elder")

        context_sections = []

        # Known profile facts
        if facts:
            fact_lines = [f"- {k.replace('_', ' ').capitalize()}: {v}" for k, v in facts.items()]
            context_sections.append("User Profile:\n" + "\n".join(fact_lines))

        # Relational graph connections
        graph_relations = self.graph.format_context_string(user_name)
        if graph_relations:
            context_sections.append("Known Relationships:\n" + graph_relations)

        # Recent conversational turns
        recent_dialogue = self.episodic.format_recent_dialogue_context(limit=2)
        if recent_dialogue:
            context_sections.append("Recent Conversation Context:\n" + recent_dialogue)

        return "\n\n".join(context_sections)
        