import requests
import pandas as pd
import logging

# ---------------- LOGGING ---------------- #

logging.basicConfig(
    filename="../logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Pipeline Started")

# ---------------- PARAMETERS ---------------- #

LATITUDE = 13.0827
LONGITUDE = 80.2707
CITY = "Chennai"

URL = (
    f"https://api.open-meteo.com/v1/forecast?"
    f"latitude={LATITUDE}&longitude={LONGITUDE}"
    f"&hourly=temperature_2m,relative_humidity_2m"
)

# ---------------- FETCH API DATA ---------------- #

try:

    response = requests.get(URL)

    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code}")

    data = response.json()

    logging.info("API data fetched successfully")

except Exception as e:

    logging.error(f"API fetch failed: {e}")

    print("API ERROR:", e)

# ---------------- TRANSFORM DATA ---------------- #

try:

    hourly_data = data["hourly"]

    df = pd.DataFrame({
        "datetime": hourly_data["time"],
        "temperature": hourly_data["temperature_2m"],
        "humidity": hourly_data["relative_humidity_2m"]
    })

    # convert datetime
    df["datetime"] = pd.to_datetime(df["datetime"])

    # add city column
    df["city"] = CITY

    # derived field
    df["temperature_category"] = df["temperature"].apply(
        lambda x: "Hot" if x > 30 else "Moderate"
    )

    # fill nulls
    df = df.fillna(0)

    logging.info("Transformation completed")

except Exception as e:

    logging.error(f"Transformation failed: {e}")

    print("TRANSFORMATION ERROR:", e)

# ---------------- SAVE CSV ---------------- #

try:

    output_file = "../data/weather_data.csv"

    df.to_csv(output_file, index=False)

    logging.info("CSV saved successfully")

    print("\nCSV FILE CREATED SUCCESSFULLY\n")

    print(df.head())

except Exception as e:

    logging.error(f"CSV save failed: {e}")

    print("CSV SAVE ERROR:", e)
# ---------------- BIGQUERY LOAD ---------------- #

from google.cloud import bigquery
from google.oauth2 import service_account

try:

    credentials = service_account.Credentials.from_service_account_file(
        "../service_account.json"
    )

    client = bigquery.Client(
        credentials=credentials,
        project=credentials.project_id,
    )

    table_id = f"{credentials.project_id}.weather_pipeline.weather_data"

    job = client.load_table_from_dataframe(df, table_id)

    job.result()

    logging.info("Data uploaded to BigQuery successfully")

    print("\nDATA UPLOADED TO BIGQUERY SUCCESSFULLY\n")

except Exception as e:

    logging.error(f"BigQuery upload failed: {e}")

    print("BIGQUERY ERROR:", e)