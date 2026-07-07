"""Fixed Week 3 analysis for the Orion Fleet Watchlist project.

This script replaces the fragile Colab-only logic with a reproducible version:
- no GitHub token in the data URL;
- watch countries are defined in the file;
- stale threshold is consistently 65 seconds;
- input columns are validated;
- output is written to outputs/watchlist_flagged_fixed.csv.

Run:
    python fleet_filter_analysis_fixed.py
"""

from __future__ import annotations

from pathlib import Path

try:
    import pandas as pd
except ModuleNotFoundError as exc:
    raise SystemExit(
        "Missing dependency: pandas. Install dependencies with "
        "`pip install -r requirements_fixed.txt` or run this notebook in Colab."
    ) from exc


WATCH_COUNTRIES = [
    "Russian Federation",
    "Belarus",
    "Syrian Arab Republic",
]

STALE_THRESHOLD_SECONDS = 65

LOCAL_INPUT_CANDIDATES = [
    Path("cleaned_opensky_data.csv"),
    Path("outputs/cleaned_opensky_data.csv"),
    Path("data/processed/cleaned_opensky_data.csv"),
    Path("opensky_raw_sample.csv"),
]

REMOTE_RAW_SAMPLE_URL = (
    "https://raw.githubusercontent.com/rmcN7/orion-t2/main/opensky_raw_sample.csv"
)

OUTPUT_PATH = Path("outputs/watchlist_flagged_fixed.csv")

REQUIRED_COLUMNS = {
    "icao24",
    "callsign",
    "origin_country",
    "time_position",
    "last_contact",
    "longitude",
    "latitude",
    "baro_altitude",
    "on_ground",
    "velocity",
    "true_track",
    "vertical_rate",
    "geo_altitude",
    "squawk",
    "spi",
    "position_source",
    "pulled_at",
}


def load_source_data() -> pd.DataFrame:
    """Load cleaned data if present, otherwise load the repo raw sample."""
    for path in LOCAL_INPUT_CANDIDATES:
        if path.exists():
            print(f"Loading local data: {path}")
            return pd.read_csv(path)

    print(f"Loading remote raw sample: {REMOTE_RAW_SAMPLE_URL}")
    return pd.read_csv(REMOTE_RAW_SAMPLE_URL)


def clean_if_needed(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the Week 2 cleaning step if the raw sample is loaded."""
    cleaned = df.copy()

    if "sensors" in cleaned.columns:
        cleaned = cleaned.drop(columns=["sensors"])

    cleaned = cleaned.sort_values(["icao24", "pulled_at"]).reset_index(drop=True)
    return cleaned


def validate_columns(df: pd.DataFrame) -> None:
    """Stop early with a clear error if the input schema is wrong."""
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")


def filter_by_country(df: pd.DataFrame, countries: list[str]) -> pd.DataFrame:
    """Filter to watchlist countries and add position freshness fields."""
    result = df[df["origin_country"].isin(countries)].copy()

    result["position_age_seconds"] = (
        result["last_contact"] - result["time_position"]
    ).astype(int)
    result["stale_position"] = (
        result["position_age_seconds"] > STALE_THRESHOLD_SECONDS
    )
    result["callsign"] = (
        result["callsign"]
        .fillna("(no callsign)")
        .astype(str)
        .str.strip()
        .replace("", "(no callsign)")
    )

    return result.sort_values(
        ["origin_country", "icao24", "pulled_at"]
    ).reset_index(drop=True)


def print_summary(flagged: pd.DataFrame, total_rows: int) -> None:
    """Print the Week 3 results in a format that can be copied into a report."""
    print("\nSummary")
    print(f"Total position reports: {total_rows}")
    print(f"Watchlist reports: {len(flagged)}")
    print(f"Watchlist share: {len(flagged) / total_rows:.1%}")
    print(f"Stale threshold: {STALE_THRESHOLD_SECONDS} seconds")

    print("\nBy country")
    print(flagged["origin_country"].value_counts().to_string())

    print("\nBy stale/current")
    print(flagged["stale_position"].value_counts().to_string())

    print("\nMean location and altitude by country")
    print(
        flagged.groupby("origin_country")[
            ["latitude", "longitude", "baro_altitude"]
        ]
        .mean()
        .round(3)
        .to_string()
    )


def main() -> None:
    source = load_source_data()
    cleaned = clean_if_needed(source)
    validate_columns(cleaned)

    flagged = filter_by_country(cleaned, WATCH_COUNTRIES)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    flagged.to_csv(OUTPUT_PATH, index=False)

    print_summary(flagged, total_rows=len(cleaned))
    print(f"\nSaved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
