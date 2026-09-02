"""Test Organization Script.

Moves historical versioned test files (v2-v20) into a clean benchmarks/tests/ folder.
"""

from __future__ import annotations

import glob
import shutil
from pathlib import Path

REPO_ROOT = Path("c:/Users/sahalm/Desktop/New folder/compare/somali-ai-main")
BENCHMARK_TESTS_DIR = REPO_ROOT / "benchmarks" / "tests"


def organize_test_files():
    BENCHMARK_TESTS_DIR.mkdir(parents=True, exist_ok=True)
    
    patterns = [
        "test_morphology_challenge_v*.py",
        "test_morphology_paradigm_v*.py",
    ]
    
    moved_files = []
    for pattern in patterns:
        for filepath in glob.glob(str(REPO_ROOT / "tests" / pattern)):
            filename = Path(filepath).name
            dest = BENCHMARK_TESTS_DIR / filename
            shutil.move(filepath, dest)
            moved_files.append(filename)
            
    return moved_files


if __name__ == "__main__":
    moved = organize_test_files()
    print(f"Moved {len(moved)} historical test files into benchmarks/tests/ folder:")
    for f in sorted(moved):
        print(f"  - {f}")
