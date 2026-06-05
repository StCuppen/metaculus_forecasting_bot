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
