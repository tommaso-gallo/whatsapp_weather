import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry (do this once)
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


def extract_weather(lat, lon, hourly_params, daily_params):
    """
    Fetch hourly and daily weather for given latitude and longitude.

    Returns a tuple: (hourly_dataframe, daily_dataframe)
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": hourly_params,
        "daily": daily_params,
        "timezone": "auto",
        "past_hours": 4,
        "forecast_hours": 20,
        "forecast_days": 1
    }

    # Make request
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]  # first model/location

    # Hourly data
    hourly = response.Hourly()
    hourly_data = {
        "date": pd.date_range(
            start=pd.to_datetime(hourly.Time(), unit="s", utc=False),
            end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=False),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )
    }
    for i, var_name in enumerate(hourly_params):
        hourly_data[var_name] = hourly.Variables(i).ValuesAsNumpy()

    hourly_df = pd.DataFrame(hourly_data)

    # daily data
    daily = response.Daily()
    daily_data = {
        "date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=False),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=False),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        )
    }
    for i, var_name in enumerate(daily_params):
        daily_data[var_name] = daily.Variables(i).ValuesAsNumpy()

    daily_df = pd.DataFrame(daily_data)

    return hourly_df, daily_df