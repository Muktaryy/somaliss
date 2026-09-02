"""Importer for sahal_somali_swedish.json dataset.

Extracts words, POS, Swedish glosses, and synonyms from somalijson/sahal_somali_swedish.json.
"""

from __future__ import annotations

import json
from pathlib import Path

SWEDISH_PATH = Path("somalijson/sahal_somali_swedish.json")
OUTPUT_MASTER_PATH = Path("data/master/recognition_index.jsonl")


def process_sahal_swedish() -> dict:
    if not SWEDISH_PATH.is_file():
        raise FileNotFoundError(f"Missing {SWEDISH_PATH}")

    with SWEDISH_PATH.open("r", encoding="utf-8") as f:
        s_data = json.load(f)

    entries = s_data.get("entries", [])
    records = []
    
    for entry in entries:
        word = str(entry.get("word", "")).strip().casefold()
        if not word or len(word) < 1 or word.isdigit():
            continue
            
        pos_raw = str(entry.get("pos", "")).strip()
        pos = None
        if "m" in pos_raw or "f" in pos_raw or "subst" in pos_raw:
            pos = "noun"
        elif "v" in pos_raw or "verb" in pos_raw:
            pos = "verb"
        elif "adj" in pos_raw:
            pos = "adjective"

        rec = {
            "surface": word,
            "lemma": word,
            "part_of_speech": pos,
            "record_type": "vocabulary",
            "confidence_tier": "supported",
            "status": "supported",
            "correction_authority": False,
            "promotion_allowed": True,
            "regions": ["Jigjiga", "Northwestern"],
            "master_record_id": f"sahal-swedish:{entry.get('id')}",
            "master_data_path": "somalijson/sahal_somali_swedish.json",
            "sources": [{"evidence_role": "sahal_somali_swedish_dictionary", "source_id": "sahal_swedish"}]
        }
        records.append(rec)
        
        # Check synonyms
        syns = entry.get("synonyms", [])
        if isinstance(syns, list):
            for syn in syns:
                syn_clean = str(syn).strip().replace(",", "").casefold()
                if syn_clean and syn_clean.isalpha():
                    records.append({
                        "surface": syn_clean,
                        "lemma": word,
                        "part_of_speech": pos,
                        "record_type": "vocabulary",
                        "confidence_tier": "supported",
                        "status": "supported",
                        "correction_authority": False,
                        "promotion_allowed": True,
                        "regions": ["Jigjiga", "Northwestern"],
                        "master_record_id": f"sahal-swedish-syn:{syn_clean}",
                        "master_data_path": "somalijson/sahal_somali_swedish.json",
                        "sources": [{"evidence_role": "sahal_somali_swedish_synonym", "source_id": "sahal_swedish"}]
                    })

    # Merge with data/master/recognition_index.jsonl
    existing_surfaces = set()
    if OUTPUT_MASTER_PATH.is_file():
        with OUTPUT_MASTER_PATH.open("r", encoding="utf-8") as mf:
            for line in mf:
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                    if "surface" in row:
                        existing_surfaces.add(row["surface"].casefold())
                except Exception:
                    pass

    new_added = 0
    with OUTPUT_MASTER_PATH.open("a", encoding="utf-8") as mf:
        for rec in records:
            if rec["surface"].casefold() not in existing_surfaces:
                mf.write(json.dumps(rec, ensure_ascii=False) + "\n")
                existing_surfaces.add(rec["surface"].casefold())
                new_added += 1

    return {
        "processed_entries": len(entries),
        "total_records": len(records),
        "new_master_entries_added": new_added,
        "total_master_surfaces": len(existing_surfaces)
    }


if __name__ == "__main__":
    res = process_sahal_swedish()
    print("Processed Sahal Somali-Swedish Dataset:", json.dumps(res, indent=2))
