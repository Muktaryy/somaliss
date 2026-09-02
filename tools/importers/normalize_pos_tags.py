import json
from pathlib import Path

MASTER_INDEX_PATH = Path("data/master/recognition_index.jsonl")

# Dedicated word lists for fine-grained POS resolution
CONJUNCTIONS = {
    "iyo", "oo", "ee", "se", "haddiise", "eese", "markii", "si", "haddii", "xataa", "balki", "sababtoo", "oouh",
    "inkastoo", "illaa", "waayo", "laakiin", "mise", "ama", "balse", "waxaa", "inkasta", "isagoo", "iyadoo"
}
PREVERBS = {"soo", "sii", "wada", "kula", "laga", "ugu", "inaa", "ogaa", "oo", "ka", "ku", "la"}
CLITICS_PARTICLES = {"baa", "ayaa", "waa", "wuxuu", "wuxuuna", "waxaa", "waxay", "wuu", "way", "waan", "waad", "waannu", "waadna"}
PRONOUNS = {"isaga", "iyada", "iyagu", "aniga", "adiga", "innaga", "anaga", "idinra", "idinka", "kan", "tan", "kuwaas", "kuwan"}
NUMERALS = {"kow", "laba", "saddex", "afar", "shaan", "lix", "todooba", "saloobo", "sagaal", "toban", "kowaad", "labaad", "saddexaad"}
AUXILIARIES = {"yahay", "tahay", "yihiin", "ahaa", "ahayd", "ahayn", "lahaa", "lahayd", "joogaa", "joogtaa"}

def infer_pos(surf: str, curr_pos: str) -> str:
    surf_lower = surf.casefold()

    if surf_lower in CLITICS_PARTICLES:
        return "particle"
    if surf_lower in CONJUNCTIONS:
        return "conjunction"
    if surf_lower in PREVERBS:
        return "preverb"
    if surf_lower in PRONOUNS:
        return "pronoun"
    if surf_lower in NUMERALS:
        return "numeral"
    if surf_lower in AUXILIARIES:
        return "auxiliary"

    if curr_pos and curr_pos not in {"other", "vocabulary", "None", ""}:
        return curr_pos

    # Morphological deduction
    if surf_lower.endswith(("nimo", "asho", "ada", "ka", "ta", "aha", "ooyinka", "yada", "o", "do", "dda")):
        return "noun"
    if surf_lower.endswith(("san", "an", "eed", "aad", "eysa")):
        return "adjective"
    if surf_lower.endswith(("ayaa", "aysaa", "ayay", "aysay", "eystay", "aday", "adaa", "id", "iyay", "isay")):
        return "verb"

    # Default noun for dictionary headwords
    return "noun"

def run_pos_normalization():
    print("===========================================================")
    print("      SOMALI AI MASTER INDEX: POS NORMALIZATION ENGINE      ")
    print("===========================================================")

    if not MASTER_INDEX_PATH.exists():
        print(f"Error: {MASTER_INDEX_PATH} not found.")
        return

    with MASTER_INDEX_PATH.open("r", encoding="utf-8") as f:
        rows = [json.loads(line) for line in f if line.strip()]

    normalized_cnt = 0
    for r in rows:
        old_pos = r.get("part_of_speech")
        new_pos = infer_pos(r["surface"], old_pos)
        if old_pos != new_pos:
            r["part_of_speech"] = new_pos
            normalized_cnt += 1

    rows.sort(key=lambda r: (r["surface"].casefold(), r.get("lemma", "").casefold()))

    with MASTER_INDEX_PATH.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Successfully normalized POS tags for {normalized_cnt:,} records!")
    print(f"Total Master Index Rows: {len(rows):,}")
    print("===========================================================")

if __name__ == "__main__":
    run_pos_normalization()
