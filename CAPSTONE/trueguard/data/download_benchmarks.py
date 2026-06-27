import os
import torch
import numpy as np
from datasets import load_dataset
import pandas as pd

def download_truthfulqa(save_dir):
    print("Downloading TruthfulQA...")
    try:
        ds = load_dataset("truthful_qa", "generation")
        df = ds['validation'].to_pandas()
        # TruthfulQA has 'question', 'best_answer', 'correct_answers', 'incorrect_answers'
        df.to_csv(os.path.join(save_dir, "truthfulqa.csv"), index=False)
        print("TruthfulQA saved.")
    except Exception as e:
        print(f"Error downloading TruthfulQA: {e}")

def download_halueval(save_dir):
    print("Downloading HaluEval (QA subset)...")
    try:
        # HaluEval is hosted on HF datasets as 'pminervini/HaluEval' or similar. 
        # Using a representative generic query if specific subset fails.
        ds = load_dataset("pminervini/HaluEval", split="train[:5000]") 
        df = ds.to_pandas()
        df.to_csv(os.path.join(save_dir, "halueval_qa.csv"), index=False)
        print("HaluEval saved.")
    except Exception as e:
        print(f"Error downloading HaluEval: {e}")

if __name__ == "__main__":
    save_dir = os.path.join(os.path.dirname(__file__), "processed")
    os.makedirs(save_dir, exist_ok=True)
    download_truthfulqa(save_dir)
    download_halueval(save_dir)
    print("Data download step complete. Ensure you review the CSVs for correct formatting.")
