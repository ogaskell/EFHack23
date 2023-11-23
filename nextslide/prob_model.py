"""
The prediction model
"""
import asyncio
import queue
from tqdm import tqdm
from typing import AsyncIterator, Generator, Optional, Any
from rake_nltk import Rake
import numpy as np
import math
import yake

# TODO 1. Fix

class WordVecs:
    words = {}

    def __init__(self, file) -> None:
        with open(file, 'r', encoding='utf-8') as f:
            for line in tqdm(f):
                values = line.strip().split()
                word = values[0]

                try:
                    vector = np.asarray(values[1:], np.float32)
                except ValueError:
                    continue

                self.words[word] = vector

    def distance(self, word1, word2) -> float:
        try:
            vec1, vec2 = [self.words[word] for word in (word1, word2)]
            return np.dot(vec1, vec2)/(np.linalg.norm(vec1) * np.linalg.norm(vec2))
        except KeyError:
            return 0


class Predictor:
    generator: Generator[str, float, None]
    wordvec: WordVecs
    yak: yake.KeywordExtractor
    keywords: dict[str, float]

    seen_text = ""
    seen_keywords = set()


    def __init__(self, notes: list[str], generator: Generator[str, float, None], wordvec) -> None:
        self.yak = yake.KeywordExtractor(n=1)

        self.keywords = {word: 0 for point in notes for word in get_keywords(point, self.yak)}

        self.generator = generator
        self.wordvec = wordvec

    def prob(self):
        key_word_prob = [dist_prob(val) for val in self.keywords.values()]
        return float(np.mean(key_word_prob))

    def wait(self):
        def is_unseen_keyword(word) -> bool:
            if word in self.seen_keywords:
                return False

            all_keywords = get_keywords(self.seen_text, self.yak)
            return word in all_keywords

        try:
            for new_word in self.generator:
                timeout = seconds_from_prob(self.prob())
                self.generator.send(timeout)
                print(f"{timeout=}")

                print(f"{new_word=}")

                self.seen_text += " " + new_word
                if not is_unseen_keyword(new_word):
                    continue

                self.seen_keywords.add(new_word)

                for word, closest_dist in self.keywords.items():
                    dist = self.wordvec.distance(word, new_word)
                    self.keywords[word]= max(closest_dist, dist)

                print(f"After {new_word} => {self.prob()} | {self.keywords}")
        except queue.Empty:
            print("Next slide")
            return

def dist_prob(dist: float) -> float:
    return dist

def get_keywords(text, yak: yake.KeywordExtractor): # TODO
    return [kw for kw, _ in yak.extract_keywords(text)]

def seconds_from_prob(prob: float) -> float:
    return 28 / (1 + math.exp(20 * (prob - 0.6))) + 2
