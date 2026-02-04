import ctypes
import subprocess
import time
import json
import os
import signal
import sys
import atexit

BLACKLIST_FILE = "blocked_usb.json"

# ---------------- Admin Check ----------------
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", "python", __file__, None, 1
    )
    sys.exit(0)

# ---------------- Helpers ----------------
def run_ps(cmd):
    subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def load_blacklist():
    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE, "r") as f:
            return set(json.load(f))
    return set()

def save_blacklist(data):
    with open(BLACKLIST_FILE, "w") as f:
        json.dump(list(data), f)

blocked = load_blacklist()
seen = set()
disabled_instances = set()

print("[+] USB Guard running")
print("[!] First ATtiny insertion allowed, future insertions blocked")
print("[!] Devices will be restored when script exits")

# ---------------- Cleanup Logic ----------------
def cleanup():
    if disabled_instances:
        print("[*] Restoring disabled USB devices...")
        for instance in disabled_instances:
            run_ps(
                f"Enable-PnpDevice -InstanceId '{instance}' -Confirm:$false"
            )
        print("[+] USB devices restored")

atexit.register(cleanup)

def handle_exit(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

# ---------------- Monitor Loop ----------------
while True:
    ps = r"""
    Get-PnpDevice -PresentOnly |
    Where-Object { $_.InstanceId -like 'USB*' } |
    Select-Object -ExpandProperty InstanceId
    """
    try:
        result = subprocess.check_output(
            ["powershell", "-Command", ps],
            text=True,
            errors="ignore"
        ).splitlines()
    except subprocess.CalledProcessError:
        time.sleep(2)
        continue

    for dev in result:
        if "VID_" not in dev:
            continue

        vidpid = dev.split("\\")[1]

        # First time seen → allow once, then blacklist
        if vidpid not in seen and vidpid not in blocked:
            print(f"[!] New USB detected (allowed once): {vidpid}")
            seen.add(vidpid)
            blocked.add(vidpid)
            save_blacklist(blocked)

        # Future insertions → block temporarily
        elif vidpid in blocked and dev not in disabled_instances:
            run_ps(
                f"Disable-PnpDevice -InstanceId '{dev}' -Confirm:$false"
            )
            disabled_instances.add(dev)
            print(f"[X] Blocked USB device: {vidpid}")

    time.sleep(2)
