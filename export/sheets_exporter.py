"""Export results to Google Sheets and CSV."""
from typing import Dict, List

import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SCOPE = ["https://www.googleapis.com/auth/spreadsheets"]


def export_to_sheets(
    rows: List[Dict[str, object]], spreadsheet_id: str, creds_path: str
) -> None:
    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPE)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_id).sheet1
    sheet.clear()
    if rows:
        headers = list(rows[0].keys())
        sheet.append_row(headers)
        for row in rows:
            sheet.append_row([row.get(h, "") for h in headers])


def export_to_google_sheet(
    rows: List[Dict[str, object]], creds_path: str, sheet_name: str
) -> str:
    """Export to Google Sheet by name (creates if doesn't exist)."""
    creds = Credentials.from_service_account_file(creds_path, scopes=SCOPE)
    client = gspread.authorize(creds)
    try:
        sheet = client.open(sheet_name).sheet1
    except gspread.SpreadsheetNotFound:
        sheet = client.create(sheet_name).sheet1
    sheet.clear()
    if rows:
        headers = list(rows[0].keys())
        sheet.append_row(headers)
        for row in rows:
            sheet.append_row([row.get(h, "") for h in headers])
    return f"https://docs.google.com/spreadsheets/d/{sheet.spreadsheet.id}"


def export_to_csv(rows: List[Dict[str, object]], path: str) -> None:
    pd.DataFrame(rows).to_csv(path, index=False)
