"""(Re)render human-readable Markdown (.md) next to every forecast-record JSON.

New records already get a .md at write time; run this to render older records or to
refresh the .md after enrichment adds outcomes/community predictions.

Usage: python scripts/render_record_markdown.py [--records-dir forecast_records]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.agent.forecast_records import render_record_markdown  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Markdown views for forecast records.")
    parser.add_argument("--records-dir", default="forecast_records")
    args = parser.parse_args()

    rendered = 0
    failed = 0
    for path in sorted(Path(args.records_dir).rglob("*.json")):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            path.with_suffix(".md").write_text(render_record_markdown(record), encoding="utf-8")
            rendered += 1
        except Exception as exc:
            failed += 1
            print(f"failed {path}: {exc}")
    print({"rendered": rendered, "failed": failed})


if __name__ == "__main__":
    main()
