"""Tests for main CLI entry point."""
import tempfile
from pathlib import Path

from main import format_for_output, read_linkedin_csv


def test_read_linkedin_csv() -> None:
    """Test reading LinkedIn CSV."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("name,title,company,linkedin_url\n")
        f.write("John Doe,CEO,Test Corp,https://linkedin.com/in/john\n")
        path = Path(f.name)
    result = read_linkedin_csv(path)
    assert len(result) == 1
    assert result[0]["name"] == "John Doe"


def test_format_for_output() -> None:
    """Test output formatting."""
    scored = [
        {
            "rank": 1,
            "probability_score": 85.5,
            "name": "Jane Smith",
            "title": "CTO",
            "company": "AI Inc",
            "person_location": "SF",
            "company_hq": "NYC",
            "scientific_signal": "yes",
            "funding_stage": "Series B",
            "linkedin_url": "https://linkedin.com/in/jane",
        }
    ]
    output = format_for_output(scored)
    assert len(output) == 1
    assert output[0]["Rank"] == 1
    assert output[0]["Probability Score (0-100)"] == 85.5
    assert output[0]["Name"] == "Jane Smith"
