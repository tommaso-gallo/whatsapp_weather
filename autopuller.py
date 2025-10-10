import json
import subprocess
import requests

# Raw URL of the JSON file on GitHub
AUTOPULL_URL = "https://raw.githubusercontent.com/tommaso-gallo/whatsapp_weather/main/autopull.json"
REPO_DIR = "/home/pi/whatsapp_weather"  # path to your repo on Pi

def check_online_autopull():
    try:
        response = requests.get(AUTOPULL_URL, timeout=10)
        response.raise_for_status()  # raise error if status != 200
        config = json.loads(response.text)
        return config.get("autopull", False)
    except Exception as e:
        print(f"⚠️ Could not fetch autopull status: {e}")
        return False

def git_pull():
    try:
        result = subprocess.run(
            ["git", "pull"],
            cwd=REPO_DIR,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print("⚠️ Git pull failed:", result.stderr)
    except Exception as e:
        print(f"⚠️ Error running git pull: {e}")

def main():
    if check_online_autopull():
        print("✅ Online autopull is enabled. Pulling latest changes...")
        git_pull()
    else:
        print("ℹ️ Online autopull is disabled.")

if __name__ == "__main__":
    main()
