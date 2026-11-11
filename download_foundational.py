import urllib.request
import os
import time

papers = {
    "21_SelfCheckGPT.pdf": "https://arxiv.org/pdf/2303.08896.pdf",
    "22_TruthfulQA.pdf": "https://arxiv.org/pdf/2109.07958.pdf",
    "23_FActScore.pdf": "https://arxiv.org/pdf/2305.14251.pdf",
    "24_Chain_of_Verification_CoVe.pdf": "https://arxiv.org/pdf/2309.11495.pdf",
    "25_RAG_Lewis.pdf": "https://arxiv.org/pdf/2005.11401.pdf",
    "26_Self_RAG_Asai.pdf": "https://arxiv.org/pdf/2310.11511.pdf",
    "27_SAPLMA_Azaria_Mitchell.pdf": "https://arxiv.org/pdf/2304.13734.pdf",
    "28_Inference_Time_Intervention_ITI.pdf": "https://arxiv.org/pdf/2306.03341.pdf",
    "29_HaluEval_Li.pdf": "https://arxiv.org/pdf/2305.11747.pdf",
    "30_Chain_of_Thought_Wei.pdf": "https://arxiv.org/pdf/2201.11903.pdf",
    "31_MultiAgent_Debate_Du.pdf": "https://arxiv.org/pdf/2305.14325.pdf",
    "32_Woodpecker_Yin.pdf": "https://arxiv.org/pdf/2310.16045.pdf",
    "33_RARR_Gao.pdf": "https://arxiv.org/pdf/2210.08726.pdf",
    "34_FacTool_Chern.pdf": "https://arxiv.org/pdf/2307.13528.pdf",
    "35_Ji_Hallucination_Survey.pdf": "https://arxiv.org/pdf/2202.03629.pdf",
    "36_Self_Contradictory_Mundler.pdf": "https://arxiv.org/pdf/2305.15852.pdf",
    "37_Bang_ChatGPT_Evaluation.pdf": "https://arxiv.org/pdf/2302.04067.pdf",
    "38_Truth_Forest_Chen.pdf": "https://arxiv.org/pdf/2403.04259.pdf"
}

dest_dir = r"e:\trueguard\foundational_papers"
os.makedirs(dest_dir, exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print(f"Downloading papers into {dest_dir}...")
for fname, url in papers.items():
    fpath = os.path.join(dest_dir, fname)
    if os.path.exists(fpath) and os.path.getsize(fpath) > 10000:
        print(f"Already exists: {fname}")
        continue
    try:
        print(f"Downloading {fname} from {url}...")
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            with open(fpath, "wb") as f:
                f.write(data)
        print(f"Successfully saved {fname} ({len(data)} bytes)")
        time.sleep(1) # respectful rate limiting
    except Exception as e:
        print(f"Failed to download {fname}: {e}")

print("Download script complete!")
