# TRUEGUARD – Dataset Sources & Verification

All files are stored under `CAPSTONE/FInal/datasets/` (one JSONL per dataset).
Machine-readable record: `datasets/manifest.json`. Downloaded 2026-11-10 with `tools/download_datasets.py`
(Hugging Face `datasets` 3.1.0).

| Local folder | File | Rows | Size | Source (verify here) | Original paper / repo |
|---|---|---|---|---|---|
| `truthful_qa/` | `validation.jsonl` | 817 | 0.5 MB | https://huggingface.co/datasets/truthfulqa/truthful_qa (config `generation`) | Lin et al., 2022, https://arxiv.org/abs/2109.07958 · https://github.com/sylinrl/TruthfulQA |
| `halueval_qa/` | `data.jsonl` | 10,000 | 5.9 MB | https://huggingface.co/datasets/pminervini/HaluEval (config `qa`) | Li et al., 2023, https://arxiv.org/abs/2305.11747 · https://github.com/RUCAIBox/HaluEval |
| `halueval_summarization/` | `data.jsonl` | 10,000 | 45 MB | same repo (config `summarization`) | same |
| `halueval_dialogue/` | `data.jsonl` | 10,000 | 6.6 MB | same repo (config `dialogue`) | same |
| `trivia_qa/` | `validation.jsonl` | 17,944 | 18.7 MB | https://huggingface.co/datasets/mandarjoshi/trivia_qa (config `rc.nocontext`) | Joshi et al., 2017, https://arxiv.org/abs/1705.03551 |

`pminervini/HaluEval` is a Hugging Face mirror of the official RUCAIBox release; compare against the GitHub repo above if you need the original files.

## Columns
- **truthful_qa:** type, category, question, best_answer, correct_answers, incorrect_answers, source
- **halueval_qa:** knowledge, question, right_answer, hallucinated_answer
- **halueval_summarization:** document, right_summary, hallucinated_summary
- **halueval_dialogue:** knowledge, dialogue_history, right_response, hallucinated_response
- **trivia_qa:** question, question_id, question_source, entity_pages, search_results, answer

## Not downloaded
- **HELM** – an evaluation framework (https://crfm.stanford.edu/helm/), not a single dataset. Earlier "HELM" numbers in `results/` came from simulated data. No dataset was ever downloaded for it.

## Other datasets present in the machine's Hugging Face cache (NOT part of this project)
`healthmemoryarena/MedHall-Bench`, `mirobody/MedHall-Bench`, `openlifescienceai/Med-HALT`, `UTAustin-AIHealth/MedHallu` (medical hallucination sets, origin unknown).

## Status of earlier results
Before this download, no dataset was used: `results/benchmark_results.json`, `metrics.csv` and the smoke test were generated from random Gaussian features. Real results come from `experiments/real_benchmark.py`.

