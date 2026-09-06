"""
TRUEGUARD Model & Tokenizer Loader
Handles loading Causal Language Models with internal state and attention hooks enabled.
"""

import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GPT2LMHeadModel, GPT2Tokenizer

def load_trueguard_model(
    model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    device="auto",
    torch_dtype=None,
    trust_remote_code=True
):
    """
    Loads causal LM and tokenizer with hidden states and attention matrices enabled.
    
    Args:
        model_name: HuggingFace model identifier or local path.
        device: "auto", "cuda", or "cpu".
        torch_dtype: torch.float16, torch.bfloat16, or torch.float32.
        trust_remote_code: bool.
        
    Returns:
        model, tokenizer, device
    """
    if device == "auto":
        target_device = "cuda" if torch.cuda.is_available() else "cpu"
    else:
        target_device = device

    if torch_dtype is None:
        dtype = torch.float16 if target_device == "cuda" else torch.float32
    else:
        dtype = torch_dtype

    print(f"[TRUEGUARD Loader] Loading model '{model_name}' on {target_device} ({dtype})...")
    
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=trust_remote_code
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Ensure output_hidden_states and output_attentions are set
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=dtype,
        output_hidden_states=True,
        output_attentions=True,
        trust_remote_code=trust_remote_code,
        low_cpu_mem_usage=True
    )
    
    model.to(target_device)
    model.eval()
    
    print(f"[TRUEGUARD Loader] Model loaded successfully: {model.__class__.__name__}")
    return model, tokenizer, target_device
