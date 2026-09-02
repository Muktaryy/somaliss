"""Importer for sahal_qaamuus.json and sahal_somali_swedish.json dataset.

Extracts lemmas, parts of speech, conjugation classes, inflected plurals,
and past-tense inflections from the 15,381 entry dictionary in somalijson/.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

QAAMUUS_PATH = Path("somalijson/sahal_qaamuus.json")
SWEDISH_PATH = Path("somalijson/sahal_somali_swedish.json")
OUTPUT_CANDIDATES_PATH = Path("data/imported/sahal_qaamuus_candidates.jsonl")
OUTPUT_MASTER_PATH = Path("data/master/recognition_index.jsonl")


def parse_pos(pos_str: str) -> tuple[str, str | None, str | None]:
    """Parse raw pos string into (part_of_speech, gender, conjugation_class)."""
    p = pos_str.strip().lower()
    if not p:
        return ("unknown", None, None)
    
    # Verbs: f.g1, f.mg1, f.g2, f.mg2, f.g3, f.mg3, f.y, f.m, etc.
    if "f.g1" in p or "f.mg1" in p or "f.m.g1" in p:
        return ("verb", None, "class_1")
    if "f.g2" in p or "f.mg2" in p or "f.m.g2" in p:
        return ("verb", None, "class_2")
    if "f.g3" in p or "f.mg3" in p or "f.m.g3" in p:
        return ("verb", None, "class_3")
    if p.startswith("f.") or "f." in p or p == "f":
        return ("verb", None, "class_1")
    
    # Nouns: m.l (masculine), m.dh (feminine), m.l / m.dh
    if "m.l" in p:
        return ("noun", "masculine", None)
    if "m.dh" in p:
        return ("noun", "feminine", None)
    if p.startswith("m"):
        return ("noun", "masculine", None)
        
    # Adjectives: ee.
    if "ee." in p or p.startswith("ee"):
        return ("adjective", None, None)
        
    # Numerals: t.
    if "t." in p or p == "t":
        return ("numeral", None, None)
        
    return ("other", None, None)


def extract_inflections_from_def(word: str, definition: str, pos: str) -> list[str]:
    """Extract inflected forms (plurals or past tenses) mentioned in definition parentheses."""
    inflections: list[str] = [word]
    if not definition or "(" not in definition:
        return inflections
        
    match = re.search(r"\(([^)]+)\)", definition)
    if not match:
        return inflections
        
    paren_text = match.group(1).strip()
    parts = [p.strip() for p in paren_text.split(",")]
    
    for part in parts:
        if part.startswith("-"):
            suffix = part[1:].strip()
            # If suffix contains POS indicators like m.l, clean it
            suffix_clean = re.sub(r"\s+m\.[a-z]+.*", "", suffix).strip()
            if not suffix_clean:
                continue
                
            # For verbs, if root ends with consonant/vowel
            if pos == "verb":
                # Handle past forms like -ray, -rtay -> word + ray, word + rtay
                # If word ends with vowel and suffix starts with consonant, combine
                stem = word[:-1] if (word.endswith("o") or word.endswith("a") or word.endswith("i") or word.endswith("e")) else word
                inflections.append(stem + suffix_clean)
                inflections.append(word + suffix_clean)
            else:
                # Noun plurals: -bayaal -> word + bayaal or stem + bayaal
                stem = word[:-1] if (word.endswith("e") or word.endswith("a") or word.endswith("o")) else word
                inflections.append(stem + suffix_clean)
                inflections.append(word + suffix_clean)
                
    return sorted(list(set(inflections)))


def process_sahal_qaamuus() -> dict:
    if not QAAMUUS_PATH.is_file():
        raise FileNotFoundError(f"Missing {QAAMUUS_PATH}")
        
    with QAAMUUS_PATH.open("r", encoding="utf-8") as f:
        q_data = json.load(f)
        
    entries = q_data.get("entries", [])
    processed_count = 0
    extracted_surfaces = set()
    records = []
    
    for entry in entries:
        word = str(entry.get("word", "")).strip().casefold()
        if not word or len(word) < 1 or re.search(r"\d", word):
            continue
            
        pos_raw = str(entry.get("pos", ""))
        definition = str(entry.get("definition", ""))
        pos, gender, conj_class = parse_pos(pos_raw)
        
        forms = extract_inflections_from_def(word, definition, pos)
        for form in forms:
            form_clean = form.strip().casefold()
            if form_clean and len(form_clean) >= 2 and form_clean.isalpha():
                extracted_surfaces.add(form_clean)
                
        rec = {
            "surface": word,
            "lemma": word,
            "part_of_speech": pos if pos != "unknown" else None,
            "somali_definition_summary": definition,
            "record_type": "vocabulary",
            "confidence_tier": "supported",
            "status": "supported",
            "correction_authority": False,
            "promotion_allowed": True,
            "regions": ["Jigjiga", "Northwestern"],
            "master_record_id": f"sahal-qaamuus:{entry.get('id', processed_count)}",
            "master_data_path": "data/imported/sahal_qaamuus_candidates.jsonl",
            "sources": [{"evidence_role": "sahal_qaamuus_dictionary", "source_id": "sahal_qaamuus"}]
        }
        records.append(rec)
        processed_count += 1
        
        # Also add extracted inflections
        for form in forms:
            form_clean = form.strip().casefold()
            if form_clean and len(form_clean) >= 2 and form_clean.isalpha():
                extracted_surfaces.add(form_clean)
                if form_clean != word:
                    records.append({
                        "surface": form_clean,
                        "lemma": word,
                        "part_of_speech": pos if pos != "unknown" else None,
                        "somali_definition_summary": f"Inflected form of '{word}': {definition[:80]}...",
                        "record_type": "morphology",
                        "confidence_tier": "supported",
                        "status": "supported",
                        "correction_authority": False,
                        "promotion_allowed": True,
                        "regions": ["Jigjiga", "Northwestern"],
                        "master_record_id": f"sahal-qaamuus-inflect:{form_clean}",
                        "master_data_path": "data/imported/sahal_qaamuus_candidates.jsonl",
                        "sources": [{"evidence_role": "sahal_qaamuus_inflection", "source_id": "sahal_qaamuus"}]
                    })
                
    # Write imported candidates file
    OUTPUT_CANDIDATES_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CANDIDATES_PATH.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            
    # Merge with data/master/recognition_index.jsonl
    existing_lines = []
    if OUTPUT_MASTER_PATH.is_file():
        with OUTPUT_MASTER_PATH.open("r", encoding="utf-8") as mf:
            existing_lines = [line.strip() for line in mf if line.strip()]
            
    existing_surfaces = set()
    for line in existing_lines:
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
        "processed_entries": processed_count,
        "unique_lemmas": len(set(r["lemma"] for r in records)),
        "total_records": len(records),
        "new_master_entries_added": new_added,
        "total_master_surfaces": len(existing_surfaces)
    }


if __name__ == "__main__":
    res = process_sahal_qaamuus()
    print("Processed Sahal Qaamuus Dataset:", json.dumps(res, indent=2))
