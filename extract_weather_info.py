import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
import os

# Setup the Open-Meteo API client with cache and retry (do this once)
base_dir = os.path.dirname(os.path.abspath(__file__))
cache_session = requests_cache.CachedSession(f'{base_dir}/.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)


def extract_weather(lat, lon, hourly_params, daily_params, timezone):
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
        "past_hours": 0,
        "forecast_hours": 17+1,
        "forecast_days": 1
    }

    # Make request
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]  # first model/location

    # Hourly data
    hourly = response.Hourly()
    hourly_start_utc = pd.to_datetime(hourly.Time(), unit="s", utc=True)
    hourly_end_utc = pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True)
    hourly_data = {
        "date": pd.date_range(
            start=hourly_start_utc.tz_convert(timezone),
            end=hourly_end_utc.tz_convert(timezone),
            freq=pd.Timedelta(seconds=hourly.Interval()),
            inclusive="left"
        )
    }
    for i, var_name in enumerate(hourly_params):
        hourly_data[var_name] = hourly.Variables(i).ValuesAsNumpy()

    hourly_df = pd.DataFrame(hourly_data)
    hourly_df["precipitation"] = hourly_df["precipitation"].shift(-1)
    hourly_df["precipitation_probability"] = hourly_df["precipitation_probability"].shift(-1)
    hourly_df = hourly_df.iloc[:-1]

    # daily data
    daily = response.Daily()
    daily_start_utc = pd.to_datetime(daily.Time(), unit="s", utc=True)
    daily_end_utc = pd.to_datetime(daily.TimeEnd(), unit="s", utc=True)
    daily_data = {
        "date": pd.date_range(
            start=daily_start_utc.tz_convert(timezone),
            end=daily_end_utc.tz_convert(timezone),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        )
    }
    for i, var_name in enumerate(daily_params):
        daily_data[var_name] = daily.Variables(i).ValuesInt64AsNumpy()

    daily_df = pd.DataFrame(daily_data)

    return hourly_df, daily_df


if __name__ == "__main__":
    from datetime import datetime
    from zoneinfo import ZoneInfo

    coordinates1 = [34.0549, -118.2426, "America/Los_Angeles"]  # LA
    coordinates2 = [45.4685, 9.1824, "Europe/Rome"]  # MI
    coordinates3 = [51.752, -1.2577, "Europe/London"]  # OX
    coordinates4 = [59.4370, 24.7536, "Europe/Tallinn"]
    coordinates = coordinates4

    lat, lon, timezone = coordinates
    hourly_params = ["temperature_2m", "precipitation", "precipitation_probability"]
    daily_params = ["sunrise", "sunset"]
    hourly_df, daily_df = extract_weather(lat, lon, hourly_params, daily_params, timezone)

    tz = ZoneInfo(timezone)
    sunrise_ts = daily_df["sunrise"][0]
    sunset_ts = daily_df["sunset"][0]

    # Convert to timezone-aware datetimes
    sunrise_dt = datetime.fromtimestamp(sunrise_ts, tz=ZoneInfo("UTC")).astimezone(tz)
    sunset_dt = datetime.fromtimestamp(sunset_ts, tz=ZoneInfo("UTC")).astimezone(tz)

    # Convert to float hours (e.g., 6.5 for 06:30)
    sunrise = sunrise_dt.hour + sunrise_dt.minute / 60
    sunset = sunset_dt.hour + sunset_dt.minute / 60

    print(hourly_df["precipitation"], hourly_df["precipitation_probability"])

    hourly_df["precipitation"] = hourly_df["precipitation"].shift(-1)
    hourly_df["precipitation_probability"] = hourly_df["precipitation_probability"].shift(-1)
    hourly_df = hourly_df.iloc[:-1]
    print(hourly_df["precipitation"], hourly_df["precipitation_probability"])
