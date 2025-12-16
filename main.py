"""BioLeadIQ reproducible lead-ranking pipeline."""
import argparse
import os
from pathlib import Path
from typing import List, Dict

import pandas as pd
from dotenv import load_dotenv

from enrichment.pubmed_client import get_scientific_intent
from enrichment.funding_enricher import load_funding, enrich_funding
from scoring.scoring_rules import composite_score
from export.sheets_exporter import export_to_csv, export_to_google_sheet

load_dotenv()

DATA_DIR = Path(__file__).parent / "data"


def read_linkedin_csv(path: Path) -> List[Dict[str, object]]:
    df = pd.read_csv(path)
    return df.to_dict(orient="records")


def enrich_pubmed(profiles: List[Dict[str, object]]) -> List[Dict[str, object]]:
    for row in profiles:
        intent = get_scientific_intent(row.get("name", ""))
        row.update(intent)
        row["scientific_signal"] = "yes" if intent["keyword_hits"] > 0 else "no"
    return profiles


def apply_scoring(profiles: List[Dict[str, object]]) -> List[Dict[str, object]]:
    scored = [composite_score(row) for row in profiles]
    scored = sorted(scored, key=lambda r: r.get("probability_score", 0), reverse=True)
    for idx, row in enumerate(scored, start=1):
        row["rank"] = idx
    return scored


def format_for_output(scored: List[Dict[str, object]]) -> List[Dict[str, object]]:
    """Map internal field names to required output headers."""
    formatted = []
    for row in scored:
        formatted.append(
            {
                "Rank": row.get("rank"),
                "Probability Score (0-100)": row.get("probability_score"),
                "Name": row.get("name"),
                "Title": row.get("title"),
                "Company": row.get("company"),
                "Person Location": row.get("person_location"),
                "Company HQ": row.get("company_hq"),
                "Scientific Signal (papers / yes-no)": row.get("scientific_signal"),
                "Funding Stage": row.get("funding_stage"),
                "LinkedIn URL": row.get("linkedin_url"),
            }
        )
    return formatted


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="BioLeadIQ reproducible scoring")
    parser.add_argument("--linkedin", type=Path, default=DATA_DIR / "linkedin_profiles.csv", help="Path to LinkedIn CSV")
    parser.add_argument("--funding", type=Path, default=DATA_DIR / "funding_data.json", help="Path to funding JSON")
    parser.add_argument("--out-csv", type=Path, default=Path("output.csv"), help="Where to write the CSV output")
    parser.add_argument("--sheet-name", type=str, default=os.getenv("GOOGLE_SHEET_NAME", "BioLeadIQ"), help="Existing Google Sheet name")
    parser.add_argument("--creds", type=str, default=os.getenv("GOOGLE_SHEETS_CREDS"), help="Path to Google service account creds JSON")
    parser.add_argument("--skip-sheets", action="store_true", help="Skip Google Sheets export even if creds are present")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    profiles = read_linkedin_csv(args.linkedin)
    funding_map = load_funding(args.funding)
    profiles = enrich_funding(profiles, funding_map)
    profiles = enrich_pubmed(profiles)
    scored = apply_scoring(profiles)
    output_rows = format_for_output(scored)

    csv_path = export_to_csv(output_rows, str(args.out_csv))
    print(f"CSV written to: {csv_path}")

    creds_path = args.creds
    if creds_path and not args.skip_sheets:
        try:
            url = export_to_google_sheet(output_rows, creds_path, args.sheet_name)
            print(f"Google Sheet updated: {url}")
        except Exception as exc:  # noqa: BLE001
            print(f"Google Sheets export failed: {exc}")
    else:
        print("Google Sheets export skipped (no creds or --skip-sheets)")


if __name__ == "__main__":
    main()
