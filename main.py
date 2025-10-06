from extract_weather_info import extract_weather
from create_message import assemble_message


dresden_coordinates = [(51.0509, 13.7383)]
rome_coordinates = [(41.8919, 12.5113)]
la_coordinates = [(34.0522, -118.2437)]
munich_coordinates = [(48.1374, 11.5755)]
coordinates = munich_coordinates

hourly_params = ["precipitation", "cloud_cover"]
daily_params = ["temperature_2m_min", "temperature_2m_max", "precipitation_probability_max"]

for lat, lon in coordinates:
    hourly_df, daily_df = extract_weather(lat, lon, hourly_params, daily_params)
    message = assemble_message(hourly_df, daily_df)
    print(message)

