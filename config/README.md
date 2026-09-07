# JARVIS: Autonomous Elderly Companion System

A market-ready, voice-first cognitive companion appliance designed for senior citizens, addressing social isolation and routine safety with unshakeable poise.

## Architectural Milestone Ledger

| Level | Component / File | System Role & Capability Explanation |
| :--- | :--- | :--- |
| **Level 1.1** | `src/brain/state.py` | Implements the core `CognitiveState` TypedDict contract tracking conversational context, emotional vectors, confidence ratings, and memory queries across the LangGraph state machine. |
| **Level 1.2** | `config/persona.yaml` | Enforces the JARVIS persona rules, anti-hesitation uncertainty protocols, empathetic validation parameters, and conversational pacing constraints. |
| **Level 1.3** | `.gitignore` | Restricts large binary checkpoints (`.gguf`, `.onnx`), local databases (`.db`), and virtual environments from leaking into source control. |