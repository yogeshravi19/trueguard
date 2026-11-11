"""
TRUEGUARD v2 core  --  sensors, trained ISP probe, logistic-regression fusion.

Implements the architecture of the review paper (Section 6):
  * four sensors computed from REAL hidden states / attentions / logits of an open LLM
      ISP  Internal State Probe        : per-layer logistic probes TRAINED on labelled data,
                                         ISP = mean_L sigmoid(w_L^T h_L + b_L)          (no proxy)
      AAS  Attention Anomaly Score     : normalised Shannon entropy of attention rows (final quartile layers)
      EEM  Entropy-Energy Monitor      : 0.6 * H_shannon_norm + 0.4 * H_renyi2_norm of output logits
      DST  Distribution Shift Tracker  : (1 - cos(h_t, h_{t-1})) / 2 on layer-averaged hidden states
  * logistic-regression fusion of the four sensors -> risk score in [0, 1]

Two equivalent extraction paths are provided and unit-tested against each other
(tests/test_equivalence.py):
  * `score_answer`          : one teacher-forced forward pass over prompt+answer (training / evaluation)
  * `OnlineSignalMonitor`   : per-token updates during cached decoding (real-time use, latency profiling)

Documented deviations from the paper's wording
  * Sensors are aggregated to the ANSWER level (mean and max over answer tokens) because ground-truth labels
    exist per answer, not per token.  The ISP probe uses the answer-mean hidden state of each probed layer.
"""
import os
os.environ.setdefault("USE_TF", "0")
import numpy as np
import torch

PROBE_FRACS = (0.45, 0.60, 0.75, 0.90)   # hidden-state depth fractions used by the ISP probes
DST_FRACS = (0.60, 0.75, 0.90)           # hidden-state depth fractions averaged for DST
W_E = 0.6                                # EEM Shannon weight
EPS = 1e-10

FEATURE_NAMES = ["AAS_mean", "AAS_max", "EEM_mean", "EEM_max", "DST_mean", "DST_max",
                 "ENT_mean", "ENT_max", "NLL_mean", "LEN"]   # last 4: baselines only, never fused
SENSOR_COLS = {"AAS": [0, 1], "EEM": [2, 3], "DST": [4, 5]}
SENSORS = ("ISP", "AAS", "EEM", "DST")


# ----------------------------------------------------------------------------- model loading
def load_model(name, device="auto", dtype=None, load_in_4bit=False):
    """Load a causal LM with EAGER attention (required to read attention weights)."""
    from transformers import AutoModelForCausalLM, AutoTokenizer
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    if dtype is None:
        dtype = torch.float16 if device == "cuda" else torch.float32
    tok = AutoTokenizer.from_pretrained(name)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    kw = dict(torch_dtype=dtype, attn_implementation="eager", low_cpu_mem_usage=True)
    if load_in_4bit:
        from transformers import BitsAndBytesConfig
        kw["quantization_config"] = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
        kw["device_map"] = "auto"
        model = AutoModelForCausalLM.from_pretrained(name, **kw)
    else:
        model = AutoModelForCausalLM.from_pretrained(name, **kw).to(device)
    model.eval()
    return model, tok, device


# ----------------------------------------------------------------------------- prompts
def build_prompt(tok, user_text, chat=None):
    """Chat template when available (instruction models), plain 'Answer:' format otherwise.
    Returns (prompt_string, answer_prefix) -- answer_prefix must be prepended to answers in plain mode."""
    if chat is None:
        chat = getattr(tok, "chat_template", None) is not None
    if chat and getattr(tok, "chat_template", None):
        p = tok.apply_chat_template([{"role": "user", "content": user_text}], tokenize=False,
                                    add_generation_prompt=True)
        return p, ""
    return f"{user_text}\nAnswer:", " "


# ----------------------------------------------------------------------------- feature maths
def _aggregate(eem, ent, aas, dst, nll):
    """Per-token arrays -> answer-level feature vector (see FEATURE_NAMES)."""
    eem, ent, aas, nll = (np.asarray(a, dtype=np.float64) for a in (eem, ent, aas, nll))
    dst = np.asarray(dst, dtype=np.float64)
    dst = dst[~np.isnan(dst)]
    d_mean = float(dst.mean()) if dst.size else 0.0
    d_max = float(dst.max()) if dst.size else 0.0
    return np.array([aas.mean(), aas.max(), eem.mean(), eem.max(), d_mean, d_max,
                     ent.mean(), ent.max(), nll.mean(), float(len(eem))], dtype=np.float64)


def _eem_ent(logits):
    """logits (n, V) float32 -> (eem, shannon_norm) per row.  Same formulas as src.signal_extractors.extract_eem."""
    V = logits.shape[-1]
    max_entropy = float(np.log(V))
    probs = torch.softmax(logits, dim=-1)
    shannon = -torch.sum(probs * torch.log(probs + EPS), dim=-1)
    h_norm = torch.clamp(shannon / max_entropy, 0.0, 1.0)
    renyi2 = -torch.log(torch.sum(probs ** 2, dim=-1) + EPS)
    e_norm = torch.clamp(renyi2 / max_entropy, 0.0, 1.0)
    eem = W_E * h_norm + (1.0 - W_E) * e_norm
    return eem.cpu().numpy(), h_norm.cpu().numpy()


def _aas_rows(attn_rows):
    """attn_rows (H, n, T): attention of n query positions over keys.  `seq_len` per row = number of valid keys.
    Returns (n,) mean-over-heads normalised Shannon entropy (matches extract_aas for the last token)."""
    return attn_rows


def _layer_ids(n_hidden, fracs):
    return [int(n_hidden * f) for f in fracs if int(n_hidden * f) < n_hidden]


@torch.no_grad()
def signals_from_forward(out, input_ids, a_start, a_end):
    """Teacher-forced extraction.  `out` = model(..., output_hidden_states, output_attentions) for ONE sequence.
    Answer tokens occupy positions [a_start, a_end); the token at position t is produced by the state at t-1."""
    P = torch.arange(a_start - 1, a_end - 1, device=out.logits.device)
    logits = out.logits[0, P, :].float()
    eem, ent = _eem_ent(logits)
    logp = torch.log_softmax(logits, dim=-1)
    tgt = input_ids[0, a_start:a_end].to(logits.device)
    nll = (-logp.gather(1, tgt[:, None])[:, 0]).cpu().numpy()

    # AAS: final-quartile attention layers, causal rows -> valid keys for query position p is p+1
    atts = out.attentions
    L = len(atts)
    aas_layers = list(range(max(0, int(L * 0.75)), L))
    seq_len = (P + 1).float()
    denom = torch.where(seq_len > 1, torch.log(seq_len), torch.ones_like(seq_len))
    per_layer = []
    for l in aas_layers:
        a = atts[l][0][:, P, :].float()                       # (H, n, T)
        H = -(a * torch.log(a + EPS)).sum(-1)                 # (H, n)
        per_layer.append((H / denom[None, :]).mean(0))
    aas = torch.stack(per_layer).mean(0).cpu().numpy()

    hs = out.hidden_states
    nh = len(hs)
    pl = _layer_ids(nh, PROBE_FRACS)
    H_mean = torch.stack([hs[l][0, P, :].float().mean(0) for l in pl]).cpu().numpy()   # (4, d)
    dl = _layer_ids(nh, DST_FRACS)
    avg = torch.stack([hs[l][0, P, :].float() for l in dl]).mean(0)                    # (n, d)
    if avg.shape[0] > 1:
        cos = torch.nn.functional.cosine_similarity(avg[1:], avg[:-1], dim=-1)
        dst = np.concatenate([[np.nan], torch.clamp((1 - cos) / 2, 0, 1).cpu().numpy()])
    else:
        dst = np.array([np.nan])
    return _aggregate(eem, ent, aas, dst, nll), H_mean


@torch.no_grad()
def score_answer(model, tok, device, prompt, answer, max_prompt_tokens=384, max_answer_tokens=48):
    """Teacher-forced features of `answer` given `prompt`.  Returns (F[10], H[4,d]) or None if answer is empty."""
    p_ids = tok(prompt, return_tensors="pt", add_special_tokens=True).input_ids[0]
    if len(p_ids) > max_prompt_tokens:
        p_ids = p_ids[-max_prompt_tokens:]
    a_ids = tok(answer, return_tensors="pt", add_special_tokens=False).input_ids[0][:max_answer_tokens]
    if len(a_ids) == 0:
        return None
    ids = torch.cat([p_ids, a_ids])[None, :].to(model.device if hasattr(model, "device") else device)
    out = model(ids, output_hidden_states=True, output_attentions=True, use_cache=False)
    return signals_from_forward(out, ids, len(p_ids), len(p_ids) + len(a_ids))


class OnlineSignalMonitor:
    """Real-time sensor bank: call `update(out, token_id)` after every decoding step.
    `out` is a model output with hidden_states / attentions / logits (cached q_len=1, or a full pass)."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.eem, self.ent, self.aas, self.dst, self.nll = [], [], [], [], []
        self._prev = None
        self._hsum = None

    @torch.no_grad()
    def update(self, out, token_id=None):
        logits = out.logits[0, -1:, :].float()
        eem, ent = _eem_ent(logits)
        self.eem.append(float(eem[0])); self.ent.append(float(ent[0]))
        if token_id is not None:
            self.nll.append(float(-torch.log_softmax(logits[0], -1)[int(token_id)]))
        atts = out.attentions
        L = len(atts)
        vals = []
        for l in range(max(0, int(L * 0.75)), L):
            a = atts[l][0, :, -1, :].float()                  # (H, T_kv)
            T = a.shape[-1]
            H = -(a * torch.log(a + EPS)).sum(-1)
            vals.append((H / (np.log(T) if T > 1 else 1.0)).mean())
        self.aas.append(float(torch.stack(vals).mean()))
        hs = out.hidden_states
        nh = len(hs)
        dl = _layer_ids(nh, DST_FRACS)
        cur = torch.stack([hs[l][0, -1, :].float() for l in dl]).mean(0)
        if self._prev is None:
            self.dst.append(np.nan)
        else:
            c = torch.nn.functional.cosine_similarity(cur, self._prev, dim=-1)
            self.dst.append(float(torch.clamp((1 - c) / 2, 0, 1)))
        self._prev = cur
        pl = _layer_ids(nh, PROBE_FRACS)
        hv = torch.stack([hs[l][0, -1, :].float() for l in pl])
        self._hsum = hv if self._hsum is None else self._hsum + hv

    def features(self):
        n = len(self.eem)
        nll = self.nll if len(self.nll) == n else [0.0] * n
        return _aggregate(self.eem, self.ent, self.aas, self.dst, nll), (self._hsum / n).cpu().numpy()


# ----------------------------------------------------------------------------- generation
@torch.no_grad()
def generate_answer(model, tok, device, prompt, max_new_tokens=24, sample=False, temperature=0.7, top_p=0.9,
                    max_prompt_tokens=384):
    """Generate a short answer (first line only).  Greedy by default."""
    ids = tok(prompt, return_tensors="pt", add_special_tokens=True).input_ids[:, -max_prompt_tokens:].to(model.device)
    kw = dict(max_new_tokens=max_new_tokens, pad_token_id=tok.pad_token_id, attention_mask=torch.ones_like(ids))
    if sample:
        kw.update(do_sample=True, temperature=temperature, top_p=top_p)
    else:
        kw.update(do_sample=False)
    out = model.generate(ids, **kw)
    text = tok.decode(out[0, ids.shape[1]:], skip_special_tokens=True)
    return text.strip().split("\n")[0].strip()


# ----------------------------------------------------------------------------- trained detector
def _logit(p):
    p = np.clip(p, 1e-4, 1 - 1e-4)
    return np.log(p / (1 - p))


class TrueGuardDetector:
    """Trained ISP probes + logistic-regression fusion.

    fit(F, H, y, groups):  F (n,10) sensor features, H (n,4,d) answer-mean hidden states, y 1=hallucinated.
      * ISP probes (one logistic regression per probed layer) are trained on the training rows only.
        The regularisation strength is chosen by grouped inner cross-validation on the training rows only.
      * The fusion layer is trained on INNER OUT-OF-FOLD probe scores, so it never sees probe scores that were
        produced by a probe that had trained on the same row (no probe-to-fusion leakage).
    """

    def __init__(self, use=SENSORS, C_grid=(0.001, 0.01, 0.1), fusion_C=1.0, n_inner=5, seed=42):
        self.use, self.C_grid, self.fusion_C, self.n_inner, self.seed = tuple(use), C_grid, fusion_C, n_inner, seed

    # -- helpers
    @staticmethod
    def _lr(C):
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import make_pipeline
        from sklearn.preprocessing import StandardScaler
        return make_pipeline(StandardScaler(), LogisticRegression(C=C, max_iter=300))

    def _splits(self, y, groups):
        from sklearn.model_selection import GroupKFold, StratifiedKFold
        if groups is not None:
            k = min(self.n_inner, len(np.unique(groups)))
            return list(GroupKFold(n_splits=k).split(np.zeros(len(y)), y, groups))
        return list(StratifiedKFold(self.n_inner, shuffle=True, random_state=self.seed).split(np.zeros(len(y)), y))

    def _oof_probe(self, H, y, splits, C):
        n, nl, _ = H.shape
        oof = np.zeros((n, nl))
        for tr, te in splits:
            for k in range(nl):
                m = self._lr(C).fit(H[tr, k], y[tr])
                oof[te, k] = m.predict_proba(H[te, k])[:, 1]
        return oof.mean(1)

    def _design(self, F, isp):
        cols = []
        if "ISP" in self.use:
            cols.append(_logit(isp)[:, None])
        for s in ("AAS", "EEM", "DST"):
            if s in self.use:
                cols.append(F[:, SENSOR_COLS[s]])
        return np.hstack(cols)

    # -- API
    def fit(self, F, H, y, groups=None):
        from sklearn.metrics import roc_auc_score
        F = np.asarray(F, np.float64); y = np.asarray(y).astype(int)
        isp_train = None
        if "ISP" in self.use:
            H = np.asarray(H, np.float32)
            splits = self._splits(y, groups)
            best = (-1, None, None)
            for C in self.C_grid:
                oof = self._oof_probe(H, y, splits, C)
                auc = roc_auc_score(y, oof)
                if auc > best[0]:
                    best = (auc, C, oof)
            self.probe_auc_inner_, self.probe_C_, isp_train = best
            self.probes_ = [self._lr(self.probe_C_).fit(H[:, k], y) for k in range(H.shape[1])]
        Z = self._design(F, isp_train)
        self.fusion_ = self._lr(self.fusion_C).fit(Z, y)
        self.train_risk_ = self.fusion_.predict_proba(Z)[:, 1]
        self.y_train_ = y
        return self

    def isp_score(self, H):
        H = np.asarray(H, np.float32)
        return np.mean([p.predict_proba(H[:, k])[:, 1] for k, p in enumerate(self.probes_)], axis=0)

    def predict_proba(self, F, H=None):
        F = np.asarray(F, np.float64)
        isp = self.isp_score(H) if "ISP" in self.use else None
        return self.fusion_.predict_proba(self._design(F, isp))[:, 1]

    def sensor_scores(self, F, H):
        """Per-sensor scalar used for individual-sensor evaluation (oriented so larger = riskier if the sensor works)."""
        F = np.asarray(F, np.float64)
        d = {"AAS": F[:, 0], "EEM": F[:, 2], "DST": F[:, 4]}
        if hasattr(self, "probes_"):
            d["ISP"] = self.isp_score(H)
        return d

    def explain(self, F, H):
        """Signed contribution of every sensor to the fused log-odds for ONE sample (1-row inputs)."""
        F = np.asarray(F, np.float64).reshape(1, -1)
        isp = self.isp_score(np.asarray(H)[None]) if "ISP" in self.use else None
        Z = self._design(F, isp)
        sc, lr = self.fusion_.steps[0][1], self.fusion_.steps[1][1]
        contrib = (sc.transform(Z) * lr.coef_)[0]
        names, k = [], 0
        out = {}
        if "ISP" in self.use:
            out["ISP"] = float(contrib[k]); k += 1
        for s in ("AAS", "EEM", "DST"):
            if s in self.use:
                out[s] = float(contrib[k:k + 2].sum()); k += 2
        return out

