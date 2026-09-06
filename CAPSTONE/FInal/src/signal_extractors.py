"""
TRUEGUARD Signal Extractors
Implements the 4 intrinsic mathematical signals:
1. ISP: Internal State Probes (Linear classifiers over hidden states)
2. AAS: Attention Anomaly Score (Normalized Shannon entropy over attention heads)
3. EEM: Entropy-Energy Monitor (Combined Shannon uncertainty and Renyi-2 confidence)
4. DST: Distribution Shift Tracker (Temporal cosine distance of latent states)
"""

import torch
import numpy as np

def extract_isp(hidden_states, probes=None, layers=None):
    """
    Extracts Internal State Probes (ISP) risk score.
    
    Args:
        hidden_states: Tuple of layer tensors, each of shape (batch, seq_len, hidden_dim).
        probes: Optional list of trained sklearn LogisticRegression models or torch Linear layers.
        layers: List of layer indices to probe (e.g., [15, 20, 25, 30]).
        
    Returns:
        isp_score: float or np.ndarray of shape (batch,) in range [0, 1].
    """
    if layers is None:
        total_layers = len(hidden_states)
        # Choose 4 uniformly spaced layers in middle-to-late region
        layers = [int(total_layers * frac) for frac in [0.45, 0.60, 0.75, 0.90]]

    valid_layers = [l for l in layers if l < len(hidden_states)]
    if not valid_layers:
        batch_size = hidden_states[0].shape[0] if len(hidden_states) > 0 else 1
        return np.zeros(batch_size, dtype=np.float32)

    batch_size = hidden_states[0].shape[0]
    layer_scores = []

    for i, l in enumerate(valid_layers):
        # Extract last-token hidden state: shape (batch, hidden_dim)
        h = hidden_states[l][:, -1, :]
        
        if probes is not None and i < len(probes) and probes[i] is not None:
            probe = probes[i]
            if hasattr(probe, "predict_proba"):
                h_np = h.detach().cpu().to(torch.float32).numpy()
                proba = probe.predict_proba(h_np)[:, 1]
                layer_scores.append(proba)
            elif isinstance(probe, torch.nn.Module):
                with torch.no_grad():
                    logits = probe(h.to(torch.float32))
                    proba = torch.sigmoid(logits).squeeze(-1).detach().cpu().numpy()
                    layer_scores.append(proba)
        else:
            # Mechanistic proxy: normalized dispersion across hidden dimensions
            h_f = h.to(torch.float32)
            h_std = torch.std(h_f, dim=-1)
            proxy_score = torch.sigmoid(h_std - 1.0).detach().cpu().numpy()
            layer_scores.append(proxy_score)

    if not layer_scores:
        return np.zeros(batch_size, dtype=np.float32)

    return np.mean(layer_scores, axis=0)


def extract_aas(attentions, layers=None, epsilon=1e-10):
    """
    Extracts Attention Anomaly Score (AAS) using normalized Shannon entropy.
    
    Args:
        attentions: Tuple of attention tensors, each of shape (batch, heads, seq_len, seq_len).
        layers: List of deep layer indices to monitor (e.g. final quartile).
        epsilon: Small constant for numerical stability.
        
    Returns:
        aas_score: float or np.ndarray of shape (batch,) in range [0, 1].
    """
    if layers is None:
        total_layers = len(attentions)
        # Final quartile layers
        start_l = max(0, int(total_layers * 0.75))
        layers = list(range(start_l, total_layers))

    valid_layers = [l for l in layers if l < len(attentions)]
    if not valid_layers:
        batch_size = attentions[0].shape[0] if len(attentions) > 0 else 1
        return np.zeros(batch_size, dtype=np.float32)

    batch_size = attentions[0].shape[0]
    layer_entropies = []

    for l in valid_layers:
        # Attention from current (last) token to all previous tokens: (batch, heads, seq_len)
        attn = attentions[l][:, :, -1, :]
        seq_len = attn.shape[-1]
        
        # Shannon entropy across context tokens: H = -sum(p * log(p + eps))
        H = -torch.sum(attn * torch.log(attn + epsilon), dim=-1) # (batch, heads)
        
        # Max theoretical entropy is log(seq_len)
        max_entropy = np.log(seq_len) if seq_len > 1 else 1.0
        H_norm = H / max_entropy # (batch, heads)
        
        # Average across all heads
        layer_entropies.append(H_norm.mean(dim=-1).detach().cpu().numpy())

    return np.mean(layer_entropies, axis=0)


def extract_eem(logits, w_e=0.6, epsilon=1e-10):
    """
    Extracts Entropy-Energy Monitor (EEM) score.
    Combines Shannon entropy (uncertainty) and Renyi-2 entropy (confidence).
    
    Args:
        logits: Tensor of shape (batch, seq_len, vocab_size) or (batch, vocab_size).
        w_e: Weight for Shannon entropy component (default 0.6).
        epsilon: Numerical stability constant.
        
    Returns:
        eem_score: np.ndarray of shape (batch,) in range [0, 1].
    """
    if logits.dim() == 3:
        last_logits = logits[:, -1, :].to(torch.float32)
    else:
        last_logits = logits.to(torch.float32)

    vocab_size = last_logits.shape[-1]
    max_entropy = np.log(vocab_size) if vocab_size > 1 else 1.0

    probs = torch.softmax(last_logits, dim=-1)

    # 1. Shannon Entropy
    shannon = -torch.sum(probs * torch.log(probs + epsilon), dim=-1)
    H_norm = torch.clamp(shannon / max_entropy, 0.0, 1.0)

    # 2. Renyi-2 Entropy: -log(sum(p^2))
    sum_p_sq = torch.sum(probs ** 2, dim=-1)
    renyi2 = -torch.log(sum_p_sq + epsilon)
    E_norm = torch.clamp(renyi2 / max_entropy, 0.0, 1.0)

    # Combined EEM
    eem = w_e * H_norm + (1.0 - w_e) * E_norm
    return eem.detach().cpu().numpy()


def extract_dst(hidden_states, prev_h_avg=None, layers=None):
    """
    Extracts Distribution Shift Tracker (DST) score via temporal cosine distance.
    
    Args:
        hidden_states: Tuple of hidden state tensors from current forward step.
        prev_h_avg: Tensor of averaged hidden representations from step t-1.
        layers: Layers to average for distribution tracking (e.g. [20, 25, 30]).
        
    Returns:
        (dst_score, current_h_avg)
    """
    if layers is None:
        total_layers = len(hidden_states)
        layers = [int(total_layers * frac) for frac in [0.60, 0.75, 0.90]]

    valid_layers = [l for l in layers if l < len(hidden_states)]
    batch_size = hidden_states[0].shape[0] if len(hidden_states) > 0 else 1

    if not valid_layers:
        return np.zeros(batch_size, dtype=np.float32), None

    # Stack last-token hidden states across layers: (num_layers, batch, hidden_dim)
    stacked = torch.stack([hidden_states[l][:, -1, :].to(torch.float32) for l in valid_layers])
    current_h_avg = torch.mean(stacked, dim=0) # (batch, hidden_dim)

    if prev_h_avg is None:
        return np.zeros(batch_size, dtype=np.float32), current_h_avg

    # Cosine distance: d = (1 - cos_sim) / 2, range [0, 1]
    cos_sim = torch.nn.functional.cosine_similarity(current_h_avg, prev_h_avg, dim=-1)
    dst = (1.0 - cos_sim) / 2.0
    dst = torch.clamp(dst, 0.0, 1.0)

    return dst.detach().cpu().numpy(), current_h_avg


def extract_all_signals(logits, hidden_states, attentions, prev_h_avg=None, probes=None, config=None):
    """
    Unified single-pass extractor for all 4 TRUEGUARD signals.
    
    Returns:
        raw_features: np.ndarray of shape (batch, 4) -> [ISP, AAS, EEM, DST]
        current_h_avg: for next step DST comparison
    """
    isp_layers = config.get("signals", {}).get("isp", {}).get("layers", None) if config else None
    aas_layers = config.get("signals", {}).get("aas", {}).get("layers", None) if config else None
    dst_layers = config.get("signals", {}).get("dst", {}).get("layers", None) if config else None
    w_e = config.get("signals", {}).get("eem", {}).get("entropy_weight_we", 0.6) if config else 0.6

    isp = extract_isp(hidden_states, probes=probes, layers=isp_layers)
    aas = extract_aas(attentions, layers=aas_layers)
    eem = extract_eem(logits, w_e=w_e)
    dst, current_h_avg = extract_dst(hidden_states, prev_h_avg=prev_h_avg, layers=dst_layers)

    # Combine into feature matrix (batch, 4)
    features = np.column_stack([isp, aas, eem, dst])
    return features, current_h_avg
