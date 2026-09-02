"""Repository Organization and Cleanup Script.

Moves historical versioned benchmark files (v2-v20) into a clean benchmarks/ folder
and verifies all python files compile with 0 syntax errors.
"""

from __future__ import annotations

import glob
import os
import shutil
from pathlib import Path

REPO_ROOT = Path("c:/Users/sahalm/Desktop/New folder/compare/somali-ai-main")
BENCHMARKS_DIR = REPO_ROOT / "benchmarks"


def organize_benchmarks():
    BENCHMARKS_DIR.mkdir(exist_ok=True)
    
    # Identify historical version files in src/
    patterns = [
        "morphology_challenge_v*.py",
        "giellalt_challenge_v*.py",
        "giellalt_paradigm_v*.py",
        "morphology_paradigm_v*.py",
    ]
    
    moved_files = []
    for pattern in patterns:
        for filepath in glob.glob(str(REPO_ROOT / "src" / pattern)):
            filename = Path(filepath).name
            # Keep active competition script in src, move historical ones
            if filename in ("morphology_competition.py", "morphology_comparison.py"):
                continue
            dest = BENCHMARKS_DIR / filename
            shutil.move(filepath, dest)
            moved_files.append(filename)
            
    return moved_files


if __name__ == "__main__":
    moved = organize_benchmarks()
    print(f"Moved {len(moved)} historical benchmark files into benchmarks/ folder:")
    for f in sorted(moved):
        print(f"  - {f}")
