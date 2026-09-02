import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.checker import check_text, load_rules
from src.subject_focus_agreement import analyze_subject_focus_agreement

class NeuroSymbolicGrammarGuardrail:
    """Real-Time Grammar & Focus Agreement Guardrail for LLM Text Outputs."""

    def __init__(self) -> None:
        self.rules = load_rules(Path("rules/orthography"))

    def sanitize_llm_output(self, text: str) -> dict:
        """Inspects and auto-corrects LLM generated Somali text in real time."""
        findings = check_text(text, self.rules)
        agreement = analyze_subject_focus_agreement(text)

        cleaned_text = text
        corrected_count = 0

        # Auto-correct orthography findings
        for f in findings:
            if hasattr(f, "suggestions") and f.suggestions:
                best_sug = f.suggestions[0]
                cleaned_text = re.sub(r"\b" + re.escape(f.word) + r"\b", best_sug, cleaned_text)
                corrected_count += 1

        is_grammatically_sound = len(findings) == 0 and agreement.agrees

        return {
            "original_text": text,
            "sanitized_text": cleaned_text,
            "is_grammatically_sound": is_grammatically_sound,
            "orthography_errors_found": len(findings),
            "subject_focus_agrees": agreement.agrees,
            "auto_corrections_made": corrected_count
        }

if __name__ == "__main__":
    guardrail = NeuroSymbolicGrammarGuardrail()
    sample_llm_text = "Ninkii gabadha wuu arkay."
    res = guardrail.sanitize_llm_output(sample_llm_text)
    print("===========================================================")
    print("   SOMALI AI REAL-TIME LLM NEURO-SYMBOLIC GUARDRAIL DEMO  ")
    print("===========================================================")
    print("Original Text:       ", res["original_text"])
    print("Sanitized Text:      ", res["sanitized_text"])
    print("Grammatically Sound: ", res["is_grammatically_sound"])
    print("Subject-Focus Agrees:", res["subject_focus_agrees"])
    print("===========================================================")
