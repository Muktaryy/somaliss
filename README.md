# Somali AI — Somali-First Language Intelligence

An evidence-based Somali language foundation and working Somali-first AI intelligence engine.

The project has two connected goals:

1. Build reliable Somali grammar, morphology, vocabulary, regional-variant, oral literature, and fine-tuning QA knowledge;
2. Combine that foundation with reasoning models and neuro-symbolic guardrails so people can converse, check orthography, generate poetry and proverbs, analyze grammar, compare options, and improve Somali writing.

---

## 📊 Somali AI System Capabilities & Scale

| Metric / Dimension | Scale / Benchmark Score | Description |
| :--- | :---: | :--- |
| **Master Index Surface Forms** | **64,673 Surface Forms** | 100% deduplicated, verified surface spellings in `data/master/recognition_index.jsonl`. |
| **Base Dictionary Roots (Lemmas)** | **47,462 Base Lemmas** | Core lemmatic headwords mapped to inflections and regional profiles. |
| **Morphological Feature Dimensions** | **37 Feature Dimensions** | Full feature coverage (verbs, noun plurals, focus particles, preverbs, subject agreement). |
| **Oral Literature Proverbs (*Maahmaahyo*)** | **1,151 Classic Proverbs** | Dynamically trained dataset of traditional Somali proverbs (`data/proverbs/`). |
| **Spelling & Proverb Instruction Dataset** | **11,151 QA Pairs** | High-quality instruction-tuning pairs for fine-tuning open LLM models (`data/qa/`). |
| **Dedicated Somali BPE Vocabulary** | **65,591 Whole Tokens** | Whole-word Somali BPE tokenizer artifact (`data/vocabulary/somali_ai_bpe_vocab.json`). |

---

## ⚡ High-Speed Lookup & Performance Benchmarks

| Benchmark Metric | Latency / Throughput | Technical Implementation |
| :--- | :---: | :--- |
| **Peak Memory Lookup Latency** | **0.0129 ms / word** *(12.9 Microseconds)* | High-performance memory-mapped JSON hash lookup with `@lru_cache`. |
| **Cold Disk Search Latency** | **0.1238 ms / word** *(123.8 Microseconds)* | Direct $\mathcal{O}(1)$ master index retrieval (`src/master_recognition.py`). |
| **Single-Thread Peak Throughput** | **77,500 Words / Second** | Fast in-memory execution with zero FST state-graph overhead. |

---

## 📚 Clean Part of Speech (POS) Breakdown (`Qaybaha Hadalka`)

Every entry in the 64,673 master index is categorized into clean, standard linguistic Part of Speech (POS) tags:

| Part of Speech (POS) | Somali Linguistic Term | Entry Count | Percentage | Representative Examples |
| :--- | :--- | :---: | :---: | :--- |
| **Nouns** | **`Magac`** | **38,678** | **59.8%** | `wadaad`, `wadaaddo`, `xiddig`, `qawmiyad`, `gabadha`, `jaajuur`, `silig` |
| **Verbs** | **`Ficil / Fael`** | **21,291** | **32.9%** | `aqaanay`, `baranayay`, `guuleystay`, `joogsaday`, `cunay`, `dheh`, `dubiyaa` |
| **Adjectives** | **`Sifo`** | **4,430** | **6.9%** | `xanaaqsan`, `adag`, `balaadh`, `xarfaaniin`, `dheeraad` |
| **Pronouns** | **`Magac-u-yaal`** | **63** | **0.1%** | `isaga`, `iyada`, `aniga`, `adiga`, `innaga`, `kan`, `tan`, `kuwaas` |
| **Preverbs & Adpositions** | **`Horgale`** | **54** | **0.1%** | `soo` (towards speaker), `sii` (away from speaker), `wada`, `kula` |
| **Numerals** | **`Tirsi`** | **52** | **0.1%** | `kowaad`, `labaad`, `saddexaad`, `kow`, `laba`, `shaan`, `toban` |
| **Focus Particles & Clitics** | **`Qodob / Erey-raacis`** | **56** | **0.1%** | `baa` (restrictive focus), `ayaa`, `waa`, `wuxuu`, `wuu`, `way` |
| **Auxiliary Verbs** | **`Ficil Caawiye`** | **29** | **0.0%** | `yahay` (copula "is"), `tahay`, `ahaa`, `doonaa`, `jiray`, `lahaa` |
| **Conjunctions & Connectives** | **`Xidhiidhiye`** | **24** | **0.0%** | `iyo`, `laakiin`, `balse`, `inkastoo`, `illaa`, `waayo`, `ama`, `mise` |

---

## 📖 Official Standard Somali Linguistic Terminology

Somali AI strictly adheres to authentic Standard Somali linguistic terminology (`src/terminology.py`):

| English NLP / Linguistic Term | Authentic Standard Somali Term | Usage Context |
| :--- | :--- | :--- |
| **Spelling / Orthography** | **`Higaad / Higaada Saxda ah`** | Correct spelling (*higaad*), avoiding literal mistranslations. |
| **Spell Checking** | **`Saxida Higaadda`** | Correcting spelling errors & typos (`src/spelling_engine.py`). |
| **Grammar & Syntax** | **`Naxwaha iyo Erey-dhiska`** | Sentence structure & agreement rules (`check.py`). |
| **Parts of Speech (POS)** | **`Qaybaha Hadalka`** | Lexical classification (Nouns, Verbs, Adjectives, etc.). |
| **Noun** | **`Magac`** | Substantives & proper names. |
| **Verb** | **`Ficil / Fael`** | Class 1-3 verbs and irregular roots. |
| **Adjective** | **`Sifo`** | Quality descriptors & stative attributes. |
| **Pronoun** | **`Magac-u-yaal`** | Personal, demonstrative, and relative pronouns. |
| **Conjunction** | **`Xidhiidhiye`** | Simple conjunctions and compound transition phrases (`hase yeeshee`). |
| **Preverb** | **`Horgale`** | Directional and co-positional preverbal particles (`soo`, `sii`, `wada`). |
| **Particle / Clitic** | **`Qodob / Erey-raacis`** | Subject focus particles (`baa`/`ayaa`) and statement clitics (`wuu`/`way`). |
| **Auxiliary Verb** | **`Ficil Caawiye`** | Tense and mood helpers (`yahay`, `ahaa`, `doonaa`, `jiray`). |
| **Subject Focus** | **`Xoog-saarista Mowduuca`** | Subject-focus agreement rules (`GRAM-SUBJFOCUS-001`). |
| **Proverb** | **`Maahmaah`** | Deep N-gram proverb learning & generation (`src/maahmaah_deep_trainer.py`). |
| **Poetry & Alliteration** | **`Gabay / Maanso` (Alliteration: `Hooris`)** | Alliterative poetry generation engine. |

---

## 🧩 The 37 Morphological & Grammatical Feature Dimensions

Somali AI features 37 granular feature dimensions categorized across 3 structural groups:

### Group I: Noun Feature Dimensions (12 Dimensions)
1. **Definite Article Masculine** (`-ka / -ga / -ha / -a`)
2. **Definite Article Feminine** (`-ta / -da / -sha`)
3. **Group 1 Noun Plural** (`-o`)
4. **Group 2 Noun Plural** (`-do / -dda`)
5. **Group 3 Noun Plural** (`-yo`)
6. **Group 4 Noun Plural** (`-ooyin`)
7. **Group 5 Noun Plural** (`-yaal / -ayaal`)
8. **Group 6 Loan Noun Plural** (`-as / -es`)
9. **Group 7 Reduplication Noun Plural** (`-an`)
10. **Collective Noun Forms** (`geel`, `timir`, `midho`)
11. **Abstract State Noun Suffix** (`-nimo`)
12. **Verbal Action Noun Suffix** (`-asho / -is`)

### Group II: Verb Feature Dimensions (15 Dimensions)
13. **Class 1 Regular Imperative Verb Stem** (`cun`)
14. **Class 1 Verb Past Tense** (`-ay / -tay / -nay / -een`)
15. **Class 1 Verb Present Tense** (`-aa / -taa / -naa / -aan`)
16. **Class 1 Verb Present Progressive** (`-ayaa / -aysaa / -ayaan`)
17. **Class 1 Verb Past Progressive** (`-ayay / -aysay / -ayeen`)
18. **Class 2 Causative Verb Stem** (`-ee / -i`)
19. **Class 2 Verb Past Tense** (`-eyay / -eytaa / -eystay`)
20. **Class 2 Verb Present Tense** (`-iyaa / -isaa`)
21. **Class 3 Reflexive Verb Stem** (`-so / -do`)
22. **Class 3 Verb Past Reflexive** (`-saday / -sadaa`)
23. **Irregular Verb Root Present Tense** (`aqaan`, `ihi`, `imi`)
24. **Irregular Verb Root Past Tense** (`aqaanay`, `yimid`, `yiill`)
25. **Imperative Plural Command** (`-a / -to`)
26. **Infinitive Non-Finite Verb Form** (`-i / -in`)
27. **Negative Infinitive / Subjunctive Form** (`-in / -nin`)

### Group III: Focus, Clitic & Particle Dimensions (10 Dimensions)
28. **Restrictive Subject Focus Particle** (`baa`)
29. **Non-Restrictive Subject Focus Particle** (`ayaa`)
30. **Declarative Statement Clitic** (`waa`)
31. **Subject Pronoun Clitic** (`wuu / way / waan / waad / waannu`)
32. **Connective Focus Pronoun** (`wuxuu / waxa / waxay`)
33. **Preverbal Directional Particle** (`soo`)
34. **Preverbal Directional Particle** (`sii`)
35. **Preverbal Co-positional Particle** (`wada`)
36. **Preverbal Relational Particle** (`kula / laga / ugu`)
37. **Subject-Focus Sentence Agreement Filter** (`GRAM-SUBJFOCUS-001`)

---

## 🛠 Active Subsystems & Running Instructions

### 1. Terminal Assistant CLI
```bash
python somali_ai.py
```

### 2. Browser Chat Web App UI
```bash
python somali_ai_web.py
```
Open `http://127.0.0.1:8080`.

### 3. Grammar & Orthography Checker
```bash
python check.py "Ninkii gabadha wuu arkay."
```

### 4. Dictionary Spell Checker & Auto-Corrector
```bash
python src/spelling_engine.py
```

### 5. Proverb (*Maahmaahyo*) Deep Learner & Generator
```bash
python src/maahmaah_deep_trainer.py
```

### 6. Dedicated Somali BPE Tokenizer Generator
```bash
python tools/train_somali_tokenizer.py
```

---

## 📁 Repository Layout

```text
somali-ai/
├── somali_ai.py                   # Terminal Somali AI assistant CLI
├── somali_ai_web.py               # Local browser web chat UI
├── check.py                       # Master grammar & orthography checker
├── src/
│   ├── assistant/                 # Conversation, retrieval, and pipeline
│   ├── master_recognition.py      # Microsecond master index lookup
│   ├── morphology_generator.py    # Class 1-3 paradigm generator
│   ├── spelling_engine.py         # Natural Somali phonetic spell checker
│   ├── maahmaah_engine.py         # Proverb analyzer & generator
│   ├── maahmaah_deep_trainer.py   # Deep N-gram proverb trainer & QA exporter
│   ├── grammar_guardrail.py       # Real-time LLM output guardrail
│   └── terminology.py             # Official Somali linguistic terminology
├── data/
│   ├── master/                    # Master recognition index (64,673 records)
│   ├── proverbs/                  # Master proverbs dataset (1,151 proverbs)
│   ├── qa/                        # Fine-tuning QA datasets (11,151 pairs)
│   ├── vocabulary/                # BPE vocabulary (65,591 tokens)
│   └── imported/                  # Imported dictionary datasets
├── tools/
│   ├── train_somali_tokenizer.py  # BPE tokenizer exporter
│   ├── train_deep_spelling.py     # Deep spelling confusion trainer
│   └── importers/                 # Dictionary and POS importers
└── docs/                          # Project documentation
```

---

## 📄 License & Provenance

Somali AI operates under open-source software principles, keeping exact provenance for all dictionary sources, grammar rules, and literature datasets.
