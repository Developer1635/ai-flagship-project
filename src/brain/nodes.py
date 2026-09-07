import re
from typing import Dict, Any
from src.brain.state import CognitiveState
from src.brain.llm import generate_local_response
from src.brain.prompt_builder import ContextBuilder
from src.memory.extractor import MemoryExtractor
from src.memory.episodic import EpisodicMemory

context_builder = ContextBuilder()
extractor = MemoryExtractor()
episodic_store = EpisodicMemory()

def classify_input_node(state: CognitiveState) -> Dict[str, Any]:
    text = state['user_input'].lower()

    # Background fact extraction
    extractor.extract_and_persist(state['user_input'])

    loneliness_cues = ['alone', 'lonely', 'nobody calls', 'miss my', 'bored', 'quiet house', 'rant']
    distress_cues = ['hurt', 'pain', 'fell', 'dizzy', 'scared', 'help me']
    query_cues = ['who', 'what', 'when', 'where', 'why', 'how', 'is it', 'does']

    if any(k in text for k in distress_cues):
        return {'detected_emotion': 'distress', 'urgency_level': 4, 'requires_grounding': False}
    elif any(k in text for k in loneliness_cues):
        return {'detected_emotion': 'lonely', 'urgency_level': 1, 'requires_grounding': False}
    elif any(k in text for k in query_cues):
        return {'detected_emotion': 'inquisitive', 'urgency_level': 1, 'requires_grounding': True}

    return {'detected_emotion': 'neutral', 'urgency_level': 0, 'requires_grounding': False}

def emotional_validation_node(state: CognitiveState) -> Dict[str, Any]:
    emotion = state.get('detected_emotion', 'neutral')
    if emotion == 'lonely':
        prefix = 'I am right here with you, and I have all the time in the world to listen. '
    elif emotion == 'distress':
        prefix = 'Please stay calm and remain still. I am attending to you immediately. '
    else:
        prefix = ''
    return {'grounded_context': prefix}

def uncertainty_arbiter_node(state: CognitiveState) -> Dict[str, Any]:
    score = state.get('confidence_score', 1.0)
    if score < 0.85 and state.get('requires_grounding', False):
        pivot = 'Allow me a moment to verify that detail with absolute precision.'
        return {'grounded_context': (state.get('grounded_context') or '') + ' ' + pivot}
    return {}

def response_synthesizer_node(state: CognitiveState) -> Dict[str, Any]:
    # Retrieve stored memory context
    retrieved_memory = context_builder.assemble_context(state['user_input'])

    emotional_prefix = state.get('grounded_context', '')
    combined_prefix = f"{emotional_prefix}\n{retrieved_memory}".strip() if emotional_prefix else retrieved_memory

    user_msg = state['user_input']
    final_text = generate_local_response(user_input=user_msg, contextual_prefix=combined_prefix)

    # Record this turn to persistent episodic logs
    episodic_store.record_turn(
        user_text=user_msg,
        assistant_text=final_text,
        detected_mood=state.get('detected_emotion', 'neutral')
    )

    return {
        'final_response': final_text,
        'messages': [{'role': 'assistant', 'content': final_text}],
        'retrieved_context': {'memory_dump': retrieved_memory}
    }