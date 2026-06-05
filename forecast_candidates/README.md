# Forecast candidates

This directory holds generated short-horizon question lists used to choose the
next forecast batch. Refresh it with:

```bash
python scripts/find_near_term_forecasts.py --days 7 --limit 10
```

The generated JSON includes forecastable Metaculus questions and active
Polymarket binary markets whose scheduled resolution/end date is inside the
requested window.
