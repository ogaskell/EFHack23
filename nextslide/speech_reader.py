"""Will contain classes to read speech from the mic, and output it as a series of timestamped strings."""
from abc import ABC, abstractmethod
import queue
import threading
from typing import AsyncGenerator, AsyncIterator, Generator
from asyncer import asyncify
from psec.secrets_environment import SecretsEnvironment
from pvrecorder import PvRecorder

import pvcheetah as pvc


class BaseSpeechReader(ABC):
    """Abstract base speech reader class"""

    @abstractmethod
    def generate_tokens(self) -> AsyncGenerator[str, None]:
        """Generate tokens from speech and yeild them."""
        pass


class PicoVoiceSpeechReader(BaseSpeechReader):
    """Speech Reader using Picovoice Cheetah."""

    def __init__(self, device_id: int = 0):
        key = SecretsEnvironment(environment='nextslide').read_secrets().get_secret("picovoice-key")

        self.rec = PvRecorder(frame_length=512, device_index=device_id)
        self.handle = pvc.create(key)

        self.buffer = queue.Queue()

    def generate_tokens(self) -> Generator[str, float, None]:
        """Generate tokens from speech and yeild them."""
        producer_thread = threading.Thread(target=self.produce_word_loop)
        self.threadrunning = True
        producer_thread.start()
        timeout = 30.0

        while True:
            timeout = yield self.buffer.get(timeout=timeout)

    def produce_word_loop(self) -> None:
        """Generate words from an input stream."""
        self.rec.start()

        try:
            while self.rec.is_recording and self.threadrunning:
                recording = self.rec.read()
                partial_transcript, is_endpoint = self.handle.process(recording)
                print(partial_transcript)

                # for word in partial_transcript.strip().split(" "):
                #     if formatted_word := word.strip().lower():
                #         print("===================", formatted_word)
                #         #self.buffer.put(formatted_word)

                if is_endpoint:
                    self.rec.stop()

        except BaseException as e:
            self.rec.stop()
            raise e

        self.rec.stop()

    def __del__(self):
        self.threadrunning = False
