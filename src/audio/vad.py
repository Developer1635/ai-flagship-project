import webrtcvad
from typing import Callable, Optional

class VoiceActivityDetector:
    def __init__(self, aggressiveness: int = 2, sample_rate: int = 16000):
        """
        Aggressiveness modes:
        0: Normal, least aggressive on background noise filtering.
        1: Low bitrate.
        2: Aggressive (recommended for conversational appliances).
        3: Very aggressive (high filtering, potential to clip soft elder speech).
        """
        self.vad = webrtcvad.Vad(aggressiveness)
        self.sample_rate = sample_rate
        self.frame_duration_ms = 30  # 10, 20, or 30 ms supported
        self.frame_size = int(self.sample_rate * (self.frame_duration_ms / 1000.0) * 2)  # 16-bit PCM = 2 bytes/sample
        self.on_barge_in_callback: Optional[Callable[[], None]] = None

    def register_barge_in_handler(self, callback: Callable[[], None]):
        """Registers a callback function to abort audio playback upon voice detection."""
        self.on_barge_in_callback = callback

    def is_speech(self, pcm_frame: bytes, is_assistant_speaking: bool = False) -> bool:
        """Evaluates whether an audio chunk contains active speech."""
        if len(pcm_frame) != self.frame_size:
            return False

        speech_detected = self.vad.is_speech(pcm_frame, self.sample_rate)

        # Fire barge-in interruption if user begins speaking while assistant is playing audio
        if speech_detected and is_assistant_speaking and self.on_barge_in_callback:
            self.on_barge_in_callback()

        return speech_detected