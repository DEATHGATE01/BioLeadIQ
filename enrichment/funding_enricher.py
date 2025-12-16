"""Funding enricher merges static funding data into profile rows."""
import json
from typing import Dict, List
from pathlib import Path


def load_funding(path: Path) -> Dict[str, Dict[str, object]]:
    with path.open("r", encoding="utf-8") as fp:
        data = json.load(fp)
    return {row["company"].strip(): row for row in data}


def enrich_funding(profiles: List[Dict[str, object]], funding_map: Dict[str, Dict[str, object]]) -> List[Dict[str, object]]:
    for row in profiles:
        company = row.get("company", "").strip()
        funding = funding_map.get(company, {})
        row["funding_stage"] = funding.get("funding_stage", "Unknown")
        row["last_funding_year"] = funding.get("last_funding_year", None)
    return profiles
