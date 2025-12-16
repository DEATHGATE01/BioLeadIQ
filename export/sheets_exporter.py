"""Export results to Google Sheets and CSV."""
import os
from typing import List

import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]


def _get_client(creds_path: str) -> gspread.Client:
    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPE)
    return gspread.authorize(creds)


def export_to_google_sheet(rows: List[dict], creds_path: str, sheet_name: str) -> str:
    client = _get_client(creds_path)
    sh = client.open(sheet_name)
    worksheet = sh.sheet1
    df = pd.DataFrame(rows)
    worksheet.clear()
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    return sh.url


def export_to_csv(rows: List[dict], path: str) -> str:
    df = pd.DataFrame(rows)
    df.to_csv(path, index=False)
    return os.path.abspath(path)
