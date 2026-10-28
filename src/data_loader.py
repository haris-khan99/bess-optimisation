import requests
import pandas as pd
import json
import logging

NESO_API = "https://api.neso.energy/api/3/action/datastore_search"
ELEXON_API = "https://data.elexon.co.uk/bmrs/api/v1"

logger = logging.getLogger(__name__)

def fetch_da_prices(date):

    params = {
        "resource_id": "4f27eea5-7038-4f73-9740-e3e4ad47c26a",
        "filters": json.dumps({"Date": date}),
        "limit": 100
    }

    response = requests.get(
        NESO_API,
        params=params,
        timeout=30
    )
    
    response.raise_for_status()
    data = response.json()

    if not data.get("success", False):
        raise RuntimeError("NESO API returned an error")

    return pd.DataFrame(data["result"]["records"])


def fetch_wind_solar_forecasts(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Retrieve GB day-ahead wind and solar generation forecasts.
    """

    wind_and_solar_api_url = f"{ELEXON_API}/forecast/generation/wind-and-solar/day-ahead"

    params = {
        "from": start_date,
        "to": end_date,
        "processType": "all"
    }

    response = requests.get(wind_and_solar_api_url, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()["data"]
    df = pd.DataFrame(data)

    logger.info("Retrieved %d forecast records", len(df))

    return df


def fetch_demand_forecasts(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Retrieve GB day-ahead electricity demand forecasts.
    """

    demand_api_url = f"{ELEXON_API}/forecast/demand/day-ahead"

    params = {
        "from": start_date,
        "to": end_date
    }

    response = requests.get(demand_api_url, params=params, timeout=30)
    response.raise_for_status()

    df = pd.DataFrame(response.json()["data"])

    logger.info("Retrieved %d demand forecast records", len(df))

    return df

df_da_prices = fetch_da_prices(
    "2026-10-27"
)

df_demand = fetch_demand_forecasts(
    "2026-10-27",
    "2026-10-27"
)

df_renewables = fetch_wind_solar_forecasts(
    "2026-10-27T00:00:00Z",
    "2026-10-28T23:30:00Z"
)


print(df_demand)
print(df_renewables)
print(df_da_prices)
