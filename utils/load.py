import pandas as pd
from sqlalchemy import create_engine
from google.oauth2 import service_account
from googleapiclient.discovery import build

def load_to_csv(df, filename="products.csv"):
    """
    Saves DataFrame to a local CSV file.
    """
    try:
        df.to_csv(filename, index=False)
        print(f"[CSV] Data successfully saved to {filename}")
    except Exception as e:
        print(f"[CSV] Error saving to CSV: {e}")

def load_to_postgres(df, db_url, table_name="products"):
    """
    Saves DataFrame to PostgreSQL database.
    """
    try:
        if not db_url:
            print("[Postgres] No Database URL provided. Skipping.")
            return

        print("[Postgres] Connecting to database...")
        engine = create_engine(db_url)
        
        # Save data (if_exists='replace' overwrites the table)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        print(f"[Postgres] Data successfully saved to table '{table_name}'")
    except Exception as e:
        print(f"[Postgres] Error saving to Database: {e}")

def load_to_sheets(df, spreadsheet_id, json_keyfile="google-sheets-api.json"):
    """
    Saves DataFrame to Google Sheets using the Sheets API.
    """
    try:
        if not spreadsheet_id:
            print("[Sheets] No Spreadsheet ID provided. Skipping.")
            return

        # Authenticate
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        creds = service_account.Credentials.from_service_account_file(
            json_keyfile, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=creds)

        # Prepare Data
        # Convert DataFrame to list of lists (header + values)
        data_values = [df.columns.values.tolist()] + df.values.tolist()
        
        # Convert all data to string to avoid JSON serialization errors
        clean_values = []
        for row in data_values:
            clean_row = []
            for item in row:
                if pd.isna(item):
                    clean_row.append("")
                else:
                    clean_row.append(str(item))
            clean_values.append(clean_row)

        # Write Data
        # Overwrite Sheet1 starting from A1
        range_name = "Sheet1!A1" 
        body = {
            'values': clean_values
        }
        
        # Clear existing data first
        service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id, range="Sheet1"
        ).execute()

        # Update with new data
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption="RAW", body=body
        ).execute()

        print(f"[Sheets] {result.get('updatedCells')} cells updated in Google Sheets.")

    except Exception as e:
        print(f"[Sheets] Error saving to Google Sheets: {e}")

def load_data(df, db_url=None, sheet_id=None):
    """
    Orchestrator function to load data to CSV, PostgreSQL, and Google Sheets.
    """
    if df.empty:
        print("No data to load.")
        return

    print("\n--- Starting Load Process ---")
    
    # Load to CSV (Local)
    load_to_csv(df)

    # Load to PostgreSQL (Database)
    if db_url:
        load_to_postgres(df, db_url)
    
    # Load to Google Sheets (Cloud)
    if sheet_id:
        load_to_sheets(df, sheet_id)
