"""Will contain classes to read speech from the mic, and output it as a series of timestamped strings."""
from abc import ABC, abstractmethod
from typing import AsyncGenerator, AsyncIterator
from asyncer import asyncify
from psec.secrets_environment import SecretsEnvironment
from pvrecorder import PvRecorder

import pvcheetah as pvc


class BaseSpeechReader(ABC):
    """Abstract base speech reader class"""

    @abstractmethod
    async def generate_tokens(self) -> AsyncGenerator[str, None]:
        """Generate tokens from speech and yeild them."""
        pass


class PicoVoiceSpeechReader(BaseSpeechReader):
    """Speech Reader using Picovoice Cheetah."""

    def __init__(self, device_id: int = 0):
        key = SecretsEnvironment(environment='nextslide').read_secrets().get_secret("picovoice-key")

        self.rec = PvRecorder(frame_length=512, device_index=device_id)
        self.handle = pvc.create(key)

    async def generate_tokens(self) -> AsyncIterator[str]:
        """Generate tokens from speech and yeild them."""
        self.rec.start()

        try:
            while self.rec.is_recording:
                recording = await asyncify(self.rec.read)()
                partial_transcript, is_endpoint = await asyncify(self.handle.process)(recording)
                print("got some words")

                for word in partial_transcript.strip().split(" "):
                    if formatted_word := word.strip().lower():
                        yield formatted_word

                if is_endpoint:
                    self.rec.stop()

        except BaseException as e:
            self.rec.stop()
            raise e
