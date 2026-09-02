"""Somali AI Auto-Writer & Auto-Corrector Engine.

Combines Dictionary Spelling Auto-Correction, Orthography Rules,
and Grammatical Agreement Correction into a single unified pipeline.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# Ensure root directory is on sys.path
root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.checker import check_text, load_rules
from src.sentence_agreement import scan_sentence_agreement
from src.spelling_engine import SomaliSpellChecker

ORTHOGRAPHY_RULES_PATH = Path("rules/orthography")

class SomaliAutoCorrector:
    """Unified Auto-Corrector & Writer for Standard Somali Text."""

    def __init__(self) -> None:
        self.spell_checker = SomaliSpellChecker()
        self.ortho_rules = load_rules(ORTHOGRAPHY_RULES_PATH)

    def auto_correct_passage(self, passage: str) -> dict:
        """Pipeline auto-corrector: Spelling (dict-only) -> Orthography -> Grammar."""
        if not passage.strip():
            return {
                "original_text": passage,
                "corrected_text": passage,
                "total_corrections": 0,
                "corrections_log": []
            }

        corrections_log = []
        words = passage.split()
        spelled_words = []

        # Step 1: Dictionary-Grounded Spelling Auto-Correction (Only fix unrecognized typos!)
        for original in words:
            clean = re.sub(r"[^\w\'-]", "", original).casefold()
            if not clean or self.spell_checker.is_correct(clean):
                spelled_words.append(original)
            else:
                sugs = self.spell_checker.suggest_corrections(clean, top_n=1)
                best_sug = sugs[0][0] if sugs else original
                if original.istitle():
                    best_sug = best_sug.capitalize()
                
                spelled_words.append(best_sug)
                corrections_log.append({
                    "stage": "spelling",
                    "original": original,
                    "corrected": best_sug,
                    "rule": "Phonetic Typo Corrector"
                })

        current_text = " ".join(spelled_words)

        # Step 2: Orthography Auto-Correction (Capitalization, Weekdays, Months, Spacing)
        ortho_findings = check_text(current_text, self.ortho_rules)

        for finding in ortho_findings:
            if finding.status not in {"ambiguous", "context_required"} and finding.suggestion:
                old_text = finding.matched_text
                new_text = finding.suggestion
                
                if old_text in current_text:
                    current_text = current_text.replace(old_text, new_text, 1)
                    corrections_log.append({
                        "stage": "orthography",
                        "original": old_text,
                        "corrected": new_text,
                        "rule": finding.rule_id
                    })

        # Step 3: Grammar Agreement Auto-Correction
        grammar_findings = scan_sentence_agreement(current_text)
        for g_finding in grammar_findings:
            if g_finding.expected_forms:
                best_expected = g_finding.expected_forms[0]
                if g_finding.verb in current_text:
                    current_text = current_text.replace(g_finding.verb, best_expected, 1)
                    corrections_log.append({
                        "stage": "grammar",
                        "original": g_finding.verb,
                        "corrected": best_expected,
                        "rule": "Subject-Verb Agreement"
                    })

        return {
            "original_text": passage,
            "corrected_text": current_text,
            "total_corrections": len(corrections_log),
            "corrections_log": corrections_log
        }

if __name__ == "__main__":
    corrector = SomaliAutoCorrector()
    print("==========================================================================")
    print("     SOMALI AI UNIFIED AUTO-WRITER & AUTO-CORRECTOR DEMO                  ")
    print("==========================================================================")

    test_samples = [
        "ninkii wuxuu yimid hargeysa axad ka dibna wuu tagay.",
        "gabadh ta waxay timaadday maahmah ka tiri.",
        "Aniga tagteen hargeysa maanta.",
        "Iyada tagay muqdisho oo maahmah ka tiri."
    ]

    for idx, sample in enumerate(test_samples, 1):
        res = corrector.auto_correct_passage(sample)
        print(f"\n[{idx}] INPUT:  \"{res['original_text']}\"")
        print(f"    OUTPUT: \"{res['corrected_text']}\"")
        print(f"    Total Auto-Corrections: {res['total_corrections']}")
        for c in res["corrections_log"]:
            print(f"      * [{c['stage'].upper()}] '{c['original']}' -> '{c['corrected']}' ({c['rule']})")

    print("\n==========================================================================")
