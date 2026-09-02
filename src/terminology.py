"""Official Standard Somali Linguistic & NLP Terminology Registry."""

SOMALI_LINGUISTIC_TERMINOLOGY = {
    # Core Language & NLP
    "spelling": "higaad / higaadda",
    "orthography": "higaada saxda ah",
    "spell_check": "saxida higaadda",
    "grammar": "naxwaha iyo erey-dhiska",
    "vocabulary": "ereyada / qaamuuska",
    "dictionary": "qaamuus",
    "lemma_root": "aasaaska ereyga (lemma)",
    "surface_form": "muuqaalka ereyga (surface form)",

    # Parts of Speech (Qaybaha Hadalka)
    "part_of_speech": "qaybta hadalka",
    "noun": "magac",
    "verb": "ficil / fael",
    "adjective": "sifo",
    "pronoun": "magac-u-yaal",
    "conjunction": "xidhiidhiye",
    "preverb": "horgale",
    "particle": "qodob / erey-raacis",
    "clitic": "erey-raacis (clitic)",
    "numeral": "tirsi / tiro",
    "auxiliary_verb": "ficil caawiye",

    # Grammar Rules & Features
    "subject": "mowduuc / maaddo",
    "object": "walax / ujeedo",
    "subject_focus": "xoog-saarista mowduuca (baa / ayaa)",
    "plurals": "wadar",
    "singular": "keli",
    "masculine": "lab",
    "feminine": "dheddig",
    "tense": "waqti / ammaan",
    "present_tense": "waqtiga la joogo",
    "past_tense": "waqtiga tagay",
    "future_tense": "waqtiga soo socda",

    # Oral Literature & Culture
    "proverb": "maahmaah",
    "poetry": "gabay / maanso",
    "alliteration": "hooris / jiib",
    "story": "sheeko / xikmad"
}

def get_somali_term(english_term: str) -> str:
    """Returns official standard Somali linguistic term."""
    return SOMALI_LINGUISTIC_TERMINOLOGY.get(english_term.casefold(), english_term)

def print_terminology_registry():
    print("==========================================================================")
    print("     OFFICIAL STANDARD SOMALI LINGUISTIC TERMINOLOGY REGISTRY              ")
    print("==========================================================================")
    print(f"{'English NLP / Linguistic Term':<32} | {'Official Authentic Somali Term':<38}")
    print("-" * 75)
    for eng, som in SOMALI_LINGUISTIC_TERMINOLOGY.items():
        print(f"  {eng:<32} | {som:<38}")
    print("==========================================================================")

if __name__ == "__main__":
    print_terminology_registry()
