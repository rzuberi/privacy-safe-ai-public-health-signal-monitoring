import argparse

import numpy as np
import pandas as pd

from src.utils import DATA_DIR, FEATURE_COLUMNS, ensure_directories


def build_synthetic_dataset(n_days: int = 180, seed: int = 7) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2025-01-01", periods=n_days, freq="D")
    t = np.arange(n_days)

    season = 0.08 * np.sin(2 * np.pi * t / 30)
    trend = 0.002 * t

    df = pd.DataFrame(
        {
            "date": dates,
            "respiratory_visits_index": 1.0 + season + trend + rng.normal(0, 0.05, n_days),
            "otc_cold_flu_index": 0.9 + 0.7 * season + rng.normal(0, 0.05, n_days),
            "school_absence_index": 1.0 + 0.5 * season + rng.normal(0, 0.04, n_days),
            "symptom_search_index": 1.1 + 0.9 * season + rng.normal(0, 0.06, n_days),
            "wastewater_proxy_index": 0.95 + 0.6 * season + rng.normal(0, 0.05, n_days),
            "reporting_lag_days": rng.choice([0, 1, 2], p=[0.74, 0.2, 0.06], size=n_days),
        }
    )

    anomaly_windows = [
        (35, 42, {"respiratory_visits_index": 0.28, "otc_cold_flu_index": 0.20, "symptom_search_index": 0.22}),
        (92, 98, {"school_absence_index": 0.18, "symptom_search_index": 0.16, "wastewater_proxy_index": 0.14}),
        (138, 146, {"respiratory_visits_index": 0.24, "school_absence_index": 0.15, "wastewater_proxy_index": 0.18}),
    ]
    df["event_label"] = 0

    for start, end, shifts in anomaly_windows:
        row_index = list(range(start, end + 1))
        for column, shift in shifts.items():
            df.loc[row_index, column] += shift + rng.normal(0, shift / 6, end - start + 1)
        df.loc[row_index, "event_label"] = 1

    # A few benign reporting artifacts make the synthetic data less tidy.
    reporting_spikes = [57, 112, 160]
    df.loc[reporting_spikes, "reporting_lag_days"] = 3
    df.loc[reporting_spikes, "symptom_search_index"] += 0.06

    df["composite_signal_mean"] = df[FEATURE_COLUMNS].mean(axis=1)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic public-health-style signals.")
    parser.add_argument("--n-days", type=int, default=180)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--output", default=str(DATA_DIR / "synthetic_signals.csv"))
    args = parser.parse_args()

    ensure_directories()
    df = build_synthetic_dataset(n_days=args.n_days, seed=args.seed)
    df.to_csv(args.output, index=False)
    print(f"wrote {len(df)} rows to {args.output}")


if __name__ == "__main__":
    main()
