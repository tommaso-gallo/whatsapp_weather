import json
import os


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
    city_lat = float(input("City latitude: ").strip())
    city_lon = float(input("City longitude: ").strip())
    email = str(input("Recipient email address: ").strip())
    subject = str(input("Email subject: ").strip())
    text = str(input("Email message text: ").strip())

    # Assemble the dictionary
    profile = {
        "status": status,
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

    print(f"✅ Email profile saved as {file_path}")


if __name__ == "__main__":
    while True:
        create_email_profile()
        cont = input("\nCreate another profile? (y/n): ").strip().lower()
        if cont != "y":
            print("Done.")
            break
