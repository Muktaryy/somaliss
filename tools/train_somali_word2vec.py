"""Dense 128-Dimensional Vector Embedding & Cosine Similarity Trainer for Somali Contexto."""

import json
import math
import random
import re
from collections import defaultdict
from pathlib import Path

MASTER_INDEX_PATH = Path("data/master/recognition_index.jsonl")
CORPUS_PROVERBS_PATH = Path("data/corpus/maahmaahyo.json")
SAHAL_PATH = Path("data/imported/sahal_qaamuus_candidates.jsonl")
VECTORS_OUT_PATH = Path("data/vocabulary/somali_word_vectors.json")

VECTOR_DIM = 64

def clean_word(w: str) -> str:
    return re.sub(r"[^\w\'-]", "", w).casefold().strip()

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

def train_somali_dense_vectors():
    print("===========================================================")
    print("      TRAINING 64-D DENSE SOMALI WORD VECTOR EMBEDDINGS    ")
    print("===========================================================")

    words_set = set()
    if MASTER_INDEX_PATH.exists():
        with MASTER_INDEX_PATH.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    r = json.loads(line)
                    words_set.add(clean_word(r["surface"]))

    print(f"Master Vocabulary Base: {len(words_set):,} Words")

    # Initialize Normalized Random Dense Vectors
    random.seed(42)
    vectors = {}
    for w in words_set:
        vec = [random.gauss(0, 1) for _ in range(VECTOR_DIM)]
        mag = magnitude(vec)
        vectors[w] = [x / mag for x in vec]

    # Train Co-Occurrence Adjustments
    co_occurs = defaultdict(lambda: defaultdict(int))
    
    if CORPUS_PROVERBS_PATH.exists():
        with CORPUS_PROVERBS_PATH.open("r", encoding="utf-8") as f:
            proverbs = json.load(f)
            for item in proverbs:
                text = item if isinstance(item, str) else item.get("text", "")
                tokens = [clean_word(t) for t in text.split() if clean_word(t) in vectors]
                for i, w1 in enumerate(tokens):
                    window = tokens[max(0, i - 4): min(len(tokens), i + 5)]
                    for w2 in window:
                        if w1 != w2:
                            co_occurs[w1][w2] += 1

    # Apply 5 Iteration Gradient Steps to Pull Co-Occurring Vectors Closer
    print("Applying Vector Alignment Iterations...")
    for iter_idx in range(5):
        for w1, neighbors in co_occurs.items():
            if w1 not in vectors:
                continue
            v1 = vectors[w1]
            for w2, freq in neighbors.items():
                if w2 not in vectors:
                    continue
                v2 = vectors[w2]
                alpha = min(0.05, 0.005 * freq)
                for d in range(VECTOR_DIM):
                    v1[d] += alpha * (v2[d] - v1[d])
            mag = magnitude(v1)
            if mag > 0:
                vectors[w1] = [x / mag for x in v1]

    # Save Vector Embeddings File for all master vocabulary words
    sample_vectors = {w: [round(x, 4) for x in vec] for w, vec in vectors.items()}
    
    VECTORS_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with VECTORS_OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(sample_vectors, f, ensure_ascii=False)

    print(f"Saved Trained 64-D Vector Embeddings ({len(sample_vectors):,} words) to: {VECTORS_OUT_PATH}")
    print("===========================================================")

if __name__ == "__main__":
    train_somali_dense_vectors()
