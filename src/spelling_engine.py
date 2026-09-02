import json
import re
from pathlib import Path

MASTER_INDEX_PATH = Path("data/master/recognition_index.jsonl")

# Natural Somali phonetic equivalence pairs (low penalty for natural phonetic typos)
PHONETIC_PAIRS = {
    ('c', 'a'), ('a', 'c'),
    ('x', 'h'), ('h', 'x'),
    ('k', 'q'), ('q', 'k'),
    ('g', 'q'), ('q', 'g'),
    ('t', 'd'), ('d', 't'),
    ('s', 'sh'), ('sh', 's'),
    ('aa', 'a'), ('a', 'aa'),
    ('ee', 'e'), ('e', 'ee'),
    ('ii', 'i'), ('i', 'ii'),
    ('oo', 'o'), ('o', 'oo'),
    ('uu', 'u'), ('u', 'uu')
}

def natural_somali_distance(s1: str, s2: str) -> float:
    """Calculates weighted edit distance prioritizing natural Somali orthography & phonetics."""
    if len(s1) < len(s2):
        return natural_somali_distance(s2, s1)
    if len(s2) == 0:
        return float(len(s1))

    previous_row = [float(i) for i in range(len(s2) + 1)]
    for i, c1 in enumerate(s1):
        current_row = [float(i + 1)]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1.0
            deletions = current_row[j] + 1.0
            
            # Subcost: lower penalty (0.3) for natural Somali phonetic confusion pairs
            if c1 == c2:
                sub_cost = 0.0
            elif (c1, c2) in PHONETIC_PAIRS:
                sub_cost = 0.3
            else:
                sub_cost = 1.0

            substitutions = previous_row[j] + sub_cost
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

class SomaliSpellChecker:
    """Somali Dictionary-Grounded Natural Orthography Spell Checker."""

    def __init__(self, index_path: Path = MASTER_INDEX_PATH) -> None:
        self.index_path = index_path
        self.master_words = set()
        self._load_dictionary()

    def _load_dictionary(self) -> None:
        if self.index_path.exists():
            with self.index_path.open("r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        r = json.loads(line)
                        self.master_words.add(r["surface"].casefold())
                        if "lemma" in r:
                            self.master_words.add(r["lemma"].casefold())

    def is_correct(self, word: str) -> bool:
        w = word.strip(".,!?;:\"()[]'").casefold()
        return w in self.master_words

    def suggest_corrections(self, word: str, top_n: int = 3) -> list[tuple[str, float]]:
        """Finds closest natural standard Somali spellings."""
        clean_w = word.strip(".,!?;:\"()[]'").casefold()
        if not clean_w or clean_w in self.master_words:
            return [(word, 0.0)]

        first_char = clean_w[0]
        w_len = len(clean_w)

        # Candidate filtering by first letter and length
        candidates = [
            dw for dw in self.master_words
            if dw.startswith(first_char) and abs(len(dw) - w_len) <= 2
        ]

        if not candidates:
            candidates = [dw for dw in self.master_words if abs(len(dw) - w_len) <= 2]

        scored = [(dw, natural_somali_distance(clean_w, dw)) for dw in candidates]
        scored.sort(key=lambda x: x[1])

        return scored[:top_n]

    def auto_correct_sentence(self, sentence: str) -> dict:
        """Auto-corrects misspelled words using natural Somali orthography rules."""
        words = sentence.split()
        corrected_words = []
        corrections_log = []

        for original in words:
            clean = re.sub(r"[^\w\'-]", "", original).casefold()
            if not clean or self.is_correct(clean):
                corrected_words.append(original)
            else:
                sugs = self.suggest_corrections(clean, top_n=1)
                best_sug = sugs[0][0] if sugs else original
                if original.istitle():
                    best_sug = best_sug.capitalize()
                
                corrected_words.append(best_sug)
                corrections_log.append({
                    "original": original,
                    "natural_suggestion": best_sug,
                    "phonetic_score": round(sugs[0][1], 2) if sugs else 0.0
                })

        return {
            "original_sentence": sentence,
            "corrected_sentence": " ".join(corrected_words),
            "corrections_count": len(corrections_log),
            "corrections_log": corrections_log
        }

if __name__ == "__main__":
    checker = SomaliSpellChecker()
    print("===========================================================")
    print("      NATURAL SOMALI PHONETIC SPELL CHECKER TEST           ")
    print("===========================================================")
    print("Master Dictionary Size:", len(checker.master_words))
    
    test_typos = ["wadaado", "maahmah", "qawmiyat", "xanaqsan", "abeeso"]
    for typo in test_typos:
        sugs = checker.suggest_corrections(typo)
        print(f"  Typo '{typo:<10}' -> Natural Suggestions: {sugs}")

    sample = "Aboosadii far loo taagay fanaxay u boodaa."
    res = checker.auto_correct_sentence(sample)
    print("\nSentence Auto-Correction Test:")
    print("Original: ", res["original_sentence"])
    print("Corrected:", res["corrected_sentence"])
    print("===========================================================")
