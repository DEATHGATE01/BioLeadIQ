"""Tests for scoring rules."""
import pytest
from scoring.scoring_rules import (
    composite_score,
    role_fit_score,
    scientific_intent_score,
    company_funding_score,
    location_hub_score,
)


def test_composite_score_basic():
    """Test composite score returns expected fields."""
    profile = {
        "name": "John Doe",
        "title": "CEO",
        "company": "Test Corp",
        "funding_stage": "Series A",
        "keyword_hits": 5,
        "recent_publication": True,
        "last_funding_year": 2024,
        "person_location": "Boston",
    }
    result = composite_score(profile)
    assert "probability_score" in result
    assert 0 <= result["probability_score"] <= 100


def test_role_fit_score():
    """Test role fit scoring."""
    assert role_fit_score("CEO") == 1.0
    assert role_fit_score("Director of Sales") == 1.0
    assert role_fit_score("Intern") == 0.5
    assert role_fit_score("") == 0.0


def test_scientific_intent_score():
    """Test scientific intent scoring."""
    assert scientific_intent_score(0, False) == 0.0
    assert scientific_intent_score(5, True) > scientific_intent_score(3, False)
    assert scientific_intent_score(5, True) <= 1.0


def test_company_funding_score():
    """Test company funding scoring."""
    assert company_funding_score("Series A", 2024) > company_funding_score("Seed", 2020)
    assert company_funding_score("Public", None) == 1.0


def test_location_hub_score():
    """Test location hub scoring."""
    assert location_hub_score("Boston") == 1.0
    assert location_hub_score("Cambridge") == 1.0
    assert location_hub_score("Unknown City") == 0.0
