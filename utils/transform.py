import pandas as pd
import re

def transform_data(data):
    """
    Transforms raw data using regex for robust extraction.
    Cleans Price, Rating, Colors, Size, and Gender columns.
    """
    try:
        if not data:
            print("No data received in transform_data.")
            return pd.DataFrame()

        df = pd.DataFrame(data)
        print(f"Initial data count: {len(df)}")

        # Filter Title (Remove Unknown Product)
        if 'Title' in df.columns:
            df = df[df['Title'] != "Unknown Product"]
            df = df.dropna(subset=['Title'])
        
        # Clean Price
        # Remove '$' and ',' then extract numeric part
        df['Price'] = df['Price'].astype(str).str.replace(r'[$,]', '', regex=True)
        df['Price'] = df['Price'].str.extract(r'(\d+\.?\d*)')
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        
        # Drop rows with invalid price
        df = df.dropna(subset=['Price'])
        
        # Convert USD to IDR (Exchange rate: 16,000)
        df['Price'] = df['Price'] * 16000

        # Clean Rating
        # Extract numeric value from string (e.g., "Rating: 3.5 / 5" -> 3.5)
        df['Rating'] = df['Rating'].astype(str).str.extract(r'(\d+\.?\d*)')
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

        # Clean Colors
        # Extract digits only (e.g., "3 Colors" -> 3)
        df['Colors'] = df['Colors'].astype(str).str.extract(r'(\d+)')
        df['Colors'] = pd.to_numeric(df['Colors'], errors='coerce')

        # Clean Size & Gender
        # Remove prefixes like "Size: " and "Gender: "
        df['Size'] = df['Size'].astype(str).str.replace(r'Size:\s*', '', regex=True)
        df['Gender'] = df['Gender'].astype(str).str.replace(r'Gender:\s*', '', regex=True)

        # Final Cleaning
        df = df.dropna()
        df = df.drop_duplicates()

        # Set Data Types
        df = df.astype({
            'Title': 'object',
            'Price': 'float64',
            'Rating': 'float64',
            'Colors': 'int64',
            'Size': 'object',
            'Gender': 'object',
            'Timestamp': 'object'
        })

        print(f"Transformation complete. Final data shape: {df.shape}")
        return df

    except Exception as e:
        print(f"Error during transformation: {e}")
        return pd.DataFrame()
