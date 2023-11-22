"""Contains a number of classes used to parse a given file/s, to retrieve slides and notes."""

from abc import ABC, abstractmethod
from typing import Optional


class Presentation:
    """Prepresents the combined slides and notes."""

    slides: None = None  # Not currently used
    notes: list[list[str]]  # notes[slide][bullet_point]


class BaseParser(ABC):
    """Base class for document parsers."""

    presentation: Optional[Presentation] = None

    @abstractmethod
    def load(*args, **kwargs) -> None:
        """Load some file/s to generate a Presentation object."""

    def get_presentation(self) -> Presentation:
        """Will return a Presentation object."""
        if self.presentation is None:
            raise ValueError("Presentation not loaded. Call .load() on the parser first.")

        return self.presentation
