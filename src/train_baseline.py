import argparse
from pathlib import Path

from src.utils import (
    DEFAULT_ALERT_THRESHOLD,
    FEATURE_COLUMNS,
    OUTPUT_DIR,
    compute_reference_stats,
    ensure_directories,
    load_signals,
    save_json,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fit a simple robust baseline on a reference window.")
    parser.add_argument("--input", default=None)
    parser.add_argument("--reference-days", type=int, default=60)
    parser.add_argument("--threshold", type=float, default=DEFAULT_ALERT_THRESHOLD)
    parser.add_argument("--output", default=str(OUTPUT_DIR / "baseline_summary.json"))
    args = parser.parse_args()

    ensure_directories()
    df = load_signals(Path(args.input) if args.input else None)
    if args.reference_days <= 0:
        raise ValueError("reference_days must be positive")
    if args.reference_days > len(df):
        raise ValueError("reference_days cannot exceed dataset length")
    if args.threshold <= 0:
        raise ValueError("threshold must be positive")

    reference_df = df.iloc[: args.reference_days].copy()
    stats = compute_reference_stats(reference_df, FEATURE_COLUMNS)

    payload = {
        "model_name": "robust_reference_zscore",
        "reference_days": args.reference_days,
        "threshold": args.threshold,
        "feature_columns": FEATURE_COLUMNS,
        "feature_stats": stats,
        "notes": [
            "Simple baseline for interpretable anomaly scoring.",
            "Uses only aggregate synthetic signals in this repository.",
            "Threshold is a demo default rather than a validated operating point.",
        ],
    }
    save_json(payload, Path(args.output))
    print(f"saved baseline summary to {args.output}")


if __name__ == "__main__":
    main()
