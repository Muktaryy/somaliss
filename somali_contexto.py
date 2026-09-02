"""Interactive Terminal Somali Contexto Word Game CLI.

Run in terminal:
    python somali_contexto.py
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.contexto_engine import SomaliContextoEngine

SECRET_WORDS_POOL = [
    ("halgan", "Struggle / Resistance / Liberation"),
    ("farxad", "Happiness / Joy"),
    ("magaalo", "City / Capital"),
    ("aqoon", "Knowledge / Education"),
    ("nabad", "Peace / Tranquility"),
    ("geesi", "Hero / Brave Warrior"),
    ("guul", "Victory / Triumph")
]

def display_spectrum_table(secret_word: str, engine: SomaliContextoEngine) -> None:
    """Prints the Top 20 Words + Milestones (Ranks #25, #30, #50, #60, #100)."""
    spectrum = engine.get_spectrum(secret_word)
    print("\n==========================================================================================================")
    print(f"     💡 SOMALI CONTEXTO HINT MAP: TOP 20 WORDS & MILESTONES FOR '{secret_word.upper()}'                   ")
    print("==========================================================================================================")
    print(f"{'Contexto Rank':<14} | {'Word Surface':<18} | {'Proximity Score':<16} | {'Temperature & Category Status':<32}")
    print("-" * 86)

    for surf, score, rank, temp in spectrum:
        rank_str = f"Rank #{rank}"
        print(f"{rank_str:<14} | {surf:<18} | {score:<16.3f} | {temp:<32}")

    print("==========================================================================================================\n")

def main() -> None:
    print("==========================================================================")
    print("      🎮 SOMALI CONTEXTO: CIYAARTA QIYAASTA EREYADA SOOMAALIYEED 🎮       ")
    print("==========================================================================")
    print("  Soo dhowow! Qiyaas ereyga qarsoon ee Soomaaliyeed.")
    print("  Gali ereyo si aad u aragto darajadooda (Rank #1 ilaa Rank #5,000+).")
    print("  Qor 'hint' ama 'spectrum' si aad u aragto jawaabaha ugu dhow (Top 20 + Ranks #25, #30, #50, #60, #100).")
    print("  Qor 'exit' ama 'jooji' si aad uga baxdo.\n")

    secret_tuple = random.choice(SECRET_WORDS_POOL)
    secret_word, meaning = secret_tuple

    engine = SomaliContextoEngine()
    attempts = 0
    history = []

    print("--------------------------------------------------------------------------")
    print("  [SYSTEM]: Ereygii waa la doortay! Bilaab ciyaarta...")
    print("--------------------------------------------------------------------------\n")

    while True:
        try:
            user_input = input("Qiyaas Ereyga (Guess Word) > ").strip().casefold()
        except (EOFError, KeyboardInterrupt):
            print("\n\nCiyaartii waa la joojiyay. Nabad gelyo!")
            break

        if not user_input:
            continue

        if user_input in {"exit", "jooji", "bax"}:
            print(f"\nEreygii qarsoonaa wuxuu ahaa: '{secret_word.upper()}' ({meaning}). Nabad gelyo!")
            break

        if user_input in {"hint", "spectrum", "taabalo", "top20", "ranks"}:
            display_spectrum_table(secret_word, engine)
            continue

        attempts += 1
        res = engine.get_word_rank(user_input, secret_word)
        history.append(res)
        history.sort(key=lambda x: x["similarity_score"], reverse=True)

        print(f"\n  ➜ Result for '{user_input}':")
        print(f"     * Similarity Score: {res['similarity_score']:.3f}")
        print(f"     * Contexto Position: Rank #{res['contexto_rank']}")
        print(f"     * Temperature:      {res['temperature']}\n")

        if res["contexto_rank"] == 1:
            print("==========================================================================")
            print(f"  🎉 HAMBALYO! WAA GAADHAY EREYGI QARSOONAA: '{secret_word.upper()}'!")
            print(f"  🏆 Waxaad ku heshay {attempts} qiyaasrood!")
            print("==========================================================================\n")
            break

        # Show Top 3 Best Guesses so far
        print("  [YOUR TOP GUESSES SO FAR]:")
        for idx, h in enumerate(history[:3], 1):
            print(f"     {idx}. '{h['guess']}' -> Rank #{h['contexto_rank']} ({h['temperature']})")
        print("  (Type 'hint' or 'spectrum' anytime to see the full Top 20 hint map!)\n")

if __name__ == "__main__":
    main()
