"""Somali AI Contexto Game & Dense Vector Proximity Engine.

Calculates Cosine Similarity over 64-Dimensional Dense Somali Word Embeddings
and fine-grained semantic distance matrices.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.thesaurus_engine import SomaliThesaurus

VECTORS_PATH = Path("data/vocabulary/somali_word_vectors.json")
MATRIX_PATH = Path("data/vocabulary/somali_contexto_matrix.json")

def dot_product(v1: list[float], v2: list[float]) -> float:
    return sum(a * b for a, b in zip(v1, v2))

def magnitude(v: list[float]) -> float:
    return math.sqrt(sum(a * a for a in v))

def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    m1 = magnitude(v1)
    m2 = magnitude(v2)
    if m1 == 0.0 or m2 == 0.0:
        return 0.0
    return dot_product(v1, v2) / (m1 * m2)

class SomaliContextoEngine:
    """Semantic Word Proximity & Dense Vector Contexto Game Engine for Somali."""

    def __init__(self) -> None:
        self.thesaurus = SomaliThesaurus()
        self.vectors: dict[str, list[float]] = {}
        self.matrix: dict[str, list[dict]] = {}
        self._load_data()

    def _load_data(self) -> None:
        if VECTORS_PATH.exists():
            with VECTORS_PATH.open("r", encoding="utf-8") as f:
                self.vectors = json.load(f)
        if MATRIX_PATH.exists():
            with MATRIX_PATH.open("r", encoding="utf-8") as f:
                self.matrix = json.load(f)

    def get_spectrum(self, secret_word: str) -> list[tuple[str, float, int, str]]:
        sec = secret_word.casefold().strip()
        spectrum = [(sec, 1.000, 1, "[BINGO!] Perfect Match")]
        
        neighbors = self.matrix.get(sec, [])
        if not neighbors and sec in self.vectors:
            # Rank all words in vectors by cosine similarity to sec
            v_sec = self.vectors[sec]
            scored = []
            for w, vec in self.vectors.items():
                if w != sec:
                    sim = cosine_similarity(v_sec, vec)
                    scored.append((w, sim))
            scored.sort(key=lambda x: x[1], reverse=True)
            for idx, (w, sim) in enumerate(scored[:20], 2):
                score = round(max(0.500, sim), 3)
                temp = "[HOT!] Extremely Close" if score >= 0.850 else "[WARM!] Same Context"
                spectrum.append((w, score, idx, temp))
        elif neighbors:
            for idx, item in enumerate(neighbors[:20], 2):
                spectrum.append((item["word"], item["score"], idx, "[HOT!] Extremely Close" if item["score"] >= 0.900 else "[WARM!] Same Context"))
        else:
            syns = self.thesaurus.get_synonyms(sec)
            for idx, s in enumerate(syns, 2):
                spectrum.append((s, round(0.960 - (idx * 0.010), 3), idx, "[HOT!] Extremely Close"))

        return spectrum

    def calculate_similarity(self, word1: str, word2: str) -> float:
        w1 = word1.casefold().strip()
        w2 = word2.casefold().strip()

        if w1 == w2:
            return 1.000

        # Dense Vector Cosine Similarity
        if w1 in self.vectors and w2 in self.vectors:
            cos_sim = cosine_similarity(self.vectors[w1], self.vectors[w2])
            norm_sim = (cos_sim + 1.0) / 2.0  # Normalize to [0, 1]
            return round(norm_sim, 3)

        # Matrix Lookup Fallback
        if w2 in self.matrix:
            for item in self.matrix[w2]:
                if item["word"] == w1:
                    return item["score"]

        # Thesaurus Fallback
        syns1 = set(self.thesaurus.get_synonyms(w1))
        syns2 = set(self.thesaurus.get_synonyms(w2))
        ants1 = set(self.thesaurus.get_antonyms(w1))

        if w2 in syns1 or w1 in syns2:
            return 0.925
        if syns1.intersection(syns2):
            return 0.865
        if w2 in ants1:
            return 0.815

        # Character N-gram Distance
        prefix_match = sum(1 for c1, c2 in zip(w1, w2) if c1 == c2)
        prefix_score = prefix_match / max(len(w1), len(w2))
        len_diff = abs(len(w1) - len(w2))
        len_score = max(0.0, 1.0 - (len_diff / 10.0))

        hash_offset = (abs(hash(w1 + w2)) % 1000) / 100000.0
        return round(min(0.790, 0.25 * prefix_score + 0.05 * len_score + hash_offset), 3)

    def get_word_rank(self, guess: str, secret_word: str) -> dict:
        g = guess.casefold().strip()
        sec = secret_word.casefold().strip()

        sim = self.calculate_similarity(g, sec)
        if sim == 1.0:
            rank = 1
            temperature = "[BINGO!] Perfect Match"
        elif sim >= 0.85:
            rank = int((1.0 - sim) * 100) + 1
            temperature = "[HOT!] Extremely Close"
        elif sim >= 0.70:
            rank = int((0.85 - sim) * 200) + 16
            temperature = "[WARM!] Same Semantic Domain"
        elif sim >= 0.40:
            rank = int((0.70 - sim) * 1000) + 46
            temperature = "[COOL] Something in Common"
        else:
            rank = int((0.40 - sim) * 5000) + 350
            temperature = "[COLD] Distant Word"

        return {
            "guess": guess,
            "secret_word": secret_word,
            "similarity_score": sim,
            "contexto_rank": rank,
            "temperature": temperature
        }

if __name__ == "__main__":
    engine = SomaliContextoEngine()
    print("==========================================================================")
    print("     SOMALI DENSE VECTOR CONTEXTO ENGINE: 64-D COSINE SIMILARITY          ")
    print("==========================================================================")
    print("Loaded Dense Vector Embeddings:", len(engine.vectors), "words")
    
    w1, w2 = "nolol", "caafimaad"
    sim = engine.calculate_similarity(w1, w2)
    print(f"\nCosine Similarity between '{w1}' and '{w2}': {sim:.3f}")

    res = engine.get_word_rank(w2, w1)
    print(f"Contexto Rank for '{w2}' against secret '{w1}': Rank #{res['contexto_rank']} ({res['temperature']})")
    print("==========================================================================")
