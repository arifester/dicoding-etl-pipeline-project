import os
from dotenv import load_dotenv  # Import library ini
from utils.extract import scrape_all_pages
from utils.transform import transform_data
from utils.load import load_data

# Load environment variables from .env file
load_dotenv()

# Configurations from .env
DATABASE_URL = os.getenv("DATABASE_URL")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

def main():
    print("Starting ETL Pipeline...")
    
    # Check if secrets are loaded
    if not DATABASE_URL or not SPREADSHEET_ID:
        print("Error: DATABASE_URL or SPREADSHEET_ID not found in .env file.")
        return

    # Extract
    raw_data = scrape_all_pages(start_page=1, end_page=50)

    if not raw_data:
        print("Extraction failed. No data found.")
        return

    # Transform
    clean_df = transform_data(raw_data)

    if clean_df.empty:
        print("Transformation failed. DataFrame is empty.")
        return

    # Load
    load_data(clean_df, db_url=DATABASE_URL, sheet_id=SPREADSHEET_ID)

    print("ETL Pipeline finished successfully.")

if __name__ == "__main__":
    main()
