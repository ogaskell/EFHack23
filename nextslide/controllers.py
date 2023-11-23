"""Presentation controllers."""

from abc import ABC, abstractmethod

import keyboard


class BaseController(ABC):
    """Controller Base Class."""

    @staticmethod
    @abstractmethod
    def next_slide() -> None:
        """Advance to the next slide."""
        pass


class KeypressController(BaseController):
    """Simply presses a single key to advance a slide.

    Requires superuser unfortunately.
    """

    key: str = "right"

    @staticmethod
    def next_slide() -> None:
        """Press `key` to advance to next slide."""
        keyboard.press_and_release(KeypressController.key)
