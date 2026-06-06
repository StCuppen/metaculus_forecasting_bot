# Forecast Records

Durable JSON forecast records are written here by the forecasting pipeline.

Each record is intended to preserve the visible forecast output needed for
feedback loops:

- question identifiers and URL when available
- final forecast values
- visible model/report output
- search/evidence metadata
- token usage and run diagnostics
- publish intent/status metadata

Outcome enrichment should append resolution and scoring fields after questions
resolve.

## Layout (for easy inspection)

Records are organized into one subfolder per platform, with a descriptive filename:

```
forecast_records/
  metaculus/   YYYYMMDD-HHMMSS_metaculus_<runtype>_<question-slug>_<digest>.json
  polymarket/  YYYYMMDD-HHMMSS_polymarket_<runtype>_<question-slug>_<digest>.json
  other/       ...
```

- `<runtype>` is `tournament`, `oneoff`, or `test` (from `FORECAST_RUN_TYPE`, set by the pipeline mode).
- Platform is inferred from the question URL/text; `platform` and `run_type` are also stored inside each record.
- Tooling (`scripts/enrich_forecast_records.py`, `scripts/forecast_scoreboard.py`) globs recursively, so
  older flat records in the root and new subfoldered records are both picked up.

