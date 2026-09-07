import os
import yaml
from pathlib import Path
from llama_cpp import Llama

# Locate configuration and weights
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = ROOT_DIR / "config" / "persona.yaml"
MODEL_PATH = ROOT_DIR / "models" / "Qwen2.5-7B-Instruct-Q4_K_M.gguf"

# Fallback to smaller model if 7B is not present in models/
if not MODEL_PATH.exists():
    fallback = ROOT_DIR / "models" / "qwen2.5-3b-instruct-q4_k_m.gguf"
    if fallback.exists():
        MODEL_PATH = fallback

# Load persona constraints
with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    persona_cfg = yaml.safe_load(f)

SYSTEM_PROMPT = f"""You are {persona_cfg['assistant']['name']}, a dedicated AI companion for seniors.
Demeanor: {' '.join(persona_cfg['assistant']['demeanor'])}
Rules:
- {persona_cfg['uncertainty_protocol']['strict_rule']}
- {persona_cfg['conversation_rules']['repetition_handling']}
- {persona_cfg['conversation_rules']['empathy_first']}
- {persona_cfg['conversation_rules']['pacing']}
Always deliver clear, articulate, and supportive spoken English without markdown formatting."""

print(f"[LLM Engine] Initializing model weights from: {MODEL_PATH.name}")
llm = Llama(
    model_path=str(MODEL_PATH),
    n_ctx=2048,
    n_gpu_layers=-1,  # Offloads layers to GPU if available; falls back to CPU cleanly
    verbose=False
)

def generate_local_response(user_input: str, contextual_prefix: str = "") -> str:
    user_content = f"{contextual_prefix}\nUser: {user_input}".strip() if contextual_prefix else user_input
    
    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content}
        ],
        temperature=0.7,
        max_tokens=150
    )
    return response["choices"][0]["message"]["content"].strip()