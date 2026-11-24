"""PubMed enrichment client with reproducible static fallback.

Uses NCBI E-utilities for live lookups when network + API key
are available. Defaults to a static lookup table to keep the
pipeline reproducible without external dependencies.
"""
import datetime
import logging
import os
from typing import Dict, List, Tuple

import requests

# Minimal static corpus to keep deterministic behavior
STATIC_PUBS: Dict[str, Dict[str, int]] = {
