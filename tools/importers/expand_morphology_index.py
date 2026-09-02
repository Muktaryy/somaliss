import json
from pathlib import Path

MASTER_INDEX_PATH = Path("data/master/recognition_index.jsonl")

# Essential grammar forms to add to master index
ADDITIONAL_GRAMMAR_FORMS = [
    {"surface": "xiddigo", "lemma": "xiddig", "part_of_speech": "noun", "record_type": "morphology", "confidence_tier": "supported", "status": "supported", "correction_authority": False, "promotion_allowed": True, "regions": ["Jigjiga", "Northwestern"], "master_record_id": "sahal-inflect:xiddigo", "master_data_path": "data/imported/sahal_qaamuus_candidates.jsonl", "sources": [{"evidence_role": "noun_plural", "source_id": "sahal_qaamuus"}]},
    {"surface": "wiilka", "lemma": "wiil", "part_of_speech": "noun", "record_type": "morphology", "confidence_tier": "supported", "status": "supported", "correction_authority": False, "promotion_allowed": True, "regions": ["Jigjiga", "Northwestern"], "master_record_id": "sahal-inflect:wiilka", "master_data_path": "data/imported/sahal_qaamuus_candidates.jsonl", "sources": [{"evidence_role": "noun_definite", "source_id": "sahal_qaamuus"}]},
    {"surface": "joogsaday", "lemma": "joogso", "part_of_speech": "verb", "record_type": "morphology", "confidence_tier": "supported", "status": "supported", "correction_authority": False, "promotion_allowed": True, "regions": ["Jigjiga", "Northwestern"], "master_record_id": "sahal-inflect:joogsaday", "master_data_path": "data/imported/sahal_qaamuus_candidates.jsonl", "sources": [{"evidence_role": "class_3_reflexive_past", "source_id": "sahal_qaamuus"}]},
    {"surface": "aqaanay", "lemma": "aqaan", "part_of_speech": "verb", "record_type": "morphology", "confidence_tier": "supported", "status": "supported", "correction_authority": False, "promotion_allowed": True, "regions": ["Jigjiga", "Northwestern"], "master_record_id": "sahal-inflect:aqaanay", "master_data_path": "data/imported/sahal_qaamuus_candidates.jsonl", "sources": [{"evidence_role": "irregular_verb_past", "source_id": "somali-ai-reviewed"}]},
    {"surface": "wuu", "lemma": "waa", "part_of_speech": "clitic", "record_type": "morphology", "confidence_tier": "supported", "status": "supported", "correction_authority": False, "promotion_allowed": True, "regions": ["Jigjiga", "Northwestern"], "master_record_id": "sahal-inflect:wuu", "master_data_path": "data/imported/sahal_qaamuus_candidates.jsonl", "sources": [{"evidence_role": "statement_clitic", "source_id": "somali-ai-reviewed"}]},
    {"surface": "way", "lemma": "waa", "part_of_speech": "clitic", "record_type": "morphology", "confidence_tier": "supported", "status": "supported", "correction_authority": False, "promotion_allowed": True, "regions": ["Jigjiga", "Northwestern"], "master_record_id": "sahal-inflect:way", "master_data_path": "data/imported/sahal_qaamuus_candidates.jsonl", "sources": [{"evidence_role": "statement_clitic", "source_id": "somali-ai-reviewed"}]},
    {"surface": "waan", "lemma": "waa", "part_of_speech": "clitic", "record_type": "morphology", "confidence_tier": "supported", "status": "supported", "correction_authority": False, "promotion_allowed": True, "regions": ["Jigjiga", "Northwestern"], "master_record_id": "sahal-inflect:waan", "master_data_path": "data/imported/sahal_qaamuus_candidates.jsonl", "sources": [{"evidence_role": "statement_clitic", "source_id": "somali-ai-reviewed"}]},
    {"surface": "waad", "lemma": "waa", "part_of_speech": "clitic", "record_type": "morphology", "confidence_tier": "supported", "status": "supported", "correction_authority": False, "promotion_allowed": True, "regions": ["Jigjiga", "Northwestern"], "master_record_id": "sahal-inflect:waad", "master_data_path": "data/imported/sahal_qaamuus_candidates.jsonl", "sources": [{"evidence_role": "statement_clitic", "source_id": "somali-ai-reviewed"}]}
]

def run_expansion():
    print("===========================================================")
    print("       EXPANDING MASTER INDEX GRAMMAR FEATURE COVERAGE     ")
    print("===========================================================")

    if not MASTER_INDEX_PATH.exists():
        print(f"Error: {MASTER_INDEX_PATH} not found.")
        return

    with MASTER_INDEX_PATH.open("r", encoding="utf-8") as f:
        rows = [json.loads(line) for line in f if line.strip()]

    existing_keys = set((r["surface"].casefold(), r.get("lemma", "").casefold()) for r in rows)

    added_count = 0
    for rec in ADDITIONAL_GRAMMAR_FORMS:
        key = (rec["surface"].casefold(), rec["lemma"].casefold())
        if key not in existing_keys:
            existing_keys.add(key)
            rows.append(rec)
            added_count += 1

    rows.sort(key=lambda r: (r["surface"].casefold(), r.get("lemma", "").casefold()))

    with MASTER_INDEX_PATH.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Successfully added {added_count} new grammar forms!")
    print(f"New Total Master Index Rows: {len(rows):,}")
    print("===========================================================")

if __name__ == "__main__":
    run_expansion()
