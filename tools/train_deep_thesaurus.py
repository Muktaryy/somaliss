import json
from pathlib import Path

THESAURUS_PATH = Path("data/vocabulary/somali_thesaurus.jsonl")
QA_THESAURUS_OUT_PATH = Path("data/qa/somali_thesaurus_deep_training.jsonl")

DEEP_THESAURUS_DATA = [
    {"word": "nolol", "category": "nature", "synonyms": ["noolal", "caafimaad", "raynrayn", "uumi"], "antonyms": ["dhimasho", "geeri"]},
    {"word": "farxad", "category": "emotion", "synonyms": ["raynrayn", "bashaal", "guul", "gobnimo"], "antonyms": ["tiiraanyo", "murug", "calool-xumo"]},
    {"word": "magaalo", "category": "geography", "synonyms": ["caasimad", "xarun", "deegaan"], "antonyms": ["baadiyo", "baadiye", "miyi"]},
    {"word": "aqoon", "category": "knowledge", "synonyms": ["cilmi", "garasho", "xikmad", "fahmo"], "antonyms": ["jahli", "moogaansho", "aqoon-dro"]},
    {"word": "tagay", "category": "movement", "synonyms": ["baxay", "dhaqaaqay", "geeddi-galay"], "antonyms": ["yimid", "joogay", "soo-laabtay"]},
    {"word": "cunay", "category": "action", "synonyms": ["qadtay", "calashay", "liqay"], "antonyms": ["soomay", "cuntada-diiday"]},
    {"word": "aragay", "category": "perception", "synonyms": ["dheegay", "muuqday", "dhaaday"], "antonyms": ["indho-la'aaday", "waayay"]},
    {"word": "adag", "category": "attribute", "synonyms": ["geesi", "khatar", "culus", "dhib-badan"], "antonyms": ["fudud", "jool-yar", "nool"]},
    {"word": "weyn", "category": "size", "synonyms": ["balaadh", "tiro-badan", "sareyo"], "antonyms": ["yar", "kooban", "dhuuban"]},
    {"word": "cad", "category": "color", "synonyms": ["dhalaalaya", "ileys", "muran-la'aan"], "antonyms": ["madow", "gudcur", "mugdi"]},
    {"word": "sare", "category": "position", "synonyms": ["qaybta-sare", "kor", "gullaam"], "antonyms": ["hoose", "hoos"]},
    {"word": "guul", "category": "status", "synonyms": ["libasho", "guuleysi", "horyaalnimo"], "antonyms": ["guuldarro", "qasaaro", "jab"]},
    {"word": "geesi", "category": "virtue", "synonyms": ["dhiirran", "haley", "libaan-qabe"], "antonyms": ["fuley", "baqdin-badan"]},
    {"word": "wanaagsan", "category": "virtue", "synonyms": ["salam", "fiican", "qurux-badan"], "antonyms": ["xun", "xumaan"]},
    {"word": "hodan", "category": "status", "synonyms": ["taneeyay", "hantida-badan", "qani"], "antonyms": ["sabool", "faqiir", "baahan"]},
    {"word": "sabool", "category": "status", "synonyms": ["faqiir", "baahan", "dhibban"], "antonyms": ["hodan", "qani", "tanayeeyay"]},
    {"word": "nabad", "category": "society", "synonyms": ["xasilooni", "daganaansho", "wada-noolansho"], "antonyms": ["dagaal", "colaad", "fitno"]},
    {"word": "dagaal", "category": "society", "synonyms": ["colaad", "fitno", "dirir"], "antonyms": ["nabad", "xasilooni", "dhexnimo"]},
    {"word": "dhakhso", "category": "time", "synonyms": ["deed", "dhaqso", "dhaqsaha", "degdeg"], "antonyms": ["tartiib", "gaabin"]},
    {"word": "tartiib", "category": "time", "synonyms": ["gaabin", "qunyar", "dawaaf"], "antonyms": ["dhakhso", "degdeg"]},
    {"word": "caqli", "category": "knowledge", "synonyms": ["fahmo", "garaad", "maan", "xikmad"], "antonyms": ["nacasnimo", "dalluun"]},
    {"word": "qaali", "category": "attribute", "synonyms": ["qiimo-badan", "sharaf-leh", "gacalo"], "antonyms": ["raqiis", "jaban"]},
    {"word": "raqiis", "category": "attribute", "synonyms": ["jaban", "qiimo-yar"], "antonyms": ["qaali", "qiimo-badan"]},
    {"word": "curad", "category": "family", "synonyms": ["wuxuu-ugu-horreeyaa", "wiilka-koowaad"], "antonyms": ["yaraangad", "yaraancuud"]},
    {"word": "gabadh", "category": "family", "synonyms": ["gabar", "huuno", "gabayasho"], "antonyms": ["wiil", "inabax"]},
    {"word": "wiil", "category": "family", "synonyms": ["inabax", "inill", "kibriya"], "antonyms": ["gabadh", "gabar"]}
]

def run_deep_thesaurus_training():
    print("===========================================================")
    print("      DEEP SOMALI THESAURUS TRAINER & QA GENERATOR         ")
    print("===========================================================")

    # Write Master Thesaurus File
    THESAURUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with THESAURUS_PATH.open("w", encoding="utf-8") as f:
        for r in DEEP_THESAURUS_DATA:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Saved Deep Master Thesaurus Dataset ({len(DEEP_THESAURUS_DATA)} words): {THESAURUS_PATH}")

    # Generate Fine-Tuning QA pairs
    qa_records = []
    for r in DEEP_THESAURUS_DATA:
        w = r["word"]
        syns = ", ".join(r["synonyms"])
        ants = ", ".join(r["antonyms"])

        # Synonyms QA (using authentic Somali phrasing 'la macnaha ah' & 'isku macnaha ah')
        qa_records.append({
            "instruction": f"Waa maxay ereyada la macnaha ah (synonyms) ereyga '{w}'?",
            "response": f"Ereyada la macnaha ah ereyga '{w}' waxaa ka mid ah: {syns}.",
            "word": w,
            "type": "synonyms"
        })

        # Antonyms QA
        qa_records.append({
            "instruction": f"Waa maxay ereyada kasoo horjeeda (antonyms) ereyga '{w}'?",
            "response": f"Ereyada kasoo horjeeda (antonyms) ereyga '{w}' waxaa ka mid ah: {ants}.",
            "word": w,
            "type": "antonyms"
        })

    QA_THESAURUS_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with QA_THESAURUS_OUT_PATH.open("w", encoding="utf-8") as f:
        for q in qa_records:
            f.write(json.dumps(q, ensure_ascii=False) + "\n")

    print(f"Generated Thesaurus Fine-Tuning QA Pairs: {len(qa_records)}")
    print(f"Saved Fine-Tuning QA Dataset to: {QA_THESAURUS_OUT_PATH}")
    print("===========================================================")

if __name__ == "__main__":
    run_deep_thesaurus_training()
