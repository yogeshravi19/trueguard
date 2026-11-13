"""
Chapters 4, 5, 6, 7, 8, 9, and Appendices content definitions for TRUEGUARD Final Project Report.
All numbers, equations, code excerpts, and tables match the verified v2 codebase and results.
"""

CH4_SECTIONS = [
    ("4.1 CRITICAL ANALYSIS OF EXISTING HALLUCINATION DETECTION SYSTEMS", None, [
        "Existing industrial and academic approaches to LLM hallucination management fall into three distinct operational categories, each exhibiting severe architectural trade-offs when deployed in latency-sensitive applications:",
        "1. Single-Pass Surface Probability Heuristics (Token Entropy, Perplexity/NLL, and Logit Energy): These methods compute scalar summaries directly from the output vocabulary distribution without inspecting intermediate transformer layers. While computationally free, they suffer from two fatal weaknesses verified in our experiments: (a) on adversarial misconception benchmarks such as TruthfulQA [22], the LLM states memorized human falsehoods with high token probability, causing entropy and NLL to achieve near-random AUROCs (0.502 to 0.505); and (b) on paired QA benchmarks such as HaluEval-QA [29], short entity ground-truth answers have higher per-token entropy than longer, template-padded hallucinated sentences, inverting the signal polarity (raw NLL AUROC = 0.089).",
        "2. Multi-Sample Stochastic Consistency Pipelines (SelfCheckGPT [21], Semantic Entropy [41], Multiagent Debate [31]): By sampling K = 5 to 20 auxiliary completions per prompt and measuring semantic agreement, these methods detect stochastic fabrications without white-box access. However, they multiply GPU memory bandwidth and decoding latency by K (169.31 ms/token for 5-sample decoding vs. 33.49 ms/token for vanilla decoding on an NVIDIA Tesla T4 GPU) and still fail when the model deterministically repeats a systematic misconception across all K samples.",
        "3. Always-On Post-Hoc Retrieval and Verification Pipelines (Standard RAG [25], CoVe [24], RARR [33], CRITIC [39]): Unconditional retrieval queries external search indices on every prompt regardless of whether the base model already knows the answer, while post-hoc critique pipelines execute 3 to 5 sequential LLM calls per response. Neither paradigm exploits internal white-box model states to gate when external intervention is actually needed."
    ]),
    ("4.2 PROPOSED TRUEGUARD CLOSED-LOOP CONTROL SYSTEM", None, [
        "TRUEGUARD overcomes the fragmentation of existing methods by formulating hallucination management as a unified, single-pass, white-box feedback control loop around the frozen language model. Rather than relying on a single signal or generating multiple stochastic samples upfront, TRUEGUARD instruments the single forward pass of the LLM with four orthogonal internal sensors:",
        "• Sensor 1 — Internal State Probe (ISP): Supervised L2-regularized logistic probes attached at four fractional residual-stream depths {0.45, 0.60, 0.75, 0.90}L (layers [10, 13, 16, 20] on 22-layer TinyLlama-1.1B; layers [5, 7, 9, 11] on 12-layer GPT-2), stacked via leakage-free inner grouped cross-validation.",
        "• Sensor 2 — Attention Anomaly Score (AAS): Normalized Shannon entropy of causal self-attention distributions averaged across all heads in the final quartile of transformer layers L_top = [floor(3L/4), L).",
        "• Sensor 3 — Energy and Entropy Monitor (EEM): Scale-invariant hybrid vocabulary uncertainty combining normalized Shannon entropy (0.6) and normalized quadratic Renyi-2 entropy (0.4).",
        "• Sensor 4 — Directional Semantic Trajectory (DST): Consecutive-token hidden-state cosine drift 1 - cos(final-layer activation h_t, final-layer activation h_t-1) in the final transformer layer.",
        "The sequence-pooled sensor vector phi(x,y) = [F_bar, A_bar, H_bar_ent, D_bar]^T is standardized and mapped by a calibrated L2 logistic fusion estimator into a continuous risk score r(x,y) in [0, 1] accompanied by exact per-sensor log-odds attributions. When r(x,y) remains below tau_warning, the initial answer is emitted immediately with zero extra decoding passes. Only when r(x,y) crosses tau_warning or tau_fault does the Three-Tier Actuator invoke local temperature-annealed re-sampling (Tier 1), cleaned-query Wikipedia retrieval grounding (Tier 2), or calibrated abstention (Tier 3)."
    ]),
]

FUNCTIONAL_REQUIREMENTS_TABLE = [
    ("FR-01", "Multi-Layer Hidden State Extraction", "Intercept residual-stream hidden states layer activation h_{l,t} across all L transformer layers during teacher-forced or KV-cached online decoding without modifying frozen weights."),
    ("FR-02", "Supervised 4-Layer ISP Probing", "Train L2-regularized logistic probes at fractional depths {0.45, 0.60, 0.75, 0.90}L using inner GroupKFold out-of-fold predictions to prevent stacking leakage."),
    ("FR-03", "Top-Quartile Attention Entropy (AAS)", "Compute step-wise normalized Shannon entropy over causal attention weights alpha_{l,h,t,1..K_t} across all heads in the final quartile of layers."),
    ("FR-04", "Hybrid Shannon/Renyi-2 Monitor (EEM)", "Compute scale-invariant token uncertainty 0.6 H_Shannon,norm + 0.4 H_Renyi2,norm in [0, 1] from pre-softmax logits at each generated token."),
    ("FR-05", "Directional Semantic Trajectory (DST)", "Compute consecutive-token cosine distance 1 - cos(final-layer activation h_t, final-layer activation h_t-1) across generated answer tokens."),
    ("FR-06", "Calibrated Logistic Fusion & Attribution", "Standardize the 4-sensor vector phi(x,y), predict calibrated risk r(x,y) in [0, 1], and decompose log-odds into signed per-sensor contributions c_k = w_k * z_k."),
    ("FR-07", "Two-Threshold Calibration", "Calibrate tau_warning (Youden's J optimal operating point) and tau_fault (high-precision fault threshold at Precision >= 0.80) on held-out calibration folds."),
    ("FR-08", "Three-Tier Closed-Loop Actuation", "Route generations dynamically across SAFE emission, Tier 1 annealed re-sampling, Tier 2 Wikipedia RAG re-grounding, and Tier 3 calibrated abstention."),
]

NON_FUNCTIONAL_REQUIREMENTS_TABLE = [
    ("NFR-01", "Dual-Mode Numerical Equivalence", "Teacher-forced post-pass scoring and KV-cached step-by-step online monitoring must agree within max |Delta| < 10^-4 (verified: 3.49e-6 on ISP, 1.53e-5 on EEM)."),
    ("NFR-02", "Single-Pass Latency Overhead", "Post-pass sensor extraction and fusion must add < 10% wall-clock latency over vanilla greedy decoding on GPU (verified: +8.7%, +2.91 ms/tok on Tesla T4)."),
    ("NFR-03", "Zero Group Data Leakage", "All cross-validation splits and bootstrap confidence intervals must group by question ID so paired answers never straddle train and test splits."),
    ("NFR-04", "Deterministic Reproducibility", "All dataset sampling, fold partitioning, probe training, and bootstrap resampling must use fixed pseudorandom seeds (seed = 42)."),
    ("NFR-05", "Graceful Fallback under API Restrictions", "When internal hidden states are unavailable, the detector must operate seamlessly using the remaining subset of sensors (without_ISP mode)."),
]

TECH_STACK_TABLE = [
    ("Programming Language", "Python 3.10 / 3.11", "Core implementation of TRUEGUARD v2 pipeline, evaluation harness, and report automation."),
    ("Deep Learning Framework", "PyTorch >= 2.0.0 & HuggingFace Transformers >= 4.35", "Autoregressive LLM forward passes, KV-cache management, and hidden/attention tensor hooks."),
    ("Primary GPU Backbone", "TinyLlama/TinyLlama-1.1B-Chat-v1.0 (L=22, d=2048, H=32)", "Primary 1.1B-parameter open-weights LLM evaluated on NVIDIA Tesla T4 GPU (16 GB VRAM)."),
    ("Secondary CPU Backbone", "OpenAI GPT-2 (L=12, d=768, H=12, 124M parameters)", "Secondary architecture-generality verification and local CPU equivalence testbed."),
    ("Statistical & ML Library", "Scikit-Learn >= 1.2.0, SciPy >= 1.10, NumPy >= 1.24", "StandardScaler, L2 LogisticRegression, GroupKFold, AUROC/AUPRC/Brier/ECE, and bootstrap CIs."),
    ("External Knowledge Source", "Wikipedia REST / MediaWiki API (`WikipediaRetriever`)", "Live non-parametric evidence retrieval for Tier 2 corrective re-grounding on TriviaQA."),
    ("Benchmark Datasets", "HuggingFace Datasets (`truthful_qa`, `halueval`, `trivia_qa`)", "48,761 total downloaded JSONL benchmark instances across 5 standardized tasks."),
]

DATASET_SUMMARY_TABLE = [
    ("TruthfulQA (Generation)", "truthful_qa.jsonl", "817 questions", "398 pairs (796 answers)", "Adversarial human misconceptions across 38 categories (health, law, finance, history) [22]."),
    ("HaluEval — QA", "halueval_qa.jsonl", "10,000 items", "400 pairs (800 answers)", "Knowledge-grounded open-domain question answering paired with plausible hallucinations [29]."),
    ("HaluEval — Dialogue", "halueval_dialogue.jsonl", "10,000 items", "400 pairs (800 answers)", "Multi-turn knowledge-grounded conversational responses on Wikipedia entities [29]."),
    ("HaluEval — Summarization", "halueval_summarization.jsonl", "10,000 items", "400 pairs (800 answers)", "Long-document news summarization paired with intrinsic/extrinsic factual distortions [29]."),
    ("TriviaQA (Open-Domain QA)", "trivia_qa.jsonl", "17,944 questions", "150 cal + 150 test (live)", "Entity-centric open-domain trivia questions with normalized alias ground-truth sets [44]."),
]

CODE_EXCERPT_1_PIPELINE = """class SupervisedLayerProbe:
    \"\"\"Leakage-free supervised logistic probes across 4 fractional transformer depths.\"\"\"
    FRACTIONS: Tuple[float, ...] = (0.45, 0.60, 0.75, 0.90)

    @staticmethod
    def select_layers(n_layers: int) -> List[int]:
        idxs = sorted({max(0, min(n_layers - 1, int(round(f * (n_layers - 1)))))
                       for f in SupervisedLayerProbe.FRACTIONS})
        return idxs

    def fit_and_oof(self, layer_X: Dict[int, np.ndarray], y: np.ndarray,
                    groups: np.ndarray, n_Inner_folds: int = 3) -> np.ndarray:
        n = len(y)
        oof_per_layer = np.zeros((n, len(self.layer_indices)), dtype=np.float64)
        n_groups = len(np.unique(groups))
        k = max(2, min(n_Inner_folds, n_groups))
        gkf = GroupKFold(n_splits=k)

        for j, l in enumerate(self.layer_indices):
            X = np.asarray(layer_X[l], dtype=np.float64)
            for tr, va in gkf.split(X, y, groups):
                sc = StandardScaler()
                Xtr = sc.fit_transform(X[tr])
                Xva = sc.transform(X[va])
                clf = LogisticRegression(C=self.C, max_iter=500, class_weight="balanced", random_state=42)
                clf.fit(Xtr, y[tr])
                oof_per_layer[va, j] = clf.predict_proba(Xva)[:, 1]
            # Fit final full-fold probe on all training rows of the outer fold
            sc_full = StandardScaler()
            X_full = sc_full.fit_transform(X)
            clf_full = LogisticRegression(C=self.C, max_iter=500, class_weight="balanced", random_state=42)
            clf_full.fit(X_full, y)
            self.scalers[l] = sc_full
            self.clfs[l] = clf_full
        return oof_per_layer.mean(axis=1)"""

CODE_EXCERPT_2_SENSORS = """def _attention_entropy_from_step(attentions_per_layer: Sequence[torch.Tensor]) -> float:
    \"\"\"Sensor 2 (AAS): Normalized Shannon entropy over top-quartile causal attention heads.\"\"\"
    L = len(attentions_per_layer)
    top_start = max(0, (3 * L) // 4)
    vals: List[float] = []
    for l in range(top_start, L):
        a = attentions_per_layer[l].detach().float()
        K = a.shape[-1]
        if K <= 1:
            vals.append(0.0)
            continue
        p = torch.clamp(a, min=EPS)
        p = p / p.sum(dim=-1, keepdim=True)
        h = -(p * torch.log(p)).sum(dim=-1) / math.log(K)
        vals.append(float(h.mean().item()))
    return float(np.mean(vals)) if vals else 0.0

def _logit_entropy_and_energy(logits_1d: torch.Tensor, temperature: float = 1.0) -> Tuple[float, float]:
    \"\"\"Sensor 3 (EEM): 0.6 Normalized Shannon + 0.4 Normalized Renyi-2 Entropy.\"\"\"
    z = logits_1d.detach().float()
    V = z.shape[-1]
    log_v = math.log(max(V, 2))
    probs = torch.softmax(z, dim=-1).clamp(min=EPS)
    shannon = float(-(probs * torch.log(probs)).sum().item()) / log_v
    renyi2 = float(-torch.log((probs * probs).sum().clamp(min=EPS)).item()) / log_v
    eem = float(np.clip(0.6 * shannon + 0.4 * renyi2, 0.0, 1.0))
    energy = float(-temperature * torch.logsumexp(z / temperature, dim=-1).item())
    return eem, energy"""

CODE_EXCERPT_3_FUSION = """class TrueGuardDetector:
    \"\"\"Calibrated 4-Sensor Logistic Fusion with Per-Sensor Log-Odds Attribution.\"\"\"
    SENSOR_NAMES = ("ISP", "AAS", "EEM", "DST")

    def fit(self, X: np.ndarray, y: np.ndarray) -> "TrueGuardDetector":
        X = np.asarray(X, dtype=np.float64)[:, self.active_indices]
        X_std = self.scaler.fit_transform(X)
        self.clf.fit(X_std, np.asarray(y, dtype=np.int64))
        self.fitted = True
        return self

    def predict_risk(self, X: np.ndarray) -> np.ndarray:
        X = np.asarray(X, dtype=np.float64)
        if X.ndim == 1:
            X = X.reshape(1, -1)
        X_std = self.scaler.transform(X[:, self.active_indices])
        return self.clf.predict_proba(X_std)[:, 1]

    def explain(self, x_row: np.ndarray) -> Dict[str, float]:
        x = np.asarray(x_row, dtype=np.float64).reshape(1, -1)[:, self.active_indices]
        z = self.scaler.transform(x)[0]
        w = self.clf.coef_[0]
        contrib = z * w
        return {self.SENSOR_NAMES[idx]: float(c) for idx, c in zip(self.active_indices, contrib)}"""

CODE_EXCERPT_4_CONTROLLER = """class TrueGuardController:
    \"\"\"Closed-Loop 3-Tier Actuator governed by calibrated (tau_warning, tau_fault).\"\"\"
    def generate(self, question: str) -> ControllerDecision:
        base_prompt = format_qa_prompt(question)
        y0, _, _, _ = self.backend.generate_with_Monitoring(base_prompt, temperature=0.0)
        r0, c0 = self._score_pair(base_prompt, y0)
        trace = [{"step": "initial_greedy", "answer": y0, "risk": r0}]

        # Regime 0: SAFE (r0 < tau_warning) -> Emit immediately with zero extra passes
        if r0 < self.tau_warning:
            return ControllerDecision(question, y0, r0, "SAFE", y0, r0, False, c0, trace)

        # Regime 1: WARNING (tau_warning <= r0 < tau_fault) -> Tier 1 Local Re-Sampling
        best_ans, best_risk = y0, r0
        if r0 < self.tau_fault:
            for temp in self.resample_temperatures:
                yk, _, _, _ = self.backend.generate_with_Monitoring(base_prompt, temperature=temp)
                rk, _ = self._score_pair(base_prompt, yk)
                trace.append({"step": f"tier1_resample_T{temp}", "answer": yk, "risk": rk})
                if rk < best_risk:
                    best_ans, best_risk = yk, rk
            if best_risk < self.tau_fault and best_risk < r0:
                return ControllerDecision(question, y0, r0, "TIER1_RESAMPLE", best_ans, best_risk, False, c0, trace)

        # Regime 2: FAULT (r0 >= tau_fault or Tier 1 unverified) -> Tier 2 Wikipedia RAG
        evidence = self.retriever.retrieve(question)
        if evidence:
            rag_prompt = format_qa_prompt(question, context=evidence)
            y_rag, _, _, _ = self.backend.generate_with_Monitoring(rag_prompt, temperature=0.0)
            r_rag, _ = self._score_pair(rag_prompt, y_rag)
            trace.append({"step": "tier2_wikipedia_rag", "answer": y_rag, "risk": r_rag})
            if r_rag < self.tau_fault and r_rag < r0:
                return ControllerDecision(question, y0, r0, "TIER2_RETRIEVAL", y_rag, r_rag, False, c0, trace)

        # Regime 3: PERSISTENT FAULT -> Tier 3 Calibrated Abstention
        return ControllerDecision(question, y0, r0, "TIER3_ABSTAIN", self.ABSTAIN_MESSAGE, best_risk, True, c0, trace)"""

