import json
from pathlib import Path

SAHAL_PATH = Path("data/imported/sahal_qaamuus_candidates.jsonl")
THESAURUS_PATH = Path("data/vocabulary/somali_thesaurus.jsonl")

def import_sahal_thesaurus():
    print("===========================================================")
    print("      EXTRACTING SOMALI SYNONYMS FROM SAHAL QAAMUUS        ")
    print("===========================================================")

    if not SAHAL_PATH.exists():
        print(f"Error: {SAHAL_PATH} not found.")
        return

    existing_db = {}
    if THESAURUS_PATH.exists():
        with THESAURUS_PATH.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line)
                    existing_db[rec["word"].casefold()] = rec

    extracted_cnt = 0
    with SAHAL_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                word = r.get("surface", "").casefold()
                meaning = r.get("definition", "") or r.get("somali_definition_summary", "")
                
                # Check for synonym clues in definitions (e.g. "e.g.", "macnaheedu waa", "u dhigma")
                if "ee " in meaning and "waxaa u dhigma" in meaning:
                    parts = meaning.split("waxaa u dhigma")
                    syn = parts[1].strip().strip(".").casefold()
                    if word and syn and len(syn) < 20:
                        rec = existing_db.get(word, {"word": word, "synonyms": [], "antonyms": []})
                        if syn not in rec["synonyms"]:
                            rec["synonyms"].append(syn)
                            existing_db[word] = rec
                            extracted_cnt += 1

    with THESAURUS_PATH.open("w", encoding="utf-8") as f:
        for rec in existing_db.values():
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"Total Thesaurus Database Records: {len(existing_db):,}")
    print("===========================================================")

if __name__ == "__main__":
    import_sahal_thesaurus()
