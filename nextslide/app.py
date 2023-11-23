"""Main App that's runnable from the CLI."""


from .controllers import BaseController
from .doc_parser import Presentation
from .prob_model import Predictor, WordVecs
from .speech_reader import BaseSpeechReader


class App:
    """App."""

    def __init__(
        self,
        srd: BaseSpeechReader,
        ctrl: BaseController,
        prs: Presentation,
        wordvec: WordVecs
    ):
        self.srd, self.ctrl, self.prs, self.wordvec = srd, ctrl, prs, wordvec

    async def run(self) -> None:
        """Run the app."""
        for slide, notes in zip(self.prs.slides, self.prs.notes):
            predictor = Predictor(notes, self.srd.generate_tokens(), self.wordvec)
            await predictor.wait()
            self.ctrl.next_slide()
