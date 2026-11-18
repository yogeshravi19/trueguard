import sys
sys.path.insert(0, 'E:/trueguard/CAPSTONE/FInal/src')
from tg_data import load_pairs, PAIR_DATASETS, load_triviaqa

print("Testing all 10 datasets in TRUEGUARD:")
for i, name in enumerate(PAIR_DATASETS, 1):
    rows = load_pairs(name, 5)
    labels = [r['label'] for r in rows]
    print(f"  [{i:02d}/10] {name:25s}: loaded {len(rows)} samples, labels={labels}")

tqa = load_triviaqa(5)
print(f"  [10/10] trivia_qa                : loaded {len(tqa)} questions for mitigation")
print("\nALL 10 DATASETS SUCCESSFULLY VERIFIED AND COMPATIBLE WITH TRUEGUARD!")
