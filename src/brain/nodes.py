import re
from typing import Dict, Any
from src.brain.state import CognitiveState

def classify_input_node(state: CognitiveState) -> Dict[str, Any]:
    text = state['user_input'].lower()
    
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
    context = state.get('grounded_context', '')
    user_msg = state['user_input']
    
    if context:
        final_text = f'{context.strip()} You mentioned: "{user_msg}". I am actively processing this with you.'
    else:
        final_text = f'Understood. I am attentive and noting every detail regarding "{user_msg}".'
        
    return {
        'final_response': final_text,
        'messages': [{'role': 'assistant', 'content': final_text}]
    }