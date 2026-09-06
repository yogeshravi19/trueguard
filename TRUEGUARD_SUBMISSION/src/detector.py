"""
TRUEGUARD Real-Time Detector Engine
Executes autoregressive generation with concurrent token-level signal extraction and risk monitoring.
"""

import time
import torch
import numpy as np

from .signal_extractors import extract_all_signals
from .normalization import OnlineZScoreScaler
from .fusion import TrueGuardFusion

class TrueGuardDetector:
    """
    Main TRUEGUARD Guard Engine.
    Intercepts autoregressive token generation to extract intrinsic signals and compute risk scores on-the-fly.
    """
    def __init__(self, model, tokenizer, fusion_layer=None, probes=None, config=None):
        self.model = model
        self.tokenizer = tokenizer
        self.fusion = fusion_layer if fusion_layer is not None else TrueGuardFusion()
        self.probes = probes
        self.config = config or {}
        self.scaler = OnlineZScoreScaler(num_features=4)
        
        mit_cfg = self.config.get("mitigation", {})
        self.risk_threshold = mit_cfg.get("risk_threshold", 0.50)
        self.sequence_gamma = mit_cfg.get("sequence_gamma", 0.20)

    def generate_and_guard(
        self,
        prompt,
        max_new_tokens=50,
        temperature=0.7,
        do_sample=False,
        halt_on_risk=True
    ):
        """
        Executes generation while monitoring hallucination risk at every token step.
        
        Args:
            prompt: str prompt text.
            max_new_tokens: Maximum tokens to generate.
            temperature: Softmax temperature.
            do_sample: Sampling vs greedy decoding.
            halt_on_risk: If True, halts generation as soon as R(t) > threshold.
            
        Returns:
            dict containing:
                - generated_text: str
                - tokens: list of token strings
                - token_risks: list of R(t) float values
                - signal_traces: dict with ISP, AAS, EEM, DST per token
                - sequence_risk: R_seq
                - halted_early: bool
                - total_latency_ms: float
                - per_token_latency_ms: float
        """
        device = next(self.model.parameters()).device
        inputs = self.tokenizer(prompt, return_tensors="pt").to(device)
        input_ids = inputs.input_ids
        
        self.scaler.reset()
        prev_h_avg = None
        
        generated_token_ids = []
        token_strings = []
        token_risks = []
        signal_traces = {"ISP": [], "AAS": [], "EEM": [], "DST": []}
        
        start_time = time.perf_counter()
        halted_early = False

        for step in range(max_new_tokens):
            t0 = time.perf_counter()
            
            with torch.no_grad():
                # Single forward pass requesting hidden states and attention matrices
                outputs = self.model(
                    input_ids,
                    output_hidden_states=True,
                    output_attentions=True
                )
            
            # 1. Generation Step
            next_token_logits = outputs.logits[:, -1, :]
            if do_sample and temperature > 0:
                probs = torch.softmax(next_token_logits / temperature, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)
            else:
                next_token = torch.argmax(next_token_logits, dim=-1, keepdim=True)

            next_token_id = next_token.item()
            tok_str = self.tokenizer.decode([next_token_id], skip_special_tokens=True)
            
            # 2. Extract TRUEGUARD Signals
            raw_features, prev_h_avg = extract_all_signals(
                logits=next_token_logits,
                hidden_states=outputs.hidden_states,
                attentions=outputs.attentions,
                prev_h_avg=prev_h_avg,
                probes=self.probes,
                config=self.config
            )
            raw_vec = raw_features[0] # (4,)

            # 3. Online Normalization
            self.scaler.update(raw_vec)
            norm_vec = self.scaler.transform(raw_vec)

            # 4. Learned Multi-Signal Fusion
            r_t = self.fusion.predict_risk_token(norm_vec)

            # Record metrics
            generated_token_ids.append(next_token_id)
            token_strings.append(tok_str)
            token_risks.append(r_t)
            signal_traces["ISP"].append(float(raw_vec[0]))
            signal_traces["AAS"].append(float(raw_vec[1]))
            signal_traces["EEM"].append(float(raw_vec[2]))
            signal_traces["DST"].append(float(raw_vec[3]))

            # Append to context
            input_ids = torch.cat([input_ids, next_token], dim=1)

            # 5. Check Active Mitigation Trigger
            if halt_on_risk and r_t > self.risk_threshold:
                halted_early = True
                break

            if next_token_id == self.tokenizer.eos_token_id:
                break

        total_time = (time.perf_counter() - start_time) * 1000.0 # ms
        num_tokens = max(1, len(generated_token_ids))
        per_token_latency = total_time / num_tokens

        sequence_risk = self.fusion.compute_sequence_risk(
            token_risks,
            threshold=self.risk_threshold,
            gamma=self.sequence_gamma
        )

        full_generated_text = self.tokenizer.decode(generated_token_ids, skip_special_tokens=True)

        return {
            "prompt": prompt,
            "generated_text": full_generated_text,
            "tokens": token_strings,
            "token_risks": token_risks,
            "signal_traces": signal_traces,
            "sequence_risk": sequence_risk,
            "halted_early": halted_early,
            "total_latency_ms": total_time,
            "per_token_latency_ms": per_token_latency,
            "tokens_generated": num_tokens
        }
