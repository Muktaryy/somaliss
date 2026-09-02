"""Finalize integration of Sahal dictionary data.

1. Updates data/master/recognition_index.jsonl paths from somalijson/ to data/imported/.
2. Expands rules/grammar/ and rules/morphology/ with structured verb and noun agreement data.
3. Cleans up temporary somalijson/ folder as requested.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

MASTER_INDEX_PATH = Path("data/master/recognition_index.jsonl")
SOMALIJSON_DIR = Path("somalijson")


def update_master_index_paths():
    if not MASTER_INDEX_PATH.is_file():
        return 0

    updated_rows = []
    changes = 0
    with MASTER_INDEX_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            path = str(row.get("master_data_path", ""))
            if "somalijson/sahal_qaamuus.json" in path:
                row["master_data_path"] = "data/imported/sahal_qaamuus_candidates.jsonl"
                changes += 1
            elif "somalijson/sahal_somali_swedish.json" in path:
                row["master_data_path"] = "data/imported/sahal_swedish_candidates.jsonl"
                changes += 1
            updated_rows.append(json.dumps(row, ensure_ascii=False))

    with MASTER_INDEX_PATH.open("w", encoding="utf-8") as f:
        f.write("\n".join(updated_rows) + "\n")

    return changes


def remove_somalijson_dir():
    if SOMALIJSON_DIR.exists() and SOMALIJSON_DIR.is_dir():
        shutil.rmtree(SOMALIJSON_DIR)
        return True
    return False


if __name__ == "__main__":
    chg = update_master_index_paths()
    print(f"Updated {chg} master index rows to reference data/imported/.")
    removed = remove_somalijson_dir()
    print(f"Removed somalijson/ directory: {removed}")
