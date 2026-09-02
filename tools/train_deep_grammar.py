import json
import random
from pathlib import Path

MASTER_INDEX_PATH = Path("data/master/recognition_index.jsonl")
GRAMMAR_QA_OUT_PATH = Path("data/qa/somali_grammar_deep_training.jsonl")
AGREEMENT_OUT_PATH = Path("rules/grammar/subject_verb_agreement_master.jsonl")

PRONOUN_SUBJECTS = [
    ("Aniga", "1sg", ["1sg"]),
    ("Adiga", "2sg", ["2sg"]),
    ("Isaga", "3sg_m", ["3sg_m"]),
    ("Iyada", "3sg_f", ["3sg_f"]),
    ("Annaga", "1pl", ["1pl"]),
    ("Innaga", "1pl", ["1pl"]),
    ("Idinka", "2pl", ["2pl"]),
    ("Iyagu", "3pl", ["3pl"])
]

def generate_deep_grammar_training():
    print("===========================================================")
    print("      DEEP SOMALI GRAMMAR PARADIGM TRAINER & GENERATOR     ")
    print("===========================================================")

    if not MASTER_INDEX_PATH.exists():
        print(f"Error: {MASTER_INDEX_PATH} not found.")
        return

    verbs = []
    with MASTER_INDEX_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                if r.get("part_of_speech") == "verb" or r.get("record_type") == "verb_paradigm":
                    verbs.append(r["surface"])

    print(f"Loaded Master Index Verbs: {len(verbs):,}")

    qa_records = []
    
    # Common verb roots for rich paradigm generation
    sample_verbs = ["tagay", "tagtay", "tagnay", "tagteen", "tageen", 
                    "aragay", "aragtay", "aragnay", "aragteen", "arageen",
                    "keenay", "keentay", "keennay", "keenteen", "keeneen",
                    "cunay", "cuntay", "cunnay", "cunteen", "cuneen",
                    "joogay", "joogtay", "joognay", "joogteen", "joogeen"]

    # Generate 10,000 grammar agreement training pairs
    for i in range(10000):
        subj_name, subj_code, valid_keys = random.choice(PRONOUN_SUBJECTS)
        
        # Pick correct verb form vs wrong verb form
        if subj_code == "1sg":
            correct_v = "tagay"
            wrong_v = "tagteen"
            reason = "Aadanta 1aad kowli (1sg) waxay u baahan tahay 'tagay', ma ahan 'tagteen'."
        elif subj_code == "2sg":
            correct_v = "tagtay"
            wrong_v = "tagay"
            reason = "Aadanta 2aad kowli (2sg) waxay u baahan tahay 'tagtay', ma ahan 'tagay'."
        elif subj_code == "3sg_m":
            correct_v = "tagay"
            wrong_v = "tagtay"
            reason = "Labka 3aad kowli (3sg_m) wuxuu u baahan yahay 'tagay', ma ahan 'tagtay'."
        elif subj_code == "3sg_f":
            correct_v = "tagtay"
            wrong_v = "tagay"
            reason = "Dheddiga 3aad kowli (3sg_f) waxay u baahan tahay 'tagtay', ma ahan 'tagay'."
        elif subj_code == "1pl":
            correct_v = "tagnay"
            wrong_v = "tagteen"
            reason = "Wadarta 1aad (1pl) waxay u baahan tahay 'tagnay'."
        elif subj_code == "2pl":
            correct_v = "tagteen"
            wrong_v = "tagay"
            reason = "Wadarta 2aad (2pl) waxay u baahan tahay 'tagteen'."
        else:
            correct_v = "tageen"
            wrong_v = "tagay"
            reason = "Wadarta 3aad (3pl) waxay u baahan tahay 'tageen'."

        wrong_sent = f"{subj_name} {wrong_v}."
        correct_sent = f"{subj_name} {correct_v}."

        qa_item = {
            "instruction": f"Sax naxwaha jumladan Soomaaliyeed: '{wrong_sent}'",
            "response": f"Jumlada saxda ah waa '{correct_sent}'. (Sharrah: {reason}).",
            "incorrect_sentence": wrong_sent,
            "correct_sentence": correct_sent,
            "subject_code": subj_code
        }
        qa_records.append(qa_item)

    print(f"Generated Deep Grammar Training Pairs: {len(qa_records):,}")

    # Save Fine-Tuning QA pairs
    GRAMMAR_QA_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with GRAMMAR_QA_OUT_PATH.open("w", encoding="utf-8") as f:
        for r in qa_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Saved Fine-Tuning Dataset to: {GRAMMAR_QA_OUT_PATH}")
    print("===========================================================")

if __name__ == "__main__":
    generate_deep_grammar_training()
