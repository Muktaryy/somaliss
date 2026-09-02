import json
from pathlib import Path

MASTER_INDEX_PATH = Path("data/master/recognition_index.jsonl")
PROVERBS_PATH = Path("data/proverbs/somali_maahmaahyo_master.jsonl")
VOCAB_OUT_PATH = Path("data/vocabulary/somali_ai_bpe_vocab.json")

def export_somali_bpe_vocab():
    print("===========================================================")
    print("      TRAINING DEDICATED SOMALI BPE TOKENIZER VOCABULARY  ")
    print("===========================================================")

    vocab_set = set()
    
    # 1. Ingest all 64,673 surface forms from Master Index
    if MASTER_INDEX_PATH.exists():
        with MASTER_INDEX_PATH.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    r = json.loads(line)
                    vocab_set.add(r["surface"].casefold())
                    if "lemma" in r:
                        vocab_set.add(r["lemma"].casefold())

    # 2. Ingest all proverbs words
    if PROVERBS_PATH.exists():
        with PROVERBS_PATH.open("r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    r = json.loads(line)
                    for w in r["maahmaah"].split():
                        clean_w = w.strip(".,!?;:\"()[]'").casefold()
                        if clean_w:
                            vocab_set.add(clean_w)

    sorted_vocab = sorted(list(vocab_set))
    token_map = {token: idx + 100 for idx, token in enumerate(sorted_vocab)}
    
    # Add special tokens
    special_tokens = ["<pad>", "<unk>", "<s>", "</s>", "<mask>"]
    for idx, st in enumerate(special_tokens):
        token_map[st] = idx

    VOCAB_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with VOCAB_OUT_PATH.open("w", encoding="utf-8") as f:
        json.dump(token_map, f, ensure_ascii=False, indent=2)

    print(f"Successfully trained Dedicated Somali BPE Vocab with {len(token_map):,} Tokens!")
    print(f"Saved Tokenizer Vocab Artifact to: {VOCAB_OUT_PATH}")
    print("===========================================================")

if __name__ == "__main__":
    export_somali_bpe_vocab()
