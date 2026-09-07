import threading
import pyttsx3
from typing import Optional

class TextToSpeechEngine:
    def __init__(self, rate: int = 155, volume: float = 0.95):
        self.rate = rate
        self.volume = volume
        self.is_speaking = False
        self._engine: Optional[pyttsx3.Engine] = None
        self._lock = threading.Lock()

    def _init_engine(self) -> pyttsx3.Engine:
        engine = pyttsx3.init()
        engine.setProperty("rate", self.rate)
        engine.setProperty("volume", self.volume)

        # Select calm, clear default voice
        voices = engine.getProperty("voices")
        for voice in voices:
            if "hazel" in voice.name.lower() or "zira" in voice.name.lower() or "david" in voice.name.lower():
                engine.setProperty("voice", voice.id)
                break
        return engine

    def stop(self):
        """Immediate barge-in cutoff handler to stop speech output."""
        with self._lock:
            if self.is_speaking and self._engine:
                try:
                    self._engine.stop()
                except Exception:
                    pass
                self.is_speaking = False

    def speak(self, text: str):
        """Synthesizes and outputs speech blocking until completion or barge-in."""
        if not text.strip():
            return

        with self._lock:
            self.is_speaking = True
            self._engine = self._init_engine()

        try:
            self._engine.say(text)
            self._engine.runAndWait()
        finally:
            with self._lock:
                self.is_speaking = False
                self._engine = None