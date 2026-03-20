import argparse
from pathlib import Path

import pandas as pd

from src.utils import OUTPUT_DIR, ensure_directories, save_json


def safe_divide(numerator: float, denominator: float) -> float:
    return 0.0 if denominator == 0 else numerator / denominator


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate predictions against synthetic event labels.")
    parser.add_argument("--predictions", default=str(OUTPUT_DIR / "sample_predictions.csv"))
    parser.add_argument("--output", default=str(OUTPUT_DIR / "evaluation_summary.json"))
    args = parser.parse_args()

    ensure_directories()
    df = pd.read_csv(args.predictions)

    tp = int(((df["alert_flag"] == 1) & (df["event_label"] == 1)).sum())
    fp = int(((df["alert_flag"] == 1) & (df["event_label"] == 0)).sum())
    tn = int(((df["alert_flag"] == 0) & (df["event_label"] == 0)).sum())
    fn = int(((df["alert_flag"] == 0) & (df["event_label"] == 1)).sum())

    precision = safe_divide(tp, tp + fp)
    recall = safe_divide(tp, tp + fn)
    f1 = safe_divide(2 * precision * recall, precision + recall)
    alert_rate = safe_divide(int(df["alert_flag"].sum()), len(df))

    summary = {
        "dataset_rows": int(len(df)),
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "alert_rate": round(alert_rate, 4),
        "note": "Metrics are against synthetic labels and are only sanity checks for the demo.",
    }
    save_json(summary, Path(args.output))
    print(f"saved evaluation summary to {args.output}")


if __name__ == "__main__":
    main()
