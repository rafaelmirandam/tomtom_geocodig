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
INPUT_CSV = os.path.join('data', 'addresses_geocoding.csv')
OUTPUT_JSON = os.path.join('results', 'geocoding.json')
# --- End of Settings ---


def batch_geocode_loop():
    """Reads a CSV and geocodes each address in a loop."""
    if not TOMTOM_API_KEY:
        print("ERROR: 'TOMTOM_API_KEY' not found in the .env file.")
        sys.exit(1)

    try:
        df = pd.read_csv(INPUT_CSV)
        print(f"✅ File '{INPUT_CSV}' read successfully. {len(df)} addresses to process.")
    except FileNotFoundError:
        print(f"ERROR: File '{INPUT_CSV}' not found.")
        sys.exit(1)

    final_results = []
    for index, row in df.iterrows():
        address = row['address']
        if not isinstance(address, str) or not address.strip():
            print(f"Warning: Skipping invalid address at row {index + 2}.")
            continue

        print(f"🔄 Geocoding address {index + 1}/{len(df)}: '{address}'...")

        encoded_address = quote(address)
        api_url = f"https://api.tomtom.com/search/2/geocode/{encoded_address}.json"
        params = {
            'key': TOMTOM_API_KEY,
            'limit': 1,
            'language': 'en-US',
        }

        try:
            response = requests.get(api_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            result_item = {
                'original_address': address,
                'api_result': data.get('results', [])
            }
            final_results.append(result_item)

        except requests.exceptions.HTTPError as errh:
            print(f"  -> ❌ HTTP Error for '{address}': {errh.response.status_code}")
        except requests.exceptions.RequestException as err:
            print(f"  -> ❌ Request Error for '{address}': {err}")
            
        # Pause for 0.2 seconds to avoid overwhelming the API
        time.sleep(0.2)

    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 Processing complete! Results saved to '{OUTPUT_JSON}'.")


if __name__ == "__main__":
    batch_geocode_loop()
