"""
Step 4 of the evaluation pipeline: profile REAL per-token latency on actual decoding (not mock tensors).

Compares four modes on the same prompts and token budget:
  1. vanilla_decode            : standard KV-cached greedy decoding (no hidden states / attentions returned)
  2. trueguard_cached_decode   : KV-cached decoding WITH output_hidden_states + output_attentions + OnlineSignalMonitor
                                 + trained ISP probe + fusion at every step
  3. trueguard_with_postpass   : vanilla decoding followed by one `score_answer` teacher-forced pass (the fastest way
                                 to run TRUEGUARD when token-by-token halting is not needed)
  4. multi_sample_5x_baseline  : 5 temperature-sampled generations (the core cost of SelfCheckGPT / Semantic Entropy)

Reports ms/token, true overhead over vanilla, and measured speedup vs the 5-sample baseline.
"""
import argparse, json, os, sys, time
os.environ.setdefault("USE_TF", "0")
import numpy as np
import torch

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
from src.tg_pipeline import load_model, build_prompt, OnlineSignalMonitor, score_answer, TrueGuardDetector
from src.tg_data import load_triviaqa


def _sync(device):
    if str(device).startswith("cuda") and torch.cuda.is_available():
        torch.cuda.synchronize()


@torch.no_grad()
def profile(model_name, n_prompts=25, n_tokens=24, out_path=None, fourbit=False):
    model, tok, device = load_model(model_name, load_in_4bit=fourbit)
    prompts = [build_prompt(tok, it["user_text"])[0] for it in load_triviaqa(n_prompts, seed=7)]

    # fit a dummy detector on 20 random vectors of the right hidden size so probe + fusion matrix multiplies are real
    d_model = model.config.hidden_size
    rng = np.random.RandomState(0)
    det = TrueGuardDetector().fit(rng.randn(40, 10), rng.randn(40, 4, d_model).astype(np.float32),
                                  np.array([0, 1] * 20))

    # warmup
    ids0 = tok(prompts[0], return_tensors="pt").input_ids.to(model.device)
    _ = model(ids0, output_hidden_states=True, output_attentions=True)
    _sync(device)

    def time_vanilla():
        t0 = time.perf_counter()
        toks = 0
        for p in prompts:
            ids = tok(p, return_tensors="pt").input_ids.to(model.device)
            past = None
            cur = ids
            for _ in range(n_tokens):
                out = model(cur, past_key_values=past, use_cache=True,
                            output_hidden_states=False, output_attentions=False)
                past = out.past_key_values
                cur = out.logits[:, -1:, :].argmax(-1)
                toks += 1
        _sync(device)
        return (time.perf_counter() - t0) * 1000 / toks

    def time_trueguard_online():
        t0 = time.perf_counter(); t_math = 0.0; toks = 0
        mon = OnlineSignalMonitor()
        for p in prompts:
            mon.reset()
            ids = tok(p, return_tensors="pt").input_ids.to(model.device)
            past = None; cur = ids
            for _ in range(n_tokens):
                out = model(cur, past_key_values=past, use_cache=True,
                            output_hidden_states=True, output_attentions=True)
                past = out.past_key_values
                nxt = out.logits[:, -1:, :].argmax(-1)
                _sync(device); tm0 = time.perf_counter()
                mon.update(out, int(nxt[0, 0]))
                F, H = mon.features()
                _ = det.predict_proba(F[None], H[None])
                _sync(device); t_math += time.perf_counter() - tm0
                cur = nxt; toks += 1
        _sync(device)
        tot = (time.perf_counter() - t0) * 1000 / toks
        return tot, t_math * 1000 / toks

    def time_postpass():
        t0 = time.perf_counter(); toks = 0
        for p in prompts:
            ids = tok(p, return_tensors="pt").input_ids.to(model.device)
            gen = model.generate(ids, max_new_tokens=n_tokens, do_sample=False,
                                 min_new_tokens=n_tokens, pad_token_id=tok.pad_token_id)
            ans = tok.decode(gen[0, ids.shape[1]:], skip_special_tokens=True)
            r = score_answer(model, tok, device, p, " " + ans)
            if r is not None:
                _ = det.predict_proba(r[0][None], r[1][None])
            toks += n_tokens
        _sync(device)
        return (time.perf_counter() - t0) * 1000 / toks

    def time_5x():
        t0 = time.perf_counter(); toks = 0
        for p in prompts[: max(5, n_prompts // 3)]:
            ids = tok(p, return_tensors="pt").input_ids.to(model.device)
            for _ in range(5):
                _ = model.generate(ids, max_new_tokens=n_tokens, do_sample=True, temperature=0.7,
                                   min_new_tokens=n_tokens, pad_token_id=tok.pad_token_id)
            toks += n_tokens
        _sync(device)
        return (time.perf_counter() - t0) * 1000 / toks

    v_ms = time_vanilla()
    tg_ms, math_ms = time_trueguard_online()
    post_ms = time_postpass()
    five_ms = time_5x()

    res = dict(
        model=model_name, device=str(device), n_prompts=n_prompts, tokens_per_prompt=n_tokens,
        vanilla_ms_per_token=v_ms,
        trueguard_online_ms_per_token=tg_ms,
        trueguard_sensor_math_only_ms_per_token=math_ms,
        trueguard_online_overhead_ms_per_token=tg_ms - v_ms,
        trueguard_online_relative_overhead=(tg_ms - v_ms) / max(v_ms, 1e-9),
        trueguard_postpass_ms_per_token=post_ms,
        trueguard_postpass_overhead_ms_per_token=post_ms - v_ms,
        multi_sample_5x_ms_per_token=five_ms,
        speedup_online_vs_5x=five_ms / max(tg_ms, 1e-9),
        speedup_postpass_vs_5x=five_ms / max(post_ms, 1e-9),
    )
    if out_path:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        json.dump(res, open(out_path, "w"), indent=2)
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="TinyLlama/TinyLlama-1.1B-Chat-v1.0")
    ap.add_argument("--n_prompts", type=int, default=20)
    ap.add_argument("--n_tokens", type=int, default=24)
    ap.add_argument("--4bit", dest="fourbit", action="store_true")
    ap.add_argument("--out", default=os.path.join(ROOT, "results", "v2", "real_latency.json"))
    a = ap.parse_args()
    print(json.dumps(profile(a.model, a.n_prompts, a.n_tokens, a.out, a.fourbit), indent=2))

