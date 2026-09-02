import json
import re
from pathlib import Path

CORPUS_JSON_PATH = Path("data/corpus/maahmaahyo.json")
MASTER_OUT_PATH = Path("data/proverbs/somali_maahmaahyo_master.jsonl")

def clean_proverb_text(text: str) -> str:
    """Cleans leading numbers (e.g., '1. ') and inline footnote markers (e.g., '(1)')."""
    # Remove leading line number e.g. "1. " or "123. "
    cleaned = re.sub(r"^\d+\.\s*", "", text).strip()
    # Remove footnote markers e.g. "(1)", "(2)"
    cleaned = re.sub(r"\(\d+\)", "", cleaned).strip()
    # Normalize multiple spaces
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned

def deduce_theme_and_pattern(text: str) -> tuple[str, str]:
    """Deduces proverb pattern and thematic category from text structure."""
    lower = text.casefold()
    pattern = "wise_observation"
    theme = "general_wisdom"

    if " waa " in lower:
        pattern = "metaphor"
    elif " ma " in lower or " aan " in lower or " nimaan " in lower:
        pattern = "conditional_contrast"
    elif " baa " in lower or " ayaa " in lower or " waxay " in lower:
        pattern = "cause_effect"
    elif " sida " in lower or " ka " in lower or " uga " in lower:
        pattern = "comparison"

    if any(k in lower for k in ["aqoon", "waxbarasho", "cilmi", "garad"]):
        theme = "aqoon"
    elif any(k in lower for k in ["rag", "nimo", "hanta", "shaqo", "geel", "dadaal"]):
        theme = "dadaal"
    elif any(k in lower for k in ["wadaag", "garab", "hiil", "wadajir", "xigaal"]):
        theme = "wadajir"
    elif any(k in lower for k in ["sabr", "dulqaad", "samir", "aakhiro"]):
        theme = "sabr"
    elif any(k in lower for k in ["af ", "hadal", "erey", "dahab", "sheeg"]):
        theme = "hadal"

    return theme, pattern

def run_import():
    print("===========================================================")
    print("      SOMALI PROVERBS (MAAHMAAHYO) MASTER IMPORTER         ")
    print("===========================================================")

    if not CORPUS_JSON_PATH.exists():
        print(f"Error: {CORPUS_JSON_PATH} not found.")
        return

    with CORPUS_JSON_PATH.open("r", encoding="utf-8") as f:
        raw_items = json.load(f)

    print(f"Raw Proverbs Count in {CORPUS_JSON_PATH}: {len(raw_items):,}")

    proverbs_map = {}
    for item in raw_items:
        clean_text = clean_proverb_text(str(item))
        if clean_text and len(clean_text) > 3:
            first_letter = clean_text[0].upper()
            theme, pattern = deduce_theme_and_pattern(clean_text)
            
            record = {
                "maahmaah": clean_text,
                "first_letter": first_letter,
                "theme": theme,
                "structure": pattern,
                "explanation_so": f"Maahmaah Soomaaliyeed oo tilmaamaysa {theme} iyo xikmadda dhabta ah.",
                "explanation_en": f"A traditional Somali proverb reflecting wisdom on {theme}."
            }
            proverbs_map[clean_text.casefold()] = record

    cleaned_records = list(proverbs_map.values())
    cleaned_records.sort(key=lambda r: r["maahmaah"].casefold())

    print(f"Cleaned Unique Proverbs to Write: {len(cleaned_records):,}")

    MASTER_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MASTER_OUT_PATH.open("w", encoding="utf-8") as f:
        for r in cleaned_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Successfully saved {len(cleaned_records):,} proverbs to {MASTER_OUT_PATH}!")
    print("===========================================================")

if __name__ == "__main__":
    run_import()
