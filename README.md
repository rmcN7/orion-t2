# Fleet Watchlist Filter

## What it does
Filters aircraft position reports to a watchlist of countries of interest
(Russian Federation, Belarus, Syrian Arab Republic) and flags whether each
position is fresh or stale, based on OpenSky data for the Turkey/Black Sea/
Crimea region.

## How to run it
Open `fleet_filter_analysis.ipynb` in Colab and run all cells top to bottom.
It loads the cleaned dataset directly from this repo's `/outputs` folder
(no re-pulling from OpenSky needed) and produces `watchlist_flagged.csv`.

## Output definition
Each row is one aircraft position report matching a watchlist country. Two
added columns explain the result:
- `position_age_seconds`: how old the position report actually is
  (last_contact minus time_position)
- `stale_position`: `True` if that gap exceeds 60 seconds, meaning the
  shown location may not reflect the aircraft's real-time position

This filter judges aircraft purely by registration country, not behavior —
it is a first-pass narrowing tool, not a verdict.

## Messy data handling
- Missing altitude, squawk, and callsign values are handled safely by
  pandas' default comparison/matching behavior; no special-case code needed.
- Blank/NaN callsigns display as "(no callsign)"; trailing whitespace is stripped.
- This filter works on individual position reports, not full tracks, so
  aircraft with only one snapshot are handled identically to those with many.

## Key finding
Of 625 total position reports, 20 (3.2%) matched the watchlist, with Russia
making up 14 of those. Exactly half (10 of 20) showed stale position data,
some over 50 minutes old — a real limitation to account for in any
operational use of this filter.
