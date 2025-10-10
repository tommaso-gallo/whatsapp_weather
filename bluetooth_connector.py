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


if __name__ == "__main__":
    devices = scan_devices()
    if not devices:
        print("No devices found.")
    else:
        mac = select_device(devices)
        connect_device(mac)
