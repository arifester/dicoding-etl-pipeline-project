import pandas as pd

def clean_currency(price_str):
    """
    Cleans price string, removes symbols, and converts to float.
    Returns None if price is unavailable or invalid.
    """
    if pd.isna(price_str) or "Unavailable" in str(price_str):
        return None
    
    clean_str = str(price_str).replace("$", "").replace(",", "").strip()
    try:
        return float(clean_str)
    except ValueError:
        return None

def transform_data(data):
    """
    Transforms raw list of dictionaries into a cleaned Pandas DataFrame.
    Applies filtering, type conversion, and currency exchange.
    """
    try:
        if not data:
            print("No data to transform.")
            return pd.DataFrame()

        df = pd.DataFrame(data)

        # Filter out invalid Titles (Unknown Product)
        df = df[df['Title'] != "Unknown Product"]

        # Clean and Transform Price
        # Convert to float first, handling 'Price Unavailable'
        df['Price'] = df['Price'].apply(clean_currency)
        
        # Drop rows where Price is NaN (was Unavailable or None)
        df = df.dropna(subset=['Price'])
        
        # Convert USD to IDR (Exchange rate: 16,000)
        df['Price'] = df['Price'] * 16000

        # Clean Rating
        # Remove " / 5", handle "Invalid Rating" or "Not Rated"
        # Coerce errors to NaN, then drop them
        df['Rating'] = df['Rating'].astype(str).str.replace(" / 5", "", regex=False)
        df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

        # Clean Colors
        # Remove " Colors" text, keep only digits
        df['Colors'] = df['Colors'].astype(str).str.replace(" Colors", "", regex=False)
        df['Colors'] = pd.to_numeric(df['Colors'], errors='coerce')

        # Clean Size and Gender
        # Remove prefixes "Size: " and "Gender: "
        df['Size'] = df['Size'].astype(str).str.replace("Size: ", "", regex=False)
        df['Gender'] = df['Gender'].astype(str).str.replace("Gender: ", "", regex=False)

        # Final Cleaning
        # Drop any remaining rows with NaN values
        df = df.dropna()
        
        # Drop duplicates
        df = df.drop_duplicates()

        # Enforce Data Types (Final Check)
        df = df.astype({
            'Title': 'object',
            'Price': 'float64',
            'Rating': 'float64',
            'Colors': 'int64',
            'Size': 'object',
            'Gender': 'object',
            'Timestamp': 'object'
        })

        print(f"Transformation complete. Data shape: {df.shape}")
        return df

    except Exception as e:
        print(f"Error during transformation: {e}")
        return pd.DataFrame()
    