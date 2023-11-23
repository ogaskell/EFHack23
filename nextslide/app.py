"""Main App that's runnable from the CLI."""


import asyncio
from .controllers import BaseController, KeypressController
from .doc_parser import MarkdownParser, Presentation
from .prob_model import Predictor, WordVecs
from .speech_reader import BaseSpeechReader, PicoVoiceSpeechReader


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
        ctrl.next_slide()

    async def run(self) -> None:
        """Run the app."""
        for slide, notes in zip(self.prs.slides, self.prs.notes):
            predictor = Predictor(notes, self.srd.generate_tokens(), self.wordvec)
            await predictor.wait()
            self.ctrl.next_slide()

if __name__ == "__main__":
    srd = PicoVoiceSpeechReader()
    ctrl = KeypressController()
    pars = MarkdownParser()
    pars.load(input("Notes file (.md) > "))
    prs = pars.get_presentation()
    wordvec = WordVecs("dataset/glove.twitter.27B.25d.txt")

    app = App(srd, ctrl, prs, wordvec)
    asyncio.run(app.run())
