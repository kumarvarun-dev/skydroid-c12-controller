# SKYDROID C12 Gimbal Control Station

A Python-based Ground Control Station (GCS) application for controlling the SKYDROID C12 gimbal over UDP while displaying a live video stream using OpenCV and Tkinter.

## Features

* Live video display using OpenCV
* UDP-based gimbal control
* Pitch and Yaw movement control
* Gimbal center/reset function
* Real-time connection status indicator
* Compatible with SKYDROID C12 Ethernet interface
* Lightweight and easy to customize

---

### Main Interface

* Live camera video feed
* Gimbal directional controls
* System status monitoring
* Zoom control placeholders

---

## Hardware Requirements

* SKYDROID C12 Camera/Gimbal
* PC, Laptop, Jetson Nano, or Raspberry Pi
* Ethernet connection to the camera

---

## Network Configuration

Configure your computer Ethernet adapter:

```text
IP Address : 192.168.144.10
Subnet Mask: 255.255.255.0
```

Default camera configuration:

```text
Camera IP   : 192.168.144.108
UDP Port    : 5000
RTSP Port   : 554
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/kumarvarun-dev/skydroid-c12-controller.git

cd skydroid-c12-controller
```

```bash
pip install -r requirements.txt
```

---

## Required Python Packages

```text
opencv-python
pillow
numpy
```

Generate requirements.txt:

```bash
pip freeze > requirements.txt
```

---

## Running the Application

```bash
python main.py
```

---

## Gimbal Control

### Directional Controls

| Button | Function      |
| ------ | ------------- |
| ↑      | Move Up       |
| ↓      | Move Down     |
| ←      | Move Left     |
| →      | Move Right    |
| ●      | Stop / Center |

The application sends UDP packets directly to the camera.

---

## Packet Structure

The camera accepts commands in the following format:

```text
#TPUG2wGS<Axis><Speed><Checksum>
```

Example:

```text
#TPUG2wGSY3269
```

Where:

* Y = Yaw Axis
* P = Pitch Axis
* Speed = Signed speed value encoded as hexadecimal
* Checksum = Sum of all ASCII bytes modulo 256

---

## Packet Generation

Example packet builder:

```python
def build_packet(axis: str, speed: int) -> bytes:
    body = f"#TPUG2wGS{axis}{speed & 0xFF:02X}"
    checksum = sum(ord(c) for c in body) % 256
    return f"{body}{checksum:02X}".encode('ascii')
```

---

## Video Streaming

Current source:

SKYDROID RTSP streaming:

```python
DAY_RTSP_URL = (
    "rtspsrc location=rtsp://192.168.144.108:554/stream=1 "
    "latency=0 ! decodebin ! videoconvert ! appsink"
)

self.cap = cv2.VideoCapture(
    DAY_RTSP_URL,
    cv2.CAP_GSTREAMER
)
```

Thermal/Night Stream:

```python
NIGHT_RTSP_URL = (
    "rtspsrc location=rtsp://192.168.144.108:554/stream=2 "
    "latency=0 ! decodebin ! videoconvert ! appsink"
)
```

---

## Project Structure

```text
skydroid-c12-control-station/
│
├── main.py
├── README.md
├── requirements.txt
│
└── assets/
    └── screenshot.png
```

---

## Future Improvements

* Zoom control implementation
* Thermal camera switching
* Joystick support
* Keyboard control
* Recording functionality

---

## Tested On

* Windows 10
* Windows 11
* Ubuntu 22.04
* Jetson Nano
* Raspberry Pi 4

---

## Disclaimer

This project uses reverse-engineered UDP commands captured from SKYDROID network traffic. Command formats may vary depending on firmware version. Always verify commands in a safe environment before operating the gimbal.
