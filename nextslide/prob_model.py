"""
The prediction model
"""
import asyncio
from tqdm import tqdm
from typing import AsyncIterator, Optional, Any
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
    BUFFER = 10
    generator: AsyncIterator[str]
    wordvec: WordVecs
    yak: yake.KeywordExtractor
    keywords: dict[str, float]

    seen_text: list[str] = []
    seen_keywords = set()


    def __init__(self, notes: list[str], generator: AsyncIterator[str], wordvec) -> None:
        self.yak = yake.KeywordExtractor(n=1)
        self.wordvec = wordvec
        self.generator = generator

        self.keywords = {word: 0 for point in notes for word in self.get_keywords(point, self.yak)}


    def prob(self):
        key_word_prob = [dist_prob(val) for val in self.keywords.values()]
        return float(np.mean(key_word_prob))

    async def wait(self):
        def is_unseen_keyword(word) -> bool:
            if word in self.seen_keywords:
                return False

            all_keywords = self.get_keywords(" ".join(self.seen_text), self.yak)
            return word in all_keywords

        try:
            while True:
                timeout = seconds_from_prob(self.prob())
                print(f"{timeout=}")

                new_word = await asyncio.wait_for(
                    self.generator.__anext__(),
                    timeout=timeout
                )

                print(f"{new_word=}")

                self.seen_text.append(new_word)

                if len(self.seen_text) > self.BUFFER:
                    self.seen_text.pop(0)

                if not is_unseen_keyword(new_word):
                    continue

                self.seen_keywords.add(new_word)

                for word, closest_dist in self.keywords.items():
                    dist = self.wordvec.distance(word, new_word)
                    self.keywords[word]= max(closest_dist, dist)

                print(f"After {new_word} => {self.prob()} | {self.keywords}")

        except TimeoutError:
            print("Next slide")
            return

    def get_keywords(self, text, yak: yake.KeywordExtractor): 
        return [kw for kw, _ in yak.extract_keywords(text) if kw in self.wordvec.words]

def dist_prob(dist: float) -> float:
    return dist


def seconds_from_prob(prob: float) -> float:
    return 29 / (1 + math.exp(10 * (prob - 0.6))) + 1
