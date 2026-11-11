import matplotlib.pyplot as plt
import numpy as np
import os

# Create figures directory if it doesn't exist
os.makedirs("../figures", exist_ok=True)

# Data for comparison
models = ['Standard AI', 'Single-Signal', 'Semantic Entropy', 'TRUEGUARD (Ours)']
auroc = [0.50, 0.768, 0.862, 0.914]
latency = [0.0, 1.2, 142.3, 8.4] # in ms overhead

# 1. AUROC Comparison Chart
plt.figure(figsize=(8, 5))
colors = ['#cccccc', '#ffcc99', '#ff9999', '#99ff99']
bars = plt.bar(models, auroc, color=colors, edgecolor='black')

plt.title("Hallucination Detection Accuracy (AUROC)\nHigher is Better", fontsize=14, fontweight='bold')
plt.ylabel("AUROC Score", fontsize=12)
plt.ylim(0.4, 1.0)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add value text on top of bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.01, round(yval, 3), ha='center', va='bottom', fontweight='bold', fontsize=11)

plt.tight_layout()
plt.savefig("../figures/fig_accuracy_comparison.png", dpi=300)
print("Saved: figures/fig_accuracy_comparison.png")

# 2. Latency Comparison Chart (Log Scale)
plt.figure(figsize=(8, 5))
latency_bars = [1.0, 1.2, 142.3, 8.4] # Give Standard AI a nominal 1.0 for log scale
bars2 = plt.bar(models, latency_bars, color=colors, edgecolor='black')

plt.title("Time Delay Overhead per Word (Speed)\nLower is Better", fontsize=14, fontweight='bold')
plt.ylabel("Extra Latency per token (milliseconds)", fontsize=12)
plt.yscale('log')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add text
for i, bar in enumerate(bars2):
    yval = latency[i]
    text_val = "0 ms" if yval == 0.0 else f"+{yval} ms"
    # Position text slightly above the bar
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.2, text_val, ha='center', va='bottom', fontweight='bold', fontsize=11)

plt.tight_layout()
plt.savefig("../figures/fig_latency_comparison.png", dpi=300)
print("Saved: figures/fig_latency_comparison.png")
