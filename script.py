import os
import requests
import snowflake.connector
from dotenv import load_dotenv
import time
from datetime import datetime, timezone

load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
SNOWFLAKE_TABLE = os.getenv("SNOWFLAKE_TABLE")

BASE_URL = "https://api.polygon.io/v3/reference/tickers"

def fetch_tickers():
    all_tickers = []
    next_url = f"{BASE_URL}?active=true&apiKey={POLYGON_API_KEY}"

    while next_url:
        print(f"Requesting page: {next_url}")
        response = requests.get(next_url)
        
        if response.status_code == 429:
            print("Rate limit hit. Waiting 60 seconds...")
            time.sleep(60)
            continue
        elif response.status_code != 200:
            raise Exception(f"Error {response.status_code}: {response.text}")
        
        data = response.json()
        results = data.get("results", [])
        all_tickers.extend(results)

        next_url = data.get("next_url")
        if next_url:
            next_url += f"&apiKey={POLYGON_API_KEY}"

        # To avoid hitting rate limits
        time.sleep(1)

    print(f"Fetched {len(all_tickers)} tickers total.")
    return all_tickers


def load_to_snowflake(data):
    print("Connecting to Snowflake...")
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
    )

    try:
        cs = conn.cursor()
        cs.execute(f"USE DATABASE {SNOWFLAKE_DATABASE}")
        cs.execute(f"USE SCHEMA {SNOWFLAKE_SCHEMA}")

        insert_query = f"""
            INSERT INTO {SNOWFLAKE_TABLE} (
                ticker, name, market, locale, primary_exchange, type,
                currency_name, cik, composite_figi, share_class_figi, last_updated_utc, ds
            ) VALUES (
                %(ticker)s, %(name)s, %(market)s, %(locale)s, %(primary_exchange)s, %(type)s,
                %(currency_name)s, %(cik)s, %(composite_figi)s, %(share_class_figi)s, %(last_updated_utc)s, %(ds)s
            )
        """

        batch_size = 500
        total_inserted = 0
        for i in range(0, len(data), batch_size):
            batch = data[i:i+batch_size]
            cs.executemany(insert_query, batch)
            total_inserted += len(batch)
            print(f"Inserted {total_inserted}/{len(data)} records...")

        conn.commit()
        print(f"✅ Loaded {total_inserted} records into {SNOWFLAKE_TABLE}.")
    
    finally:
        cs.close()
        conn.close()


if __name__ == "__main__":
    tickers = fetch_tickers()
    # Use current UTC date for ds (DATE)
    current_ds = datetime.now(timezone.utc).date().isoformat()
    formatted_data = [
        {
            "ticker": t.get("ticker"),
            "name": t.get("name"),
            "market": t.get("market"),
            "locale": t.get("locale"),
            "primary_exchange": t.get("primary_exchange"),
            "type": t.get("type"),
            "currency_name": t.get("currency_name"),
            "cik": t.get("cik"),
            "composite_figi": t.get("composite_figi"),
            "share_class_figi": t.get("share_class_figi"),
            "last_updated_utc": t.get("last_updated_utc"),
            "ds": current_ds,
        }
        for t in tickers
    ]
    
    load_to_snowflake(formatted_data)
