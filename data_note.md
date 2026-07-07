# Data Note — OpenSky Network Pull

## Source
OpenSky Network REST API (https://opensky-network.org), `/states/all` endpoint,
accessed via authenticated OAuth2 client credentials.

## Scope
Bounding box: lat 40-47, lon 27-42 — covers Turkey, Georgia, Romania, Bulgaria,
and the edges of the Black Sea/Crimea region.

We originally targeted a narrower box directly over the Black Sea/Crimea
(lat 44-46.5, lon 32-37) but it returned zero aircraft — likely because
commercial airlines avoid that airspace due to the ongoing war, and OpenSky's
volunteer-hosted ground receivers have little to no coverage there. We widened
the box to include neighboring commercial air traffic while still capturing
activity at the conflict zone's edges.

Time window: 2026-07-06, 06:14:56 UTC to 06:40:02 UTC (~26 minutes), captured
as 6 snapshots taken 5 minutes apart, since `/states/all` only returns a live
snapshot with no built-in history.

## Size
625 rows, 17 columns (after dropping the `sensors` column — see below).

## Cleaning steps
- Checked for duplicate (icao24, pulled_at) pairs across the 6 snapshots — found 0.
- Dropped the `sensors` column — always null for non-feeder API accounts, carries no information.
- Left missing `baro_altitude`, `vertical_rate`, `geo_altitude` values as-is (2.6-3.2% of rows) —
  confirmed these correspond to aircraft with `on_ground = True`, where these fields don't apply.
- Left missing `squawk` values as-is (29.4% of rows) — transponder codes aren't always broadcast;
  this is expected, not a data quality issue.

## Assumptions
- Altitude fields (`baro_altitude`, `geo_altitude`) are in meters.
- `velocity` is in meters/second; `true_track` is degrees clockwise from true north.
- Latitude/longitude use WGS-84, decimal degrees.
- `time_position`, `last_contact`, `pulled_at` are Unix timestamps in UTC.
- Missing values appear as `None`/`NaN`, never as `0` or `-1`.

## Known limits
- Our "tracks" are 6 timestamped snapshots per aircraft at most, not continuous flight paths.
- OpenSky coverage depends on volunteer ground receivers, which are sparse in active conflict
  zones — our dataset captures traffic at the edges of Black Sea/Crimea airspace, not necessarily
  inside it.
- Access tokens expire after 30 minutes; our pull script refreshes the token automatically.
- Our account has a daily credit limit (4,000/day per endpoint) — future pulls should pace
  around this.
- This ~26-minute window is a narrow slice of one day/time — not necessarily representative of
  other times.

## Dataset description
Each row represents one aircraft's position at a single point in time. Most aircraft are
commercial flights cruising between roughly 3,300m-11,000m altitude (median ~9,754m) at
130-220 m/s, with a small number (16 of 625 rows) on the ground. No obviously impossible
altitude or speed values were found.


