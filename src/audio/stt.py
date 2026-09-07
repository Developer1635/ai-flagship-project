import io
import numpy as np
from faster_whisper import WhisperModel

class SpeechToTextEngine:
    def __init__(self, model_size: str = "base.en", device: str = "cpu", compute_type: str = "int8"):
        """
        Uses quantized local Whisper for rapid turnaround.
        'base.en' provides sub-250ms transcription on local CPU/GPU.
        """
        print(f"[STT Engine] Loading Whisper ({model_size}) on {device}...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)

    def transcribe_audio_buffer(self, audio_data: np.ndarray, sample_rate: int = 16000) -> str:
        """Transcribes normalized float32 or int16 numpy audio buffers."""
        if audio_data.dtype == np.int16:
            audio_data = audio_data.astype(np.float32) / 32768.0

        segments, _ = self.model.transcribe(
            audio_data,
            beam_size=1,
            language="en",
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )

        transcript = " ".join([segment.text for segment in segments]).strip()
        return transcript