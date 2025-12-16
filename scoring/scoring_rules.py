"""Rule-based scoring aligned to business signals."""
from typing import Dict

ROLE_KEYWORDS = [
    "director",
    "head",
    "lead",
    "vp",
    "vice president",
    "chief",
    "cso",
    "scientist",
]

BIOTECH_HUBS = [
    "boston",
    "cambridge",
    "san diego",
    "san francisco",
    "south san francisco",
    "basel",
    "london",
    "cambridge, uk",
    "oxford",
    "bangalore",
]

FUNDING_WEIGHTS = {
    "seed": 0.4,
    "series a": 0.6,
    "series b": 0.8,
    "series c": 0.9,
    "public": 1.0,
}


def _normalize(value: float, floor: float = 0.0, ceil: float = 1.0) -> float:
    return max(floor, min(ceil, value))


def role_fit_score(title: str) -> float:
    t = (title or "").lower()
    return 1.0 if any(k in t for k in ROLE_KEYWORDS) else 0.5 if t else 0.0


def scientific_intent_score(keyword_hits: int, recent_publication: bool) -> float:
    if keyword_hits == 0:
        return 0.0
    base = 0.5 if recent_publication else 0.3
    bonus = min(keyword_hits, 5) * 0.1
    return _normalize(base + bonus)


def company_funding_score(stage: str, last_funding_year: int | None) -> float:
    stage_weight = FUNDING_WEIGHTS.get((stage or "").lower(), 0.3)
    recency_bonus = 0.1 if last_funding_year and last_funding_year >= 2023 else 0.0
    return _normalize(stage_weight + recency_bonus)


def location_hub_score(location: str) -> float:
    loc = (location or "").lower()
    return 1.0 if any(hub in loc for hub in BIOTECH_HUBS) else 0.0


def composite_score(row: Dict[str, object]) -> Dict[str, object]:
    role = role_fit_score(str(row.get("title", "")))
    sci = scientific_intent_score(int(row.get("keyword_hits", 0)), bool(row.get("recent_publication")))
    fund = company_funding_score(str(row.get("funding_stage", "")), row.get("last_funding_year"))
    hub = location_hub_score(str(row.get("person_location", "")))

    raw = (role * 30) + (sci * 40) + (fund * 20) + (hub * 10)
    normalized = round(_normalize(raw / 100.0) * 100, 1)

    row["role_fit"] = round(role, 2)
    row["scientific_intent"] = round(sci, 2)
    row["company_funding"] = round(fund, 2)
    row["location_hub"] = round(hub, 2)
    row["probability_score"] = normalized
    return row
