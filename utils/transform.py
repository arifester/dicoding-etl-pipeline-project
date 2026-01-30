import pandas as pd
import re

def transform_data(data):
    try:
        if not data:
            print("No data received in transform_data.")
            return pd.DataFrame()

        df = pd.DataFrame(data)
        print(f"Initial data count: {len(df)}")

        # Handle "Dirty Patterns"
        if 'Title' in df.columns:
            df = df[df['Title'] != "Unknown Product"]

        if 'Price' in df.columns:
            df = df[df['Price'] != "Price Unavailable"]
            
        if 'Rating' in df.columns:
            df = df[~df['Rating'].isin(["Invalid Rating / 5", "Not Rated"])]

        # Clean and Convert Data
        # Price: Remove symbols, extract numeric part, convert to IDR
        df['Price'] = df['Price'].astype(str).str.replace(r'[$,]', '', regex=True)
        df['Price'] = df['Price'].str.extract(r'(\d+\.?\d*)')[0]
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        df['Price'] = df['Price'] * 16000

        # Rating: Extract numeric value
        df['Rating'] = df['Rating'].astype(str).str.extract(r'(\d+\.?\d*)')[0]
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

        # Colors: Extract digits only
        df['Colors'] = df['Colors'].astype(str).str.extract(r'(\d+)')[0]
        df['Colors'] = pd.to_numeric(df['Colors'], errors='coerce')

        # Size & Gender: Remove prefixes "Size: " and "Gender: "
        df['Size'] = df['Size'].astype(str).str.replace(r'Size:\s*', '', regex=True)
        df['Gender'] = df['Gender'].astype(str).str.replace(r'Gender:\s*', '', regex=True)

        # Final Cleanup
        # Remove any rows with NaN values resulting from conversion errors
        df = df.dropna()
        
        # Deduplicate based on product attributes, ignoring Timestamp
        df = df.drop_duplicates(subset=['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender'])

        # Enforce Data Types
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
