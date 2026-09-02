import json
from pathlib import Path

MASTER_INDEX_PATH = Path("data/master/recognition_index.jsonl")

def clean_master_index():
    print("===========================================================")
    print("        SOMALI AI MASTER INDEX DEDUPLICATION & CLEANUP      ")
    print("===========================================================")

    if not MASTER_INDEX_PATH.is_file():
        print(f"Error: {MASTER_INDEX_PATH} not found.")
        return

    with MASTER_INDEX_PATH.open("r", encoding="utf-8") as handle:
        rows = [json.loads(line) for line in handle if line.strip()]

    print(f"Original Row Count: {len(rows)}")

    dedup_map = {}
    for row in rows:
        surf = row.get("surface")
        lem = row.get("lemma")
        pos = row.get("part_of_speech")
        key = (surf, lem, pos)

        if key not in dedup_map:
            dedup_map[key] = row
        else:
            existing = dedup_map[key]
            # Preference hierarchy for status
            status_rank = {"reviewed": 3, "supported": 2, "provisional": 1, "context_required": 0}
            existing_rank = status_rank.get(existing.get("status"), 0)
            new_rank = status_rank.get(row.get("status"), 0)

            if new_rank > existing_rank:
                dedup_map[key] = row
            else:
                # Combine sources cleanly
                existing_sources = existing.get("sources", [])
                new_sources = row.get("sources", [])
                combined_sources = existing_sources + [s for s in new_sources if s not in existing_sources]
                existing["sources"] = combined_sources

    cleaned_rows = list(dedup_map.values())
    cleaned_rows.sort(key=lambda r: (str(r.get("surface")).casefold(), str(r.get("lemma")).casefold()))

    print(f"Cleaned Row Count: {len(cleaned_rows)} (Removed {len(rows) - len(cleaned_rows)} duplicates)")

    with MASTER_INDEX_PATH.open("w", encoding="utf-8") as handle:
        for row in cleaned_rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"Successfully cleaned and deduplicated {MASTER_INDEX_PATH}!")
    print("===========================================================")

if __name__ == "__main__":
    clean_master_index()
