"""Tests for scoring rules."""
import pytest
from scoring.scoring_rules import composite_score, company_size_score, title_seniority_score


def test_composite_score_basic():
    """Test composite score returns expected fields."""
    profile = {
        "name": "John Doe",
        "title": "CEO",
        "company": "Test Corp",
        "company_size": 100,
        "funding_stage": "Series A",
        "keyword_hits": 5,
    }
    result = composite_score(profile)
    assert "probability_score" in result
    assert 0 <= result["probability_score"] <= 100


def test_company_size_score():
    """Test company size scoring."""
    assert company_size_score(10) < company_size_score(1000)
    assert company_size_score(0) == 0


def test_title_seniority_score():
    """Test title seniority scoring."""
    assert title_seniority_score("CEO") >= title_seniority_score("Intern")
    assert title_seniority_score("") == 0
