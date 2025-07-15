import pandas as pd
import requests
import json
import urllib.parse
import sys
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# --- Settings ---
# 1. Read the API key from the environment. Returns None if not found.
TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")

# 2. File path definitions
INPUT_CSV = os.path.join('data', 'addresses_batch.csv')
OUTPUT_JSON = os.path.join('results', 'geocoding_batch_api.json')
# --- End of Settings ---


def create_batch_payload(addresses):
    """
    Creates the request body (payload) for a batch request from a list of addresses.
    """
    batch_items = []
    for address in addresses:
        if not isinstance(address, str) or not address.strip():
            print(f"Warning: Skipping invalid or empty address: {address}")
            continue
            
        # Encode the address for use in a URL
        query_encoded = urllib.parse.quote(address)
        
        # The 'query' within the batch should not include the API version (/2/) in the path.
        # The correct path starts directly with 'geocode/'.
        query_path = f"/geocode/{query_encoded}.json?limit=1"
        batch_items.append({"query": query_path})
    
    return {"batchItems": batch_items}

def main():
    """
    Main function: reads the CSV, calls the API, and saves the results.
    """
    # Validate that the API key is set
    if not TOMTOM_API_KEY:
        print("ERROR: 'TOMTOM_API_KEY' not found.")
        print("Please ensure you have created a .env file and added your API key to it.")
        sys.exit(1)

    # 1. Read addresses from the CSV file using pandas
    try:
        df = pd.read_csv(INPUT_CSV, dtype=str).fillna('')
        if 'address' not in df.columns:
            print(f"ERROR: The CSV file '{INPUT_CSV}' must have a column named 'address'.")
            return
        addresses = df['address'].tolist()
        print(f"✅ Found {len(addresses)} addresses in '{INPUT_CSV}'.")
    except FileNotFoundError:
        print(f"ERROR: File '{INPUT_CSV}' not found.")
        print("Please create the file and try again.")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading the CSV: {e}")
        return

    # 2. Create the payload for the batch request
    payload = create_batch_payload(addresses)
    
    if not payload["batchItems"]:
        print("No valid addresses to process. Exiting.")
        return

    # 3. Send the POST request to the TomTom API
    # The base URL for the batch API already includes the version /2/
    api_url = f"https://api.tomtom.com/search/2/batch.json?key={TOMTOM_API_KEY}"
    
    print("🚀 Sending request to the TomTom API...")
    try:
        response = requests.post(api_url, json=payload, timeout=30)
        response.raise_for_status()
        
        results = response.json()
        
        with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
            
        print(f"✔️ Success! Results have been saved to '{OUTPUT_JSON}'.")

    except requests.exceptions.HTTPError as errh:
        print(f"\n❌ HTTP Error: {errh.response.status_code} {errh.response.reason}")
        print("Details:", errh.response.text)
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error: Could not connect to the API. Check your internet connection.")
    except requests.exceptions.Timeout:
        print("\n❌ Timeout Error: The request timed out.")
    except requests.exceptions.RequestException as err:
        print(f"\n❌ An error occurred with the request: {err}")

if __name__ == "__main__":
    main()