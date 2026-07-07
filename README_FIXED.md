# Orion Fleet Watchlist Dashboard

## What this project does

This project turns a short OpenSky aircraft movement sample into a first-pass analyst dashboard for the Turkey / Black Sea / Crimea region.

The tool does three things:

1. Uses a cleaned OpenSky aircraft position dataset.
2. Filters aircraft position reports to a watchlist of countries of interest.
3. Flags whether each displayed position is current or potentially stale, then shows the result on a Streamlit map.

This is not a final intelligence judgment. It is a triage tool that helps an analyst narrow a noisy dataset to a smaller set of records worth inspecting.

## Data

Source: OpenSky Network REST API, `/states/all` endpoint.

Scope:

- latitude 40 to 47;
- longitude 27 to 42;
- Turkey / Black Sea / Crimea edge region;
- 6 snapshots;
- 5 minutes between snapshots;
- time window: 2026-07-06 06:14:56 UTC to 06:40:02 UTC.

The raw sample contains:

```text
625 rows
18 columns
```

After cleaning, the dataset contains:

```text
625 rows
17 columns
```

The `sensors` column was dropped because it was empty for every row.

See `data_note.md` or `data_note_fixed.md` for details.

## Week 3 analysis: watchlist filter

The Week 3 analysis filters aircraft position reports to these countries:

- Russian Federation;
- Belarus;
- Syrian Arab Republic.

For each matching position report, the analysis calculates:

```text
position_age_seconds = last_contact - time_position
```

The final stale-position rule is:

```text
stale_position = True if position_age_seconds > 65
```

The threshold is 65 seconds because the evaluation step found that the original 60-second threshold was too sensitive for a few borderline cases.

Output:

```text
outputs/watchlist_flagged.csv
```

or, in the fixed replacement workflow:

```text
outputs/watchlist_flagged_fixed.csv
```

## Key findings

Out of 625 total aircraft position reports:

```text
20 matched the watchlist
3.2% of all reports
```

By country:

```text
Russian Federation: 14
Belarus: 3
Syrian Arab Republic: 3
```

Position freshness:

```text
10 current positions
10 stale positions
```

This matters because a stale map marker can mislead an analyst. The aircraft may no longer be exactly where the map dot appears.

## Dashboard

The Streamlit dashboard maps the watchlist aircraft and lets the user:

- filter by country;
- show only stale positions;
- click markers for details;
- inspect the records in a table;
- download the filtered CSV.

Current live app:

```text
https://orion-t2-jxhzbvogzdtr35civhpcji.streamlit.app/
```

Source:

```text
app.py
```

Fixed replacement source:

```text
app_fixed.py
```

## Evaluation

We evaluated the stale-position rule on 33 hand-labeled position reports:

- 10 random records;
- 23 records selected near the stale/current threshold.

Original rule:

```text
threshold = 60 seconds
31 / 33 agreement
94% agreement
```

Final rule:

```text
threshold = 65 seconds
33 / 33 agreement on the labeled set
```

See `evaluation_fixed.md` for the full explanation.

## How to run the fixed analysis

Install dependencies:

```bash
pip install -r requirements_fixed.txt
```

Run Week 3 analysis:

```bash
python fleet_filter_analysis_fixed.py
```

Run dashboard:

```bash
streamlit run app_fixed.py
```

## Repository files

Core current files:

- `opensky_pull.ipynb` - pulls and cleans OpenSky data.
- `fleet_filter_analysis.ipynb` - original Week 3 watchlist filter.
- `outputs/watchlist_flagged.csv` - original watchlist output.
- `app.py` - current Streamlit dashboard.
- `data_note.md` - current data note.
- `README.md` and `README4.md` - current written project notes.

Fixed replacement files:

- `README_FIXED.md`
- `fleet_filter_analysis_fixed.ipynb`
- `fleet_filter_analysis_fixed.py`
- `app_fixed.py`
- `evaluation_fixed.md`
- `data_note_fixed.md`
- `requirements_fixed.txt`
- `outputs/watchlist_flagged_fixed.csv`

## Known limits

This tool is a first-pass filter, not a final anomaly detector.

Important limits:

- It filters by aircraft registration country, not by suspicious behavior.
- It uses a short static OpenSky sample, not a continuously updating live feed.
- OpenSky coverage depends on volunteer receivers and can be sparse near conflict zones.
- A stale position means "be careful with this map dot", not "this aircraft is suspicious".
- The evaluation set is small and only evaluates the stale-position rule.

## Next steps

The strongest next technical improvement would be behavior-based anomaly scoring:

- large time gaps;
- sudden altitude changes;
- unusual speeds;
- sharp turns;
- aircraft that appear stationary while not marked as on ground.

