"""Tests for enrichment modules."""
import tempfile
from pathlib import Path

from enrichment.funding_enricher import enrich_funding, load_funding


def test_load_funding_empty() -> None:
    """Test loading funding data from empty file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        f.write("{}")
        path = Path(f.name)
    result = load_funding(path)
    assert result == {}


def test_enrich_funding_no_match() -> None:
    """Test funding enrichment with no matching company."""
    profiles = [{"company": "Unknown Corp"}]
    funding_map = {"Known Corp": {"stage": "Series B"}}
    result = enrich_funding(profiles, funding_map)
    assert result[0].get("funding_stage") is None
