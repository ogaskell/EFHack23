"""Code to run the app. Run with `python -m nextslide` from parent dir."""
from .prob_model import Predictor, WordVecs
import asyncio
import sys
wordvec = WordVecs("/home/saatvikl/Documents/internships/EFHackathon/dataset/glove.twitter.27B.25d.txt")

# word1 = ''
# while word1 != 'quit':
#     try:
#         word1 = input("word1: ")
#         word2 = input("word2: ")

#         print(wordvec.distance(word1, word2))
#     except KeyError:
#         print("Key did not exist")

async def user_input():
    while True:
        string = await ainput("> ")
        for word in string.strip().split(" "):
            yield word.strip().lower()

async def ainput(string: str) -> str:
    await asyncio.get_event_loop().run_in_executor(
            None, lambda s=string: sys.stdout.write(s+' '))
    return await asyncio.get_event_loop().run_in_executor(
            None, sys.stdin.readline)

u = user_input()
notes = [
    "introduce yourself",
    "introduce the task",
    "introduce the prizes"
    ]

predictor = Predictor(notes, u, wordvec)
asyncio.run(predictor.wait())
