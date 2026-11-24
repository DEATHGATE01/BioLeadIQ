"""Funding enricher merges static funding data into profile rows."""
import json
from pathlib import Path
from typing import Dict, List


def load_funding(path: Path | str) -> Dict[str, Dict[str, object]]:
    path = Path(path)
    with path.open("r", encoding="utf-8") as fp:
        data = json.load(fp)
    return {row["company"].strip(): row for row in data}


def enrich_funding(
    profiles: List[Dict[str, object]], funding_map: Dict[str, Dict[str, object]]
) -> List[Dict[str, object]]:
    for profile in profiles:
        company = (profile.get("company") or "").strip()
        if company in funding_map:
            profile["funding_stage"] = funding_map[company].get("stage")
            profile["last_funding_year"] = funding_map[company].get("year")
    return profiles
