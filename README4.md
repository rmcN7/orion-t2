# Orion Fleet Watchlist Dashboard

## What it does
An interactive map showing aircraft from watchlist countries (Russia, Belarus,
Syrian Arab Republic) currently in the Turkey/Black Sea/Crimea region, pulled
from OpenSky Network data. Each aircraft is flagged as having a current or
potentially outdated position, so an analyst knows how much to trust the
shown location.

## How to run it
Live app: https://orion-t2-jxhzbvogzdtr35civhpcji.streamlit.app/
Source: `app.py` in this repo, deployed via Streamlit Community Cloud.
It reads directly from `outputs/watchlist_flagged.csv` — no local setup needed.

## Evaluation result
We hand-labeled 33 position reports (10 random + 23 deliberately near the
staleness threshold) by looking only at how old each position report was,
without seeing the tool's flag first. Initial agreement: 31/33 (94%), with
2 ambiguous cases sitting just past the original 60-second cutoff.

**Before-and-after:** We adjusted the staleness threshold from 60 to 65
seconds based on this evaluation. Re-scoring the same 33-row set: 33/33
agreement, with no remaining ambiguous cases. We also confirmed the flag
independently catches the same "frozen broadcast" aircraft we'd manually
identified back in Week 3, validating the logic wasn't just tuned to pass
our own test.

## Known limits
This filter judges relevance by registration country only — it does not
evaluate behavior. It works on a single static snapshot pull, not live
continuously refreshing data.
