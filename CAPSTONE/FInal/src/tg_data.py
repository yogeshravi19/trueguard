"""
Updated dataset adapter for TRUEGUARD v2 with full native support for the 10-Dataset Suite:
1. halueval_dialogue (01_halueval_dialogue)
2. halueval_qa (02_halueval_qa)
3. halueval_summarization (03_halueval_summarization)
4. truthful_qa (04_truthful_qa)
5. trivia_qa (05_trivia_qa)
6. halueval_general (06_halueval_general)
7. faithdial (07_faithdial)
8. wikibio_gpt3 (08_wikibio_gpt3)
9. fever (09_fever)
10. xsum_factuality (10_xsum_factuality)
"""
import json
import os
import re
import string
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT, "datasets")
TRUEGUARD_ROOT = os.path.abspath(os.path.join(ROOT, "..", ".."))
IEEE_DATA_DIR = os.path.join(TRUEGUARD_ROOT, "ieee", "datasets")

PAIR_DATASETS = [
    "halueval_qa", 
    "halueval_dialogue", 
    "halueval_summarization", 
    "truthful_qa",
    "halueval_general",
    "faithdial",
    "wikibio_gpt3",
    "fever",
    "xsum_factuality"
]
QA_INSTR = "Answer the question briefly in one short sentence.\nQuestion: "


def _read_jsonl(path):
    with open(path, encoding="utf8") as f:
        return [json.loads(l) for l in f if l.strip()]


def _load_rows(name, hf_repo, hf_cfg, hf_split, local_file):
    # Check 1: IEEE numbered folders (e.g., 01_halueval_dialogue, 02_halueval_qa, etc.)
    for folder in os.listdir(IEEE_DATA_DIR):
        if name in folder and os.path.isdir(os.path.join(IEEE_DATA_DIR, folder)):
            p_cand = os.path.join(IEEE_DATA_DIR, folder, local_file)
            if os.path.exists(p_cand):
                return _read_jsonl(p_cand)
            # Find any jsonl in that folder
            for f in os.listdir(os.path.join(IEEE_DATA_DIR, folder)):
                if f.endswith(".jsonl"):
                    return _read_jsonl(os.path.join(IEEE_DATA_DIR, folder, f))
                    
    # Check 2: CAPSTONE primary datasets dir
    p = os.path.join(DATA_DIR, name, local_file)
    if os.path.exists(p):
        return _read_jsonl(p)
        
    # Check 3: Fallback to HuggingFace
    from datasets import load_dataset
    if hf_cfg:
        return [dict(r) for r in load_dataset(hf_repo, hf_cfg, split=hf_split)]
    return [dict(r) for r in load_dataset(hf_repo, split=hf_split, trust_remote_code=True)]


def load_pairs(name, n, seed=42):
    """Return list of dicts: {group, user_text, answer, label}."""
    rng = np.random.RandomState(seed)
    out = []
    
    if name == "halueval_qa":
        rows = _load_rows(name, "pminervini/HaluEval", "qa", "data", "data.jsonl")
        for gi, i in enumerate(rng.permutation(len(rows))[:n]):
            r = rows[int(i)]
            ut = QA_INSTR + r["question"]
            out += [dict(group=gi, user_text=ut, answer=r["right_answer"], label=0),
                    dict(group=gi, user_text=ut, answer=r["hallucinated_answer"], label=1)]
                    
    elif name == "halueval_dialogue":
        rows = _load_rows(name, "pminervini/HaluEval", "dialogue", "data", "data.jsonl")
        for gi, i in enumerate(rng.permutation(len(rows))[:n]):
            r = rows[int(i)]
            ut = ("Continue the dialogue with one short reply.\nDialogue:\n" + r["dialogue_history"][-1200:])
            out += [dict(group=gi, user_text=ut, answer=r["right_response"], label=0),
                    dict(group=gi, user_text=ut, answer=r["hallucinated_response"], label=1)]
                    
    elif name == "halueval_summarization":
        rows = _load_rows(name, "pminervini/HaluEval", "summarization", "data", "data.jsonl")
        for gi, i in enumerate(rng.permutation(len(rows))[:n]):
            r = rows[int(i)]
            ut = "Summarize the document in one or two sentences.\nDocument: " + r["document"][:1200]
            out += [dict(group=gi, user_text=ut, answer=r["right_summary"], label=0),
                    dict(group=gi, user_text=ut, answer=r["hallucinated_summary"], label=1)]
                    
    elif name == "truthful_qa":
        rows = _load_rows(name, "truthfulqa/truthful_qa", "generation", "validation", "validation.jsonl")
        for gi, i in enumerate(rng.permutation(len(rows))[:n]):
            r = rows[int(i)]
            ut = QA_INSTR + r["question"]
            wrong = r["incorrect_answers"][int(rng.randint(len(r["incorrect_answers"])))]
            out += [dict(group=gi, user_text=ut, answer=r["best_answer"], label=0),
                    dict(group=gi, user_text=ut, answer=wrong, label=1)]
                    
    elif name in ["halueval_general", "faithdial", "wikibio_gpt3", "fever", "xsum_factuality"]:
        # Standardized schema loader from IEEE datasets
        rows = _load_rows(name, None, None, None, f"{name}_eval.jsonl")
        n_take = min(n * 2, len(rows))
        for gi, r in enumerate(rows[:n_take]):
            prompt = r.get("prompt", r.get("user_text", r.get("user_query", "")))
            ans = r.get("response", r.get("answer", r.get("chatgpt_response", "")))
            lbl = r["label"]
            group_id = r.get("group", gi // 2)
            out.append(dict(group=group_id, user_text=prompt, answer=ans, label=lbl))
            
    else:
        raise ValueError(f"Unknown dataset name: {name}. Supported: {PAIR_DATASETS}")
        
    return out


# ---------------------------------------------------------------- TriviaQA (generation-mode mitigation experiment)
def norm_text(s):
    s = s.lower()
    s = "".join(c for c in s if c not in string.punctuation)
    return " ".join(s.split())


def load_triviaqa(n, seed=42, offset=0):
    rows = _load_rows("trivia_qa", "mandarjoshi/trivia_qa", "rc.nocontext", "validation", "validation.jsonl")
    idx = np.random.RandomState(seed).permutation(len(rows))[offset:offset + n]
    items = []
    for i in idx:
        r = rows[int(i)]
        aliases = [a for a in r["answer"]["normalized_aliases"] if a]
        items.append(dict(id=int(i), question=r["question"], user_text=QA_INSTR + r["question"], gold=aliases))
    return items


def is_correct(answer, gold):
    """1 if any gold alias appears (word-boundary) in the normalised answer, else 0."""
    a = norm_text(answer)
    return int(any(re.search(r"\b" + re.escape(g) + r"\b", a) for g in gold))
