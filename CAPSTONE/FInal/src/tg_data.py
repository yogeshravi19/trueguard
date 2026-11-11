"""
Dataset adapters for TRUEGUARD v2.  Reads the local JSONL files written by tools/download_datasets.py
(datasets/<name>/*.jsonl) and falls back to Hugging Face if they are missing.

Detection datasets are PAIRS (grounded answer = label 0, hallucinated answer = label 1) sharing a `group` id so that
both answers of one question always land in the same train/test split (prevents question-level leakage).
"""
import json
import os
import re
import string
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT, "datasets")

PAIR_DATASETS = ["halueval_qa", "halueval_dialogue", "halueval_summarization", "truthful_qa"]
QA_INSTR = "Answer the question briefly in one short sentence.\nQuestion: "


def _read_jsonl(path):
    with open(path, encoding="utf8") as f:
        return [json.loads(l) for l in f if l.strip()]


def _load_rows(name, hf_repo, hf_cfg, hf_split, local_file):
    p = os.path.join(DATA_DIR, name, local_file)
    if os.path.exists(p):
        return _read_jsonl(p)
    from datasets import load_dataset
    return [dict(r) for r in load_dataset(hf_repo, hf_cfg, split=hf_split)]


def load_pairs(name, n, seed=42):
    """Return list of dicts: {group, user_text, answer, label} (2 rows per sampled question)."""
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
    else:
        raise ValueError(name)
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

