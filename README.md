# BioLeadIQ

**Reproducible Lead Intelligence for 3D In-Vitro Therapeutics**

---

## Overview

BioLeadIQ is a lightweight lead-intelligence system designed to help business development teams prioritize **who to speak to first** when selling or collaborating around **3D in-vitro models for therapeutic research**.

Instead of collecting large volumes of unverified data, the system focuses on **explainable decision signals** and produces a **ranked, reproducible output** that can be inspected directly in a spreadsheet.

The emphasis is on **clarity, reproducibility, and business relevance**, not automation for its own sake.

---

## What Problem Does This Solve?

Business development teams often have access to many potential contacts but limited insight into:

* Who is scientifically active in the relevant area
* Who is likely to have budget
* Who fits the right seniority and role

BioLeadIQ consolidates **identity**, **scientific intent**, and **budget readiness** into a single, ranked view, allowing teams to prioritize outreach instead of manually triaging long contact lists.

---

## Design Principles

This project was built with the following principles:

* **Reproducibility over live scraping**
* **Explainability over black-box scoring**
* **Business signals over raw data volume**

Every design decision in the system reflects these priorities.

---

## Data Sources and Why They Were Chosen

### LinkedIn (Identification)

For the demo, LinkedIn profile data is ingested from a static CSV (`data/linkedin_profiles.csv`) containing:

* Name
* Title
* Company
* Location
* LinkedIn URL

This approach ensures the demo is **easy to verify and reproduce**.
In a production setup, the same schema could be populated via providers such as Proxycurl or Apify without changing the rest of the pipeline.

---

### PubMed (Scientific Intent)

Scientific intent is inferred using publication signals from PubMed:

* Recency of publications (last 24 months)
* Presence of domain-specific keywords (e.g., toxicology, hepatic models, DILI)

For reproducibility, the demo uses a **deterministic, cached mapping** inside `enrichment/pubmed_client.py`.
An optional live PubMed lookup via NCBI E-utilities is supported but **disabled by default** to avoid network and rate-limit variability.

This allows reviewers to see consistent results while still demonstrating how live enrichment would work.

---

### Funding Data (Budget Signal)

Company funding data is sourced from a static JSON file (`data/funding_data.json`) containing:

* Funding stage
* Last funding year

This captures a coarse but practical signal of budget readiness.
The design intentionally keeps this layer simple; in production, it can be replaced with a Crunchbase or PitchBook integration.

---

## How the Scoring Works

Each lead is assigned a **Propensity Score (0–100)** using a transparent, rule-based model:

```
score = role_fit * 30
      + scientific_intent * 40
      + company_funding * 20
      + location_hub * 10
```

The weights reflect typical business priorities:

* **Scientific activity** is the strongest indicator of near-term relevance
* **Role seniority and fit** determine decision-making power
* **Funding stage** indicates ability to purchase or adopt new tools
* **Location** acts as a secondary signal for ecosystem maturity

All scoring logic is implemented in `scoring/scoring_rules.py` and is fully inspectable.

---

## Output and Demo Artifact

Running the pipeline via:

```bash
python main.py
```

always produces a ranked `output.csv`.

If Google Sheets credentials are provided, the same results are also written to a Google Sheet, where they can be:

* Sorted
* Filtered
* Reviewed without running code

The Google Sheet is treated as the **primary demo artifact**, while the code remains the source of truth.

---

## Reproducibility and Tradeoffs

This demo deliberately avoids:

* Live LinkedIn scraping
* Black-box ML or LLM scoring
* Non-deterministic pipelines

These choices ensure:

* Results can be verified quickly
* Reviewers can inspect logic without setup friction
* The system remains easy to reason about

The tradeoff is reduced data breadth, which is acceptable for a demo focused on **decision logic rather than scale**.

---

## Limitations and Extensions

* LinkedIn and funding data are static samples; coverage depends on input quality
* PubMed live lookup is optional and rate-limited
* Funding stages are coarse and may miss nuance
* Location hub detection is heuristic and region-specific

These limitations are intentional for the demo and can be addressed in a production deployment.

---

## Summary

BioLeadIQ demonstrates how a small, well-designed system can turn fragmented public signals into a **clear, ranked decision tool**.

The goal is not to replace CRM systems or crawlers, but to show how **transparent logic and scientific context** can meaningfully improve lead prioritization.


