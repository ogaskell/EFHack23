"""Code to run the app. Run with `python -m nextslide` from parent dir."""
import asyncio
from .controllers import BaseController, DebugController, KeypressController
from .doc_parser import MarkdownParser, Presentation
from .prob_model import Predictor, WordVecs
from .speech_reader import BaseSpeechReader, PicoVoiceSpeechReader
from .app import App

from pvrecorder import PvRecorder

print("Available devices:\n", "\n".join(PvRecorder.get_available_devices()), sep="")

srd = PicoVoiceSpeechReader(int(input("Device index > ")))
ctrl = DebugController()
pars = MarkdownParser()
pars.load(input("Notes file (.md) > "))
prs = pars.get_presentation()
wordvec = WordVecs("dataset/glove.twitter.27B.25d.txt")

app = App(srd, ctrl, prs, wordvec)
asyncio.run(app.run())
