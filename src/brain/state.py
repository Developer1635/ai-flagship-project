from typing import List, Dict, Any, Optional, Annotated
from typing_extensions import TypedDict
import operator

class CognitiveState(TypedDict):
    user_input: str
    messages: Annotated[List[Dict[str, str]], operator.add]
    detected_emotion: str
    urgency_level: int
    requires_grounding: bool
    confidence_score: float
    grounded_context: Optional[str]
    user_profile: Dict[str, Any]
    retrieved_memories: List[str]
    pending_tool_calls: List[Dict[str, Any]]
    final_response: str
