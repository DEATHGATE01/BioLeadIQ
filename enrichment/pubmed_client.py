"""PubMed enrichment client with reproducible static fallback.

Uses NCBI E-utilities for live lookups when network + API key
are available. Defaults to a static lookup table to keep the
pipeline reproducible without external dependencies.
"""
import os
import datetime
import logging
from typing import Dict, List, Tuple

import requests

# Minimal static corpus to keep deterministic behavior
STATIC_PUBS: Dict[str, Dict[str, int]] = {
    "Dr. Maya Chen": {"last_publication_year": 2024, "keyword_hits": 3},
    "Lucas Patel": {"last_publication_year": 2023, "keyword_hits": 1},
    "Amelia Rossi": {"last_publication_year": 2024, "keyword_hits": 4},
    "Ravi Narayanan": {"last_publication_year": 2022, "keyword_hits": 0},
}

KEYWORDS = [
    "Drug-Induced Liver Injury",
    "hepatic",
    "toxicology",
    "3D culture",
]

NCBI_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"


def _within_last_24_months(year: int) -> bool:
    current_year = datetime.date.today().year
    return (current_year - year) <= 2


def _static_intent(name: str) -> Tuple[int, bool]:
    entry = STATIC_PUBS.get(name)
    if not entry:
        return 0, False
    return entry["keyword_hits"], _within_last_24_months(entry["last_publication_year"])


def _live_pubmed_count(name: str, keywords: List[str]) -> int:
    api_key = os.getenv("NCBI_API_KEY")
    query = f"{name} AND (" + " OR ".join(keywords) + ")"
    params = {
        "db": "pubmed",
        "retmode": "json",
        "term": query,
        "datetype": "pdat",
        "reldate": 730,  # last 24 months
    }
    if api_key:
        params["api_key"] = api_key
    try:
        resp = requests.get(NCBI_BASE, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return int(data.get("esearchresult", {}).get("count", 0))
    except Exception as exc:  # noqa: BLE001
        logging.warning("PubMed live lookup failed, falling back to static: %s", exc)
        return 0


def get_scientific_intent(name: str) -> Dict[str, object]:
    """Return scientific signal for a person.

    Output schema:
    {
        "keyword_hits": int,
        "recent_publication": bool,
        "used_live_lookup": bool,
    }
    """
    live_allowed = os.getenv("ENABLE_PUBMED_LIVE", "false").lower() == "true"
    if live_allowed:
        hits = _live_pubmed_count(name, KEYWORDS)
        recent = hits > 0
        return {"keyword_hits": hits, "recent_publication": recent, "used_live_lookup": True}

    hits, recent = _static_intent(name)
    return {"keyword_hits": hits, "recent_publication": recent, "used_live_lookup": False}
