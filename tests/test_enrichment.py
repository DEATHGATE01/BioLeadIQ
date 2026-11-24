"""Tests for enrichment modules."""
import pytest
from enrichment.funding_enricher import load_funding, enrich_funding


def test_load_funding_empty():
    """Test loading funding data from empty file."""
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write('{}')
        path = f.name
    result = load_funding(path)
    assert result == {}


def test_enrich_funding_no_match():
    """Test funding enrichment with no matching company."""
    profiles = [{"company": "Unknown Corp"}]
    funding_map = {"Known Corp": {"stage": "Series B"}}
    result = enrich_funding(profiles, funding_map)
    assert result[0].get("funding_stage") is None
