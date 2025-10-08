from extract_weather_info import extract_weather
from create_image import assemble_image
from send_email import send_email
from schedulers_handler import load_active_schedulers, get_imminent_schedulers
from check_imminent_jobs import CHECK_INTERVAL_MINUTES
import os

base_dir = os.path.dirname(os.path.abspath(__file__))

# --- Configuration ---
sender_email = "tommasogallo2016@gmail.com"
with open("password.txt", "r") as f:
    sender_password = str(f.readline())

hourly_params = ["temperature_2m", "precipitation", "cloud_cover", "precipitation_probability"]
daily_params = ["sunrise", "sunset"]

images_path = base_dir + f"/images"

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
if __name__ == "__main__":
    schedulers = load_active_schedulers(base_dir + "/email_profiles")
    imminent_schedulers = get_imminent_schedulers(schedulers, CHECK_INTERVAL_MINUTES)

    city_names = []
    for scheduler in imminent_schedulers:
        city_name = scheduler["city name"]
        if city_name not in city_names:
            city_names.append(city_name)
            coordinates = scheduler["coordinates"]
            lat = coordinates["latitude"]
            lon = coordinates["longitude"]
            hourly_df, daily_df = extract_weather(lat, lon, hourly_params, daily_params)
            assemble_image(hourly_df, daily_df, city_name)

    for scheduler in imminent_schedulers:
        coordinates = scheduler["coordinates"]
        city_name = scheduler["city name"]
        email_subject = scheduler["subject"]
        receiver_email = scheduler["email"]
        email_message = scheduler["text"]
        send_email(sender_email, sender_password, receiver_email, subject=email_subject, message=email_message,
                   str_path=images_path + f"/{city_name}.jpg")

    for filename in os.listdir(images_path):
        file_path = os.path.join(images_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

"""
things to improve:
- correct the time shift of the precipitation prediction 
- better graphics for the image
- change the rain icons: using single raindrops
- improve the timestamp robustness
- add a user specification
"""
