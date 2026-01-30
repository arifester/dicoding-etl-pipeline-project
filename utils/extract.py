import requests
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = "https://fashion-studio.dicoding.dev"

def get_html_content(url):
    """
    Fetches HTML content from the given URL with error handling.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def parse_product_card(card):
    """
    Parses a single product card to extract details.
    Handles different HTML structures for price tags.
    """
    try:
        # Extract Title
        title_elem = card.find("h3", class_="product-title")
        title = title_elem.text.strip() if title_elem else None

        # Attempt to find price in 'span' (standard) first, then 'p' (unavailable/different format)
        price_elem = card.find("span", class_="price")
        if not price_elem:
            price_elem = card.find("p", class_="price")
        
        price = price_elem.text.strip() if price_elem else None

        # Extract Details (Rating, Colors, Size, Gender)
        details = card.find("div", class_="product-details")
        p_tags = details.find_all("p", recursive=False)
        
        rating = None
        colors = None
        size = None
        gender = None

        for p in p_tags:
            text = p.text.strip()
            if "Rating" in text:
                rating = text
            elif "Colors" in text:
                colors = text
            elif "Size" in text:
                size = text
            elif "Gender" in text:
                gender = text

        # Add Timestamp
        timestamp = datetime.now().isoformat()

        return {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": colors,
            "Size": size,
            "Gender": gender,
            "Timestamp": timestamp
        }

    except Exception as e:
        print(f"Error parsing product card: {e}")
        return None

def scrape_all_pages(start_page=1, end_page=50):
    """
    Iterates through pages to scrape all product data.
    Fixes URL construction to ensure pagination works correctly.
    """
    all_products = []
    print(f"Starting scraping process from page {start_page} to {end_page}...")

    for page in range(start_page, end_page + 1):
        if page == 1:
            url = BASE_URL
        else:
            url = f"{BASE_URL}/page{page}"
            
        print(f"Scraping page {page}...", end="\r")
        
        html = get_html_content(url)
        
        if html:
            soup = BeautifulSoup(html, "html.parser")
            cards = soup.find_all("div", class_="collection-card")
            
            if not cards:
                print(f"\nNo products found on page {page}.")
                continue

            for card in cards:
                data = parse_product_card(card)
                if data:
                    all_products.append(data)
    
    print(f"\nCompleted! Successfully scraped {len(all_products)} products.")
    return all_products

if __name__ == "__main__":
    # Test run
    data = scrape_all_pages(start_page=1, end_page=2)
    print(f"Test run captured {len(data)} items")
