"""Somali AI Thesaurus & Synonym/Antonym Engine."""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure root directory is on sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

THESAURUS_PATH = Path("data/vocabulary/somali_thesaurus.jsonl")

class SomaliThesaurus:
    """Somali Synonyms & Antonyms Lookup Engine."""

    def __init__(self, dataset_path: Path = THESAURUS_PATH) -> None:
        self.dataset_path = dataset_path
        self.synonyms_db: dict[str, list[str]] = {}
        self.antonyms_db: dict[str, list[str]] = {}
        self._load_dataset()

    def _load_dataset(self) -> None:
        if not self.dataset_path.exists():
            return
        with self.dataset_path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line)
                    w = rec["word"].casefold()
                    self.synonyms_db[w] = rec.get("synonyms", [])
                    self.antonyms_db[w] = rec.get("antonyms", [])

    def get_synonyms(self, word: str) -> list[str]:
        """Returns list of synonyms (ereyo isku macna ah)."""
        w = word.strip(".,!?;:\"()[]'").casefold()
        return self.synonyms_db.get(w, [])

    def get_antonyms(self, word: str) -> list[str]:
        """Returns list of antonyms (ereyo kasoo horjeeda)."""
        w = word.strip(".,!?;:\"()[]'").casefold()
        return self.antonyms_db.get(w, [])

    def lookup(self, word: str) -> dict:
        """Full thesaurus record for a word."""
        w = word.strip(".,!?;:\"()[]'").casefold()
        return {
            "word": word,
            "has_record": w in self.synonyms_db,
            "synonyms": self.get_synonyms(w),
            "antonyms": self.get_antonyms(w)
        }

if __name__ == "__main__":
    engine = SomaliThesaurus()
    print("==========================================================================")
    print("     SOMALI AI THESAURUS: SYNONYMS & ANTONYMS ENGINE DEMO                 ")
    print("==========================================================================")
    print("Loaded Thesaurus Words:", len(engine.synonyms_db))
    
    test_words = ["nolol", "farxad", "magaalo", "aqoon", "guul", "adag", "geesi"]
    for tw in test_words:
        res = engine.lookup(tw)
        syn_str = ", ".join(res["synonyms"]) if res["synonyms"] else "None"
        ant_str = ", ".join(res["antonyms"]) if res["antonyms"] else "None"
        print(f"\n* Word: '{tw.upper()}'")
        print(f"  - Synonyms (Ereyo Isku Macna ah): {syn_str}")
        print(f"  - Antonyms (Ereyo Kasoo Horjeeda): {ant_str}")

    print("\n==========================================================================")
