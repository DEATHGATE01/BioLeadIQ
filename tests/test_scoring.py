"""Tests for scoring rules."""
from scoring.scoring_rules import (
    company_funding_score,
    composite_score,
    location_hub_score,
    role_fit_score,
    scientific_intent_score,
)


def test_role_fit_score() -> None:
    """Test role fit scoring."""
    assert role_fit_score("CEO") == 1.0
    assert role_fit_score("director") == 1.0
    assert role_fit_score("Software Engineer") == 0.5
    assert role_fit_score("") == 0.0
    assert role_fit_score(None) == 0.0


def test_scientific_intent_score() -> None:
    """Test scientific intent scoring."""
    assert scientific_intent_score(0, False) == 0.0
    assert scientific_intent_score(1, False) == 0.4
    assert scientific_intent_score(1, True) == 0.6
    assert scientific_intent_score(5, True) == 1.0
    assert scientific_intent_score(10, True) == 1.0


def test_company_funding_score() -> None:
    """Test company funding scoring."""
    assert company_funding_score("Series A", 2024) == 0.7
    assert company_funding_score("Series B", 2023) == 0.9
    assert company_funding_score("Seed", 2022) == 0.4
    assert company_funding_score("Unknown", None) == 0.3


def test_location_hub_score() -> None:
    """Test location hub scoring."""
    assert location_hub_score("Boston") == 1.0
    assert location_hub_score("Bangalore") == 1.0
    assert location_hub_score("Mumbai") == 0.0


def test_composite_score() -> None:
    """Test composite scoring produces expected structure."""
    row = {
        "title": "CEO",
        "keyword_hits": 3,
        "recent_publication": True,
        "funding_stage": "Series B",
        "last_funding_year": 2024,
        "person_location": "Boston",
    }
    result = composite_score(row)
    assert "probability_score" in result
    assert 0 <= result["probability_score"] <= 100
    assert "role_fit" in result
    assert "scientific_intent" in result
    assert "company_funding" in result
    assert "location_hub" in result
