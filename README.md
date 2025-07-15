# TomTom Geocoding API Scripts

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

This project provides a collection of Python scripts for interacting with the TomTom Search APIs, offering different methods for converting addresses into geographic coordinates and searching for points of interest.

## Features

The project includes three main scripts:

1.  **Looping Geocoding:** Converts a list of addresses from a CSV file into coordinates by making an API request for each address.
2.  **Looping Fuzzy Search:** Searches for points of interest (e.g., "restaurant") near a reference location, reading data from a CSV file.
3.  **Batch Geocoding (Batch API):** The most efficient way to geocode a large volume of addresses by sending them all in a single API request.

## Project Structure

```
tomtom_geocoding/
├── .env
├── requirements.txt
├── geocoding_search.py
├── fuzzy_search.py
├── batch_search.py
├── data/
│   ├── addresses_geocoding.csv
│   ├── addresses_fuzzy.csv
│   └── addresses_batch.csv
├── results/
│   ├── geocoding.json
│   ├── fuzzy.json
│   └── geocoding_batch_api.json
└── README.md
```

## General Setup and Installation

1.  **Clone the repository** and navigate to the project folder.

2.  **(Recommended) Create and activate a virtual environment:**
    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    (Ensure your `requirements.txt` contains `pandas`, `requests`, and `python-dotenv`)
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API key:**
    Create a `.env` file in the project root and add your key.
    ```env
    TOMTOM_API_KEY="YOUR_REAL_API_KEY_HERE"
    ```

---

## How to Use

Choose the script that corresponds to the task you want to perform.

### 1. Looping Geocoding

Ideal for small to medium-sized lists of addresses.

-   **Script:** `geocoding_search.py`
-   **Input File:** `data/addresses_geocoding.csv`
-   **Output File:** `results/geocoding.json`

**Steps:**

1.  Create the `data/addresses_geocoding.csv` file with the following structure:
    ```csv
    address
    "Avenida da Liberdade, 190, Lisboa"
    "Rua de Santa Catarina, 500, Porto"
    "Praça do Giraldo, Évora"
    ```
2.  Run the script:
    ```bash
    python geocoding_search.py
    ```
3.  **Example Output (`results/geocoding.json`):**
    ```json
    [
      {
        "query": "Avenida da Liberdade, 190, Lisboa",
        "latitude": 38.71986,
        "longitude": -9.14312
      },
      {
        "query": "Rua de Santa Catarina, 500, Porto",
        "latitude": 41.15076,
        "longitude": -8.60553
      }
    ]
    ```

### 2. Looping Fuzzy Search

Perfect for finding types of places (POIs) near different cities or addresses.

-   **Script:** `fuzzy_search.py`
-   **Input File:** `data/addresses_fuzzy.csv`
-   **Output File:** `results/fuzzy.json`

**Steps:**

1.  Create the `data/addresses_fuzzy.csv` file with `query` and `context` columns:
    ```csv
    query,context
    "restaurante italiano","Avenida da Liberdade, Lisboa"
    "museu","Porto, Portugal"
    "farmácia","Faro"
    ```
2.  Run the script:
    ```bash
    python fuzzy_search.py
    ```

### 3. Batch Geocoding (Using the Batch API)

The best option for quickly and efficiently geocoding a large volume of addresses.

-   **Script:** `batch_search.py`
-   **Input File:** `data/addresses_batch.csv`
-   **Output File:** `results/geocoding_batch_api.json`

**Steps:**

1.  Create the `data/addresses_batch.csv` file with a single `address` column:
    ```csv
    address
    "Avenida Paulista, 1578, São Paulo, SP"
    "Praça da Sé, s/n, São Paulo, SP"
    "Rua do Russel, 632, Rio de Janeiro, RJ"
    ```
2.  Run the script:
    ```bash
    python batch_search.py
    ```

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
