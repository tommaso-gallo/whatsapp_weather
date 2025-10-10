import subprocess
import time
import re


def scan_devices(scan_time=5, rssi_threshold=-70):
    print("Scanning for Bluetooth devices...")
    cmd = subprocess.Popen(['bluetoothctl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           text=True)
    cmd.stdin.write('scan on\n')
    cmd.stdin.flush()

    time.sleep(scan_time)  # scan for a few seconds

    cmd.stdin.write('scan off\n')
    cmd.stdin.write('devices\n')
    cmd.stdin.write('quit\n')
    cmd.stdin.flush()

    output = cmd.stdout.read()
    cmd.wait()

    devices = []
    for line in output.splitlines():
        # Parse lines like: Device XX:XX:XX:XX:XX:XX DeviceName
        match = re.match(r'Device ([0-9A-F:]{17}) (.+)', line)
        if match:
            mac, name = match.groups()
            # For now RSSI filtering is left for further steps if we get RSSI info
            devices.append((name, mac))
    return devices


def select_device(devices):
    print("\nFound devices:")
    for i, (name, mac) in enumerate(devices, 1):
        print(f"{i}. {name} ({mac})")
    choice = int(input("Choose a device to connect: ")) - 1
    return devices[choice][1]


def connect_device(mac):
    print(f"Connecting to {mac}...")
    commands = [
        f'select {mac}',
        'trust',
        'pair',
        'connect',
        'quit'
    ]
    cmd = subprocess.Popen(['bluetoothctl'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           text=True)
    for c in commands:
        cmd.stdin.write(c + '\n')
    cmd.stdin.close()
    output = cmd.stdout.read()
    cmd.wait()
    print(output)


def get_bluetooth_devices():
    """Returns two lists: paired_devices, connected_devices"""
    try:
        result_connected = subprocess.run(
            ["bluetoothctl", "devices", "Connected"],
            capture_output=True, text=True, check=True
        )

        connected = []
        for line in result_connected.stdout.splitlines():
            if line.startswith("Device"):
                parts = line.split(" ", 2)
                if len(parts) >= 3:
                    mac, name = parts[1], parts[2]
                    connected.append((mac, name))

        result_paired = subprocess.run(
            ["bluetoothctl", "devices", "Paired"],
            capture_output=True, text=True, check=True
        )

        paired = []
        for line in result_paired.stdout.splitlines():
            if line.startswith("Device"):
                parts = line.split(" ", 2)
                if len(parts) >= 3:
                    mac, name = parts[1], parts[2]
                    if (mac, name) not in connected:
                        paired.append((mac, name))

        return paired, connected

    except subprocess.CalledProcessError as e:
        print("Error running bluetoothctl:", e)
        return [], []


def print_bluetooth_status():
    paired, connected = get_bluetooth_devices()

    print("\nPaired Devices:")
    if paired:
        for i, (mac, name) in enumerate(paired, 1):
            print(f"  {i}. {name} ({mac})")
    else:
        print("  None")

    print("\nConnected Devices:")
    if connected:
        for i, (mac, name) in enumerate(connected, 1):
            print(f"  {i}. {name} ({mac}) ✅")
    else:
        print("  None")

    print()  # spacing


if __name__ == "__main__":
    print("Choose operation:")
    print("1. Show available devices")
    print("2. Show paired devices")
    operation = int(input("Enter the number: "))
    if operation == 1:
        devices = scan_devices()
        if not devices:
            print("No devices found.")
        else:
            mac = select_device(devices)
            connect_device(mac)
    elif operation == 2:
        print_bluetooth_status()
    else:
        print("Please, insert valid number")
