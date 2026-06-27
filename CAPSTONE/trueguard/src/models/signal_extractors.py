import torch
import numpy as np

def extract_isp(hidden_states, probes, layers=[15, 20, 25, 30]):
    """
    Extract ISP (Internal State Probes) risk score.
    hidden_states: tuple of layer outputs from LLM.
    probes: list of trained logistic regression classifiers (sklearn).
    """
    if not probes:
        # If no trained probes are provided, return random proxy for demonstration
        return np.random.uniform(0, 1, size=hidden_states[0].shape[0])
        
    isp_scores = []
    for i, layer_idx in enumerate(layers):
        if layer_idx < len(hidden_states):
            h = hidden_states[layer_idx][:, -1, :].detach().cpu().numpy()
            score = probes[i].predict_proba(h)[:, 1]
            isp_scores.append(score)
    
    if len(isp_scores) == 0:
        return np.zeros(hidden_states[0].shape[0])
    return np.mean(isp_scores, axis=0)

def extract_aas(attentions, layers=[25, 26, 27, 28, 29, 30, 31]):
    """
    Extract AAS (Attention Anomaly Score) using normalized Shannon entropy.
    """
    aas_scores = []
    for l in layers:
        if l < len(attentions):
            # attentions[l] shape: (batch, heads, seq_len, seq_len)
            attn = attentions[l][:, :, -1, :] 
            entropy = -torch.sum(attn * torch.log(attn + 1e-10), dim=-1)
            max_entropy = np.log(attn.shape[-1] if attn.shape[-1] > 1 else 2)
            norm_entropy = entropy / max_entropy
            aas_scores.append(norm_entropy.mean(dim=-1).detach().cpu().numpy())
            
    if len(aas_scores) == 0:
        return np.zeros(attentions[0].shape[0])
    return np.mean(aas_scores, axis=0)

def extract_eem(logits, w_e=0.6):
    """
    Extract EEM (Entropy-Energy Monitor) using Shannon and Renyi-2 entropy.
    """
    last_logits = logits[:, -1, :]
    probs = torch.softmax(last_logits, dim=-1)
    
    # Shannon Entropy
    entropy = -torch.sum(probs * torch.log(probs + 1e-10), dim=-1)
    max_entropy = np.log(probs.shape[-1])
    h_norm = entropy / max_entropy
    
    # Renyi-2 Energy
    r2 = -torch.log(torch.sum(probs**2, dim=-1) + 1e-10)
    e_norm = r2 / max_entropy
    
    eem = w_e * h_norm + (1 - w_e) * e_norm
    return eem.detach().cpu().numpy()

def extract_dst(hidden_states, prev_h_avg, layers=[20, 25, 30]):
    """
    Extract DST (Distribution Shift Tracker) using cosine distance.
    """
    valid_layers = [l for l in layers if l < len(hidden_states)]
    if not valid_layers:
        return np.zeros(hidden_states[0].shape[0]), None
        
    h_avg = torch.mean(torch.stack([hidden_states[l][:, -1, :] for l in valid_layers]), dim=0)
    
    if prev_h_avg is None:
        return np.zeros(h_avg.shape[0]), h_avg
    
    cos_sim = torch.nn.functional.cosine_similarity(h_avg, prev_h_avg, dim=-1)
    dist = (1 - cos_sim) / 2
    
    return dist.detach().cpu().numpy(), h_avg
