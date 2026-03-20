import argparse
from pathlib import Path

import pandas as pd

from src.utils import OUTPUT_DIR, ensure_directories, load_json, save_json


def safe_divide(numerator: float, denominator: float) -> float:
    return 0.0 if denominator == 0 else numerator / denominator


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate predictions against synthetic event labels.")
    parser.add_argument("--predictions", default=str(OUTPUT_DIR / "sample_predictions.csv"))
    parser.add_argument("--baseline", default=str(OUTPUT_DIR / "baseline_summary.json"))
    parser.add_argument("--output", default=str(OUTPUT_DIR / "evaluation_summary.json"))
    args = parser.parse_args()

    ensure_directories()
    df = pd.read_csv(args.predictions)
    baseline = load_json(Path(args.baseline))
    reference_days = int(baseline.get("reference_days", 60))
    if reference_days >= len(df):
        raise ValueError("reference_days must be smaller than the number of prediction rows")

    evaluated_df = df.iloc[reference_days:].reset_index(drop=True)

    tp = int(((evaluated_df["alert_flag"] == 1) & (evaluated_df["event_label"] == 1)).sum())
    fp = int(((evaluated_df["alert_flag"] == 1) & (evaluated_df["event_label"] == 0)).sum())
    tn = int(((evaluated_df["alert_flag"] == 0) & (evaluated_df["event_label"] == 0)).sum())
    fn = int(((evaluated_df["alert_flag"] == 0) & (evaluated_df["event_label"] == 1)).sum())

    precision = safe_divide(tp, tp + fp)
    recall = safe_divide(tp, tp + fn)
    f1 = safe_divide(2 * precision * recall, precision + recall)
    alert_rate = safe_divide(int(evaluated_df["alert_flag"].sum()), len(evaluated_df))

    summary = {
        "dataset_rows": int(len(df)),
        "evaluated_rows": int(len(evaluated_df)),
        "reference_days_excluded": reference_days,
        "data_scope": "synthetic aggregate toy signals only",
        "intended_use": "repository sanity check only",
        "operational_relevance": "none",
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "alert_rate": round(alert_rate, 4),
        "evaluation_limits": [
            "Labels are synthetic and were generated for a narrow toy scenario.",
            "Metrics exclude the reference window used to fit the baseline.",
            "These metrics should not be treated as evidence of real-world monitoring performance.",
            "The summary is useful for regression checks inside the demo repository only.",
        ],
        "note": "Metrics come from a single synthetic run with hand-authored toy anomalies and are computed only on the out-of-sample monitoring period after the reference window.",
    }
    save_json(summary, Path(args.output))
    print(f"saved evaluation summary to {args.output}")


if __name__ == "__main__":
    main()
