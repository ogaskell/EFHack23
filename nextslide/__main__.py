"""Code to run the app. Run with `python -m nextslide` from parent dir."""
from .prob_model import Predictor, WordVecs

wordvec = WordVecs("/home/saatvikl/Documents/internships/EFHackathon/dataset/glove.twitter.27B.25d.txt")

# word1 = ''
# while word1 != 'quit':
#     try:
#         word1 = input("word1: ")
#         word2 = input("word2: ")

#         print(wordvec.distance(word1, word2))
#     except KeyError:
#         print("Key did not exist")

def user_input():
    while True:
        string = input("> ")
        for word in string.strip().split(" "):
            yield word.strip().lower()

u = user_input()
notes = [
    "introduce yourself",
    "introduce the task",
    "introduce the prizes"
    ]

predictor = Predictor(notes, u, wordvec)
predictor.wait()
