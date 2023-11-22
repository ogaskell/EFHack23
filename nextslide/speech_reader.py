"""Will contain classes to read speech from the mic, and output it as a series of timestamped strings."""

from abc import ABC, abstractmethod
from typing import Generator
from psec.secrets_environment import SecretsEnvironment
from pvrecorder import PvRecorder

import pvcheetah as pvc


class BaseSpeechReader(ABC):
    """Abstract base speech reader class"""

    @abstractmethod
    def generate_tokens(self) -> Generator[str, None, None]:
        """Generate tokens from speech and yeild them."""
        pass


class PicoVoiceSpeechReader(BaseSpeechReader):
    """Speech Reader using Picovoice Cheetah."""

    def __init__(self, device_id: int = 0):
        key = SecretsEnvironment().read_secrets().get_secret("picovoice-key")

        self.rec = PvRecorder(frame_length=512, device_index=device_id)
        self.handle = pvc.create(key)

    def generate_tokens(self) -> Generator[str, None, None]:
        """Generate tokens from speech and yeild them."""
        self.rec.start()

        try:
            while self.rec.is_recording:
                partial_transcript, is_endpoint = self.handle.process(self.rec.read())

                for word in partial_transcript.strip().split(" "):
                    if formatted_word := word.strip().lower():
                        yield formatted_word

                if is_endpoint:
                    self.rec.stop()

        except BaseException as e:
            self.rec.stop()
            raise e
