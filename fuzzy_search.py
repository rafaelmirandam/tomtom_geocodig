import os
import sys
import json
import requests
import pandas as pd
from urllib.parse import quote
from dotenv import load_dotenv
import time

# Load environment variables from the .env file
load_dotenv()

# --- Settings ---
TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")
SEARCH_RADIUS_METERS = 10000
RESULT_LIMIT = 5

# File path definitions
INPUT_CSV = os.path.join('data', 'addresses_fuzzy.csv')
OUTPUT_JSON = os.path.join('results', 'fuzzy.json')
# --- End of Settings ---

def get_coordinates(address):
    """Geocodes an address to get its latitude and longitude."""
    encoded_address = quote(address)
    api_url = f"https://api.tomtom.com/search/2/geocode/{encoded_address}.json"
    params = {'key': TOMTOM_API_KEY, 'limit': 1}

    try:
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('results'):
            position = data['results'][0]['position']
            return position.get('lat'), position.get('lon')
    except requests.exceptions.RequestException as e:
        print(f"  -> Error geocoding '{address}': {e}")
    return None, None


def batch_fuzzy_search():
    """Reads a CSV and performs a fuzzy search for each row."""
    if not TOMTOM_API_KEY:
        print("ERROR: 'TOMTOM_API_KEY' not found in the .env file.")
        sys.exit(1)

    try:
        df = pd.read_csv(INPUT_CSV)
        print(f"✅ File '{INPUT_CSV}' read successfully. {len(df)} rows to process.")
    except FileNotFoundError:
        print(f"ERROR: File '{INPUT_CSV}' not found.")
        sys.exit(1)

    all_results = []
    for index, row in df.iterrows():
        query = row['query']
        context = row['context'] # Keeping 'context' as it's a column name from the CSV
        print(f"\n🔄 Processing row {index + 1}: Query='{query}', Context='{context}'")

        lat, lon = get_coordinates(context)
        if not lat or not lon:
            print(f"  -> Could not get coordinates for '{context}'. Skipping.")
            continue
        
        print(f"  -> Coordinates for '{context}': lat={lat}, lon={lon}")

        encoded_query = quote(query)
        api_url = f"https://api.tomtom.com/search/2/search/{encoded_query}.json"
        params = {
            'key': TOMTOM_API_KEY,
            'lat': lat,
            'lon': lon,
            'radius': SEARCH_RADIUS_METERS,
            'limit': RESULT_LIMIT,
            'language': 'en-US', # Changed to en-US for consistency
        }

        try:
            response = requests.get(api_url, params=params, timeout=15)
            response.raise_for_status()
            api_results = response.json()
            
            # Add the original query to the results for reference
            result_item = {
                'original_search': {'query': query, 'context': context},
                'found_results': api_results.get('results', [])
            }
            all_results.append(result_item)
            print(f"  -> ✔️ Search for '{query}' completed successfully.")
            
        except requests.exceptions.RequestException as e:
            print(f"  -> ❌ Error in fuzzy search for '{query}': {e}")
        
        # Pause to avoid exceeding API rate limits
        time.sleep(0.2) 

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)

    print(f"\n🎉 Processing complete! Results saved to '{OUTPUT_JSON}'.")


if __name__ == "__main__":
    batch_fuzzy_search()
