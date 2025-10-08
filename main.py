from extract_weather_info import extract_weather
from create_image import assemble_image
import pywhatkit as kit
from datetime import datetime
import pyautogui as pg

dresden_coordinates = [(51.0509, 13.7383)]
rome_coordinates = [(41.8919, 12.5113)]
la_coordinates = [(34.0522, -118.2437)]
munich_coordinates = [(48.1374, 11.5755)]
kyoto_coordinates = [(35.0116, 135.7681)]
cleveland_coordinates = [(41.4993, -81.6944)]
louisville_coordinates = [(38.2469, -85.7664)]
coordinates = louisville_coordinates

hourly_params = ["temperature_2m", "precipitation", "cloud_cover", "precipitation_probability"]
daily_params = ["sunrise", "sunset"]

for lat, lon in coordinates:
    hourly_df, daily_df = extract_weather(lat, lon, hourly_params, daily_params)
    assemble_image(hourly_df, daily_df)
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    kit.sendwhatmsg("+393314869493", "Hello from Python!", hour, minute+2, 90)
    pg.press("enter")
    kit.sendwhats_image("+393314869493", f"weather_info.jpg")


"""
things to improve:
- correct the time shift of the precipitation prediction 
- better ui
- change the rain icons: using single raindrops
- improve the timestamp robustness
- add a user specification
"""
