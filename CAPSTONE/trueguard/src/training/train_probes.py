def train_isp_probes(model, train_dataset, config):
    """
    Train lightweight linear probes on LLM hidden states.
    
    Args:
        model: Loaded LLM (LLaMA-2-7B or Mistral-7B)
        train_dataset: Labeled hallucination data
            - Format: List of dicts with keys:
              - 'input': str (prompt)
              - 'output': str (generated text)
              - 'label': int (0=factual, 1=hallucination)
        config: Configuration dict with ISP settings
        
    Returns:
        probes: List of trained linear classifiers (one per layer)
        scalers: Feature scalers for each layer (for inference)
        
    Procedure:
        1. For each layer in config.isp.layers:
           - Extract hidden state h^L_t at that layer
           - For each sample in train_dataset:
             * Run forward pass to get h^L (hidden state)
             * Label: 0 (factual) or 1 (hallucination)
        
        2. For each layer:
           - Concatenate all hidden states → matrix H (N × hidden_dim)
           - Normalize using StandardScaler
           - Train logistic regression classifier:
             * X = H (normalized hidden states)
             * y = labels (0 or 1)
             * Loss: Binary cross-entropy
             * Optimizer: Adam, lr=0.001
             * Regularization: L2 (λ=0.0001)
             * Early stopping: validation loss patience=5
        
        3. Save probes and scalers to disk for inference
        
    Hyperparameters:
        - layers: [15, 20, 25, 30] (uniformly spaced middle to late)
        - hidden_dim: 4096 (from LLaMA-2-7B architecture)
        - regularization: L2 with λ=0.0001
        - train/val split: 80/20 of provided dataset
    
    Example:
        >>> train_data = load_hallucination_dataset('train_split')
        >>> probes, scalers = train_isp_probes(model, train_data, config)
        >>> save_checkpoints(probes, scalers, 'checkpoints/isp_probes.pkl')
    """
    pass
