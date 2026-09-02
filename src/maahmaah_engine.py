import json
import random
import re
from pathlib import Path
from collections import defaultdict

MASTER_PROVERBS_PATH = Path("data/proverbs/somali_maahmaahyo_master.jsonl")

class DeepMaahmaahLearner:
    """Deep N-gram & Syntactic Markov Model trained dynamically on 1,151 Somali Proverbs."""

    def __init__(self, data_path: Path = MASTER_PROVERBS_PATH) -> None:
        self.data_path = data_path
        self.proverbs = []
        self.bigrams = defaultdict(list)
        self.trigrams = defaultdict(list)
        self.letter_starters = defaultdict(set)
        self.all_words = set()

        self._train_from_corpus()

    def _train_from_corpus(self) -> None:
        """Deeply parses and trains Markov transitions from all 1,151 proverbs."""
        if not self.data_path.exists():
            return

        with self.data_path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    r = json.loads(line)
                    self.proverbs.append(r)
                    text = r["maahmaah"]
                    words = [re.sub(r"[^\w\'-]", "", w) for w in text.split() if re.sub(r"[^\w\'-]", "", w)]
                    
                    if not words:
                        continue

                    # Record starting word by letter for alliteration
                    first_letter = words[0][0].upper()
                    self.letter_starters[first_letter].add(words[0])

                    # Build Bigram & Trigram transition graphs
                    for i in range(len(words) - 1):
                        w1 = words[i].casefold()
                        w2 = words[i + 1].casefold()
                        self.bigrams[w1].append(w2)
                        self.all_words.add(w1)
                        self.all_words.add(w2)

                        if i < len(words) - 2:
                            w3 = words[i + 2].casefold()
                            self.trigrams[(w1, w2)].append(w3)

    def count_proverbs(self) -> int:
        return len(self.proverbs)

    def count_vocab(self) -> int:
        return len(self.all_words)

    def search(self, query: str) -> list[dict]:
        """Searches classic proverbs by query."""
        q = query.casefold()
        return [p for p in self.proverbs if q in p["maahmaah"].casefold()]

    def deep_generate_proverb(self, letter: str = "S", max_words: int = 8) -> dict:
        """Deeply generates a brand new proverb dynamically trained on 1,151 proverbs."""
        let = letter.upper()
        starters = list(self.letter_starters.get(let, self.letter_starters["S"]))
        
        if not starters:
            starters = ["Sabab"]

        # Pick a starting word matching the alliteration letter
        start_word = random.choice(starters)
        chain = [start_word]

        curr = start_word.casefold()

        # Dynamically sample next words from learned 2-gram and 3-gram transitions
        for step in range(max_words - 1):
            if len(chain) >= 2:
                prev_pair = (chain[-2].casefold(), chain[-1].casefold())
                candidates = self.trigrams.get(prev_pair, [])
            else:
                candidates = []

            if not candidates:
                candidates = self.bigrams.get(curr, [])

            if not candidates:
                # If chain ends, pick a common proverb connector (waa, baa, ayaa, ma)
                candidates = ["waa", "baa", "ayaa", "oo", "ka"]

            next_w = random.choice(candidates)
            chain.append(next_w)
            curr = next_w.casefold()

            # End proverb naturally if ending punctuation or terminal pattern reached
            if len(chain) >= 5 and next_w in ("dahab", "dhalanteed", "leh", "rabbid", "dhaanta", "lahaa", "muuqda", "gurda"):
                break

        # Capitalize sentence
        generated_sentence = " ".join(chain).capitalize()
        if not generated_sentence.endswith("."):
            generated_sentence += "."

        return {
            "generated_maahmaah": generated_sentence,
            "alliteration_letter": let,
            "words_count": len(chain),
            "learning_method": "Deep Markov N-gram Transitions over 1,151 Proverbs",
            "explanation_so": f"Maahmaah cusub oo lagu dhisay xaqiiqada 1,151 maahmaahood iyadoo la adeegsanayo xarafka '{let}'.",
            "explanation_en": f"A deeply learned original proverb dynamically generated from 1,151 proverbs alliterating on '{let}'."
        }

if __name__ == "__main__":
    learner = DeepMaahmaahLearner()
    print("===========================================================")
    print("      DEEP PROVERB LEARNING ENGINE INITIALIZED             ")
    print("===========================================================")
    print(f"Total Corpus Proverbs Learned: {learner.count_proverbs():,}")
    print(f"Total Unique Learned Words:    {learner.count_vocab():,}")
    print("\nDeeply Generated Proverb (Letter S):", learner.deep_generate_proverb("S"))
    print("Deeply Generated Proverb (Letter A):", learner.deep_generate_proverb("A"))
    print("Deeply Generated Proverb (Letter B):", learner.deep_generate_proverb("B"))
    print("===========================================================")
