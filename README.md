# BioLeadIQ

## 1) What problem does this solve?
Produces a reproducible, explainable ranking of professionals most likely to adopt 3D in-vitro models, consolidating LinkedIn identity, PubMed intent, and funding signals into one scored sheet.

## 2) What data sources are used?
- LinkedIn identification: `data/linkedin_profiles.csv` (name, title, company, location, LinkedIn URL). Demo uses manual CSV; Proxycurl/Apify could generate the same schema.
- PubMed scientific intent: static fallback in `enrichment/pubmed_client.py` with optional live NCBI E-utilities lookup (disabled by default for reproducibility).
- Funding data: `data/funding_data.json` (funding stage, last funding year), substitutable with Crunchbase API if desired.

## 3) How is the score calculated?
Rule-based weight: `score = role_fit*30 + scientific_intent*40 + company_funding*20 + location_hub*10`, normalized to 0–100. Sub-scores are derived from title keywords, PubMed keyword hits (last 24 months emphasis), funding stage/recency, and whether the person sits in a biotech hub. Implemented in `scoring/scoring_rules.py`.

## 4) How is the Google Sheet generated?
Pipeline runs via `python main.py`. Results are always written to `output.csv`. If `GOOGLE_SHEETS_CREDS` (path to service account JSON) and `GOOGLE_SHEET_NAME` are set, `export/sheets_exporter.py` updates the first worksheet with the ranked table (sortable/filterable in Sheets).

## 5) What are the limitations?
- Demo relies on static LinkedIn and funding samples; replace with real exports to broaden coverage.
- PubMed live lookup is opt-in and rate-limited; default static mapping may drift from reality over time.
- Funding stages are coarse and may miss round nuances; update the JSON or wire to Crunchbase for accuracy.
- Location hub logic is heuristic (string contains known hubs); refine as needed for your go-to-market regions.
