import os
import datetime
import requests
import warnings
warnings.filterwarnings("ignore")

from duckduckgo_search import DDGS
from llama_cpp import Llama

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "Qwen2.5-7B-Instruct-Q4_K_M.gguf"
)

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Could not find model file at: {MODEL_PATH}")

print("\n[System]: Loading 3B Local LLM Engine...")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,
    n_threads=4,
    verbose=False
)

print("[System]: 3B Engine Ready.")

chat_history = []
MAX_HISTORY = 6

def search_web(query):
    """Fetches fast web snippets with fallback parsing."""
    try:
        if "weather" in query.lower():
            # Dedicated lightweight weather fetcher
            city = "Mumbai"
            words = query.lower().split()
            if "in" in words:
                idx = words.index("in") + 1
                if idx < len(words):
                    city = words[idx].strip("?.,")
            res = requests.get(f"https://wttr.in/{city}?format=3", timeout=3)
            if res.status_code == 200:
                return f"Weather for {city}: {res.text.strip()}"

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            if results:
                snippets = [f"{r.get('title', '')}: {r.get('body', '')}" for r in results if r.get('body')]
                return "\n".join(snippets)
    except Exception as e:
        print(f"[Search Warning]: {e}")
    return ""

def process_user_request(user_input):
    global chat_history
    clean_input = user_input.lower().strip()
    today_str = datetime.date.today().strftime("%B %d, %Y")

    if "time" in clean_input and "what" in clean_input:
        return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}."
    if "date" in clean_input and "what" in clean_input:
        return f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}."

    web_context = ""
    personal_queries = ["my name", "who am i", "my age", "my detail", "remember"]
    search_keywords = ["who", "what", "where", "when", "why", "latest", "news", "price", "weather", "score", "today", "rain", "temperature"]

    is_personal = any(pq in clean_input for pq in personal_queries)
    needs_search = any(keyword in clean_input for keyword in search_keywords)

    if needs_search and not is_personal:
        print(f"[System]: Searching web for context...")
        web_context = search_web(user_input)

    system_prompt = (
        f"You are Stark, a direct AI voice assistant. Today is {today_str}.\n"
        "Guidelines:\n"
        "- Answer concisely in 1 direct sentence under 20 words.\n"
        "- Never write placeholder text like '[Insert data]'. If no data is available, answer from general knowledge."
    )

    if web_context:
        system_prompt += f"\n\nLive Web Data:\n{web_context}"

    prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n"

    for role, text in chat_history:
        prompt += f"<|im_start|>{role}\n{text}<|im_end|>\n"

    prompt += f"<|im_start|>user\n{user_input}<|im_end|>\n<|im_start|>assistant\n"

    output = llm(
        prompt,
        max_tokens=60,
        stop=["<|im_end|>", "\nUser:", "\nYou:", "["],
        temperature=0.2
    )

    response = output["choices"][0]["text"].strip()

    chat_history.append(("user", user_input))
    chat_history.append(("assistant", response))

    if len(chat_history) > MAX_HISTORY * 2:
        chat_history = chat_history[-(MAX_HISTORY * 2):]

    return response
