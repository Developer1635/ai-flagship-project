import time
import queue
import numpy as np
import sounddevice as sd
from typing import Optional, Generator
from src.audio.vad import VoiceActivityDetector

class AudioCaptureStream:
    def __init__(self, sample_rate: int = 16000, vad_aggressiveness: int = 2):
        self.sample_rate = sample_rate
        self.vad = VoiceActivityDetector(aggressiveness=vad_aggressiveness, sample_rate=sample_rate)
        self.audio_queue = queue.Queue()
        self.stream: Optional[sd.RawInputStream] = None
        self.is_assistant_speaking = False

    def _audio_callback(self, indata, frames, time_info, status):
        if status:
            pass
        self.audio_queue.put(bytes(indata))

    def start(self):
        """Opens low-latency 16kHz 16-bit mono input stream."""
        frame_size = self.vad.frame_size // 2  # Samples per frame (480 for 30ms @ 16kHz)
        self.stream = sd.RawInputStream(
            samplerate=self.sample_rate,
            blocksize=frame_size,
            dtype="int16",
            channels=1,
            callback=self._audio_callback
        )
        self.stream.start()

    def stop(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

    def listen_for_utterance(self, silence_threshold_sec: float = 1.2) -> Optional[np.ndarray]:
        """
        Collects audio frames until speech starts, then continues until
        silence duration indicates the user finished speaking.
        """
        speech_frames = []
        has_speech_started = False
        silence_start_time = None

        while True:
            try:
                frame = self.audio_queue.get(timeout=3.0)
            except queue.Empty:
                if has_speech_started:
                    break
                continue

            is_speech = self.vad.is_speech(frame, is_assistant_speaking=self.is_assistant_speaking)

            if is_speech:
                has_speech_started = True
                silence_start_time = None
                speech_frames.append(frame)
            elif has_speech_started:
                speech_frames.append(frame)
                if silence_start_time is None:
                    silence_start_time = time.time()
                elif time.time() - silence_start_time >= silence_threshold_sec:
                    break

        if not speech_frames:
            return None

        raw_pcm = b"".join(speech_frames)
        audio_np = np.frombuffer(raw_pcm, dtype=np.int16).astype(np.float32) / 32768.0
        return audio_np