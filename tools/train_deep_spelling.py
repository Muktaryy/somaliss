import json
import random
import re
from pathlib import Path

MASTER_INDEX_PATH = Path("data/master/recognition_index.jsonl")
SPELLING_QA_OUT_PATH = Path("data/qa/somali_spelling_deep_training.jsonl")
CONFUSION_OUT_PATH = Path("data/vocabulary/somali_spelling_confusion_matrix.json")

def generate_typo(word: str) -> tuple[str, str] | None:
    """Generates a realistic Somali typo based on common orthographic rules."""
    w = word.casefold()
    if len(w) < 4:
        return None

    # Typo Strategy 1: Shorten long vowel (aa -> a, ee -> e, ii -> i, oo -> o, uu -> u)
    if "aa" in w:
        return w.replace("aa", "a", 1), "long_vowel_shortened_aa"
    if "ee" in w:
        return w.replace("ee", "e", 1), "long_vowel_shortened_ee"
    if "oo" in w:
        return w.replace("oo", "o", 1), "long_vowel_shortened_oo"
    if "ii" in w:
        return w.replace("ii", "i", 1), "long_vowel_shortened_ii"

    # Typo Strategy 2: Dental substitution (d <-> t, x <-> h, c <-> a)
    if w.endswith("yad"):
        return w[:-1] + "at", "terminal_dental_t"
    if w.endswith("ddo"):
        return w[:-3] + "do", "missing_double_d"
    if "x" in w:
        return w.replace("x", "h", 1), "phonetic_x_h"
    if "c" in w:
        return w.replace("c", "a", 1), "phonetic_c_a"

    # Typo Strategy 3: Drop double consonant
    for char in "bdfgklmnprst":
        double_c = char + char
        if double_c in w:
            return w.replace(double_c, char, 1), "missing_double_consonant"

    return None

def run_deep_spelling_training():
    print("===========================================================")
    print("      DEEP SOMALI SPELLING CORRECTION MODEL TRAINER        ")
    print("===========================================================")

    if not MASTER_INDEX_PATH.exists():
        print(f"Error: {MASTER_INDEX_PATH} not found.")
        return

    words = []
    with MASTER_INDEX_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                words.append(json.loads(line)["surface"])

    print(f"Loaded Master Index Surface Forms: {len(words):,}")

    qa_records = []
    confusion_stats = {}

    for target in words:
        res = generate_typo(target)
        if res:
            typo, typo_type = res
            if typo != target and len(typo) >= 3:
                confusion_stats[typo_type] = confusion_stats.get(typo_type, 0) + 1
                
                qa_item = {
                    "instruction": f"Sax higaadda ereyga Soomaaliyeed ee khaldan: '{typo}'",
                    "response": f"Ereyga saxda ah waa '{target}'. (Qaladaad: {typo_type}).",
                    "typo": typo,
                    "correction": target,
                    "typo_type": typo_type
                }
                qa_records.append(qa_item)

                if len(qa_records) >= 10000:
                    break

    print(f"Generated Deep Spelling Training Pairs: {len(qa_records):,}")

    # Save Fine-Tuning QA pairs
    SPELLING_QA_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SPELLING_QA_OUT_PATH.open("w", encoding="utf-8") as f:
        for r in qa_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # Save Confusion Matrix Stats
    CONFUSION_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CONFUSION_OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(confusion_stats, f, ensure_ascii=False, indent=2)

    print(f"Saved Fine-Tuning Dataset to: {SPELLING_QA_OUT_PATH}")
    print(f"Saved Confusion Matrix Matrix to: {CONFUSION_OUT_PATH}")
    print("===========================================================")

if __name__ == "__main__":
    run_deep_spelling_training()
