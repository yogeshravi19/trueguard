"""Download every dataset referenced by TRUEGUARD into FInal/datasets/<name>/ as JSONL + record provenance."""
import os, json, sys, hashlib, datetime
os.environ["USE_TF"] = "0"
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "datasets")
os.makedirs(OUT, exist_ok=True)

# (local name, hf repo, config, [splits], page url, role in project)
JOBS = [
    ("truthful_qa", "truthfulqa/truthful_qa", "generation", ["validation"],
     "https://huggingface.co/datasets/truthfulqa/truthful_qa", "TruthfulQA benchmark (817 questions)"),
    ("halueval_qa", "pminervini/HaluEval", "qa", ["data"],
     "https://huggingface.co/datasets/pminervini/HaluEval", "HaluEval-QA (10k)"),
    ("halueval_summarization", "pminervini/HaluEval", "summarization", ["data"],
     "https://huggingface.co/datasets/pminervini/HaluEval", "HaluEval-Summ (10k)"),
    ("halueval_dialogue", "pminervini/HaluEval", "dialogue", ["data"],
     "https://huggingface.co/datasets/pminervini/HaluEval", "HaluEval-Dial (10k)"),
    ("trivia_qa", "mandarjoshi/trivia_qa", "rc.nocontext", ["validation"],
     "https://huggingface.co/datasets/mandarjoshi/trivia_qa", "TriviaQA (used by real_benchmark.py)"),
]

def main():
    from datasets import load_dataset
    log = []
    for name, repo, cfg, splits, url, role in JOBS:
        d = os.path.join(OUT, name); os.makedirs(d, exist_ok=True)
        for sp in splits:
            entry = {"name": name, "hf_repo": repo, "config": cfg, "split": sp, "url": url, "role": role}
            try:
                ds = load_dataset(repo, cfg, split=sp)
                path = os.path.join(d, f"{sp}.jsonl")
                ds.to_json(path)
                entry.update(status="OK", rows=len(ds), file=os.path.relpath(path, ROOT),
                             bytes=os.path.getsize(path), columns=list(ds.column_names))
            except Exception as e:
                entry.update(status="FAILED", error=str(e)[:300])
            print(entry["name"], entry["status"], entry.get("rows", ""), flush=True)
            log.append(entry)
    json.dump({"downloaded_at": datetime.datetime.now().isoformat(timespec="seconds"), "datasets": log},
              open(os.path.join(OUT, "manifest.json"), "w"), indent=2)

if __name__ == "__main__":
    main()

