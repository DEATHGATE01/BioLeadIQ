"""Funding enricher merges static funding data into profile rows."""
import json
from pathlib import Path
from typing import Dict, List


def load_funding(path: Path) -> Dict[str, Dict[str, object]]:
    with path.open("r", encoding="utf-8") as fp:
        data = json.load(fp)
    return {row["company"].strip(): row for row in data}
