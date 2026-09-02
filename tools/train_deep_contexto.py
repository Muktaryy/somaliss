import json
import re
from collections import defaultdict
from pathlib import Path

MASTER_INDEX_PATH = Path("data/master/recognition_index.jsonl")
CORPUS_PROVERBS_PATH = Path("data/corpus/maahmaahyo.json")
SAHAL_PATH = Path("data/imported/sahal_qaamuus_candidates.jsonl")
MATRIX_OUT_PATH = Path("data/vocabulary/somali_contexto_matrix.json")

def clean_word(w: str) -> str:
    return re.sub(r"[^\w\'-]", "", w).casefold().strip()

def train_deep_contexto_matrix():
    print("===========================================================")
    print("      DEEP SOMALI CONTEXTO CO-OCCURRENCE MODEL TRAINER     ")
    print("===========================================================")

    co_occurrence = defaultdict(lambda: defaultdict(int))
    word_frequencies = defaultdict(int)

    # 1. Train from Proverbs Corpus
    if CORPUS_PROVERBS_PATH.exists():
        with CORPUS_PROVERBS_PATH.open("r", encoding="utf-8") as f:
            proverbs = json.load(f)
            print(f"Training on {len(proverbs):,} Proverbs...")
            for item in proverbs:
                text = item if isinstance(item, str) else item.get("text", "")
                tokens = [clean_word(t) for t in text.split() if len(clean_word(t)) > 2]
                for i, w1 in enumerate(tokens):
                    word_frequencies[w1] += 1
                    # Sliding context window of 5 words
                    window = tokens[max(0, i - 5): min(len(tokens), i + 6)]
                    for w2 in window:
                        if w1 != w2:
                            co_occurrence[w1][w2] += 1

    # 2. Train from Sahal Qaamuus Definitions
    if SAHAL_PATH.exists():
        with SAHAL_PATH.open("r", encoding="utf-8") as f:
            print("Training on Sahal Qaamuus Dictionary Definitions...")
            for line in f:
                if line.strip():
                    r = json.loads(line)
                    surf = clean_word(r.get("surface", ""))
                    defn = r.get("definition", "") or r.get("somali_definition_summary", "")
                    if surf and defn:
                        word_frequencies[surf] += 5
                        tokens = [clean_word(t) for t in defn.split() if len(clean_word(t)) > 2]
                        for w2 in tokens:
                            if surf != w2:
                                co_occurrence[surf][w2] += 3
                                co_occurrence[w2][surf] += 3

    print(f"Unique Contextual Vocabulary Words: {len(word_frequencies):,}")

    # Build High-Top Similarity Matrix (Top 50 closest contextual neighbors per word)
    semantic_matrix = {}
    for word, neighbors in co_occurrence.items():
        if len(neighbors) == 0:
            continue
        sorted_neighbors = sorted(neighbors.items(), key=lambda x: x[1], reverse=True)[:50]
        max_freq = sorted_neighbors[0][1] if sorted_neighbors else 1
        
        normalized_neighbors = []
        for n_word, freq in sorted_neighbors:
            score = round(min(0.980, 0.40 + (freq / max_freq) * 0.58), 3)
            normalized_neighbors.append({"word": n_word, "score": score})
            
        semantic_matrix[word] = normalized_neighbors

    # Save Matrix
    MATRIX_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MATRIX_OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(semantic_matrix, f, ensure_ascii=False, indent=2)

    print(f"Saved Trained Contexto Matrix ({len(semantic_matrix):,} words) to: {MATRIX_OUT_PATH}")
    print("===========================================================")

if __name__ == "__main__":
    train_deep_contexto_matrix()
