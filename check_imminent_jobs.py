from schedulers_handler import load_active_schedulers, get_imminent_schedulers
import subprocess
import platform
import os

# How far ahead to consider a job as "imminent"
CHECK_INTERVAL_MINUTES = 10

base_dir = os.path.dirname(os.path.abspath(__file__))
system = platform.system()
if system == "Windows":
    PYTHON_PATH = f"{base_dir}/venv1/Scripts/python.exe"
    MAIN_SCRIPT = f"{base_dir}/main.py"
elif system == "Linux":
    PYTHON_PATH = f"{base_dir}/venv/bin/python"
    MAIN_SCRIPT = f"{base_dir}/main.py"
else:
    raise Exception(f"Unsupported OS: {system}")


def main():
    schedulers = load_active_schedulers(base_dir + "/email_profiles")
    if len(get_imminent_schedulers(schedulers, CHECK_INTERVAL_MINUTES)) > 0:
        subprocess.run([PYTHON_PATH, MAIN_SCRIPT])


if __name__ == "__main__":
    main()
