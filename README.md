
# USB Guard – Adaptive USB Security Tool

## Overview

**USB Guard** is a security tool designed to **mitigate malicious USB devices** such as **ATtiny85 / BadUSB / Rubber Ducky–style HID attacks**.

Instead of attempting unreliable “full USB blocking”, this tool uses an **adaptive strategy**:

> **Allow a USB device once → learn it → block it on all future insertions**

This approach works within real operating system limitations and avoids system lockouts.

---

## Key Security Concept

Modern operating systems (especially Windows) **trust HID devices** (keyboards, mice) by design.
Because of this, **no user-space script can prevent the very first HID execution**.

USB Guard implements the **maximum possible protection in user space**.

---

## How It Works 

1. A USB device is inserted for the **first time**
2. The device is **allowed once** (unavoidable on Windows)
3. The tool records the device **VID/PID**
4. On **every future insertion**:

   * The device is **immediately disabled**
   * Payload execution is prevented
5. When the tool exits:

   * All devices disabled by the tool are **automatically restored**

---

## Features

* ✅ Blocks **ATtiny85 / BadUSB / HID injection devices** after first insertion
* ✅ No reboot required
* ✅ Single Python file (no `.bat` files)
* ✅ Automatic device restore on exit
* ✅ Persistent learning via blacklist
* ✅ Works in real time
* ✅ Administrator-safe implementation

---

## Platform Support

### Windows

✔ Supported
✔ Uses Windows Plug-and-Play (PnP) APIs
⚠ First HID execution **cannot be prevented** (OS limitation)

### Linux

❌ This script does **not** work on Linux
✔ Linux supports **kernel-level USB blocking** via `udev` rules (recommended)

---

## Requirements (Windows)

* Windows 10 / 11
* PowerShell 5+
* Python 3.x
* Administrator privileges

---

## Usage (Windows)

### 1. Run the tool

```bash
python usb_guard.py
```

The script will automatically request **administrator privileges**.

---

### 2. Test behavior

* Plug ATtiny (first time) → device works
* Unplug & replug ATtiny → device blocked
* Stop the script → device works again

---

## Files Created

### `blocked_usb.json`

Stores learned USB device identifiers (VID/PID) for adaptive blocking.

Example:

```json
[
  "VID_16C0&PID_05DF"
]
```

---

## Important Limitations (Read This)

* ❌ Cannot prevent **first HID execution** on Windows
* ❌ Cannot stop devices that **spoof legitimate keyboard VID/PID**
* ❌ Does not replace kernel-level endpoint protection
* ❌ If script is force-killed, cleanup may not run

These are **operating system security boundaries**, not bugs.

---

## Why This Design Was Chosen

Traditional “USB blocker” scripts:

* Only block storage devices
* Fail against HID attacks
* Provide a false sense of security

USB Guard:

* Acknowledges OS reality
* Implements a **defensible mitigation strategy**
* Matches real-world endpoint behavior

---

## Security Use Cases

* BadUSB research demonstrations
* Endpoint hardening experiments
* Defensive cybersecurity projects
* Academic or educational labs

---

## Disclaimer

This tool is provided for **educational and defensive purposes only**.
It is not intended to bypass security controls or perform offensive actions.

---

## Author Notes

This project demonstrates a **real limitation in Windows USB security** and why kernel-level defenses are required for complete protection.

If you are documenting this as a project or research work, this behavior is **expected, correct, and defensible**.

---
