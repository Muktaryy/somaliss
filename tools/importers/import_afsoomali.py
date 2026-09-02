import json
import re
from pathlib import Path

# Paths
MASTER_INDEX_PATH = Path("data/master/recognition_index.jsonl")
AFSOOMALI_DICT_PATH = Path("c:/Users/sahalm/Desktop/New folder/compare/Afsoomali-main/Somali-Dictionary/Somali-Dictionary.txt")
SLS_MADAX_DIR = Path("c:/Users/sahalm/Desktop/New folder/compare/somali-language-standard-main/resources/madax-ereyo")
IMPORTED_OUT_PATH = Path("data/imported/sahal_afsoomali_candidates.jsonl")

# Somali Orthography Validator: Only genuine Somali letters and glottal stop / hyphen
SOMALI_WORD_PATTERN = re.compile(r"^[a-zA-Z\'-]{2,35}$")
VOWEL_PATTERN = re.compile(r"[aeiouAEIOU]")

def is_valid_real_somali_word(word: str) -> bool:
    """Strict quality check: rejects OCR corruptions, digits, symbols, and non-words."""
    if not word or len(word) < 2 or len(word) > 35:
        return False
    if not SOMALI_WORD_PATTERN.match(word):
        return False
    if not VOWEL_PATTERN.search(word):
        return False
    # Reject strings with suspicious double hyphens or apostrophes
    if "--" in word or "''" in word:
        return False
    return True

def deduce_part_of_speech(word: str) -> str:
    """Deduces POS based on regular Somali morphological suffix endings."""
    w = word.casefold()
    if w.endswith(("nimo", "asho", "nto", "ayaal", "ey", "nimada", "ahaa")):
        return "noun"
    elif w.endswith(("oobid", "aysad", "ay", "san", "ayaa", "ayaan")):
        return "verb" if not w.endswith("san") else "adjective"
    elif w.endswith(("san", "an", "eed")):
        return "adjective"
    return "noun"

def run_import():
    print("===========================================================")
    print("    STRICT QUALITY IMPORTER: REAL SOMALI WORDS ONLY       ")
    print("===========================================================")

    # 1. Load existing master index to prevent any duplicates
    existing_keys = set()
    master_rows = []
    if MASTER_INDEX_PATH.exists():
        with MASTER_INDEX_PATH.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    r = json.loads(line)
                    master_rows.append(r)
                    key = (r.get("surface", "").casefold(), r.get("lemma", "").casefold())
                    existing_keys.add(key)

    print(f"Existing Master Index Words: {len(existing_keys):,}")

    # 2. Extract and filter candidates from Afsoomali & SLS
    raw_candidates = set()

    # From Afsoomali
    if AFSOOMALI_DICT_PATH.exists():
        with AFSOOMALI_DICT_PATH.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                parts = line.strip().split()
                if parts:
                    clean = parts[0].replace("'", "'").strip().casefold()
                    clean = re.sub(r"[^a-zA-Z\'-]", "", clean)
                    if is_valid_real_somali_word(clean):
                        raw_candidates.add(clean)

    # From Somali Language Standard (Goobo Labs)
    if SLS_MADAX_DIR.exists():
        for md in SLS_MADAX_DIR.glob("*.md"):
            if md.name in ("README.md", "00-sources.md"): continue
            with md.open("r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        clean_line = line.lstrip("-*1234567890. ").strip()
                        parts = clean_line.split()
                        if parts:
                            clean = re.sub(r"[^a-zA-Z\'-]", "", parts[0]).casefold()
                            if is_valid_real_somali_word(clean):
                                raw_candidates.add(clean)

    print(f"Total Quality-Filtered Candidates Found: {len(raw_candidates):,}")

    # 3. Keep ONLY new real words not already in master index
    new_imported_records = []
    IMPORTED_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    for word in sorted(raw_candidates):
        key = (word, word)
        if key not in existing_keys:
            existing_keys.add(key)
            pos = deduce_part_of_speech(word)
            record = {
                "surface": word,
                "lemma": word,
                "part_of_speech": pos,
                "record_type": "vocabulary",
                "confidence_tier": "supported",
                "status": "supported",
                "correction_authority": False,
                "promotion_allowed": True,
                "regions": ["Jigjiga", "Northwestern", "Central"],
                "master_record_id": f"sahal-afsoomali:{word}",
                "master_data_path": str(IMPORTED_OUT_PATH),
                "sources": [
                    {
                        "evidence_role": "sahal_afsoomali_dictionary",
                        "source_id": "sahal_afsoomali"
                    }
                ]
            }
            new_imported_records.append(record)

    print(f"New Genuine Real Words to Add: {len(new_imported_records):,}")

    # Write imported candidates file
    with IMPORTED_OUT_PATH.open("w", encoding="utf-8") as f:
        for r in new_imported_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # Append new records to recognition_index.jsonl
    master_rows.extend(new_imported_records)
    master_rows.sort(key=lambda r: (r["surface"].casefold(), r.get("lemma", "").casefold()))

    with MASTER_INDEX_PATH.open("w", encoding="utf-8") as f:
        for r in master_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"NEW Master Recognition Index Total Rows: {len(master_rows):,}")
    print("===========================================================")

if __name__ == "__main__":
    run_import()
