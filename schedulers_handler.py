import json
import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def load_active_schedulers(directory: str):
    """
    Reads all JSON files in the given directory, loads the ones marked as active,
    and returns a list of dictionaries with their information.

    Parameters:
        directory (str): Path to the folder containing scheduler JSON files.

    Returns:
        list[dict]: List of active scheduler configurations.
    """
    schedulers = []

    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            filepath = os.path.join(directory, filename)
            try:
                # Open and load the JSON content
                with open(filepath, "r") as file:
                    data = json.load(file)

                # Check if scheduler is marked as active
                if data.get("status", "").lower() == "active":
                    schedulers.append(data)

            except (json.JSONDecodeError, OSError) as e:
                print(f"⚠️ Could not read {filename}: {e}")

    return schedulers


def get_imminent_schedulers(schedulers, CHECK_INTERVAL_MINUTES):
    imminent_schedulers = []
    now_utc = datetime.now().astimezone(ZoneInfo("UTC"))
    soon_utc = now_utc + timedelta(minutes=CHECK_INTERVAL_MINUTES)

    for scheduler in schedulers:
        send_time_str = scheduler["time"]  # e.g., "14:30"
        scheduler_timezone = scheduler.get("timezone", "UTC")

        if send_time_str:
            try:
                hour, minute = map(int, send_time_str.split(":"))

                # Create a datetime today in the scheduler's timezone
                tz = ZoneInfo(scheduler_timezone)
                now_local = now_utc.astimezone(tz)
                send_datetime_local = now_local.replace(hour=hour, minute=minute, second=0, microsecond=0)

                # Convert to UTC for comparison
                send_datetime_utc = send_datetime_local.astimezone(ZoneInfo("UTC"))

                # Skip if the send time has already passed
                if send_datetime_utc < now_utc:
                    continue

                # Add to imminent schedulers if within the check interval
                if now_utc <= send_datetime_utc <= soon_utc:
                    imminent_schedulers.append(scheduler)

            except ValueError:
                print(f"Invalid time format in {scheduler['scheduler name']}: {send_time_str}")

    return imminent_schedulers


def create_email_profile():
    print("\n=== Create a new email profile ===")

    # Get the name for the JSON file (without .json)
    file_name = input("Enter a name for this scheduler: ").strip()
    if not file_name:
        print("❌ File name cannot be empty.")
        return

    # Ask for all the relevant info
    status = str(input("Status (active/inactive): ").strip().lower())
    time = str(input("Send time (HH:MM, 24-hour format): ").strip())
    timezone = str(input("Enter the timezone (e.g. Europe/Rome, America/New_York): "))
    city_name = str(input("City name: ").strip())
    city_lat = float(input("City latitude: ").strip())
    city_lon = float(input("City longitude: ").strip())
    email = str(input("Recipient email address: ").strip())
    subject = str(input("Email subject: ").strip())
    text = str(input("Email message text: ").strip())

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
        "time": time,
        "timezone": timezone
    }

    # Ensure directory exists
    os.makedirs("email_profiles", exist_ok=True)

    # Save to JSON file
    file_path = os.path.join("email_profiles", f"{file_name}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=4)

    input(f"\n✅ Email profile saved as {file_path}")


if __name__ == "__main__":
    while True:
        create_email_profile()
        cont = input("\nCreate another profile? (y/n): ").strip().lower()
        if cont != "y":
            print("Done.")
            break
