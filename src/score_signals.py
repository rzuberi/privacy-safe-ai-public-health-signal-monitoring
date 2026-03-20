import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from src.utils import (
    DEFAULT_ALERT_THRESHOLD,
    FEATURE_COLUMNS,
    OUTPUT_DIR,
    ROBUST_SCALE_FACTOR,
    ensure_directories,
    load_json,
    load_signals,
    top_feature_explanation,
)


def score_dataframe(df: pd.DataFrame, baseline: dict) -> pd.DataFrame:
    scored = df.copy()
    contributions_per_feature = {}

    for column in FEATURE_COLUMNS:
        median = baseline["feature_stats"][column]["median"]
        mad = baseline["feature_stats"][column]["mad"]
        robust_z = (scored[column] - median) / (ROBUST_SCALE_FACTOR * mad)
        contribution = robust_z.clip(lower=0)
        scored[f"{column}_z"] = robust_z
        scored[f"{column}_contribution"] = contribution
        contributions_per_feature[column] = contribution

    contribution_columns = [f"{column}_contribution" for column in FEATURE_COLUMNS]
    scored["risk_score"] = scored[contribution_columns].mean(axis=1)
    threshold = float(baseline.get("threshold", DEFAULT_ALERT_THRESHOLD))
    scored["alert_flag"] = (scored["risk_score"] >= threshold).astype(int)

    explanation_text = []
    for _, row in scored.iterrows():
        contributions = {column: float(row[f"{column}_contribution"]) for column in FEATURE_COLUMNS}
        explanation_text.append(top_feature_explanation(contributions))
    scored["explanation"] = explanation_text
    return scored


def make_plot(scored: pd.DataFrame, output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(scored["date"], scored["risk_score"], label="risk score", color="#0f766e", linewidth=2)
    ax.scatter(
        scored.loc[scored["alert_flag"] == 1, "date"],
        scored.loc[scored["alert_flag"] == 1, "risk_score"],
        color="#b91c1c",
        label="alert",
        s=22,
        zorder=3,
    )
    ax.set_title("Synthetic public-health signal risk score")
    ax.set_xlabel("date")
    ax.set_ylabel("risk score")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Score synthetic signals with the saved baseline.")
    parser.add_argument("--input", default=None)
    parser.add_argument("--baseline", default=str(OUTPUT_DIR / "baseline_summary.json"))
    parser.add_argument("--output", default=str(OUTPUT_DIR / "sample_predictions.csv"))
    parser.add_argument("--plot-output", default=str(OUTPUT_DIR / "sample_plot.png"))
    args = parser.parse_args()

    ensure_directories()
    df = load_signals(Path(args.input) if args.input else None)
    baseline = load_json(Path(args.baseline))
    missing_columns = [column for column in FEATURE_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError("input dataset is missing expected columns: {}".format(", ".join(missing_columns)))
    if float(baseline.get("threshold", DEFAULT_ALERT_THRESHOLD)) <= 0:
        raise ValueError("baseline threshold must be positive")
    scored = score_dataframe(df, baseline)
    scored.to_csv(args.output, index=False)
    make_plot(scored, Path(args.plot_output))
    print(f"saved predictions to {args.output}")
    print(f"saved plot to {args.plot_output}")


if __name__ == "__main__":
    main()
