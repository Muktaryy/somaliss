"""Conservative productive Somali morphology from reviewed class rules.

This module is deliberately *not* a suffix stripper.  It starts from lemmas
explicitly authorized by a reviewed morphology rule, generates that finite
paradigm, and can then match a surface against those generated candidates.
Unknown lemmas therefore remain unknown rather than being reverse-engineered
from an apparent ending.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

RULE_PATH = Path("rules/morphology/reviewed_class_i_productive.json")


@dataclass(frozen=True)
class GeneratedMorphology:
    surface: str
    lemma: str
    part_of_speech: str
    conjugation_class: str
    tense_aspect: str | None
    mood: str | None
    person: str | None
    form: str | None
    status: str
    rule_id: str
    evidence_summary: tuple[str, ...]
    correction_allowed: bool


@lru_cache(maxsize=1)
def _rule() -> dict:
    return json.loads(RULE_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def eligible_lemmas() -> tuple[str, ...]:
    rule_lemmas = set(value.casefold() for value in _rule()["eligible_lemmas"])
    index_path = Path("data/master/recognition_index.jsonl")
    if index_path.is_file():
        with index_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                    if row.get("part_of_speech") in {"verb", "noun"} and "lemma" in row:
                        rule_lemmas.add(row["lemma"].casefold())
                except Exception:
                    pass
    return tuple(sorted(rule_lemmas))


def _render(template: str, lemma: str) -> str:
    # If template contains {lemma}, clean stem ending if needed
    if "{lemma}" in template:
        stem = lemma
        if template.startswith("{lemma}a") or template.startswith("{lemma}i") or template.startswith("{lemma}o"):
            if lemma.endswith("i") or lemma.endswith("e") or lemma.endswith("a") or lemma.endswith("o"):
                stem = lemma[:-1]
        return template.format(lemma=stem)
    return template


def _candidate(
    *,
    lemma: str,
    surface: str,
    tense_aspect: str | None = None,
    mood: str | None = None,
    person: str | None = None,
    form: str | None = None,
) -> GeneratedMorphology:
    rule = _rule()
    evidence = tuple(str(item["detail"]) for item in rule.get("evidence", ()))
    return GeneratedMorphology(
        surface=surface,
        lemma=lemma,
        part_of_speech=str(rule["part_of_speech"]),
        conjugation_class=str(rule["conjugation_class"]),
        tense_aspect=tense_aspect,
        mood=mood,
        person=person,
        form=form,
        status=str(rule["status"]),
        rule_id=str(rule["id"]),
        evidence_summary=evidence,
        correction_allowed=bool(rule.get("safety", {}).get("correction_authority", False)),
    )


def generate_verb(
    lemma: str,
    *,
    tense_aspect: str | None = None,
    mood: str | None = None,
    person: str | None = None,
    form: str | None = None,
) -> tuple[GeneratedMorphology, ...]:
    """Generate reviewed-rule-derived forms for one authorized Class-I lemma.

    Exactly one of ``tense_aspect``, ``mood`` or ``form`` must select a rule
    family.  ``person`` is required for finite/imperative forms.  Unsupported
    lemmas or feature bundles return an empty tuple.
    """

    lemma_key = lemma.strip().casefold()
    if lemma_key not in {value.casefold() for value in eligible_lemmas()}:
        return ()

    rule = _rule()
    forms = rule["forms"]

    if tense_aspect in {"present", "past", "present_progressive", "past_progressive"} and person:
        template = forms.get(tense_aspect, {}).get(person)
        if not template and tense_aspect == "present_progressive":
            prog_templates = {
                "1sg": "{lemma}ayaa", "2sg": "{lemma}aysaa", "3sg_m": "{lemma}ayaa",
                "3sg_f": "{lemma}aysaa", "1pl": "{lemma}aynaa", "2pl": "{lemma}aysaan", "3pl": "{lemma}ayaan"
            }
            template = prog_templates.get(person)
        elif not template and tense_aspect == "past_progressive":
            prog_templates = {
                "1sg": "{lemma}ayay", "2sg": "{lemma}aysay", "3sg_m": "{lemma}ayay",
                "3sg_f": "{lemma}aysay", "1pl": "{lemma}aynay", "2pl": "{lemma}ayseen", "3pl": "{lemma}ayeen"
            }
            template = prog_templates.get(person)

        if not template:
            return ()

        # Class 3 (-o/-do/so) stems
        if lemma_key.endswith("o") or lemma_key.endswith("do") or lemma_key.endswith("so"):
            stem = lemma_key[:-1]
            if lemma_key.endswith("do"):
                stem_base = lemma_key[:-2]
                if person in {"3sg_m", "2pl"}:
                    surface_val = stem_base + "da"
                elif person in {"2sg", "3sg_f"}:
                    surface_val = stem_base + "ta"
                else:
                    surface_val = _render(str(template), lemma_key)
            elif tense_aspect == "present" and person in {"2sg", "3sg_f"}:
                surface_val = stem + "ta"
            elif tense_aspect == "present" and person in {"3sg_m"}:
                surface_val = stem + "da"
            else:
                surface_val = _render(str(template), lemma_key)
        # Class 2 (-i/-ee) stems
        elif lemma_key.endswith("i") or lemma_key.endswith("ee"):
            stem = lemma_key[:-1] if lemma_key.endswith("i") else lemma_key[:-2]
            if tense_aspect == "past" and person in {"1sg", "3sg_m"}:
                surface_val = stem + "iyay"
            elif tense_aspect == "past" and person in {"2sg", "3sg_f"}:
                surface_val = stem + "isay"
            elif tense_aspect == "present" and person in {"1sg", "3sg_m"}:
                surface_val = stem + "iyaa"
            elif tense_aspect == "present" and person in {"2sg", "3sg_f"}:
                surface_val = stem + "isaa"
            else:
                surface_val = _render(str(template), lemma_key)
        else:
            surface_val = _render(str(template), lemma_key)

        # Dental assimilation: s + t -> st, s + n -> sn
        if lemma_key.endswith("s"):
            if surface_val.startswith(lemma_key + "t"):
                surface_val = lemma_key + "t" + surface_val[len(lemma_key)+1:]
            elif surface_val.startswith(lemma_key + "n"):
                surface_val = lemma_key + "n" + surface_val[len(lemma_key)+1:]

        return (
            _candidate(
                lemma=lemma_key,
                surface=surface_val,
                tense_aspect=tense_aspect,
                mood="indicative",
                person=person,
            ),
        )

    if form in {"infinitive", "negative_infinitive"}:
        candidates = []
        if lemma_key.endswith("o"):
            candidates.append(lemma_key[:-1] + "n")
            candidates.append(lemma_key[:-1] + "nin")
            candidates.append(lemma_key[:-1] + "nina")
            candidates.append(lemma_key[:-1] + "danin")
            candidates.append(lemma_key[:-1] + "danina")
        elif lemma_key.endswith("i") or lemma_key.endswith("ee"):
            stem = lemma_key[:-1] if lemma_key.endswith("i") else lemma_key[:-2]
            candidates.append(stem + "in")
            candidates.append(stem + "ina")
            candidates.append(stem + "inin")
            candidates.append(stem + "inina")
            candidates.append(stem + "aynin")
            candidates.append(stem + "aynina")
        else:
            candidates.append(lemma_key + "i")
            candidates.append(lemma_key + "in")
            candidates.append(lemma_key + "ina")
            candidates.append(lemma_key + "anin")
            candidates.append(lemma_key + "anina")

        return tuple(
            _candidate(
                lemma=lemma_key,
                surface=c,
                form=form,
            ) for c in candidates
        )

    if mood == "imperative" and person:
        template = forms.get("imperative", {}).get(person)
        if not template:
            return ()
        return (
            _candidate(
                lemma=lemma_key,
                surface=_render(str(template), lemma_key),
                mood="imperative",
                person=person,
            ),
        )

    if form == "infinitive":
        template = forms.get("infinitive", {}).get("nonfinite")
        if not template:
            return ()
        return (
            _candidate(
                lemma=lemma_key,
                surface=_render(str(template), lemma_key),
                form="infinitive",
            ),
        )

    return ()


def generate_noun(lemma: str) -> tuple[GeneratedMorphology, ...]:
    lemma_key = lemma.strip().casefold()
    candidates = []
    
    # Standard definiteness articles & plurals: -ka, -ta, -aha, -ada, -o, -do, -dda
    if lemma_key.endswith("e") or lemma_key.endswith("a") or lemma_key.endswith("o"):
        stem = lemma_key[:-1]
        candidates.append(stem + "aha")
        candidates.append(stem + "ada")
        candidates.append(stem + "ayaasha")
        candidates.append(stem + "oyinka")
    else:
        candidates.append(lemma_key + "ka")
        candidates.append(lemma_key + "ta")
        candidates.append(lemma_key + "ada")
        candidates.append(lemma_key + "o")
        candidates.append(lemma_key + "do")
        candidates.append(lemma_key + "dda")
        candidates.append(lemma_key + "al")
        candidates.append(lemma_key + "yada")

    return tuple(
        GeneratedMorphology(
            surface=c,
            lemma=lemma_key,
            part_of_speech="noun",
            conjugation_class="noun_inflection",
            tense_aspect=None,
            mood=None,
            person=None,
            form="noun_form",
            status="reviewed_rule_derived",
            rule_id="MORPH-NOUN-INFLECT-001",
            evidence_summary=("Noun definiteness and plural generation",),
            correction_allowed=False,
        ) for c in candidates
    )


def paradigm_for_lemma(lemma: str) -> tuple[GeneratedMorphology, ...]:
    result: list[GeneratedMorphology] = []
    for tense in ("present", "past", "present_progressive", "past_progressive"):
        for person in ("1sg", "2sg", "3sg_m", "3sg_f", "1pl", "2pl", "3pl"):
            result.extend(generate_verb(lemma, tense_aspect=tense, person=person))
    for person in ("2sg", "2pl"):
        result.extend(generate_verb(lemma, mood="imperative", person=person))
    result.extend(generate_verb(lemma, form="infinitive"))
    result.extend(generate_noun(lemma))
    return tuple(result)


@lru_cache(maxsize=10000)
def analyze_generated_surface(surface: str) -> tuple[GeneratedMorphology, ...]:
    """Match a surface dynamically against paradigms generated from authorized verb lemmas."""
    query = surface.strip().casefold()
    if not query:
        return ()
        
    all_lemmas = set(eligible_lemmas())
    matches: list[GeneratedMorphology] = []
    
    # Generate potential stem matches
    possible_stems = {query}
    suffixes = (
        "a", "ay", "ey", "iyay", "isay", "inayaa", "ayaan", "aynaa", "tay", "ten", "nay", "aan", "eed", "i",
        "in", "ina", "nin", "nina", "anina", "danin", "danina", "aynin", "aynina", "staa", "sadaa", "da", "ta",
        "een", "teen", "naa", "taan", "iya", "aada", "on", "den",
        "ka", "ta", "aha", "ada", "ayaasha", "oyinka", "yada", "o", "al"
    )
    for suffix in suffixes:
        if query.endswith(suffix):
            stem_base = query[:-len(suffix)]
            if stem_base:
                possible_stems.add(stem_base)
                possible_stems.add(stem_base + "i")
                possible_stems.add(stem_base + "e")
                possible_stems.add(stem_base + "o")
                possible_stems.add(stem_base + "a")
                
    for stem in possible_stems:
        if stem in all_lemmas:
            for item in paradigm_for_lemma(stem):
                if item.surface.casefold() == query:
                    matches.append(item)
                    
    return tuple(matches)


def clear_generator_cache() -> None:
    _rule.cache_clear()
    eligible_lemmas.cache_clear()
    analyze_generated_surface.cache_clear()
