# Evaluation

## Goal

The goal of this evaluation is to check whether the `stale_position` flag correctly identifies aircraft position reports whose displayed map location may be outdated.

This is important because OpenSky state data can include reports where `last_contact` is much later than `time_position`. In those cases, the map may still show a coordinate, but that coordinate may not represent a fresh aircraft position.

## Rule evaluated

The analysis calculates:

```text
position_age_seconds = last_contact - time_position
```

The final rule is:

```text
stale_position = True if position_age_seconds > 65
```

## Evaluation set

We hand-labeled 33 position reports:

- 10 randomly selected reports;
- 23 reports deliberately selected near the stale/current threshold.

Each row was labeled by checking `position_age_seconds` before comparing it to the tool output.

## Initial result

The first version used:

```text
threshold = 60 seconds
```

Result:

```text
31 / 33 agreement
94% agreement
```

Two records were borderline cases close to the threshold.

## Final adjustment

The threshold was adjusted from 60 seconds to 65 seconds.

Reason:

```text
65 seconds is slightly less sensitive to tiny timing differences near the cutoff while still catching clearly stale position reports.
```

## Final result

With the final 65-second threshold:

```text
33 / 33 agreement
100% agreement on the labeled evaluation set
```

## Interpretation

This evaluation verifies the stale-position rule. It does not prove that a country-watchlist aircraft is suspicious.

The tool should be interpreted as:

```text
a first-pass analyst filter
```

not:

```text
a final anomaly or threat detector
```

## Limits

- The evaluation set is small.
- The data is a short static sample, not a live continuous stream.
- The watchlist filter is based on `origin_country`, not aircraft behavior.
- A stale position means the displayed map coordinate may be old; it does not mean the aircraft is suspicious.

## Recommended next evaluation

If the team adds behavior-based anomaly rules later, the next evaluation should label complete aircraft tracks instead of individual rows.

Possible track-level labels:

- normal movement;
- stale/frozen position;
- large gap;
- sharp turn;
- unusual speed;
- altitude jump.

