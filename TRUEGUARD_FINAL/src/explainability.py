"""
TRUEGUARD Explainability Engine
Generates token-level trust annotations, HTML highlights, and contrastive signal attributions.
"""

class TokenTrustVisualizer:
    """
    Renders token-level trust annotations and explanations from TRUEGUARD detection traces.
    """
    @staticmethod
    def render_ansi_terminal(tokens, risks):
        """Prints ANSI color-coded tokens to terminal console."""
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        RED = "\033[91m"
        RESET = "\033[0m"

        output_parts = []
        for token, risk in zip(tokens, risks):
            if risk < 0.30:
                color = GREEN
            elif risk < 0.60:
                color = YELLOW
            else:
                color = RED
            output_parts.append(f"{color}{token}{RESET}")
        return "".join(output_parts)

    @staticmethod
    def render_html(tokens, risks, title="TRUEGUARD Token Risk Visualizer"):
        """Generates rich interactive HTML span markup with tooltips."""
        html = [
            f"<div style='font-family: monospace; font-size: 16px; line-height: 1.8; "
            f"padding: 15px; border-radius: 8px; border: 1px solid #ddd; background: #fafafa;'>"
            f"<div style='font-weight: bold; margin-bottom: 8px;'>{title}</div>"
        ]

        for token, risk in zip(tokens, risks):
            if risk < 0.30:
                color = "#155724"
                bg = "#d4edda"
                border = "#c3e6cb"
            elif risk < 0.60:
                color = "#856404"
                bg = "#fff3cd"
                border = "#ffeeba"
            else:
                color = "#721c24"
                bg = "#f8d7da"
                border = "#f5c6cb"

            clean_tok = token.replace("\n", "&para;<br/>").replace(" ", "&nbsp;")
            span = (
                f"<span title='Risk: {risk:.3f}' style='background-color: {bg}; color: {color}; "
                f"border: 1px solid {border}; border-radius: 4px; padding: 2px 4px; margin: 0 1px;'>"
                f"{clean_tok}</span>"
            )
            html.append(span)

        html.append(
            "</div><div style='margin-top: 8px; font-size: 12px;'>"
            "<span style='background:#d4edda; color:#155724; padding:2px 6px; border-radius:3px;'>🟢 Confident (&lt;0.30)</span> "
            "<span style='background:#fff3cd; color:#856404; padding:2px 6px; border-radius:3px;'>🟡 Review (0.30-0.60)</span> "
            "<span style='background:#f8d7da; color:#721c24; padding:2px 6px; border-radius:3px;'>🔴 Risk (&gt;0.60)</span>"
            "</div>"
        )
        return "\n".join(html)

    @staticmethod
    def generate_contrastive_explanation(signal_traces, token_idx=-1):
        """
        Explains which of the 4 intrinsic signals drove the risk alert.
        """
        isp = signal_traces["ISP"][token_idx]
        aas = signal_traces["AAS"][token_idx]
        eem = signal_traces["EEM"][token_idx]
        dst = signal_traces["DST"][token_idx]

        signals = {"Internal Representation (ISP)": isp, "Attention Dispersal (AAS)": aas,
                   "Predictive Uncertainty (EEM)": eem, "Distribution Drift (DST)": dst}

        dominant_signal, max_val = max(signals.items(), key=lambda item: item[1])

        explanation = (
            f"Dominant hallucination driver: {dominant_signal} (score: {max_val:.3f}). "
        )
        if dominant_signal == "Predictive Uncertainty (EEM)":
            explanation += "The model experienced an entropy spike across vocabulary tokens."
        elif dominant_signal == "Attention Dispersal (AAS)":
            explanation += "Attention dispersed away from context tokens toward irrelevant positions."
        elif dominant_signal == "Distribution Drift (DST)":
            explanation += "Hidden states deviated significantly from preceding factual trajectory."
        else:
            explanation += "Linear probe detected latent state inconsistent with verified facts."

        return explanation
