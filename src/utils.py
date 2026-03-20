import json
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "outputs"
DEFAULT_ALERT_THRESHOLD = 2.35
ROBUST_SCALE_FACTOR = 1.4826
FEATURE_COLUMNS = [
    "respiratory_visits_index",
    "otc_cold_flu_index",
    "school_absence_index",
    "symptom_search_index",
    "wastewater_proxy_index",
]


def ensure_directories() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_signals(path: Optional[Path] = None) -> pd.DataFrame:
    csv_path = path or DATA_DIR / "synthetic_signals.csv"
    df = pd.read_csv(csv_path, parse_dates=["date"])
    return df.sort_values("date").reset_index(drop=True)


def robust_mad(values: pd.Series) -> float:
    median = float(values.median())
    mad = float(np.median(np.abs(values - median)))
    return mad if mad > 1e-6 else 1.0


def compute_reference_stats(df: pd.DataFrame, feature_columns: Iterable[str]) -> Dict[str, Dict[str, float]]:
    stats: Dict[str, Dict[str, float]] = {}
    for column in feature_columns:
        stats[column] = {
            "median": float(df[column].median()),
            "mad": robust_mad(df[column]),
        }
    return stats


def save_json(payload: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def top_feature_explanation(contributions: Dict[str, float], top_k: int = 2) -> str:
    ranked: List[tuple[str, float]] = sorted(contributions.items(), key=lambda item: item[1], reverse=True)
    snippets = [f"{name}={value:.2f}" for name, value in ranked[:top_k] if value > 0]
    return "stable baseline" if not snippets else "top contributors: " + ", ".join(snippets)
