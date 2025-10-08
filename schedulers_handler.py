import json
import os
from datetime import datetime, timedelta

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
    now = datetime.now()
    soon = now + timedelta(minutes=CHECK_INTERVAL_MINUTES)

    for scheduler in schedulers:
        send_time_str = scheduler["time"]  # e.g., "14:30"
        if send_time_str:
            try:
                hour, minute = map(int, send_time_str.split(":"))
                send_datetime = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

                # If send time has already passed today, skip
                if send_datetime < now:
                    continue

                if now <= send_datetime <= soon:
                    imminent_schedulers.append(scheduler)
            except ValueError:
                print(f"Invalid time format in {scheduler["scheduler name"]}: {send_time_str}")

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
        "time": time
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
