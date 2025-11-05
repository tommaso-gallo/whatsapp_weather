from check_imminent_jobs import PYTHON_PATH, MAIN_SCRIPT, run_main
from datetime import datetime, timedelta
import os
import json
import time
from zoneinfo import ZoneInfo

if __name__ == "__main__":
    now = datetime.now(ZoneInfo("Europe/London"))
    future_time = now + timedelta(minutes=5)
    time_str = future_time.strftime("%H:%M")

    timezone = "Europe/London"
    file_name = "trial"
    status = "active"
    city_name = "London"
    city_lat = 51.5072
    city_lon = -0.1276
    subject = "This is a trial email"
    email = "tommasogallo2023@gmail.com"
    text = "This is a trial email sent automatically"

    # Assemble the dictionary
    profile = {
        "scheduler name": file_name,
        "status": status,
        "city name": city_name,
        "coordinates": {
            "latitude": city_lat,
            "longitude": city_lon
        },
        "subject": subject,
        "email": email,
        "text": text,
        "time": time_str,
        "timezone": timezone
    }


    # Save to JSON file
    file_path = os.path.join("email_profiles", f"{file_name}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=4)

    print(f"\nTrial email profile saved as {file_path}")

    run_main(PYTHON_PATH, MAIN_SCRIPT)

    print("The email should have now be sent")
    time.sleep(10)
    os.remove(file_path)
    print("The email profile has been removed")
