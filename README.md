# JARVIS: Autonomous Elderly Companion System

A market-ready, voice-first cognitive companion appliance designed for senior citizens, addressing social isolation and routine safety with unshakeable poise.

## Architectural Milestone Ledger

| Level | Component / File | System Role & Capability Explanation |
| :--- | :--- | :--- |
| **Level 1.1** | src/brain/state.py | Implements the core CognitiveState TypedDict contract tracking conversational context, emotional vectors, confidence ratings, and memory queries across the LangGraph state machine. |
| **Level 1.2** | config/persona.yaml | Enforces the JARVIS persona rules, anti-hesitation uncertainty protocols, empathetic validation parameters, and conversational pacing constraints. |
| **Level 1.3** | .gitignore | Restricts large binary checkpoints (.gguf, .onnx), local databases (.db), and virtual environments from leaking into source control. |
| **Level 2.1** | src/brain/nodes.py | Houses the LangGraph decision nodes: user intent/emotion classification, elder empathy validation, anti-doubt uncertainty arbitration, and dignified response generation. |
| **Level 2.2** | src/brain/graph.py | Assembles the LangGraph DAG state machine; wires dynamic routing between classification, emotional validation, uncertainty arbitration, and output generation. |
| **Level 3.1** | src/brain/llm.py | Connects quantized Qwen2.5-7B via llama-cpp-python; offloads layers to local hardware and drives live response generation. |
| **Level 4.1** | src/memory/profile.py | Initializes SQLite vault; manages persistent key-value user profile and elder preferences. |
| **Level 4.2** | src/memory/graph_store.py | Maintains relational knowledge graph triplets (subject-predicate-object) for deterministic entity tracking. |
| **Level 4.3** | src/memory/episodic.py | Logs multi-turn conversation logs and emotional trajectories for chronological working memory retrieval. |
| **Level 4.4** | src/memory/extractor.py & src/brain/prompt_builder.py | Extracts identity markers and relations in real-time; dynamically injects multi-tier memory blocks into state prompts. |
