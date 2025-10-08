from extract_weather_info import extract_weather
from create_image import assemble_image
from send_email import send_email
import os

dresden_coordinates = [(51.0509, 13.7383)]
rome_coordinates = [(41.8919, 12.5113)]
la_coordinates = [(34.0522, -118.2437)]
munich_coordinates = [(48.1374, 11.5755)]
kyoto_coordinates = [(35.0116, 135.7681)]
cleveland_coordinates = [(41.4993, -81.6944)]
louisville_coordinates = [(38.2469, -85.7664)]
coordinates = dresden_coordinates

# --- Configuration ---
sender_email = "tommasogallo2016@gmail.com"
with open("password.txt", "r") as f:
    sender_password = str(f.readline())
hourly_params = ["temperature_2m", "precipitation", "cloud_cover", "precipitation_probability"]
daily_params = ["sunrise", "sunset"]


"""
receiver_email = "tommasogallo2023@gmail.com"
subject = "The surprise: morning weather reports"
message = (f"Dear Derya, \n"
           f"Good morning my aşkım. This is the surprise I have been working on.\n"
           f"I have set up a program that automatically checks the weather and sends you an email with the report every morning.\n"
           f"As I told you this was going to be something stupid but cute.\n\n"
           
           f"Love you! \n"
           f"Tommaso")
"""

base_dir = os.path.dirname(os.path.abspath(__file__))

for lat, lon in coordinates:
    hourly_df, daily_df = extract_weather(lat, lon, hourly_params, daily_params)
    assemble_image(hourly_df, daily_df, base_dir)
    send_email(sender_email, sender_password, receiver_email, subject=subject, message=message, str_path="weather_info.jpg")



"""
things to improve:
- correct the time shift of the precipitation prediction 
- better graphics for the image
- change the rain icons: using single raindrops
- improve the timestamp robustness
- add a user specification
"""
