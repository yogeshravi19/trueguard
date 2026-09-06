# ============================================================
# TRUEGUARD: Comparative Analysis of 20 LLM Hallucination Papers
# R Script — Publication-Quality ggplot2 Visualizations
# Run: source("e:/mini-project/paper_comparison.R")
# Required packages: ggplot2, dplyr, tidyr, scales, ggrepel,
#                    cowplot, viridis, patchwork
# ============================================================

# ---- 0. Install/Load Packages -------------------------------------------
pkgs <- c("ggplot2", "dplyr", "tidyr", "scales", "ggrepel",
          "cowplot", "viridis", "patchwork", "forcats", "RColorBrewer")
for (p in pkgs) {
  if (!requireNamespace(p, quietly = TRUE)) install.packages(p, repos = "https://cran.rstudio.com/")
  library(p, character.only = TRUE)
}

#OUTPUT_DIR <- "e:/mini-project/R_Plotscol"
#dir.create(OUTPUT_DIR, showWarnings = FALSE, recursive = TRUE)
#cat("Plots will be saved to:", OUTPUT_DIR, "\n")

# ---- Publication-quality light theme for all plots -----------------------
theme_pub <- function(base_size = 11) {
  theme_bw(base_size = base_size) +
    theme(
      # White background with black panel border
      plot.background   = element_rect(fill = "white", color = NA),
      panel.background  = element_rect(fill = "white", color = "black", linewidth = 0.6),
      panel.border      = element_rect(fill = NA, color = "black", linewidth = 0.6),
      panel.grid.major  = element_line(color = "grey85", linewidth = 0.3),
      panel.grid.minor  = element_blank(),
      # Dark text for readability
      axis.text         = element_text(color = "black", size = 9),
      axis.title        = element_text(color = "black", size = 11, face = "bold"),
      axis.ticks        = element_line(color = "black", linewidth = 0.4),
      plot.title        = element_text(color = "black", size = 13, face = "bold", hjust = 0),
      plot.subtitle     = element_text(color = "grey30", size = 9, hjust = 0),
      plot.caption      = element_text(color = "grey40", size = 7),
      # Legend styling
      legend.background = element_rect(fill = "white", color = "grey70", linewidth = 0.3),
      legend.key        = element_rect(fill = "white", color = NA),
      legend.text       = element_text(color = "black", size = 8),
      legend.title      = element_text(color = "black", size = 9, face = "bold"),
      strip.text        = element_text(color = "black", size = 9, face = "bold"),
      strip.background  = element_rect(fill = "grey92", color = "black", linewidth = 0.4),
      plot.margin       = margin(12, 16, 10, 12)
    )
}

save_plot <- function(p, name, w = 10, h = 7) {
  path <- file.path(OUTPUT_DIR, paste0(name, ".png"))
  ggsave(path, plot = p, width = w, height = h, dpi = 300, bg = "white")
  cat("Saved:", path, "\n")
}

# ---- Publication-quality color palettes (print-safe, distinct) -----------
pal_signal <- c(
  "Internal States" = "#2166AC",   # strong blue
  "Entropy/Energy"  = "#D6604D",   # muted red
  "Attention"       = "#1B7837",   # forest green
  "Distribution"    = "#7570B3"    # purple
)

pal_category <- c(
  "Detection"   = "#2166AC",
  "Evaluation"  = "#1B7837",
  "Calibration" = "#7570B3",
  "Trust"       = "#D6604D",
  "Retrieval"   = "#E08214"
)

# ============================================================
# DATASET 1: AUROC on HaluEval benchmark (shared across 9 papers)
# ============================================================
auroc_halueval <- data.frame(
  method    = c("MIND\n(P1)", "PRISM\n(P2)", "Sem.Energy\n(P4)", "MHAD\n(P5)",
                "RAUQ\n(P11)", "LLM-Check\n(P12)", "HALLUSHIFT\n(P13)", "SEP\n(P14)", "EPR\n(P17)"),
  paper     = c("P1","P2","P4","P5","P11","P12","P13","P14","P17"),
  auroc     = c(83.6, 86.4, 89.7, 87.1, 90.2, 92.8, 86.9, 94.3, 83.9),
  signal    = c("Internal States","Internal States","Entropy/Energy","Internal States",
                "Attention","Internal States","Distribution","Entropy/Energy","Entropy/Energy"),
  stringsAsFactors = FALSE
)
auroc_halueval$method <- factor(auroc_halueval$method,
                                 levels = auroc_halueval$method[order(auroc_halueval$auroc)])

p1 <- ggplot(auroc_halueval, aes(x = method, y = auroc, fill = signal)) +
  geom_col(width = 0.65, color = "black", linewidth = 0.3, show.legend = TRUE) +
  geom_text(aes(label = paste0(auroc, "%")), hjust = -0.12, color = "black", size = 3.2, fontface = "bold") +
  coord_flip(clip = "on", ylim = c(78, 100)) +
  scale_fill_manual(values = pal_signal) +
  labs(
    title    = "AUROC on HaluEval Benchmark \u2014 9 Papers Compared",
    subtitle = "All methods evaluated on the same HaluEval hallucination detection dataset",
    x        = NULL, y = "AUROC (%)",
    fill     = "Detection Signal",
    caption  = "Sources: Papers 1,2,4,5,11,12,13,14,17 \u00b7 HaluEval benchmark"
  ) +
  theme_pub()

save_plot(p1, "01_auroc_halueval_comparison", w = 10, h = 6)

# ============================================================
# DATASET 2: AUROC on TruthfulQA benchmark (shared across 6 papers)
# ============================================================
auroc_truthfulqa <- data.frame(
  method  = c("MIND\n(P1)", "PRISM\n(P2)", "Sem.Energy\n(P4)", "LLM-Check\n(P12)", "SEP\n(P14)", "EPR\n(P17)"),
  paper   = c("P1","P2","P4","P12","P14","P17"),
  auroc   = c(81.2, 84.7, 88.1, 90.6, 93.7, 82.4),
  stringsAsFactors = FALSE
)
auroc_truthfulqa$method <- factor(auroc_truthfulqa$method,
                                   levels = auroc_truthfulqa$method[order(auroc_truthfulqa$auroc)])

p2 <- ggplot(auroc_truthfulqa, aes(x = method, y = auroc)) +
  geom_segment(aes(xend = method, yend = 78), color = "grey60", linewidth = 0.8) +
  geom_point(aes(fill = auroc), size = 7, shape = 21, color = "black", stroke = 0.6) +
  geom_text(aes(label = paste0(auroc, "%")), color = "black", size = 2.7, fontface = "bold") +
  coord_flip(ylim = c(78, 97)) +
  scale_fill_viridis_c(option = "plasma", name = "AUROC %", limits = c(78, 96)) +
  labs(
    title    = "AUROC on TruthfulQA Benchmark \u2014 6 Papers Compared",
    subtitle = "Hallucination detection performance on the TruthfulQA dataset",
    x = NULL, y = "AUROC (%)",
    caption  = "Sources: Papers 1,2,4,12,14,17 \u00b7 TruthfulQA benchmark"
  ) +
  theme_pub()

save_plot(p2, "02_auroc_truthfulqa_comparison", w = 10, h = 5.5)

# ============================================================
# DATASET 3: AUROC vs F1 Score Scatter — All detection papers
# ============================================================
perf_all <- data.frame(
  method    = c("MIND","PRISM","Sem.Energy","MHAD","Map.Misbelief",
                "RAUQ","LLM-Check","HALLUSHIFT","SEP","HALLUSHIFT++","EPR"),
  paper     = c("P1","P2","P4","P5","P9","P11","P12","P13","P14","P16","P17"),
  auroc     = c(83.6, 86.4, 89.7, 87.1, 84.5, 90.2, 92.8, 86.9, 94.3, 86.3, 83.9),
  f1        = c(80.4, 83.2, 87.1, 84.5, 81.2, 87.3, 89.7, 83.8, 91.2, 82.4, 81.6),
  speedup   = c(1, 1, 1, 1, 3, 1, 45, 1, 8, 1, 1),
  signal    = c("Internal States","Internal States","Entropy/Energy","Internal States",
                "Attention","Attention","Internal States","Distribution",
                "Entropy/Energy","Distribution","Entropy/Energy"),
  stringsAsFactors = FALSE
)

p3 <- ggplot(perf_all, aes(x = auroc, y = f1, fill = signal, size = log(speedup + 1))) +
  geom_point(shape = 21, color = "black", stroke = 0.5, alpha = 0.9) +
  geom_text_repel(aes(label = method), color = "black", size = 3,
                  box.padding = 0.5, point.padding = 0.3,
                  segment.color = "grey50", max.overlaps = 15) +
  scale_fill_manual(values = pal_signal) +
  scale_size_continuous(name = "log(Speedup+1)", range = c(3, 10)) +
  labs(
    title    = "AUROC vs F1 Score \u2014 All Detection Papers",
    subtitle = "Point size = log(speedup factor) \u00b7 Color = detection signal type",
    x = "AUROC (%)", y = "F1 Score (%)",
    fill     = "Detection Signal",
    caption  = "Sources: Papers 1,2,4,5,9,11,12,13,14,16,17"
  ) +
  theme_pub() +
  guides(size = guide_legend(override.aes = list(fill = "grey50")))

save_plot(p3, "03_auroc_vs_f1_scatter", w = 10, h = 7)

# ============================================================
# DATASET 4: Improvement over baseline — papers reporting %gain
# ============================================================
improvement <- data.frame(
  method   = c("PRISM\n(P2)","Sem.Energy\n(P4)","MHAD\n(P5)","FaithEval\n(P10)",
                "RAUQ\n(P11)","LLM-Check\n(P12)","HALLUSHIFT\n(P13)","SEP\n(P14)",
                "BehCal-RL\n(P15)","HALLUSHIFT++\n(P16)","EPR\n(P17)","HumanTrust\n(P19)","ExpandR\n(P20)"),
  gain_pct = c(12.4, 13.0, 9.2, 11.5, 8.9, 15.2, 11.3, 4.1, 18.6, 9.4, 7.3, 22.0, 5.3),
  category = c("Detection","Detection","Detection","Evaluation",
               "Detection","Detection","Detection","Detection",
               "Calibration","Detection","Detection","Trust","Retrieval"),
  stringsAsFactors = FALSE
)
improvement$method <- factor(improvement$method,
                              levels = improvement$method[order(improvement$gain_pct)])

p4 <- ggplot(improvement, aes(x = method, y = gain_pct, fill = category)) +
  geom_col(width = 0.7, color = "black", linewidth = 0.3) +
  geom_text(aes(label = paste0("+", gain_pct, "%")), hjust = -0.12,
            color = "black", size = 3, fontface = "bold") +
  coord_flip(clip = "off", ylim = c(0, 26)) +
  scale_fill_manual(values = pal_category) +
  labs(
    title    = "Improvement Over Baseline (%) \u2014 13 Papers",
    subtitle = "Percentage gain each method achieves over its strongest reported baseline",
    x = NULL, y = "Improvement (%)",
    fill     = "Research Area",
    caption  = "Sources: Papers 2,4,5,10,11,12,13,14,15,16,17,19,20"
  ) +
  theme_pub()

save_plot(p4, "04_improvement_over_baseline", w = 11, h = 7)

# ============================================================
# DATASET 5: Efficiency — Speedup vs AUROC (trade-off analysis)
# ============================================================
efficiency <- data.frame(
  method    = c("Sem.Energy","MHAD","HALLUSHIFT","PRISM","MIND",
                "Map.Misbelief","EPR","RAUQ","SEP","LLM-Check (45x)","LLM-Check (450x)"),
  auroc     = c(89.7, 87.1, 86.9, 86.4, 83.6, 84.5, 83.9, 90.2, 94.3, 92.8, 90.1),
  speedup   = c(1, 1, 1, 1, 1, 3, 1, 1, 8, 45, 450),
  stringsAsFactors = FALSE
)

p5 <- ggplot(efficiency, aes(x = speedup, y = auroc, fill = auroc, label = method)) +
  geom_point(size = 5, shape = 21, color = "black", stroke = 0.6) +
  geom_text_repel(size = 2.8, color = "black", box.padding = 0.5,
                  segment.color = "grey50", max.overlaps = 15) +
  scale_x_log10(
    breaks = c(1, 3, 8, 45, 450),
    labels = c("1\u00d7\n(baseline)", "3\u00d7", "8\u00d7", "45\u00d7", "450\u00d7")
  ) +
  scale_fill_viridis_c(option = "turbo", name = "AUROC %", limits = c(82, 95)) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "grey50", linewidth = 0.5) +
  annotate("text", x = 1.15, y = 82.5, label = "1\u00d7 = same cost as\nmulti-sampling SE",
           color = "grey40", size = 2.5, hjust = 0) +
  labs(
    title    = "Efficiency Trade-off: Speedup Factor vs AUROC",
    subtitle = "X-axis (log scale) = inference speedup relative to multi-sampling baseline",
    x = "Speedup Factor (log scale)", y = "AUROC (%)",
    caption  = "LLM-Check has two variants: 45\u00d7 (white-box) and 450\u00d7 (approximate)"
  ) +
  theme_pub()

save_plot(p5, "05_speedup_vs_auroc_tradeoff", w = 10, h = 7)

# ============================================================
# DATASET 6: TrustLLM — 8 Trustworthiness Dimensions × 3 Model Groups
# ============================================================
trust_dims <- c("Truthfulness","Safety","Fairness","Robustness",
                "Privacy","Ethics","Transparency","Accountability")
trust_df <- data.frame(
  dimension = rep(trust_dims, 3),
  group     = rep(c("GPT-4 Class\n(Proprietary)", "Llama-3 70B\n(Open-Source)", "Avg Open-Source"), each = 8),
  score     = c(
    89.2, 91.4, 83.7, 87.3, 85.6, 88.1, 80.9, 84.2,
    74.1, 79.3, 75.2, 71.8, 76.4, 77.1, 68.3, 72.5,
    67.8, 71.9, 68.6, 64.9, 69.7, 70.8, 62.1, 65.9
  ),
  stringsAsFactors = FALSE
)

p6 <- ggplot(trust_df, aes(x = reorder(dimension, score), y = score, fill = group)) +
  geom_col(position = position_dodge(width = 0.8), width = 0.7, color = "black", linewidth = 0.25) +
  geom_text(aes(label = paste0(score, "%")),
            position = position_dodge(width = 0.8),
            hjust = -0.08, size = 2.2, color = "black") +
  coord_flip(ylim = c(55, 98)) +
  scale_fill_manual(values = c(
    "GPT-4 Class\n(Proprietary)"    = "#2166AC",
    "Llama-3 70B\n(Open-Source)"    = "#1B7837",
    "Avg Open-Source"               = "#7570B3"
  )) +
  labs(
    title    = "TrustLLM (P3): 8 Trustworthiness Dimensions Across Model Classes",
    subtitle = "Proprietary vs open-source LLMs on the TrustLLM benchmark (30+ datasets)",
    x = NULL, y = "Score (%)",
    fill     = "Model Group",
    caption  = "Source: Paper 3 \u2014 TrustLLM, 16 LLMs evaluated"
  ) +
  theme_pub()

save_plot(p6, "06_trustllm_dimensions", w = 11, h = 7)

# ============================================================
# DATASET 7: SEP vs Semantic Entropy — direct comparison across models
# ============================================================
sep_comparison <- data.frame(
  model    = rep(c("LLaMA-2-7B","LLaMA-2-13B","Mistral-7B","Falcon-7B"), 3),
  method   = rep(c("Semantic Entropy\n(multi-pass, 10x cost)",
                   "SEP (single-pass)", "Prev. Probe Baseline"), each = 4),
  auroc    = c(
    91.2, 93.4, 90.8, 88.6,
    94.1, 96.8, 93.7, 91.4,
    84.3, 87.1, 83.9, 81.6
  ),
  stringsAsFactors = FALSE
)

p7 <- ggplot(sep_comparison, aes(x = model, y = auroc, fill = method)) +
  geom_col(position = position_dodge(width = 0.85), width = 0.75, color = "black", linewidth = 0.25) +
  geom_text(aes(label = paste0(auroc, "%")),
            position = position_dodge(width = 0.85),
            vjust = -0.5, size = 2.4, color = "black", fontface = "bold") +
  scale_fill_manual(values = c(
    "Semantic Entropy\n(multi-pass, 10x cost)" = "#D6604D",
    "SEP (single-pass)"                        = "#1B7837",
    "Prev. Probe Baseline"                      = "#999999"
  )) +
  coord_cartesian(ylim = c(78, 101)) +
  labs(
    title    = "SEP (P14) vs Semantic Entropy \u2014 Per-Model AUROC",
    subtitle = "SEP achieves higher AUROC than SE at 8\u00d7 lower cost across 4 LLMs",
    x = "Language Model", y = "AUROC (%)",
    fill     = "Method",
    caption  = "Source: Paper 14 \u2014 Semantic Entropy Probes (SEP)"
  ) +
  theme_pub()

save_plot(p7, "07_sep_vs_semantic_entropy", w = 11, h = 6.5)

# ============================================================
# DATASET 8: Attention vs Entropy methods — Extrinsic vs Intrinsic
# ============================================================
hallu_type <- expand.grid(
  method   = c("Semantic Entropy", "Attention Aggregation\n(Map of Misbelief)", "P-True\n(baseline)"),
  hallu_type = c("Extrinsic Hallucination\n(fabricated info)", "Intrinsic Hallucination\n(contradiction)")
)
hallu_type$auroc <- c(
  89.3, 76.2, 72.1,
  61.4, 84.5, 67.3
)

p8 <- ggplot(hallu_type, aes(x = method, y = auroc, fill = hallu_type)) +
  geom_col(position = position_dodge(width = 0.85), width = 0.75, color = "black", linewidth = 0.25) +
  geom_text(aes(label = paste0(auroc, "%")),
            position = position_dodge(width = 0.85),
            vjust = -0.4, size = 3, color = "black", fontface = "bold") +
  scale_fill_manual(values = c(
    "Extrinsic Hallucination\n(fabricated info)"  = "#D6604D",
    "Intrinsic Hallucination\n(contradiction)"    = "#2166AC"
  )) +
  coord_cartesian(ylim = c(55, 96)) +
  labs(
    title    = "Paper 9: SE vs Attention \u2014 by Hallucination Type",
    subtitle = "SE excels at extrinsic; Attention aggregation excels at intrinsic hallucination",
    x = "Method", y = "AUROC (%)",
    fill     = "Hallucination Type",
    caption  = "Source: Paper 9 \u2014 Map of Misbelief \u00b7 Key motivation for TRUEGUARD multi-signal fusion"
  ) +
  theme_pub()

save_plot(p8, "08_intrinsic_vs_extrinsic_hallucination", w = 10, h = 6.5)

# ============================================================
# DATASET 9: ExpandR — Retrieval Performance (Paper 20)
# ============================================================
expandr <- data.frame(
  dataset  = rep(c("MSMARCO\nPassage","NQ","HotpotQA","BEIR\n(avg)"), 4),
  method   = rep(c("ExpandR (P20, joint opt.)", "DPR (baseline)",
                   "Query Expansion Only", "MonoT5 (CE reranker)"), each = 4),
  ndcg     = c(
    41.2, 54.8, 38.7, 39.6,
    36.8, 51.2, 35.4, 37.3,
    38.9, 52.6, 36.1, 38.1,
    40.1, 53.9, 37.8, 38.8
  ),
  stringsAsFactors = FALSE
)

p9 <- ggplot(expandr, aes(x = dataset, y = ndcg, color = method, group = method)) +
  geom_line(linewidth = 0.9) +
  geom_point(aes(shape = method), size = 3.5, fill = "white", stroke = 0.8) +
  scale_color_manual(values = c(
    "ExpandR (P20, joint opt.)" = "#1B7837",
    "DPR (baseline)"            = "#D6604D",
    "Query Expansion Only"      = "#E08214",
    "MonoT5 (CE reranker)"      = "#2166AC"
  )) +
  scale_shape_manual(values = c(21, 22, 23, 24)) +
  labs(
    title    = "ExpandR (P20): NDCG@10 Across Retrieval Benchmarks",
    subtitle = "Joint LLM + retriever optimization consistently outperforms all baselines",
    x = "Dataset", y = "NDCG@10",
    color    = "Method", shape = "Method",
    caption  = "Source: Paper 20 \u2014 ExpandR"
  ) +
  theme_pub() +
  theme(legend.position = "bottom", legend.box = "horizontal",
        legend.key.width = unit(1.5, "cm"))

save_plot(p9, "09_expandr_retrieval_ndcg", w = 9, h = 6.5)

# ============================================================
# DATASET 10: BehCal-RL (P15) — Calibration quality: ECE comparison
# ============================================================
ece_df <- data.frame(
  method   = rep(c("Standard RLVR", "BehCal-RL (P15, Qwen3-4B)",
                   "GPT-4o (frontier)", "Llama-3-8B (SFT)"), 3),
  dataset  = rep(c("GSM8K", "MATH", "ARC-Challenge"), each = 4),
  ece      = c(
    0.182, 0.043, 0.091, 0.138,
    0.214, 0.057, 0.108, 0.161,
    0.171, 0.038, 0.085, 0.129
  ),
  accuracy = c(
    81.2, 79.4, 92.3, 72.1,
    62.3, 60.1, 76.8, 51.4,
    74.6, 72.9, 87.2, 68.3
  ),
  stringsAsFactors = FALSE
)

p10 <- ggplot(ece_df, aes(x = accuracy, y = ece, shape = dataset, fill = method)) +
  geom_point(size = 4.5, color = "black", stroke = 0.5) +
  geom_text_repel(aes(label = paste0(method, "\n(", dataset, ")")),
                  size = 2.2, color = "black", segment.color = "grey50", max.overlaps = 20) +
  scale_fill_manual(values = c(
    "Standard RLVR"             = "#D6604D",
    "BehCal-RL (P15, Qwen3-4B)" = "#1B7837",
    "GPT-4o (frontier)"         = "#2166AC",
    "Llama-3-8B (SFT)"          = "#7570B3"
  )) +
  scale_shape_manual(values = c(21, 24, 22)) +
  annotate("text", x = 75, y = 0.19, label = "Worse calibration\n(higher ECE)",
           color = "#D6604D", size = 2.5, hjust = 0, fontface = "italic") +
  annotate("text", x = 75, y = 0.035, label = "Better calibration\n(lower ECE)",
           color = "#1B7837", size = 2.5, hjust = 0, fontface = "italic") +
  labs(
    title    = "BehCal-RL (P15): Expected Calibration Error vs Accuracy",
    subtitle = "Lower ECE = better calibrated uncertainty \u00b7 BehCal-RL is well-calibrated at competitive accuracy",
    x = "Accuracy (%)", y = "ECE (lower = better)",
    fill     = "Method", shape = "Dataset",
    caption  = "Source: Paper 15 \u2014 Behaviorally Calibrated Reinforcement Learning"
  ) +
  theme_pub() +
  theme(legend.position = "bottom",
        legend.box = "horizontal") +
  guides(fill = guide_legend(nrow = 1, override.aes = list(shape = 21, size = 4)),
         shape = guide_legend(nrow = 1, override.aes = list(size = 4)))

save_plot(p10, "10_behcal_calibration_ece", w = 10, h = 7.5)

# ============================================================
# DATASET 11: LLM-Check (P12) — Speedup vs baseline (3 variants)
# ============================================================
llmcheck <- data.frame(
  setting   = c("Internal Hidden States\n(white-box, full)",
                "Auxiliary LLM + Attn\n(white-box, fast 45\u00d7)",
                "Prediction Probabilities\n(black-box, 450\u00d7)",
                "Consistency Check\n(baseline)",
                "Retrieval-based\n(baseline)"),
  auroc     = c(93.4, 91.8, 89.2, 84.6, 87.1),
  speedup   = c(1, 45, 450, 0.2, 0.05),
  type      = c("P12 Variant","P12 Variant","P12 Variant","Baseline","Baseline"),
  stringsAsFactors = FALSE
)

p11 <- ggplot(llmcheck, aes(x = log10(speedup + 0.1), y = auroc, fill = type, size = type)) +
  geom_point(shape = 21, color = "black", stroke = 0.6) +
  geom_text_repel(aes(label = setting), size = 2.5, color = "black",
                  segment.color = "grey50", box.padding = 0.6) +
  scale_fill_manual(values = c("P12 Variant" = "#2166AC", "Baseline" = "#D6604D")) +
  scale_size_manual(values  = c("P12 Variant" = 7, "Baseline" = 5)) +
  scale_x_continuous(
    breaks = log10(c(0.1, 1, 45, 450) + 0.1),
    labels = c("Baseline\n(slower)", "1\u00d7", "45\u00d7", "450\u00d7")
  ) +
  labs(
    title    = "LLM-Check (P12): All Variants \u2014 Speedup vs. AUROC",
    subtitle = "Three detection settings from full white-box to efficient black-box",
    x = "Inference Speedup (log scale)", y = "AUROC (%)",
    caption  = "Source: Paper 12 \u2014 LLM-Check. Competing baselines shown in red."
  ) +
  theme_pub() +
  theme(legend.position = "bottom") +
  guides(size = "none")

save_plot(p11, "11_llmcheck_variants", w = 10, h = 6)

# ============================================================
# DATASET 12: Human Trust Study (P19) — Explanation framing effect
# ============================================================
trust_framing <- data.frame(
  condition   = c("No Explanation\n(Isolated)",
                  "Explanation Added\n(Isolated)",
                  "No Explanation\n(Comparative)",
                  "Explanation Added\n(Comparative)"),
  trust_score = c(64.1, 65.8, 61.3, 83.3),
  detection   = c(47.2, 49.1, 44.8, 71.6),
  stringsAsFactors = FALSE
)
trust_long <- pivot_longer(trust_framing, cols = c(trust_score, detection),
                           names_to = "metric", values_to = "value")
trust_long$metric <- ifelse(trust_long$metric == "trust_score",
                             "User Trust Score (%)", "Hallucination Detection Rate (%)")

p12 <- ggplot(trust_long, aes(x = condition, y = value, fill = condition)) +
  geom_col(width = 0.65, color = "black", linewidth = 0.25, show.legend = FALSE) +
  geom_text(aes(label = paste0(value, "%")), vjust = -0.4, size = 3, color = "black", fontface = "bold") +
  facet_wrap(~metric) +
  scale_fill_manual(values = c(
    "No Explanation\n(Isolated)"     = "#999999",
    "Explanation Added\n(Isolated)"  = "#BDBDBD",
    "No Explanation\n(Comparative)"  = "#2166AC",
    "Explanation Added\n(Comparative)" = "#1B7837"
  )) +
  ylim(0, 95) +
  labs(
    title    = "HumanTrust (P19): Impact of Explanation Framing on User Trust",
    subtitle = "Explanations significantly boost trust (+22%) only in comparative evaluation settings",
    x = NULL, y = "Score (%)",
    caption  = "Source: Paper 19 \u2014 Human Trust in Language Model Responses"
  ) +
  theme_pub() +
  theme(axis.text.x = element_text(size = 7))

save_plot(p12, "12_human_trust_framing", w = 11, h = 6.5)

# ============================================================
# FINAL: Combined 4-panel summary figure
# ============================================================
p_combined <- (p1 + p7) / (p8 + p4) +
  plot_annotation(
    title   = "TRUEGUARD Research: Cross-Paper Numerical Comparison",
    subtitle = "Top-left: HaluEval AUROC | Top-right: SEP vs SE | Bottom-left: Intrinsic vs Extrinsic | Bottom-right: Improvements",
    theme   = theme(
      plot.background = element_rect(fill = "white", color = NA),
      plot.title      = element_text(color = "black", size = 14, face = "bold"),
      plot.subtitle   = element_text(color = "grey30", size = 8)
    )
  )

save_plot(p_combined, "00_combined_summary_4panel", w = 20, h = 16)

cat("\n========================================\n")
cat("All 12 plots saved to:", OUTPUT_DIR, "\n")
cat("Files created:\n")
cat(paste0(" - ", sprintf("%02d", 0:12), c("_combined_summary_4panel",
   "_auroc_halueval_comparison", "_auroc_truthfulqa_comparison",
   "_auroc_vs_f1_scatter", "_improvement_over_baseline",
   "_speedup_vs_auroc_tradeoff", "_trustllm_dimensions",
   "_sep_vs_semantic_entropy", "_intrinsic_vs_extrinsic_hallucination",
   "_expandr_retrieval_ndcg", "_behcal_calibration_ece",
   "_llmcheck_variants", "_human_trust_framing"), ".png\n"), sep = "")
cat("========================================\n")
